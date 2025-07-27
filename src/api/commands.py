from .models import db, Usuario

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

def setup_commands(app):
    """Configurar comandos CLI para la aplicación"""
    
    @app.cli.command()
    def init_db():
        """Inicializar base de datos"""
        db.create_all()
        print("✅ Base de datos inicializada")
    
    @app.cli.command()
    def create_admin():
        """Crear usuario administrador"""
        crear_usuario_admin()
    
    @app.cli.command()
    def create_user():
        """Crear un nuevo usuario interactivamente"""
        import getpass
        
        print("=== Crear Nuevo Usuario ===")
        
        email = input("Email: ").strip().lower()
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        
        print("Roles disponibles: admin, apicultor, inspector")
        rol = input("Rol [apicultor]: ").strip() or 'apicultor'
        
        password = getpass.getpass("Contraseña: ")
        
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
    
    @app.cli.command()
    def list_users():
        """Listar todos los usuarios"""
        print("=== Lista de Usuarios ===")
        
        usuarios = Usuario.query.all()
        
        if not usuarios:
            print("No hay usuarios registrados")
            return
        
        print(f"{'ID':<5} {'Email':<30} {'Nombre':<20} {'Rol':<12} {'Activo':<8}")
        print("-" * 75)
        
        for usuario in usuarios:
            activo_str = 'Sí' if usuario.activo else 'No'
            print(f"{usuario.id:<5} {usuario.email:<30} {usuario.nombre:<20} {usuario.rol:<12} {activo_str:<8}")