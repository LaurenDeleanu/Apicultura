#!/usr/bin/env python3
"""
Script de gestión de usuarios para el sistema de apicultura
"""

import getpass
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from api.models import Usuario, db  # Asegúrate que models.py está en el mismo directorio

# Configuración básica para standalone (si no usas app.py con create_app)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-muy-segura-para-apicultura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apicultura.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def crear_usuario():
    """Crear un nuevo usuario"""
    print("=== Crear Nuevo Usuario ===")

    email = input("Email: ").strip().lower()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()

    print("Roles disponibles: admin, apicultor, inspector")
    rol = input("Rol [apicultor]: ").strip() or 'apicultor'

    password = getpass.getpass("Contraseña: ")
    password_confirm = getpass.getpass("Confirmar contraseña: ")

    if password != password_confirm:
        print("❌ Las contraseñas no coinciden")
        return

    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(email=email).first():
        print(f"❌ Ya existe un usuario con el email: {email}")
        return

    # Crear usuario
    usuario = Usuario(
        email=email,
        nombre=nombre,
        apellido=apellido,
        rol=rol
    )
    usuario.set_password(password)

    try:
        db.session.add(usuario)
        db.session.commit()
        print(f"✅ Usuario creado exitosamente: {email}")
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        db.session.rollback()

def listar_usuarios():
    """Listar todos los usuarios"""
    print("=== Lista de Usuarios ===")

    usuarios = Usuario.query.all()

    if not usuarios:
        print("No hay usuarios registrados")
        return

    print(f"{'ID':<5} {'Email':<30} {'Nombre':<20} {'Rol':<12} {'Activo':<8}")
    print("-" * 75)

    for usuario in usuarios:
        print(f"{usuario.id:<5} {usuario.email:<30} {usuario.nombre:<20} {usuario.rol:<12} {'Sí' if usuario.activo else 'No':<8}")

def cambiar_password():
    """Cambiar contraseña de un usuario"""
    print("=== Cambiar Contraseña ===")

    email = input("Email del usuario: ").strip().lower()
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        print(f"❌ Usuario no encontrado: {email}")
        return

    nueva_password = getpass.getpass("Nueva contraseña: ")
    confirmar_password = getpass.getpass("Confirmar contraseña: ")

    if nueva_password != confirmar_password:
        print("❌ Las contraseñas no coinciden")
        return

    try:
        usuario.set_password(nueva_password)
        db.session.commit()
        print(f"✅ Contraseña cambiada exitosamente para: {email}")
    except Exception as e:
        print(f"❌ Error al cambiar contraseña: {e}")
        db.session.rollback()

def activar_desactivar_usuario():
    """Activar o desactivar un usuario"""
    print("=== Activar/Desactivar Usuario ===")

    email = input("Email del usuario: ").strip().lower()
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        print(f"❌ Usuario no encontrado: {email}")
        return

    estado_actual = "activo" if usuario.activo else "inactivo"
    print(f"Estado actual: {estado_actual}")

    nuevo_estado = input("Nuevo estado (activo/inactivo): ").strip().lower()

    if nuevo_estado not in ['activo', 'inactivo']:
        print("❌ Estado inválido. Use 'activo' o 'inactivo'")
        return

    try:
        usuario.activo = nuevo_estado == 'activo'
        db.session.commit()
        print(f"✅ Usuario {email} ahora está {nuevo_estado}")
    except Exception as e:
        print(f"❌ Error al cambiar estado: {e}")
        db.session.rollback()

def eliminar_usuario():
    """Eliminar un usuario"""
    print("=== Eliminar Usuario ===")

    email = input("Email del usuario: ").strip().lower()
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        print(f"❌ Usuario no encontrado: {email}")
        return

    confirmacion = input(f"¿Está seguro de eliminar el usuario {email}? (sí/no): ").strip().lower()

    if confirmacion not in ['sí', 'si', 'yes', 'y']:
        print("❌ Operación cancelada")
        return

    try:
        db.session.delete(usuario)
        db.session.commit()
        print(f"✅ Usuario eliminado: {email}")
    except Exception as e:
        print(f"❌ Error al eliminar usuario: {e}")
        db.session.rollback()

def menu_principal():
    """Mostrar menú principal"""
    while True:
        print("\n=== Sistema de Gestión de Usuarios - Apicultura ===")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Cambiar contraseña")
        print("4. Activar/Desactivar usuario")
        print("5. Eliminar usuario")
        print("6. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == '1':
            crear_usuario()
        elif opcion == '2':
            listar_usuarios()
        elif opcion == '3':
            cambiar_password()
        elif opcion == '4':
            activar_desactivar_usuario()
        elif opcion == '5':
            eliminar_usuario()
        elif opcion == '6':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        menu_principal()
