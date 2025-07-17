from flask import Blueprint, request, jsonify
from functools import wraps
from models import Usuario
from utils import validar_email, validar_password
from models import db
import jwt
import datetime
from flask import current_app as app

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'mensaje': 'Formato de token inválido'}), 401
        if not token:
            return jsonify({'mensaje': 'Token requerido'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            usuario_actual = Usuario.query.get(data['user_id'])
            if not usuario_actual or not usuario_actual.activo:
                return jsonify({'mensaje': 'Usuario inválido o inactivo'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'Token inválido'}), 401
        return f(usuario_actual, *args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400
    if not validar_email(email):
        return jsonify({'error': 'Formato de email inválido'}), 400
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.check_password(password) or not usuario.activo:
        return jsonify({'error': 'Credenciales inválidas o usuario inactivo'}), 401
    usuario.ultimo_login = datetime.datetime.utcnow()
    db.session.commit()
    token = usuario.generate_token()
    return jsonify({
        'mensaje': 'Login exitoso',
        'token': token,
        'usuario': usuario.to_dict(),
        'expira_en': app.config['JWT_EXPIRATION_DELTA'].total_seconds()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(usuario_actual):
    return jsonify({
        'mensaje': 'Logout exitoso',
        'usuario': usuario_actual.email
    }), 200

@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify_token(usuario_actual):
    return jsonify({
        'valido': True,
        'usuario': usuario_actual.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@token_required
def refresh_token(usuario_actual):
    nuevo_token = usuario_actual.generate_token()
    return jsonify({
        'mensaje': 'Token renovado',
        'token': nuevo_token,
        'expira_en': app.config['JWT_EXPIRATION_DELTA'].total_seconds()
    }), 200
