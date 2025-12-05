"""
============================================================
TESLA COTIZADOR V3.0 - AUDITORÍA Y REPARACIÓN AUTOMÁTICA
============================================================
Script profesional que detecta Y REPARA problemas automáticamente

EJECUTAR: python audit_system.py
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import time
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE COLORES
# ============================================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# ============================================
# CLASE PRINCIPAL
# ============================================

class TeslaAuditorAndFixer:
    """Auditor y reparador automático del sistema"""
    
    def __init__(self):
        self.project_root = self.find_project_root()
        self.backend_dir = self.project_root / "backend"
        self.errors_found = []
        self.fixes_applied = []
        
    def find_project_root(self) -> Path:
        """Encuentra la raíz del proyecto automáticamente"""
        current = Path(__file__).resolve().parent
        
        # Si estamos en la raíz
        if (current / "backend").exists() and (current / "frontend").exists():
            return current
        
        # Buscar hacia arriba
        while current.parent != current:
            if (current / "backend").exists() and (current / "frontend").exists():
                return current
            current = current.parent
        
        raise Exception("No se pudo encontrar la raíz del proyecto")
    
    def print_header(self, text: str):
        """Imprimir encabezado"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    def print_success(self, text: str):
        """Imprimir éxito"""
        print(f"{Colors.GREEN}✓{Colors.RESET} {text}")
    
    def print_error(self, text: str):
        """Imprimir error"""
        print(f"{Colors.RED}✗{Colors.RESET} {text}")
        self.errors_found.append(text)
    
    def print_fixing(self, text: str):
        """Imprimir reparación"""
        print(f"{Colors.YELLOW}🔧{Colors.RESET} {text}")
    
    def print_fixed(self, text: str):
        """Imprimir reparado"""
        print(f"{Colors.GREEN}✅{Colors.RESET} {text}")
        self.fixes_applied.append(text)
    
    # ============================================
    # VERIFICACIONES Y REPARACIONES
    # ============================================
    
    def fix_database_py(self) -> bool:
        """Verificar y reparar database.py"""
        self.print_header("VERIFICANDO database.py")
        
        db_path = self.backend_dir / "app" / "core" / "database.py"
        
        if not db_path.exists():
            self.print_error("database.py no existe")
            return False
        
        # Leer contenido
        with open(db_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar bug de 'options'
        if '"options"' in content and 'postgresql' in content:
            self.print_error("Bug detectado: configuración 'options' para PostgreSQL")
            self.print_fixing("Reparando database.py...")
            
            # Crear versión corregida
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
            
            # Hacer backup
            backup_path = db_path.parent / "database.py.backup"
            shutil.copy(db_path, backup_path)
            self.print_success(f"Backup creado: {backup_path.name}")
            
            # Escribir versión corregida
            with open(db_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            self.print_fixed("database.py reparado correctamente")
            return True
        else:
            self.print_success("database.py está correcto")
            return True
    
    def fix_cotizacion_schema(self) -> bool:
        """Verificar y reparar schemas de cotización"""
        self.print_header("VERIFICANDO schemas/cotizacion.py")
        
        schema_path = self.backend_dir / "app" / "schemas" / "cotizacion.py"
        
        if not schema_path.exists():
            self.print_error("schemas/cotizacion.py no existe")
            return False
        
        # Leer contenido
        with open(schema_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si tiene los campos obligatorios
        if 'class CotizacionCreate' in content:
            if 'subtotal:' not in content or 'igv:' not in content or 'total:' not in content:
                self.print_error("Schema CotizacionCreate le faltan campos (subtotal, igv, total)")
                self.print_fixing("Agregando campos faltantes...")
                
                # Crear versión corregida
                fixed_content = '''"""
Schemas de Cotización
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

class ItemBase(BaseModel):
    """Schema base de Item"""
    descripcion: str = Field(..., min_length=1, description="Descripción del item")
    cantidad: Decimal = Field(..., gt=0, description="Cantidad")
    precio_unitario: Decimal = Field(..., ge=0, description="Precio unitario")

class ItemCreate(ItemBase):
    """Schema para crear un item"""
    pass

class ItemResponse(ItemBase):
    """Schema de respuesta de Item"""
    id: int
    total: Decimal
    cotizacion_id: int
    
    model_config = ConfigDict(from_attributes=True)

class CotizacionBase(BaseModel):
    """Schema base de Cotización"""
    cliente: str = Field(..., min_length=3, max_length=200, description="Nombre del cliente")
    proyecto: str = Field(..., min_length=3, max_length=200, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción de la cotización")

class CotizacionCreate(CotizacionBase):
    """Schema para crear una cotización - CORREGIDO"""
    items: List[Dict[str, Any]] = Field(..., description="Items de la cotización")
    
    # CAMPOS OBLIGATORIOS
    subtotal: Decimal = Field(..., ge=0, description="Subtotal sin IGV")
    igv: Decimal = Field(..., ge=0, description="Monto del IGV")
    total: Decimal = Field(..., ge=0, description="Total con IGV")
    
    # Campos opcionales
    observaciones: Optional[str] = Field(None, description="Observaciones")
    vigencia: Optional[str] = Field("30 días", description="Vigencia de la cotización")
    proyecto_id: Optional[int] = Field(None, description="ID del proyecto relacionado")
    estado: Optional[str] = Field("borrador", description="Estado de la cotización")
    metadata_adicional: Optional[Dict[str, Any]] = Field(None, description="Metadata adicional")
    
    @field_validator('items')
    @classmethod
    def validar_items(cls, v):
        """Validar que los items tengan la estructura correcta"""
        if not v or len(v) == 0:
            raise ValueError("Debe haber al menos un item en la cotización")
        
        for idx, item in enumerate(v):
            if not isinstance(item, dict):
                raise ValueError(f"Item {idx + 1}: debe ser un diccionario")
            
            required_fields = ["descripcion", "cantidad", "precio_unitario"]
            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Item {idx + 1}: debe tener el campo '{field}'")
            
            if not isinstance(item["descripcion"], str) or len(item["descripcion"]) < 1:
                raise ValueError(f"Item {idx + 1}: la descripción debe ser un texto no vacío")
            
            try:
                cantidad = float(item["cantidad"])
                if cantidad <= 0:
                    raise ValueError(f"Item {idx + 1}: la cantidad debe ser mayor a 0")
            except (ValueError, TypeError):
                raise ValueError(f"Item {idx + 1}: la cantidad debe ser un número válido")
            
            try:
                precio = float(item["precio_unitario"])
                if precio < 0:
                    raise ValueError(f"Item {idx + 1}: el precio debe ser mayor o igual a 0")
            except (ValueError, TypeError):
                raise ValueError(f"Item {idx + 1}: el precio debe ser un número válido")
            
            if "total" not in item:
                item["total"] = cantidad * precio
        
        return v
    
    @field_validator('total')
    @classmethod
    def validar_total(cls, v, info):
        """Validar que el total sea coherente"""
        if 'subtotal' in info.data and 'igv' in info.data:
            total_calculado = info.data['subtotal'] + info.data['igv']
            if abs(float(v) - float(total_calculado)) > 0.01:
                raise ValueError(f"El total ({v}) no coincide con subtotal + IGV ({total_calculado})")
        return v

class CotizacionUpdate(BaseModel):
    """Schema para actualizar una cotización"""
    cliente: Optional[str] = Field(None, min_length=3, max_length=200)
    proyecto: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    subtotal: Optional[Decimal] = None
    igv: Optional[Decimal] = None
    total: Optional[Decimal] = None
    observaciones: Optional[str] = None
    vigencia: Optional[str] = None
    estado: Optional[str] = None
    metadata_adicional: Optional[Dict[str, Any]] = None

class CotizacionResponse(CotizacionBase):
    """Schema de respuesta de Cotización"""
    id: int
    numero: str
    subtotal: Decimal
    igv: Decimal
    total: Decimal
    estado: str
    items: Optional[List[Dict[str, Any]]] = None
    metadata_adicional: Optional[Dict[str, Any]] = None
    fecha_creacion: datetime
    fecha_modificacion: datetime
    proyecto_id: Optional[int] = None
    observaciones: Optional[str] = None
    vigencia: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
'''
                
                # Hacer backup
                backup_path = schema_path.parent / "cotizacion.py.backup"
                shutil.copy(schema_path, backup_path)
                self.print_success(f"Backup creado: {backup_path.name}")
                
                # Escribir versión corregida
                with open(schema_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                self.print_fixed("schemas/cotizacion.py reparado correctamente")
                return True
            else:
                self.print_success("schemas/cotizacion.py tiene los campos necesarios")
                return True
        else:
            self.print_error("No se encontró class CotizacionCreate en el schema")
            return False
    
    def clear_python_cache(self):
        """Limpiar todo el cache de Python"""
        self.print_header("LIMPIANDO CACHE DE PYTHON")
        
        cache_cleared = 0
        
        # Buscar y eliminar __pycache__
        for pycache_dir in self.backend_dir.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
                cache_cleared += 1
            except Exception as e:
                self.print_error(f"Error eliminando {pycache_dir}: {e}")
        
        # Buscar y eliminar .pyc
        for pyc_file in self.backend_dir.rglob("*.pyc"):
            try:
                pyc_file.unlink()
                cache_cleared += 1
            except Exception as e:
                self.print_error(f"Error eliminando {pyc_file}: {e}")
        
        if cache_cleared > 0:
            self.print_fixed(f"Cache eliminado: {cache_cleared} elementos")
        else:
            self.print_success("No hay cache para eliminar")
    
    def verify_structure(self):
        """Verificar estructura de directorios"""
        self.print_header("VERIFICANDO ESTRUCTURA")
        
        required_dirs = [
            ("backend", self.project_root / "backend"),
            ("frontend", self.project_root / "frontend"),
            ("database", self.project_root / "database"),
            ("storage/documentos", self.project_root / "storage" / "documentos"),
            ("storage/generados", self.project_root / "storage" / "generados"),
            ("storage/templates", self.project_root / "storage" / "templates"),
        ]
        
        for name, path in required_dirs:
            if path.exists():
                self.print_success(f"Directorio OK: {name}")
            else:
                self.print_error(f"Directorio faltante: {name}")
                # Crear si no existe
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self.print_fixed(f"Directorio creado: {name}")
                except Exception as e:
                    self.print_error(f"No se pudo crear {name}: {e}")
    
    def restart_backend(self):
        """Instrucciones para reiniciar el backend"""
        self.print_header("SIGUIENTE PASO: REINICIAR BACKEND")
        
        print(f"{Colors.YELLOW}📋 INSTRUCCIONES:{Colors.RESET}\n")
        print(f"1. Ve a la terminal donde está corriendo el backend")
        print(f"2. Presiona {Colors.BOLD}Ctrl+C{Colors.RESET} para detenerlo")
        print(f"3. Ejecuta:\n")
        print(f"   {Colors.BOLD}cd {self.backend_dir}{Colors.RESET}")
        print(f"   {Colors.BOLD}.\\venv\\Scripts\\activate{Colors.RESET}")
        print(f"   {Colors.BOLD}python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000{Colors.RESET}\n")
    
    # ============================================
    # EJECUCIÓN PRINCIPAL
    # ============================================
    
    def run(self):
        """Ejecutar auditoría y reparación completa"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  TESLA COTIZADOR - AUDITORÍA Y REPARACIÓN AUTOMÁTICA      ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        
        start_time = time.time()
        
        # Ejecutar verificaciones y reparaciones
        self.verify_structure()
        self.fix_database_py()
        self.fix_cotizacion_schema()
        self.clear_python_cache()
        
        # Reporte final
        elapsed = time.time() - start_time
        
        self.print_header("REPORTE FINAL")
        
        print(f"⏱️  Tiempo: {elapsed:.2f}s")
        print(f"{Colors.RED}❌ Errores encontrados: {len(self.errors_found)}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Reparaciones aplicadas: {len(self.fixes_applied)}{Colors.RESET}\n")
        
        if self.fixes_applied:
            print(f"{Colors.GREEN}{Colors.BOLD}REPARACIONES APLICADAS:{Colors.RESET}")
            for fix in self.fixes_applied:
                print(f"  ✓ {fix}")
            print()
        
        if self.errors_found and not self.fixes_applied:
            print(f"{Colors.RED}{Colors.BOLD}ERRORES NO REPARABLES AUTOMÁTICAMENTE:{Colors.RESET}")
            for error in self.errors_found:
                print(f"  ✗ {error}")
            print()
        
        # Instrucciones finales
        if self.fixes_applied:
            self.restart_backend()
            print(f"{Colors.GREEN}{Colors.BOLD}🎯 SISTEMA REPARADO - Reinicia el backend{Colors.RESET}\n")
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ SISTEMA OK - No se requieren reparaciones{Colors.RESET}\n")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    try:
        auditor = TeslaAuditorAndFixer()
        auditor.run()
    except Exception as e:
        print(f"{Colors.RED}{Colors.BOLD}ERROR CRÍTICO: {e}{Colors.RESET}")
        sys.exit(1)