"""
Configuración de la aplicación - VERSIÓN FINAL CORREGIDA
"""
from pydantic_settings import BaseSettings
from pydantic import Field, validator, model_validator
from typing import List, Optional
import os
from pathlib import Path
import logging
import sys
from logging.handlers import RotatingFileHandler

# =======================================
# DETECCIÓN AUTOMÁTICA DE RUTAS
# =======================================

def encontrar_directorio_backend() -> Path:
    """Encuentra el directorio 'backend' automáticamente"""
    current = Path(__file__).resolve()
    while current.name != 'backend' and current.parent != current:
        current = current.parent
    if current.name == 'backend':
        return current
    else:
        raise Exception("No se pudo encontrar el directorio 'backend'")

def encontrar_raiz_proyecto() -> Path:
    """Encuentra la raíz del proyecto (padre de 'backend')"""
    backend_dir = encontrar_directorio_backend()
    return backend_dir.parent

# Calcular rutas
BASE_DIR = encontrar_directorio_backend()
PROJECT_ROOT = encontrar_raiz_proyecto()

# =======================================
# CONFIGURACIÓN DE LOGGING
# =======================================
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"
LOG_LEVEL_DEFAULT = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL_DEFAULT,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
    ]
)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
logging.getLogger('watchfiles').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("🔍 RUTAS DETECTADAS:")
logger.info(f"   BASE_DIR: {BASE_DIR}")
logger.info(f"   PROJECT_ROOT: {PROJECT_ROOT}")
logger.info("=" * 60)


# =======================================
# CLASE DE CONFIGURACIÓN
# =======================================

