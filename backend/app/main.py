"""
Tesla Cotizador V3 - Aplicación Principal
FastAPI Backend
"""
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine, Base, get_db
from sqlalchemy.orm import Session
from pathlib import Path
import logging
from app.routers import cotizaciones, proyectos, documentos, chat, system # <--- AÑADE "system" A ESTA LÍNEA
logger = logging.getLogger(__name__)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Tus rutas aquí...
@app.get("/")
def read_root():
    return {"Hello": "World"}

# ============================================
# CREAR APLICACIÓN FASTAPI
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Sistema de cotización inteligente con IA (Gemini 1.5 Pro)",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================
# CONFIGURAR CORS
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# ============================================
# MANEJADORES DE ERRORES
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manejador personalizado para errores de validación
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
    Manejador general de excepciones
    """
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "message": str(exc) if settings.DEBUG else "Ha ocurrido un error"
        }
    )

# ============================================
# EVENTOS DE INICIO Y CIERRE
# ============================================

@app.on_event("startup")
async def startup_event():
    """
    Ejecutar al iniciar la aplicación
    """
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Modo: {settings.ENVIRONMENT}")
    logger.info(f"Debug: {settings.DEBUG}")
    
    # Crear tablas en la base de datos
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos verificadas/creadas")
    except Exception as e:
        logger.error(f"Error al crear tablas: {str(e)}")
    
    # Verificar directorios de storage
    dirs_to_check = [
        settings.UPLOAD_DIR,
        settings.GENERATED_DIR,
        settings.CHROMA_PERSIST_DIRECTORY
    ]
    
    for directory in dirs_to_check:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directorio verificado: {directory}")
    
    # Verificar configuración de Gemini
    if settings.GEMINI_API_KEY:
        logger.info("✅ Gemini API Key configurada")
    else:
        logger.warning("⚠️ Gemini API Key NO configurada - funcionalidad IA limitada")
    
    logger.info("🚀 Aplicación iniciada exitosamente")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Ejecutar al cerrar la aplicación
    """
    logger.info("Cerrando aplicación...")

# ============================================
# RUTAS PRINCIPALES
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    Ruta raíz - Información de la API
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "cotizaciones": "/api/cotizaciones",
            "proyectos": "/api/proyectos",
            "chat": "/api/chat",
            "documentos": "/api/documentos"
        }
    }

@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    from app.core.database import check_db_connection
    
    db_status = "connected" if check_db_connection() else "disconnected"
    
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }

@app.get("/api/info", tags=["Info"])
async def app_info():
    """
    Información detallada de la aplicación
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "database": settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else "local",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "gemini_model": settings.GEMINI_MODEL if settings.GEMINI_API_KEY else None,
        "upload_dir": settings.UPLOAD_DIR,
        "max_file_size_mb": settings.MAX_FILE_SIZE / (1024 * 1024),
        "allowed_extensions": settings.ALLOWED_EXTENSIONS,
        "cors_origins": settings.CORS_ORIGINS
    }

# ============================================
# INCLUIR ROUTERS
# ============================================

from app.routers import (
    cotizaciones_router,
    proyectos_router,
    chat_router,
    documentos_router,
    informes_router
    
)

app.include_router(
    cotizaciones_router,
    prefix="/api/cotizaciones",
    tags=["Cotizaciones"]
)

app.include_router(
    proyectos_router,
    prefix="/api/proyectos",
    tags=["Proyectos"]
)

app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat IA"]
)

app.include_router(
    documentos_router,
    prefix="/api/documentos",
    tags=["Documentos"]
)

app.include_router(
    informes_router,
    prefix="/api/informes",
    tags=["Informes"]
)

# ============================================
# SERVIR ARCHIVOS ESTÁTICOS (DESCARGAS)
# ============================================

# Montar directorio de archivos generados
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
    Descargar archivo generado
    """
    ruta_archivo = Path(settings.GENERATED_DIR) / nombre_archivo
    
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

# ============================================
# ENDPOINT DE PRUEBA DE IA
# ============================================

@app.post("/api/test/gemini", tags=["Testing"])
async def test_gemini(prompt: str = "Hola, ¿cómo estás?"):
    """
    Probar conexión con Gemini AI (solo para desarrollo)
    """
    if not settings.DEBUG:
        return {"error": "Endpoint solo disponible en modo DEBUG"}
    
    try:
        from app.services.gemini_service import gemini_service
        
        if not gemini_service.model:
            return {
                "error": "Gemini no configurado",
                "message": "Configura GEMINI_API_KEY en .env"
            }
        
        response = gemini_service.model.generate_content(prompt)
        
        return {
            "success": True,
            "prompt": prompt,
            "response": response.text,
            "model": settings.GEMINI_MODEL
        }
        
    except Exception as e:
        logger.error(f"Error en test Gemini: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# ============================================
# ESTADÍSTICAS GENERALES
# ============================================

@app.get("/api/estadisticas", tags=["Estadísticas"])
async def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    """
    Obtener estadísticas generales del sistema
    """
    from sqlalchemy.orm import Session
    from app.core.database import get_db
    from app.models.cotizacion import Cotizacion
    from app.models.proyecto import Proyecto
    from app.models.documento import Documento
    
    try:
        total_cotizaciones = db.query(Cotizacion).count()
        total_proyectos = db.query(Proyecto).count()
        total_documentos = db.query(Documento).count()
        
        # Total facturado
        cotizaciones_aprobadas = db.query(Cotizacion).filter(
            Cotizacion.estado == "aprobado"
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
        return {
            "error": str(e)
        }

# ============================================
# PARA EJECUTAR DIRECTAMENTE
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )


# En backend/app/main.py

from fastapi import FastAPI
from app.core.config import settings  # Importa la configuración
import logging

# Configura el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- (Aquí va la creación de tu 'app = FastAPI()') ---
app = FastAPI(title="Tesla Cotizador API")


# === INICIO DEL CÓDIGO A AÑADIR ===
@app.on_event("startup")
def on_startup():
    """
    Se ejecuta una vez cuando el servidor arranca.
    Nos anunciará qué configuración está activa.
    """
    logger.info("🚀 Servidor Iniciando...")
    logger.info("==================================================")
    logger.info(f"== Entorno de Trabajo: {settings.ENVIRONMENT.upper()}")
    
    # Extraemos el tipo de BD de la URL para no imprimir contraseñas
    db_type = "Desconocida"
    if settings.DATABASE_URL:
        db_type = settings.DATABASE_URL.split("://")[0]
        
    logger.info(f"== Base de Datos (ACTIVA): {db_type.upper()}")
    logger.info(f"== Modelo de IA (ACTIVO): {settings.GEMINI_MODEL}")
    logger.info("==================================================")
# === FIN DEL CÓDIGO A AÑADIR ===


# --- (Aquí van tus 'app.include_router(...)') ---
# from app.routers import cotizaciones, system, ...
# app.include_router(cotizaciones.router)
# ... etc ...