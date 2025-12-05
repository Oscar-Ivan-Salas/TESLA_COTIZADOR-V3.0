"""
Script para capturar la excepción exacta que está ocurriendo
"""
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=" * 80)
print("CAPTURANDO EXCEPCIÓN EXACTA EN MAIN.PY")
print("=" * 80)
print()

# Simular exactamente lo que hace main.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROUTERS_AVANZADOS_DISPONIBLES = False
routers_info = {}

try:
    logger.info("🔄 Intentando cargar routers avanzados...")
    
    # Importar routers uno por uno
    try:
        from app.routers import chat
        routers_info["chat"] = {
            "router": chat.router,
            "prefix": "/api/chat",
            "tags": ["Chat PILI"],
            "descripcion": "Chat conversacional con PILI IA"
        }
        logger.info("✅ Router Chat PILI cargado")
    except Exception as e:
        logger.warning(f"⚠️ Router chat no disponible: {e}")
    
    try:
        from app.routers import cotizaciones
        routers_info["cotizaciones"] = {
            "router": cotizaciones.router,
            "prefix": "/api/cotizaciones",
            "tags": ["Cotizaciones"],
            "descripcion": "CRUD completo cotizaciones"
        }
        logger.info("✅ Router Cotizaciones cargado")
    except Exception as e:
        logger.warning(f"⚠️ Router cotizaciones no disponible: {e}")
    
    try:
        from app.routers import proyectos
        routers_info["proyectos"] = {
            "router": proyectos.router,
            "prefix": "/api/proyectos",
            "tags": ["Proyectos"],
            "descripcion": "Gestión completa de proyectos"
        }
        logger.info("✅ Router Proyectos cargado")
    except Exception as e:
        logger.warning(f"⚠️ Router proyectos no disponible: {e}")
    
    try:
        from app.routers import informes
        routers_info["informes"] = {
            "router": informes.router,
            "prefix": "/api/informes",
            "tags": ["Informes"],
            "descripcion": "Generación de informes técnicos"
        }
        logger.info("✅ Router Informes cargado")
    except Exception as e:
        logger.warning(f"⚠️ Router informes no disponible: {e}")
    
    try:
        from app.routers import documentos
        routers_info["documentos"] = {
            "router": documentos.router,
            "prefix": "/api/documentos",
            "tags": ["Documentos"],
            "descripcion": "Gestión y análisis de documentos"
        }
        logger.info("✅ Router Documentos cargado")
    except Exception as e:
        logger.warning(f"⚠️ Router documentos no disponible: {e}")
    
    try:
        from app.routers import system
        routers_info["system"] = {
            "router": system.router,
            "prefix": "/api/system",
            "tags": ["Sistema"],
            "descripcion": "Health checks y configuración"
        }
        logger.info("✅ Router System cargado")
    except Exception as e:
        logger.warning(f"⚠️ Router system no disponible: {e}")
    
    print()
    print(f"📊 Routers en routers_info: {len(routers_info)}")
    print(f"📋 Routers: {list(routers_info.keys())}")
    print()
    
    # Verificar si tenemos suficientes routers para modo completo
    if len(routers_info) >= 1:
        ROUTERS_AVANZADOS_DISPONIBLES = True
        logger.info(f"🎉 ROUTERS AVANZADOS ACTIVADOS: {len(routers_info)}/6 disponibles")
        logger.info(f"📋 Routers cargados: {list(routers_info.keys())}")
        print()
        print(f"✅ ROUTERS_AVANZADOS_DISPONIBLES = {ROUTERS_AVANZADOS_DISPONIBLES}")
    else:
        logger.warning("⚠️ Ningún router avanzado disponible, manteniendo modo básico")
        print()
        print(f"❌ ROUTERS_AVANZADOS_DISPONIBLES = {ROUTERS_AVANZADOS_DISPONIBLES}")
    
    print()
    print("=" * 80)
    print("🎯 RESULTADO: El bloque try se completó SIN EXCEPCIONES")
    print("=" * 80)
    print(f"ROUTERS_AVANZADOS_DISPONIBLES = {ROUTERS_AVANZADOS_DISPONIBLES}")
    print()
        
except Exception as e:
    print()
    print("=" * 80)
    print("❌ ¡EXCEPCIÓN CAPTURADA!")
    print("=" * 80)
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()
    print("Traceback completo:")
    import traceback
    traceback.print_exc()
    print()
    print("=" * 80)
    print("Esta es la excepción que está forzando ROUTERS_AVANZADOS_DISPONIBLES = False")
    print("=" * 80)
    
    ROUTERS_AVANZADOS_DISPONIBLES = False
    logger.warning(f"⚠️ Error general cargando routers avanzados: {e}")
    logger.info("🔄 Continuando en modo básico/demo")
    
    print()
    print(f"ROUTERS_AVANZADOS_DISPONIBLES = {ROUTERS_AVANZADOS_DISPONIBLES}")
