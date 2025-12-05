"""
Router: Informes
Endpoints para generación de informes técnicos y ejecutivos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import os
import logging

from app.core.database import get_db
from app.models.informe import Informe
from app.services.word_generator import word_generator
from app.services.pdf_generator import pdf_generator
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def _preparar_datos_informe(informe: Informe) -> dict:
    """
    Helper para convertir un modelo de Informe a un diccionario
    para los generadores de Word/PDF.
    """
    datos = {
        "titulo": informe.titulo,
        "tipo": informe.tipo.value if informe.tipo else "simple",
        "fecha": informe.fecha_creacion.strftime('%d/%m/%Y') if informe.fecha_creacion else datetime.now().strftime('%d/%m/%Y'),
        "contenido": informe.contenido or "",
        "resumen_ejecutivo": informe.resumen_ejecutivo or "",
        "conclusiones": informe.conclusiones or "",
        "recomendaciones": informe.recomendaciones or "",
        "incluir_graficos": informe.incluir_graficos,
        "incluir_tablas": informe.incluir_tablas,
        "metadata_adicional": informe.metadata_adicional or {}
    }
    return datos

# ============================================
# ENDPOINTS DE GENERACIÓN
# ============================================

@router.post("/{informe_id}/generar-word")
async def generar_word_informe(
    informe_id: int,
    db: Session = Depends(get_db)
):
    """
    Genera un documento Word del informe
    """

    # Obtener informe
    informe = db.query(Informe).filter(Informe.id == informe_id).first()

    if not informe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Informe no encontrado"
        )

    # Preparar datos
    datos = _preparar_datos_informe(informe)

    # Definir ruta de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"Informe_{informe.tipo.value}_{timestamp}.docx"
    ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)

    try:
        # Generar Word usando el generador existente
        # Usar el método generar_informe_simple del word_generator
        word_generator.generar_informe_simple(
            datos=datos,
            ruta_salida=ruta_salida,
            opciones={'incluir_graficos': informe.incluir_graficos}
        )

        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el documento Word"
            )

        logger.info(f"✅ Word de informe generado: {nombre_archivo}")

        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        logger.error(f"Error al generar Word: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar Word: {str(e)}"
        )

@router.post("/{informe_id}/generar-pdf")
async def generar_pdf_informe(
    informe_id: int,
    db: Session = Depends(get_db)
):
    """
    Genera un PDF del informe
    """

    # Obtener informe
    informe = db.query(Informe).filter(Informe.id == informe_id).first()

    if not informe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Informe no encontrado"
        )

    # Preparar datos
    datos = _preparar_datos_informe(informe)

    # Definir ruta de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"Informe_{informe.tipo.value}_{timestamp}.pdf"
    ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)

    try:
        # Generar PDF
        pdf_generator.generar_informe_simple(
            datos=datos,
            ruta_salida=ruta_salida
        )

        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el PDF"
            )

        logger.info(f"✅ PDF de informe generado: {nombre_archivo}")

        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )

    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar PDF: {str(e)}"
        )

@router.get("/formatos-disponibles")
async def obtener_formatos_disponibles():
    """
    Lista los formatos de documentos disponibles
    """

    return {
        "formatos": [
            {
                "tipo": "pdf",
                "descripcion": "Documento PDF profesional",
                "uso": "Para envío a clientes, presentaciones formales"
            },
            {
                "tipo": "word",
                "descripcion": "Documento Word editable",
                "uso": "Para edición posterior, personalización"
            },
            {
                "tipo": "informe_ejecutivo",
                "descripcion": "Informe completo del proyecto",
                "uso": "Resúmenes ejecutivos, análisis de IA"
            }
        ]
    }
