"""
Script para inicializar/actualizar base de datos
Crea todas las tablas definidas en los modelos
"""
import sys
from pathlib import Path

# Agregar directorio app al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import Base, engine, init_db
from app.models import Cliente, Proyecto, Cotizacion, Documento, Item
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Inicializar base de datos"""
    logger.info("🔧 Iniciando creación/actualización de tablas...")

    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)

        logger.info("✅ Tablas creadas/actualizadas exitosamente:")
        for table in Base.metadata.tables.keys():
            logger.info(f"   - {table}")

        logger.info("\n✅ Base de datos inicializada correctamente")

    except Exception as e:
        logger.error(f"❌ Error al inicializar base de datos: {e}")
        raise

if __name__ == "__main__":
    main()
