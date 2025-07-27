from flask import Blueprint, request, jsonify
from api.models import db, Participation
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