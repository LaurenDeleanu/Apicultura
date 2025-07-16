from .models import db, Usuario

def crear_usuario_admin():
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
