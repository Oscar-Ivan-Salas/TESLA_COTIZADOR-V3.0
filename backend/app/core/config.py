"""
Configuración de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Configuración general de la aplicación
    Carga variables desde .env
    """
    
    # ========================================
    # INFORMACIÓN DE LA APP
    # ========================================
    APP_NAME: str = "Tesla Cotizador"
    VERSION: str = "3.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # ========================================
    # BASE DE DATOS
    # ========================================
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tesla_cotizador"
    DATABASE_ECHO: bool = False
    
    # ========================================
    # GEMINI AI (Google)
    # ========================================
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 2048
    
    # ========================================
    # ARCHIVOS Y STORAGE
    # ========================================
    UPLOAD_DIR: str = str(BASE_DIR / "backend" / "storage" / "documentos")
    GENERATED_DIR: str = str(BASE_DIR / "backend" / "storage" / "generados")
    TEMPLATES_DIR: str = str(BASE_DIR / "backend" / "templates")
    
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [
        "pdf", "docx", "doc", "xlsx", "xls", 
        "txt", "jpg", "jpeg", "png", "gif"
    ]
    
    # ========================================
    # SEGURIDAD
    # ========================================
    SECRET_KEY: str = "tesla-cotizador-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ========================================
    # CORS (Frontend URLs permitidas)
    # ========================================
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # ========================================
    # CHROMADB (Vector Database para RAG)
    # ========================================
    CHROMA_PERSIST_DIRECTORY: str = str(BASE_DIR / "backend" / "storage" / "chroma_db")
    CHROMA_COLLECTION_NAME: str = "documentos_cotizador"
    
    # ========================================
    # OCR (Tesseract)
    # ========================================
    OCR_LANGUAGES: str = "spa+eng"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


# ========================================
# INSTANCIA GLOBAL DE CONFIGURACIÓN
# ========================================
settings = Settings()


# ========================================
# FUNCIONES AUXILIARES
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
    path = Path(settings.UPLOAD_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_generated_directory() -> Path:
    """
    Retorna el directorio de archivos generados como Path
    """
    path = Path(settings.GENERATED_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_file_extension(filename: str) -> bool:
    """
    Valida si la extensión del archivo está permitida
    """
    extension = filename.split('.')[-1].lower()
    return extension in settings.ALLOWED_EXTENSIONS


# ========================================
# LOGGING CONFIGURATION
# ========================================

import logging

def setup_logging():
    """
    Configura el sistema de logging
    """
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Silenciar logs muy verbosos
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)


# Configurar logging al importar
setup_logging()