"""
Configuración de la aplicación
"""
### <<< CORREGIDO: Importaciones añadidas para la lógica flexible
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

# Directorio base del proyecto
# __file__ es .../backend/app/core/config.py
# .parent.parent.parent -> .../backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Configuración general de la aplicación
    Carga variables desde .env
    """
    
    # ========================================
    # INFORMACIÓN DE LA APP (Leído desde el .env o con valor por defecto)
    # ========================================
    APP_NAME: str = "Tesla Cotizador"
    VERSION: str = "3.0.0"
    DEBUG: bool = Field(True, env="DEBUG")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    # ========================================
    # BASE DE DATOS (Con lógica flexible)
    # ========================================
    DEV_DATABASE_URL: str = Field(..., env="DEV_DATABASE_URL")
    PROD_DATABASE_URL: str = Field(..., env="PROD_DATABASE_URL")
    DATABASE_URL: Optional[str] = None
    DATABASE_ECHO: bool = False

    @validator("DATABASE_URL", pre=False, always=True)
    def set_database_url(cls, v, values):
        """
        Elige la URL de la base de datos correcta basándose en el ENTORNO.
        """
        env = values.get("ENVIRONMENT", "development")
        if env == "production":
            print("INFO: Usando configuración de Base de Datos de PRODUCCIÓN (PostgreSQL).")
            return values.get("PROD_DATABASE_URL")
        else:
            print("INFO: Usando configuración de Base de Datos de DESARROLLO (SQLite).")
            return values.get("DEV_DATABASE_URL")
    
    # ========================================
    # GEMINI AI (Google)
    # ========================================
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(..., env="GEMINI_MODEL")
    TEMPERATURE: float = Field(0.7, env="TEMPERATURE")
    MAX_TOKENS: int = Field(2048, env="MAX_TOKENS")
    
    # ========================================
    # ARCHIVOS Y STORAGE
    # ========================================

    ### <<< CORREGIDO: Se cambió de 'str' a 'Path' y se quitó la conversión str()
    # Esto soluciona el 'TypeError' porque permite usar el operador /
    UPLOAD_DIR: Path = BASE_DIR / "storage" / "documentos"
    GENERATED_DIR: Path = BASE_DIR / "storage" / "generados"
    TEMPLATES_DIR: Path = BASE_DIR / "storage" / "templates"
    
    MAX_UPLOAD_SIZE_MB: int = Field(50, env="MAX_UPLOAD_SIZE_MB")
    ALLOWED_EXTENSIONS: str = Field(..., env="ALLOWED_EXTENSIONS")

    ### <<< CORREGIDO: Se añadieron las variables del .env que faltaban
    # Esto soluciona el error 'extra_forbidden'
    STORAGE_PATH: str = Field(..., env="STORAGE_PATH")
    TEMPLATES_PATH: str = Field(..., env="TEMPLATES_PATH")

    # ========================================
    # MÓDULOS DE SERVICIO
    # ========================================
    
    # Ahora esto funciona, porque TEMPLATES_DIR es un Path
    WORD_TEMPLATE_PATH: str = str(TEMPLATES_DIR / "plantilla_cotizacion.docx")
    PDF_TEMPLATE_PATH: str = str(TEMPLATES_DIR / "plantilla_informe_pdf.html")
    PDF_LOGO_PATH: str = str(TEMPLATES_DIR / "logo_tesla.png")
    
    # ========================================
    # RAG (Vector Database)
    # ========================================
    
    ### <<< CORREGIDO: Se cambió de 'str' a 'Path'
    CHROMA_PERSIST_DIRECTORY: Path = BASE_DIR / "storage" / "chroma_db"
    EMBEDDING_MODEL: str = Field(..., env="EMBEDDING_MODEL")

    # ========================================
    # SEGURIDAD (JWT)
    # ========================================
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # ========================================
    # SERVIDOR Y CORS
    # ========================================
    FRONTEND_URL: str = Field("http://localhost:3000", env="FRONTEND_URL")
    BACKEND_HOST: str = Field("0.0.0.0", env="BACKEND_HOST")
    BACKEND_PORT: int = Field(8000, env="BACKEND_PORT")

    # ========================================
    # Configuración de Pydantic
    # ========================================
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        ### <<< CORREGIDO: Se añade esto para permitir el tipo 'Path'
        arbitrary_types_allowed = True 


# Instancia única de la configuración
settings = Settings()


# =============================================================================
#
# TU CÓDIGO ORIGINAL (INTACTO)
# Todas tus funciones helper y configuración de logging 
# permanecen exactamente igual.
#
# =============================================================================

# =======================================
# HELPERS DE CONFIGURACIÓN
# ========================================

def get_database_url() -> str:
    """
    Retorna la URL de la base de datos
    """
    return settings.DATABASE_URL


def is_debug_mode() -> bool:
    """
    Verifica si está en modo debug
    """
    return settings.DEBUG


def get_upload_directory() -> Path:
    """
    Retorna el directorio de uploads como Path
    """
    ### <<< CORREGIDO: settings.UPLOAD_DIR ya es un Path
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return settings.UPLOAD_DIR


def get_generated_directory() -> Path:
    """
    Retorna el directorio de archivos generados como Path
    """
    ### <<< CORREGIDO: settings.GENERATED_DIR ya es un Path
    settings.GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return settings.GENERATED_DIR


def validate_file_extension(filename: str) -> bool:
    """
    Valida si la extensión del archivo está permitida
    """
    extension = filename.split('.')[-1].lower()
    ### <<< CORREGIDO: Compara contra una lista, no un string
    allowed_list = [ext.strip() for ext in settings.ALLOWED_EXTENSIONS.split(',')]
    return extension in allowed_list


# =======================================
# LOGGING CONFIGURATION
# =======================================

import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Configura el sistema de logging
    """
    ### <<< CORREGIDO: Lee el LOG_LEVEL desde la variable correcta
    log_level_str = settings.LOG_LEVEL.upper()
    level = getattr(logging, log_level_str, logging.INFO)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler(sys.stdout)] 
    )
    
    # Silenciar logs muy verbosos
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('watchfiles').setLevel(logging.WARNING)
    
    # Configurar logging a archivo
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "app.log"
    
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024, 
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(file_formatter)
    
    logging.getLogger().addHandler(file_handler)
    
    logger = logging.getLogger(__name__)
    logger.info("==================================================")
    logger.info(f"Logging configurado. Nivel: {log_level_str}")
    logger.info(f"Logs de archivo en: {log_file}")
    logger.info("==================================================")


