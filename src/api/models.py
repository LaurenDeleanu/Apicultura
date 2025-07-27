from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Float, Text
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# --------------------------
# Modelo de Usuario
# --------------------------
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

# --------------------------
# Modelo de Participación
# --------------------------
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

# --------------------------
# Modelo de Categoría
# --------------------------
class Categoria(db.Model):
    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(200), unique=True, nullable=False)

    articulos = relationship("Articulo", backref="categoria", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "articulos": [a.to_dict() for a in self.articulos]
        }

# --------------------------
# Modelo de Tipo
# --------------------------
class Tipo(db.Model):
    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(200), unique=True, nullable=False)

    articulos = relationship("Articulo", backref="tipo", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "articulos": [a.to_dict() for a in self.articulos]
        }

# --------------------------
# Modelo de ArticuloNombre
# --------------------------
class ArticuloNombre(db.Model):
    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(200), unique=True, nullable=False)

    articulos = relationship("Articulo", backref="nombre_articulo", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "articulos": [a.to_dict() for a in self.articulos]
        }

# --------------------------
# Modelo principal de Articulo
# --------------------------
class Articulo(db.Model):
    id = db.Column(Integer, primary_key=True)
    numero_registro_general = db.Column(String(100), nullable=False, unique=True)
    nombre_tradicional = db.Column(String(150))
    descripcion = db.Column(Text)
    referencia_topografica = db.Column(String(150))
    numero_piezas = db.Column(Integer)
    fecha_origen = db.Column(String(50))
    fecha_adquisicion = db.Column(String(50))
    procedencia = db.Column(String(150))
    autor = db.Column(String(150))
    aportado_por = db.Column(String(150))
    propietario = db.Column(String(150))
    precio_compra = db.Column(Float)
    valoracion_actual = db.Column(Float)
    materiales = db.Column(String(250))
    medidas = db.Column(String(150))
    foto = db.Column(String(300))  # URL o nombre del archivo
    estado_general = db.Column(String(150))
    restauraciones = db.Column(Text)
    uso_funcion = db.Column(Text)
    observaciones = db.Column(Text)
    exposiciones = db.Column(Text)
    referencias_bibliograficas = db.Column(Text)
    prestamos = db.Column(Text)
    codigo_qr = db.Column(String(300))

    # Foreign Keys
    categoria_id = db.Column(Integer, ForeignKey('categoria.id'))
    tipo_id = db.Column(Integer, ForeignKey('tipo.id'))
    articulo_nombre_id = db.Column(Integer, ForeignKey('articulo_nombre.id'))

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

