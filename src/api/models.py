from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from flask import current_app as app

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), default='apicultor')
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        payload = {
            'user_id': self.id,
            'email': self.email,
            'rol': self.rol,
            'exp': datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
    def to_dict(self):
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
