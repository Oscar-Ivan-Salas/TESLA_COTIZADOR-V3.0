from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import os

from app.core.database import get_db
from app.models import Cotizacion, Proyecto
from app.services.word_generator import word_generator
from app.services.pdf_generator import pdf_generator

router = APIRouter()

@router.post("/generar-pdf/{cotizacion_id}")
async def generar_pdf_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Genera un PDF profesional de la cotización
    """
    
    # Obtener cotización
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    # Preparar datos
    datos = {
        "numero": cotizacion.numero,
        "cliente": cotizacion.cliente,
        "proyecto": cotizacion.proyecto,
        "descripcion": cotizacion.descripcion,
        "items": cotizacion.items or [],
        "subtotal": cotizacion.subtotal,
        "igv": cotizacion.igv,
        "total": cotizacion.total,
        "observaciones": cotizacion.metadata_adicional.get("observaciones", "") if cotizacion.metadata_adicional else "",
        "vigencia": cotizacion.metadata_adicional.get("vigencia", "30 días") if cotizacion.metadata_adicional else "30 días"
    }
    
    # Generar PDF
    try:
        nombre_archivo = f"cotizacion_{cotizacion.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_salida = os.path.join("storage", "generados", nombre_archivo)
        
        pdf_generator.generar_cotizacion(datos, ruta_salida)
        
        # Verificar que se creó el archivo
        if not os.path.exists(ruta_salida):
            raise Exception("No se pudo crear el archivo PDF")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar PDF: {str(e)}"
        )

@router.post("/generar-word/{cotizacion_id}")
async def generar_word_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Genera un documento Word profesional de la cotización
    """
    
    # Obtener cotización
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    # Preparar datos
    datos = {
        "numero": cotizacion.numero,
        "cliente": cotizacion.cliente,
        "proyecto": cotizacion.proyecto,
        "descripcion": cotizacion.descripcion,
        "items": cotizacion.items or [],
        "subtotal": cotizacion.subtotal,
        "igv": cotizacion.igv,
        "total": cotizacion.total,
        "observaciones": cotizacion.metadata_adicional.get("observaciones", "") if cotizacion.metadata_adicional else "",
        "vigencia": cotizacion.metadata_adicional.get("vigencia", "30 días") if cotizacion.metadata_adicional else "30 días"
    }
    
    # Generar Word
    try:
        nombre_archivo = f"cotizacion_{cotizacion.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join("storage", "generados", nombre_archivo)
        
        word_generator.generar_cotizacion(datos, ruta_salida)
        
        # Verificar que se creó el archivo
        if not os.path.exists(ruta_salida):
            raise Exception("No se pudo crear el archivo Word")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar Word: {str(e)}"
        )

@router.post("/generar-informe-ejecutivo/{proyecto_id}")
async def generar_informe_ejecutivo(
    proyecto_id: int,
    incluir_cotizaciones: bool = True,
    incluir_documentos: bool = True,
    db: Session = Depends(get_db)
):
    """
    Genera un informe ejecutivo completo del proyecto
    """
    
    # Obtener proyecto
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Obtener cotizaciones relacionadas
    cotizaciones = []
    if incluir_cotizaciones:
        cotizaciones = db.query(Cotizacion).filter(
            Cotizacion.proyecto_id == proyecto_id
        ).all()
    
    # Preparar datos
    datos = {
        "nombre": proyecto.nombre,
        "descripcion": proyecto.descripcion,
        "cliente": proyecto.cliente,
        "estado": proyecto.estado.value,
        "fecha_inicio": proyecto.fecha_inicio,
        "fecha_fin": proyecto.fecha_fin,
        "cotizaciones": [
            {
                "numero": cot.numero,
                "estado": cot.estado,
                "total": cot.total
            }
            for cot in cotizaciones
        ] if cotizaciones else [],
        "valor_total": sum(cot.total for cot in cotizaciones if cot.estado == "aprobada") if cotizaciones else 0
    }
    
    # Generar informe
    try:
        nombre_archivo = f"informe_ejecutivo_{proyecto.nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx"
        ruta_salida = os.path.join("storage", "generados", nombre_archivo)
        
        word_generator.generar_informe_ejecutivo(datos, ruta_salida)
        
        if not os.path.exists(ruta_salida):
            raise Exception("No se pudo crear el informe")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar informe: {str(e)}"
        )

@router.post("/generar-pdf-simple")
async def generar_pdf_simple(
    datos: dict
):
    """
    Genera un PDF simple con datos arbitrarios (para testing)
    """
    
    try:
        nombre_archivo = f"informe_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_salida = os.path.join("storage", "generados", nombre_archivo)
        
        pdf_generator.generar_informe_simple(datos, ruta_salida)
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
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
                "uso": "Resúmenes ejecutivos, reportes de estado"
            }
        ]
    }