class Settings(BaseSettings):
    """Configuración general de la aplicación"""
    
    APP_NAME: str = "Tesla Cotizador"
    VERSION: str = "3.0.0"
    
    ENVIRONMENT: str = Field(..., env="ENVIRONMENT")
    DEBUG: bool = Field(..., env="DEBUG")
    LOG_LEVEL: str = Field(..., env="LOG_LEVEL")
    
    PROD_DATABASE_URL: Optional[str] = Field(None, env="PROD_DATABASE_URL")
    DEV_DATABASE_URL: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    DATABASE_ECHO: bool = False
    
    UPLOAD_DIR: Optional[Path] = None
    GENERATED_DIR: Optional[Path] = None
    TEMPLATES_DIR: Optional[Path] = None
    CHROMA_PERSIST_DIRECTORY: Optional[Path] = None
    
    ALLOWED_EXTENSIONS: str = Field(..., env="ALLOWED_EXTENSIONS")
    MAX_UPLOAD_SIZE_MB: int = Field(..., env="MAX_UPLOAD_SIZE_MB")
    STORAGE_PATH: Optional[str] = None
    TEMPLATES_PATH: Optional[str] = None
    
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(..., env="GEMINI_MODEL")
    EMBEDDING_MODEL: str = Field(..., env="EMBEDDING_MODEL")
    TEMPERATURE: float = Field(..., env="TEMPERATURE")
    MAX_TOKENS: int = Field(..., env="MAX_TOKENS")
    
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    FRONTEND_URL: str = Field(..., env="FRONTEND_URL")
    BACKEND_HOST: str = Field(..., env="BACKEND_HOST")
    BACKEND_PORT: int = Field(..., env="BACKEND_PORT")
    
    @model_validator(mode='before')
    @classmethod
    def set_paths(cls, values):
        """Calcular todas las rutas dinámicamente"""
        # Base de datos - USAR RUTA ABSOLUTA
        db_path = PROJECT_ROOT / 'database' / 'tesla_cotizador.db'
        values['DEV_DATABASE_URL'] = f"sqlite:///{db_path}"
        
        # Storage
        values['UPLOAD_DIR'] = PROJECT_ROOT / "storage" / "documentos"
        values['GENERATED_DIR'] = PROJECT_ROOT / "storage" / "generados"
        values['TEMPLATES_DIR'] = PROJECT_ROOT / "storage" / "templates"
        values['CHROMA_PERSIST_DIRECTORY'] = PROJECT_ROOT / "storage" / "chroma_db"
        values['STORAGE_PATH'] = str(PROJECT_ROOT / "storage")
        values['TEMPLATES_PATH'] = str(PROJECT_ROOT / "storage" / "templates")
        
        return values
    
    @validator("DATABASE_URL", pre=False, always=True)
    def set_database_url(cls, v, values):
        """Elegir URL de BD según entorno"""
        env = values.get("ENVIRONMENT", "development")
        logger = logging.getLogger(__name__)
        
        if env == "production":
            logger.info("Usando BD de PRODUCCIÓN (PostgreSQL)")
            prod_url = values.get("PROD_DATABASE_URL")
            if not prod_url:
                raise ValueError("PROD_DATABASE_URL requerida en producción")
            return prod_url
        else:
            logger.info("Usando BD de DESARROLLO (SQLite)")
            # Usar directamente la ruta calculada en model_validator
            sqlite_url = values.get("DEV_DATABASE_URL")
            db_path = PROJECT_ROOT / "database" / "tesla_cotizador.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"   📂 Ruta BD: {db_path}")
            return sqlite_url
    
    @property
    def MAX_FILE_SIZE(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    @property
    def WORD_TEMPLATE_PATH(self) -> str:
        return str(self.TEMPLATES_DIR / "plantilla_cotizacion.docx")
    
    @property
    def PDF_TEMPLATE_PATH(self) -> str:
        return str(self.TEMPLATES_DIR / "plantilla_informe_pdf.html")
    
    @property
    def PDF_LOGO_PATH(self) -> str:
        return str(self.TEMPLATES_DIR / "logo_tesla.png")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        arbitrary_types_allowed = True
        extra = 'ignore'

# Instancia global
settings = Settings()

# Log final
logger.info("📂 RUTAS CONFIGURADAS:")
logger.info(f"   📊 BD: {settings.DATABASE_URL}")
logger.info(f"   📁 Uploads: {settings.UPLOAD_DIR}")
logger.info(f"   📄 Generados: {settings.GENERATED_DIR}")
logger.info(f"   📋 Templates: {settings.TEMPLATES_DIR}")
logger.info(f"   🔍 ChromaDB: {settings.CHROMA_PERSIST_DIRECTORY}")


# =======================================
# FUNCIONES HELPER
# =======================================

def get_database_url() -> str:
    return settings.DATABASE_URL

def is_debug_mode() -> bool:
    return settings.DEBUG

def get_upload_directory() -> Path:
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return settings.UPLOAD_DIR

def get_generated_directory() -> Path:
    settings.GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return settings.GENERATED_DIR

def validate_file_extension(filename: str) -> bool:
    extension = filename.split('.')[-1].lower()
    allowed_list = [ext.strip() for ext in settings.ALLOWED_EXTENSIONS.split(',')]
    return extension in allowed_list

def get_word_template_path() -> Path:
    path = Path(settings.WORD_TEMPLATE_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Plantilla Word no encontrada: {path}")
    return path

def get_pdf_template_path() -> Path:
    path = Path(settings.PDF_TEMPLATE_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Plantilla PDF no encontrada: {path}")
    return path

def get_pdf_logo_path() -> Path:
    path = Path(settings.PDF_LOGO_PATH)
    if not path.exists():
        logging.warning(f"Logo PDF no encontrado: {path}")
        return None
    return path

def get_chroma_persist_directory() -> str:
    settings.CHROMA_PERSIST_DIRECTORY.mkdir(parents=True, exist_ok=True)
    return str(settings.CHROMA_PERSIST_DIRECTORY)

def get_embedding_model_name() -> str:
    return settings.EMBEDDING_MODEL

def get_secret_key() -> str:
    if settings.SECRET_KEY == "tu_secret_key_aqui":
        logging.warning("Usando SECRET_KEY por defecto!")
    return settings.SECRET_KEY

def get_jwt_algorithm() -> str:
    return settings.ALGORITHM

def get_access_token_expire_minutes() -> int:
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES

def get_frontend_url() -> str:
    return settings.FRONTEND_URL

def get_max_upload_size_bytes() -> int:
    return settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024