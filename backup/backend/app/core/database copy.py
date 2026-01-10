"""
Configuración de base de datos con SQLAlchemy
"""
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Inicializamos las variables globales como None
engine = None
SessionLocal = None
Base = declarative_base()

# ============================================
# INICIALIZACIÓN DIFERIDA
# ============================================

def init_database(settings):
    """
    Inicializa la configuración de la base de datos.
    Debe llamarse al inicio de la aplicación después de cargar la configuración.
    """
    global engine, SessionLocal, Base
    
    # Preparamos los argumentos de conexión de forma condicional
    connect_args = {}
    
    # Configuración específica para PostgreSQL
    if settings.DATABASE_URL.startswith("postgresql"):
        connect_args["options"] = "-c timezone=America/Lima"
        logger.info("Configurando zona horaria de PostgreSQL a America/Lima.")
    
    # Creamos el engine
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
        connect_args=connect_args
    )
    
    # Configuramos la sesión
    global SessionLocal  # Asegurarnos de que estamos actualizando la variable global
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    return engine, SessionLocal, Base

# ============================================
# SESSION LOCAL (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

def get_db() -> Session:
    """
    Dependency que proporciona una sesión de base de datos.
    Asegura que la sesión se cierre después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# FUNCIONES DE UTILIDAD (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

def init_db():
    """
    Crear todas las tablas en la base de datos
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada con éxito.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
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
            # En SQLAlchemy v1.x se usa connection.execute("SELECT 1")
            # En SQLAlchemy v2+ se recomienda usar text()
            from sqlalchemy import text
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Error de conexión a base de datos: {str(e)}")
        return False

# ============================================
# CONTEXT MANAGER PARA SESIONES (TU CÓDIGO ORIGINAL INTACTO)
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