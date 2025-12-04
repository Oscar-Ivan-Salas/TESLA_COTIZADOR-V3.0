# backend/app/routers/system.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import google.generativeai as genai
import logging

# Importaciones correctas según la estructura de tu proyecto
from app.core.database import get_db
from app.core.config import settings, get_empresa_info

# Usar el mismo logger que el resto de la aplicación
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["System Health"],
)

@router.get("/health", 
            summary="Verifica la salud del sistema",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Una o más dependencias críticas no están operativas"}
            })
async def check_system_health(db: Session = Depends(get_db)):
    """
    Verifica el estado de las conexiones críticas del sistema:
    1.  **Base de Datos**: Realiza una consulta simple para asegurar la conexión.
    2.  **Servicio de IA**: Se comunica con la API de Google Gemini para validar la clave y la conectividad.
    """
    db_status = "disconnected"
    ai_status = "unresponsive"
    
    # --- 1. Verificar la conexión a la Base de Datos ---
    try:
        # La dependencia get_db ya maneja la creación de la sesión.
        # Solo necesitamos ejecutar una consulta para probarla.
        db.execute(text("SELECT 1"))
        db_status = "connected"
        logger.info("Conexión a la base de datos verificada con éxito.")
    except Exception as e:
        logger.error(f"Error de conexión a la BD durante el health check: {e}", exc_info=True)
        # No lanzamos excepción aquí para poder reportar ambos estados

    # --- 2. Verificar la conexión a la API de Gemini ---
    try:
        # Obtenemos la clave desde la configuración centralizada, no de variables de entorno directas
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            ai_status = "api_key_not_found_in_settings"
            logger.warning("GEMINI_API_KEY no encontrada en el archivo de configuración.")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = await model.generate_content_async("test", generation_config={"max_output_tokens": 5})
            if response.text:
                ai_status = "responsive"
                logger.info("Conexión con el servicio de IA (Gemini) verificada con éxito.")
    except Exception as e:
        logger.error(f"Error de conexión con la IA durante el health check: {e}", exc_info=True)

    # --- 3. Reportar el estado final ---
    if db_status != "connected" or ai_status != "responsive":
        # Si algo falla, el estado general es de error 503 Service Unavailable
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"database": db_status, "ai_service": ai_status}
        )

    return {"status": "ok", "database": db_status, "ai_service": ai_status}


@router.get("/empresa-info",
            summary="Obtiene información de la empresa (SSOT)",
            status_code=status.HTTP_200_OK)
async def get_empresa_information():
    """
    Retorna información corporativa de Tesla Electricidad.

    Esta es la **Single Source of Truth (SSOT)** para datos de la empresa.
    Todos los documentos (Word, PDF) y el frontend obtienen datos desde aquí.

    **Returns:**
    - nombre: Nombre legal de la empresa
    - ruc: RUC de la empresa
    - direccion: Dirección física
    - telefono: Teléfono de contacto
    - email: Email de contacto
    - ciudad: Ciudad y región
    - web: Sitio web (opcional)
    """
    try:
        info = get_empresa_info()
        logger.info("Información de empresa solicitada")
        return {
            "exito": True,
            "datos": info
        }
    except Exception as e:
        logger.error(f"Error al obtener información de empresa: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener información de la empresa"
        )