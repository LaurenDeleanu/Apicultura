from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
class Humeador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Integer, unique=True, nullable=False)
    tipo = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Humeador {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "tipo": self.tipo,
        }
