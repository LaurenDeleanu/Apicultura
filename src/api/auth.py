from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
from datetime import timedelta
import os
import re

app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = 'tu-clave-secreta-muy-segura-para-apicultura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apicultura.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24)

# Inicializar extensiones
db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), default='apicultor')  # admin, apicultor, inspector
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hashear y guardar contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Generar JWT token"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'rol': self.rol,
            'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
    def to_dict(self):
        """Convertir usuario a diccionario (sin password)"""
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rol': self.rol,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'ultimo_login': self.ultimo_login.isoformat() if self.ultimo_login else None
        }

# Middleware de autenticación
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Buscar token en headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({'mensaje': 'Formato de token inválido'}), 401
        
        if not token:
            return jsonify({'mensaje': 'Token requerido'}), 401
        
        try:
            # Decodificar token
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

# Funciones de validación
def validar_email(email):
    """Validar formato de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_password(password):
    """Validar que la contraseña cumpla requisitos mínimos"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una minúscula"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    return True, "Contraseña válida"

# Rutas de autenticación

@app.route('/auth/login', methods=['POST'])
def login():
    """Endpoint de login"""
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validaciones
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        if not validar_email(email):
            return jsonify({'error': 'Formato de email inválido'}), 400
        
        # Buscar usuario
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        if not usuario.activo:
            return jsonify({'error': 'Usuario inactivo'}), 401
        
        # Verificar contraseña
        if not usuario.check_password(password):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Actualizar último login
        usuario.ultimo_login = datetime.datetime.utcnow()
        db.session.commit()
        
        # Generar token
        token = usuario.generate_token()
        
        return jsonify({
            'mensaje': 'Login exitoso',
            'token': token,
            'usuario': usuario.to_dict(),
            'expira_en': app.config['JWT_EXPIRATION_DELTA'].total_seconds()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/auth/logout', methods=['POST'])
@token_required
def logout(usuario_actual):
    """Endpoint de logout"""
    try:
        # En un sistema con JWT, el logout se maneja en el cliente
        # eliminando el token. Aquí podríamos registrar el logout
        
        return jsonify({
            'mensaje': 'Logout exitoso',
            'usuario': usuario_actual.email
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/auth/verify', methods=['GET'])
@token_required
def verify_token(usuario_actual):
    """Verificar si el token es válido"""
    return jsonify({
        'valido': True,
        'usuario': usuario_actual.to_dict()
    }), 200

@app.route('/auth/refresh', methods=['POST'])
@token_required
def refresh_token(usuario_actual):
    """Renovar token"""
    try:
        nuevo_token = usuario_actual.generate_token()
        
        return jsonify({
            'mensaje': 'Token renovado',
            'token': nuevo_token,
            'expira_en': app.config['JWT_EXPIRATION_DELTA'].total_seconds()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# Rutas protegidas de ejemplo
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(usuario_actual):
    """Obtener perfil del usuario autenticado"""
    return jsonify({
        'usuario': usuario_actual.to_dict()
    }), 200

@app.route('/api/colmenas', methods=['GET'])
@token_required
def get_colmenas(usuario_actual):
    """Ejemplo de ruta protegida para colmenas"""
    return jsonify({
        'mensaje': f'Colmenas del usuario {usuario_actual.email}',
        'colmenas': []  # Aquí iría la lógica de colmenas
    }), 200

# Función para crear usuario admin por defecto
def crear_usuario_admin():
    """Crear usuario administrador por defecto"""
    admin = Usuario.query.filter_by(email='admin@apicultura.com').first()
    
    if not admin:
        admin = Usuario(
            email='admin@apicultura.com',
            nombre='Administrador',
            apellido='Sistema',
            rol='admin'
        )
        admin.set_password('Admin123!')
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado: admin@apicultura.com / Admin123!")

# Inicialización
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        crear_usuario_admin()
    
    app.run(debug=True, host='0.0.0.0', port=3001)