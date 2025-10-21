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
# CREAR ENGINE DE SQLALCHEMY (SECCIÓN CORREGIDA Y MEJORADA)
# ============================================

# Preparamos los argumentos de conexión de forma condicional
connect_args = {}
# Esta configuración de zona horaria es específica de PostgreSQL.
# La aplicamos solo si estamos usando una base de datos PostgreSQL.
if settings.DATABASE_URL.startswith("postgresql"):
    connect_args["options"] = "-c timezone=America/Lima"
    logger.info("Configurando zona horaria de PostgreSQL a America/Lima.")

# Creamos el engine usando los argumentos que preparamos
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,      # Verificar conexión antes de usar
    pool_size=5,             # Tamaño del pool de conexiones
    max_overflow=10,         # Conexiones adicionales permitidas
    pool_recycle=3600,       # Reciclar conexiones cada hora
    connect_args=connect_args  # Usamos el diccionario preparado
)

# ============================================
# SESSION LOCAL (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================
# BASE PARA MODELOS (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

Base = declarative_base()

# ============================================
# DEPENDENCY PARA FASTAPI (TU CÓDIGO ORIGINAL INTACTO)
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