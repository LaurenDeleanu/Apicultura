from flask import Blueprint, request, jsonify, Flask
from api.models import db, Participation, Categoria, Tipo, Articulo, ArticuloNombre
from api.utils import APIException

api = Blueprint('api', __name__)

@api.route('/participations', methods=['POST'])
def create_participation():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    number = data.get('number')

    if not (name and phone and number is not None):
        raise APIException("Debe enviar name, phone y number", status_code=400)

    try:
        number = int(number)
    except ValueError:
        raise APIException("Número inválido", status_code=400)

    if not (0 <= number <= 99):
        raise APIException("Número debe estar entre 0 y 99", status_code=400)

    exists = Participation.query.filter_by(number=number).first()
    if exists:
        raise APIException("Número ya asignado, elige otro", status_code=409)

    participation = Participation(name=name, phone=phone, number=number)
    db.session.add(participation)
    db.session.commit()

    return jsonify(participation.serialize()), 201

@api.route('/available-numbers', methods=['GET'])
def available_numbers():
    assigned = db.session.query(Participation.number).all()
    assigned_numbers = {num for (num,) in assigned}
    all_numbers = set(range(100))
    available = sorted(list(all_numbers - assigned_numbers))
    return jsonify({"available_numbers": available}), 200

app = Flask(__name__)
# Asegúrate de configurar tu base de datos aquí
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://..."

# -----------------------------
# CATEGORÍAS
# -----------------------------

@app.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([cat.serialize() for cat in categorias]), 200

@app.route('/categorias/<int:id>', methods=['GET'])
def get_categoria_by_id(id):
    categoria = Categoria.query.get_or_404(id)
    return jsonify(categoria.serialize()), 200

# -----------------------------
# TIPOS
# -----------------------------

@app.route('/tipos', methods=['GET'])
def get_tipos():
    tipos = Tipo.query.all()
    return jsonify([t.serialize() for t in tipos]), 200

@app.route('/tipos/<int:id>', methods=['GET'])
def get_tipo_by_id(id):
    tipo = Tipo.query.get_or_404(id)
    return jsonify(tipo.serialize()), 200

# -----------------------------
# ARTÍCULOS
# -----------------------------

@app.route('/articulos', methods=['GET'])
def get_articulos():
    # Filtrado opcional por categoría, tipo o nombre
    categoria_id = request.args.get('categoria_id')
    tipo_id = request.args.get('tipo_id')
    articulo_nombre_id = request.args.get('articulo_nombre_id')

    query = Articulo.query

    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if tipo_id:
        query = query.filter_by(tipo_id=tipo_id)
    if articulo_nombre_id:
        query = query.filter_by(articulo_nombre_id=articulo_nombre_id)

    articulos = query.all()
    return jsonify([a.to_dict() for a in articulos]), 200

@app.route('/articulos/<int:id>', methods=['GET'])
def get_articulo_by_id(id):
    articulo = Articulo.query.get_or_404(id)
    return jsonify(articulo.to_dict()), 200

# -----------------------------
# ARTICULO NOMBRE (Opcional)
# -----------------------------

@app.route('/nombres-articulo', methods=['GET'])
def get_articulo_nombres():
    nombres = ArticuloNombre.query.all()
    return jsonify([n.serialize() for n in nombres]), 200

@app.route('/nombres-articulo/<int:id>', methods=['GET'])
def get_articulo_nombre_by_id(id):
    nombre = ArticuloNombre.query.get_or_404(id)
    return jsonify(nombre.serialize()), 200