# =======================================
# RUTAS DE SERVICIOS Y PLANTILLAS
# ========================================

def get_word_template_path() -> Path:
    """
    Retorna la ruta de la plantilla de Word
    """
    path = Path(settings.WORD_TEMPLATE_PATH)
    if not path.exists():
        logging.error(f"No se encontró la plantilla de Word en: {path}")
        raise FileNotFoundError(f"No se encontró la plantilla de Word en: {path}")
    return path

def get_pdf_template_path() -> Path:
    """
    Retorna la ruta de la plantilla de PDF
    """
    path = Path(settings.PDF_TEMPLATE_PATH)
    if not path.exists():
        logging.error(f"No se encontró la plantilla de PDF en: {path}")
        raise FileNotFoundError(f"No se encontró la plantilla de PDF en: {path}")
    return path

def get_pdf_logo_path() -> Path:
    """
    Retorna la ruta del logo para el PDF
    """
    path = Path(settings.PDF_LOGO_PATH)
    if not path.exists():
        logging.warning(f"No se encontró el logo de PDF en: {path}. El PDF se generará sin logo.")
        return None
    return path


# =======================================
# HELPERS DE DATOS Y RAG
# ========================================

def get_chroma_persist_directory() -> str:
    """
    Retorna el directorio de persistencia de ChromaDB
    """
    ### <<< CORREGIDO: settings.CHROMA_PERSIST_DIRECTORY es un Path
    settings.CHROMA_PERSIST_DIRECTORY.mkdir(parents=True, exist_ok=True)
    return str(settings.CHROMA_PERSIST_DIRECTORY)

def get_embedding_model_name() -> str:
    """
    Retorna el nombre del modelo de embedding
    """
    return settings.EMBEDDING_MODEL


# =======================================
# HELPERS DE SEGURIDAD
# ========================================

def get_secret_key() -> str:
    """
    Retorna la secret key para JWT
    """
    if settings.SECRET_KEY == "tu_secret_key_aqui":
        logging.warning("Estás usando la SECRET_KEY por defecto. ¡Cámbiala en producción!")
    return settings.SECRET_KEY

def get_jwt_algorithm() -> str:
    """
    Retorna el algoritmo JWT
    """
    return settings.ALGORITHM

def get_access_token_expire_minutes() -> int:
    """
    Retorna los minutos de expiración del token
    """
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES


# =======================================
# HELPERS DE API
# ========================================

def get_frontend_url() -> str:
    """
    Retorna la URL del frontend
    """
    return settings.FRONTEND_URL

def get_max_upload_size_bytes() -> int:
    """
    Retorna el tamaño máximo de archivo en bytes
    """
    ### <<< CORREGIDO: Usa la variable correcta
    return settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


# =======================================
# EJECUTAR CONFIGURACIÓN INICIAL
# ========================================

# Configurar el logging tan pronto como se importa este módulo
setup_logging()