"""
REPARACIÓN AUTOMÁTICA DEL SISTEMA
Ejecuta: python fix_database.py
"""

import os
import shutil
from pathlib import Path

# Colores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

# Encontrar proyecto
script_dir = Path(__file__).resolve().parent
if (script_dir / "backend").exists():
    project_root = script_dir
else:
    project_root = script_dir.parent if (script_dir.parent / "backend").exists() else script_dir

backend_dir = project_root / "backend"
database_py = backend_dir / "app" / "core" / "database.py"

print("\n" + "="*60)
print("REPARACIÓN AUTOMÁTICA - TESLA COTIZADOR")
print("="*60 + "\n")

# 1. VERIFICAR QUE EXISTE
if not database_py.exists():
    print_error(f"No se encuentra: {database_py}")
    exit(1)

print_info(f"Archivo encontrado: {database_py}")

# 2. HACER BACKUP
backup = database_py.parent / "database.py.backup"
shutil.copy(database_py, backup)
print_success(f"Backup creado: {backup.name}")

# 3. ESCRIBIR VERSIÓN CORREGIDA
fixed_content = '''"""
Configuración de base de datos con SQLAlchemy - VERSIÓN CORREGIDA
"""
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Preparamos los argumentos de conexión
connect_args = {}

# Configuración específica para SQLite
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    logger.info("Configurando SQLite con check_same_thread=False.")

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

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db() -> Session:
    """Dependency que proporciona una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Crear todas las tablas en la base de datos"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada con éxito.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
        raise

def drop_db():
    """CUIDADO: Elimina todas las tablas"""
    if settings.ENVIRONMENT == "production":
        raise Exception("No se puede eliminar base de datos en producción")
    Base.metadata.drop_all(bind=engine)
    logger.warning("Todas las tablas han sido eliminadas")

def check_db_connection() -> bool:
    """Verificar conexión a base de datos"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Error de conexión a base de datos: {str(e)}")
        return False

class DatabaseSession:
    """Context manager para manejar sesiones de base de datos"""
    
    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
        self.db.close()
'''

with open(database_py, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print_success("database.py reparado")

# 4. LIMPIAR CACHE
print_info("Limpiando cache de Python...")

cache_count = 0
for pycache_dir in backend_dir.rglob("__pycache__"):
    try:
        shutil.rmtree(pycache_dir)
        cache_count += 1
    except:
        pass

for pyc_file in backend_dir.rglob("*.pyc"):
    try:
        pyc_file.unlink()
        cache_count += 1
    except:
        pass

print_success(f"Cache limpiado: {cache_count} elementos")

# 5. ELIMINAR BD VIEJA
db_file = project_root / "database" / "tesla_cotizador.db"
if db_file.exists():
    db_file.unlink()
    print_success(f"BD eliminada: {db_file.name}")
else:
    print_info("BD no existía (se creará nueva)")

print("\n" + "="*60)
print("✅ REPARACIÓN COMPLETADA")
print("="*60)
print("\n📋 SIGUIENTE PASO:")
print("   1. Reinicia el backend:")
print("      cd backend")
print("      .\\venv\\Scripts\\activate")
print("      python -m uvicorn app.main:app --reload\n")
print("   2. Prueba crear cotización de nuevo\n")