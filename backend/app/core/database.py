"""
Configuración de base de datos con SQLAlchemy
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# ============================================
# CREAR ENGINE DE SQLALCHEMY
# ============================================

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_size=5,          # Tamaño del pool de conexiones
    max_overflow=10,      # Conexiones adicionales permitidas
    pool_recycle=3600,    # Reciclar conexiones cada hora
    connect_args={
        "options": "-c timezone=America/Lima"  # Zona horaria Perú
    }
)

# ============================================
# SESSION LOCAL
# ============================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================
# BASE PARA MODELOS
# ============================================

Base = declarative_base()

# ============================================
# DEPENDENCY PARA FASTAPI
# ============================================

def get_db() -> Session:
    """
    Dependency que proporciona una sesión de base de datos.
    
    Uso en FastAPI:
    @app.get("/items")
    def get_items(db: Session = Depends(get_db)):
        return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# EVENTOS DE SQLALCHEMY
# ============================================

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Configurar pragmas para SQLite (si se usa)
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
        logger.info("Conexión a base de datos establecida")
    except Exception as e:
        logger.error(f"Error al conectar a base de datos: {str(e)}")
    finally:
        cursor.close()

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def init_db():
    """
    Inicializar base de datos (crear todas las tablas)
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar base de datos: {str(e)}")
        raise

def drop_db():
    """
    CUIDADO: Elimina todas las tablas
    Solo usar en desarrollo
    """
    if settings.ENVIRONMENT == "production":
        raise Exception("No se puede eliminar base de datos en producción")
    
    Base.metadata.drop_all(bind=engine)
    logger.warning("Todas las tablas han sido eliminadas")

def check_db_connection() -> bool:
    """
    Verificar conexión a base de datos
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Error de conexión a base de datos: {str(e)}")
        return False

# ============================================
# CONTEXT MANAGER PARA SESIONES
# ============================================

class DatabaseSession:
    """
    Context manager para manejar sesiones de base de datos
    
    Uso:
    with DatabaseSession() as db:
        user = db.query(User).first()
    """
    
    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        self.db.close()

# ============================================
# LOGGING
# ============================================

logger.info(f"Engine de base de datos creado: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'local'}")