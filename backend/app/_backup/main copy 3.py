"""
Tesla Cotizador V3 - Aplicación Principal (Versión Corregida - Lógica Original Intacta)
FastAPI Backend
"""
from fastapi import FastAPI, Request, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine, Base, get_db, init_db # <-- AÑADIDO init_db
from sqlalchemy.orm import Session
from pathlib import Path
import logging

# === IMPORTACIÓN DE MODELOS (¡SECCIÓN AÑADIDA Y CRÍTICA!) ===
# Importamos todos los modelos aquí para que se "registren" en
# SQLAlchemy Base.metadata antes de que 'init_db()' sea llamado.
# Esto soluciona el error '_run_ddl_visitor' y 'no such table'.
from app.models import cotizacion, item, proyecto, documento
# Si tienes más modelos (ej. user.py), impórtalos también aquí.


# === IMPORTACIÓN DE ROUTERS (TU CÓDIGO ORIGINAL) ===
from app.routers import cotizaciones, proyectos, documentos, chat, system, informes

logger = logging.getLogger(__name__)

# ============================================\
# CREAR APLICACIÓN FASTAPI (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Sistema de cotización inteligente con IA (Gemini 1.5 Pro)",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================\
# CONFIGURAR CORS (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        settings.FRONTEND_URL # (Añadido desde tu config para robustez)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# ============================================\
# MANEJADORES DE ERRORES (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    (Tu manejador de errores de validación original)
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": errors
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    (Tu manejador de errores general original)
    """
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    
    is_debug = settings.ENVIRONMENT == "development"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "message": str(exc) if is_debug else "Ha ocurrido un error"
        }
    )

# ============================================\
# EVENTOS DE INICIO Y CIERRE (SECCIÓN AÑADIDA Y CRÍTICA)
# ============================================

@app.on_event("startup")
async def startup_event():
    """
    Ejecutar al iniciar la aplicación
    ¡AQUÍ SE CREAN LAS TABLAS!
    """
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Modo: {settings.ENVIRONMENT}")
    logger.info(f"Debug: {settings.DEBUG}")
    
    # Crear tablas en la base de datos
    # Esto soluciona el error "no such table"
    init_db()
    
    # Verificar directorios de storage
    dirs_to_check = [
        settings.UPLOAD_DIR,
        settings.GENERATED_DIR,
        settings.CHROMA_PERSIST_DIRECTORY,
        settings.TEMPLATES_DIR
    ]
    
    for directory in dirs_to_check:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directorio verificado: {directory}")
    
    # Verificar configuración de Gemini
    if settings.GEMINI_API_KEY and "AIza" in settings.GEMINI_API_KEY:
        logger.info("✅ Gemini API Key configurada")
    else:
        logger.warning("⚠️ Gemini API Key NO configurada o inválida")
    
    logger.info("🚀 Aplicación iniciada exitosamente")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Ejecutar al cerrar la aplicación
    """
    logger.info("Cerrando aplicación...")


# ============================================\
# RUTAS PRINCIPALES (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    (Tu ruta raíz original)
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "system": "/api/system",
            "cotizaciones": "/api/cotizaciones",
            "proyectos": "/api/proyectos",
            "chat": "/api/chat",
            "documentos": "/api/documentos",
            "informes": "/api/informes"
        }
    }

# ============================================\
# INCLUIR ROUTERS (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

logger.info("Incluyendo routers de la aplicación...")

app.include_router(
    system.router,
    prefix="/api/system",
    tags=["System"]
)

app.include_router(
    cotizaciones.router,
    prefix="/api/cotizaciones",
    tags=["Cotizaciones"]
)

app.include_router(
    proyectos.router,
    prefix="/api/proyectos",
    tags=["Proyectos"]
)

app.include_router(
    chat.router,
    prefix="/api/chat",
    tags=["Chat IA"]
)

app.include_router(
    documentos.router,
    prefix="/api/documentos",
    tags=["Documentos"]
)

app.include_router(
    informes.router,
    prefix="/api/informes",
    tags=["Informes"]
)

# ============================================\
# SERVIR ARCHIVOS ESTÁTICOS (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

try:
    app.mount(
        "/api/descargas",
        StaticFiles(directory=settings.GENERATED_DIR),
        name="descargas"
    )
    logger.info(f"Directorio de descargas montado: {settings.GENERATED_DIR}")
except Exception as e:
    logger.warning(f"No se pudo montar directorio de descargas: {str(e)}")

@app.get("/api/descargas/{nombre_archivo}", tags=["Descargas"])
async def descargar_archivo(nombre_archivo: str):
    """
    (Tu endpoint de descargas original)
    """
    ruta_archivo = settings.GENERATED_DIR / nombre_archivo
    
    if not ruta_archivo.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado"
        )
    
    return FileResponse(
        path=ruta_archivo,
        filename=nombre_archivo,
        media_type='application/octet-stream'
    )

# ============================================\
# ESTADÍSTICAS (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

@app.get("/api/estadisticas", tags=["Estadísticas"])
async def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    """
    (Tu endpoint de estadísticas original)
    """
    try:
        total_cotizaciones = db.query(cotizacion.Cotizacion).count()
        total_proyectos = db.query(proyecto.Proyecto).count()
        total_documentos = db.query(documento.Documento).count()
        
        cotizaciones_aprobadas = db.query(cotizacion.Cotizacion).filter(
            cotizacion.Cotizacion.estado == "aprobado"
        ).all()
        
        total_facturado = sum(
            float(cot.total) if cot.total else 0
            for cot in cotizaciones_aprobadas
        )
        
        return {
            "total_cotizaciones": total_cotizaciones,
            "total_proyectos": total_proyectos,
            "total_documentos": total_documentos,
            "total_facturado": round(total_facturado, 2),
            "cotizaciones_aprobadas": len(cotizaciones_aprobadas)
        }
        
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {str(e)}")
        # Si las tablas aún no existen, esto fallará
        return {
            "error": "Error al calcular estadísticas (posiblemente tablas no creadas)",
            "detalle": str(e)
        }

# ============================================\
# PARA EJECUTAR DIRECTAMENTE (TU CÓDIGO ORIGINAL INTACTO)
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )