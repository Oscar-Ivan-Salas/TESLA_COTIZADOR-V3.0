# Contenido para: backend/app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    
    # === LÓGICA DE BD FLEXIBLE (LA QUE AÑADIMOS) ===
    
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    DEV_DATABASE_URL: str = Field(..., env="DEV_DATABASE_URL")
    PROD_DATABASE_URL: str = Field(..., env="PROD_DATABASE_URL")
    DATABASE_URL: Optional[str] = None
    
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
            
    # === TUS VARIABLES ORIGINALES (INTACTAS) ===
    
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(..., env="GEMINI_MODEL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FRONTEND_URL: str
    CHROMA_PERSIST_DIRECTORY: str = Field(..., env="CHROMA_PERSIST_DIRECTORY")
    EMBEDDING_MODEL: str = Field(..., env="EMBEDDING_MODEL")

    # === LAS 12 VARIABLES FALTANTES (AHORA AÑADIDAS) ===
    # Estas son las variables que causaban el error 'extra_forbidden'
    
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    MAX_TOKENS: int = 8192
    TEMPERATURE: float = 0.7
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    STORAGE_PATH: str = "./backend/storage"
    TEMPLATES_PATH: str = "./backend/templates"
    UPLOAD_DIR: str = "./storage/documentos"
    GENERATED_DIR: str = "./storage/generados"
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: str = "pdf,docx,xlsx,jpg,jpeg,png,txt,csv"

    # --- Configuración de Pydantic ---
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Creamos la instancia única de configuración
settings = Settings()