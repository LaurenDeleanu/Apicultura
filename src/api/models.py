from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(255), nullable=False)
    is_active = db.Column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Participation(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(120), nullable=False)
    phone = db.Column(String(50), nullable=False)
    number = db.Column(Integer, nullable=False, unique=True)  # único número entre 0 y 99

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "number": self.number
        }
class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_registro_general = db.Column(db.String(100), nullable=False, unique=True)
    nombre_tradicional = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    referencia_topografica = db.Column(db.String(150))
    numero_piezas = db.Column(db.Integer)
    fecha_origen = db.Column(db.String(50))
    fecha_adquisicion = db.Column(db.String(50))
    procedencia = db.Column(db.String(150))
    autor = db.Column(db.String(150))
    aportado_por = db.Column(db.String(150))
    propietario = db.Column(db.String(150))
    precio_compra = db.Column(db.Float)
    valoracion_actual = db.Column(db.Float)
    materiales = db.Column(db.String(250))
    medidas = db.Column(db.String(150))
    foto = db.Column(db.String(300))  # URL o nombre del archivo
    estado_general = db.Column(db.String(150))
    restauraciones = db.Column(db.Text)
    uso_funcion = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    exposiciones = db.Column(db.Text)
    referencias_bibliograficas = db.Column(db.Text)
    prestamos = db.Column(db.Text)
    codigo_qr = db.Column(db.String(300))  # Podría ser una imagen o texto
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}









