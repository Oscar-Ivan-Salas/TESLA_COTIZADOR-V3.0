from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path
import logging
import os

from app.core.database import get_db
from app.models import Proyecto, Cotizacion, Documento
from app.models.proyecto import EstadoProyecto
from app.schemas.proyecto import (
    ProyectoCreate,
    ProyectoUpdate,
    ProyectoResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
async def crear_proyecto(
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo proyecto
    """
    
    db_proyecto = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        cliente=proyecto.cliente,
        estado=EstadoProyecto.PLANIFICACION,
        metadata_adicional=proyecto.metadata_adicional,
        fecha_inicio=datetime.utcnow()
    )
    
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto

@router.get("/", response_model=List[ProyectoResponse])
async def listar_proyectos(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[EstadoProyecto] = None,
    cliente: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos los proyectos con filtros opcionales
    """
    
    query = db.query(Proyecto)
    
    # Aplicar filtros
    if estado:
        query = query.filter(Proyecto.estado == estado)
    
    if cliente:
        query = query.filter(Proyecto.cliente.ilike(f"%{cliente}%"))
    
    # Ordenar por fecha de creación
    query = query.order_by(Proyecto.fecha_creacion.desc())
    
    proyectos = query.offset(skip).limit(limit).all()
    
    return proyectos

@router.get("/{proyecto_id}", response_model=ProyectoResponse)
async def obtener_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un proyecto por ID con información completa
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    return proyecto

@router.get("/{proyecto_id}/detalle")
async def obtener_proyecto_detallado(
    proyecto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un proyecto con todas sus relaciones (cotizaciones, documentos)
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Obtener cotizaciones relacionadas
    cotizaciones = db.query(Cotizacion).filter(
        Cotizacion.proyecto_id == proyecto_id
    ).all()
    
    # Obtener documentos relacionados
    documentos = db.query(Documento).filter(
        Documento.proyecto_id == proyecto_id
    ).all()
    
    return {
        "proyecto": proyecto,
        "cotizaciones": cotizaciones,
        "documentos": documentos,
        "estadisticas": {
            "total_cotizaciones": len(cotizaciones),
            "total_documentos": len(documentos),
            "cotizaciones_aprobadas": sum(1 for c in cotizaciones if c.estado == "aprobada"),
            "valor_total": sum(c.total for c in cotizaciones if c.estado == "aprobada")
        }
    }

@router.put("/{proyecto_id}", response_model=ProyectoResponse)
async def actualizar_proyecto(
    proyecto_id: int,
    proyecto_update: ProyectoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un proyecto existente
    """
    
    db_proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Actualizar campos
    update_data = proyecto_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_proyecto, field, value)
    
    db_proyecto.fecha_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto

@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un proyecto
    NOTA: Esto también eliminará todas las cotizaciones y documentos relacionados
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    db.delete(proyecto)
    db.commit()
    
    return None

@router.patch("/{proyecto_id}/estado")
async def cambiar_estado_proyecto(
    proyecto_id: int,
    nuevo_estado: EstadoProyecto,
    db: Session = Depends(get_db)
):
    """
    Cambia el estado de un proyecto
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    proyecto.estado = nuevo_estado
    proyecto.fecha_modificacion = datetime.utcnow()
    
    # Si se completa o cancela, establecer fecha de fin
    if nuevo_estado in [EstadoProyecto.COMPLETADO, EstadoProyecto.CANCELADO]:
        if not proyecto.fecha_fin:
            proyecto.fecha_fin = datetime.utcnow()
    
    db.commit()
    db.refresh(proyecto)
    
    return proyecto

@router.get("/stats/resumen")
async def obtener_estadisticas_proyectos(
    db: Session = Depends(get_db)
):
    """
    Obtiene estadísticas generales de proyectos
    """
    
    total = db.query(Proyecto).count()
    
    por_estado = {}
    for estado in EstadoProyecto:
        por_estado[estado.value] = db.query(Proyecto).filter(
            Proyecto.estado == estado
        ).count()
    
    return {
        "total_proyectos": total,
        "por_estado": por_estado
    }

# ════════════════════════════════════════════════════════════════
# ✅ NUEVOS ENDPOINTS - GENERACIÓN DE INFORMES DE PROYECTO
# ════════════════════════════════════════════════════════════════

@router.post("/{proyecto_id}/generar-informe-word")
async def generar_informe_proyecto_word(
    proyecto_id: int,
    incluir_cotizaciones: bool = Body(True),
    incluir_documentos: bool = Body(True),
    incluir_estadisticas: bool = Body(True),
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    usar_plantilla: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Genera un informe ejecutivo del proyecto en formato Word
    
    MODO COMPLEJO - Proyecto Complejo
    
    Incluye:
    - Información general del proyecto
    - Todas las cotizaciones asociadas
    - Documentos relacionados
    - Estadísticas financieras
    - Timeline del proyecto
    - Logo personalizado
    - Formato profesional
    
    Args:
        proyecto_id: ID del proyecto
        incluir_cotizaciones: Si incluir tabla de cotizaciones
        incluir_documentos: Si listar documentos del proyecto
        incluir_estadisticas: Si incluir gráficos y estadísticas
        opciones: Opciones de visualización
        logo_base64: Logo en base64
        usar_plantilla: Nombre de plantilla personalizada (opcional)
    
    Returns:
        Archivo Word para descarga
    """
    
    try:
        # Obtener proyecto
        proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
        
        if not proyecto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proyecto no encontrado"
            )
        
        logger.info(f"Generando informe Word para proyecto: {proyecto.nombre}")
        
        # Obtener cotizaciones relacionadas
        cotizaciones = []
        if incluir_cotizaciones:
            cotizaciones_db = db.query(Cotizacion).filter(
                Cotizacion.proyecto_id == proyecto_id
            ).all()
            
            for cot in cotizaciones_db:
                cotizaciones.append({
                    "numero": cot.numero,
                    "cliente": cot.cliente,
                    "proyecto": cot.proyecto,
                    "estado": cot.estado,
                    "subtotal": float(cot.subtotal) if cot.subtotal else 0,
                    "igv": float(cot.igv) if cot.igv else 0,
                    "total": float(cot.total) if cot.total else 0,
                    "fecha_creacion": cot.fecha_creacion.strftime("%d/%m/%Y") if cot.fecha_creacion else "N/A"
                })
        
        # Obtener documentos relacionados
        documentos_info = []
        if incluir_documentos:
            documentos_db = db.query(Documento).filter(
                Documento.proyecto_id == proyecto_id
            ).all()
            
            for doc in documentos_db:
                documentos_info.append({
                    "nombre": doc.nombre_original,
                    "tipo": doc.tipo_mime,
                    "tamano_mb": round(doc.tamano / (1024 * 1024), 2),
                    "fecha_subida": doc.fecha_subida.strftime("%d/%m/%Y") if doc.fecha_subida else "N/A",
                    "procesado": "Sí" if doc.procesado == 1 else "No"
                })
        
        # Calcular estadísticas
        total_cotizaciones = len(cotizaciones)
        cotizaciones_aprobadas = sum(1 for c in cotizaciones if c.get('estado') == 'aprobada')
        valor_total = sum(c.get('total', 0) for c in cotizaciones if c.get('estado') == 'aprobada')
        
        # Preparar datos del informe
        datos_informe = {
            # Información del proyecto
            "cliente": proyecto.cliente,
            "proyecto": proyecto.nombre,
            "numero": f"PROY-{proyecto.id:04d}",
            "descripcion": proyecto.descripcion or "Sin descripción",
            
            # Metadata del proyecto
            "estado": proyecto.estado.value if hasattr(proyecto.estado, 'value') else str(proyecto.estado),
            "fecha_inicio": proyecto.fecha_inicio.strftime("%d/%m/%Y") if proyecto.fecha_inicio else "N/A",
            "fecha_fin": proyecto.fecha_fin.strftime("%d/%m/%Y") if proyecto.fecha_fin else "En curso",
            
            # Cotizaciones
            "cotizaciones": cotizaciones,
            
            # Documentos
            "documentos": documentos_info,
            
            # Estadísticas
            "total_cotizaciones": total_cotizaciones,
            "cotizaciones_aprobadas": cotizaciones_aprobadas,
            "total_documentos": len(documentos_info),
            "subtotal": valor_total,
            "igv": valor_total * 0.18,
            "total": valor_total * 1.18
        }
        
        # Usar word_generator o template_processor
        from app.services.word_generator import word_generator
        from app.core.config import settings
        
        # Nombre del archivo
        nombre_archivo = f"informe_proyecto_{proyecto.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        # Si hay plantilla personalizada, usar template_processor
        if usar_plantilla:
            from app.services.template_processor import template_processor
            
            ruta_plantilla = os.path.join(
                settings.TEMPLATES_DIR,
                usar_plantilla
            )
            
            if not os.path.exists(ruta_plantilla):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Plantilla no encontrada: {usar_plantilla}"
                )
            
            ruta_salida = template_processor.procesar_plantilla(
                ruta_plantilla=ruta_plantilla,
                datos_cotizacion=datos_informe,
                ruta_salida=ruta_salida,
                logo_base64=logo_base64
            )
        else:
            # Usar generador estándar
            word_generator.generar_informe_proyecto(
                datos=datos_informe,
                ruta_salida=ruta_salida,
                opciones=opciones or {},
                logo_base64=logo_base64
            )
        
        # Verificar que se creó el archivo
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el informe"
            )
        
        logger.info(f"✅ Informe generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al generar informe Word: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar informe: {str(e)}"
        )

@router.post("/{proyecto_id}/generar-informe-pdf")
async def generar_informe_proyecto_pdf(
    proyecto_id: int,
    incluir_cotizaciones: bool = Body(True),
    incluir_documentos: bool = Body(True),
    incluir_estadisticas: bool = Body(True),
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Genera un informe ejecutivo del proyecto en formato PDF
    
    MODO COMPLEJO - Proyecto Complejo
    
    Similar al Word pero genera PDF (no editable)
    
    Args:
        proyecto_id: ID del proyecto
        incluir_cotizaciones: Si incluir tabla de cotizaciones
        incluir_documentos: Si listar documentos del proyecto
        incluir_estadisticas: Si incluir gráficos y estadísticas
        opciones: Opciones de visualización
        logo_base64: Logo en base64
    
    Returns:
        Archivo PDF para descarga
    """
    
    try:
        # Obtener proyecto
        proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
        
        if not proyecto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proyecto no encontrado"
            )
        
        logger.info(f"Generando informe PDF para proyecto: {proyecto.nombre}")
        
        # Obtener cotizaciones relacionadas
        cotizaciones = []
        if incluir_cotizaciones:
            cotizaciones_db = db.query(Cotizacion).filter(
                Cotizacion.proyecto_id == proyecto_id
            ).all()
            
            for cot in cotizaciones_db:
                cotizaciones.append({
                    "numero": cot.numero,
                    "estado": cot.estado,
                    "total": float(cot.total) if cot.total else 0
                })
        
        # Obtener documentos relacionados
        documentos_info = []
        if incluir_documentos:
            documentos_db = db.query(Documento).filter(
                Documento.proyecto_id == proyecto_id
            ).all()
            
            for doc in documentos_db:
                documentos_info.append({
                    "nombre": doc.nombre_original,
                    "tipo": doc.tipo_mime,
                    "fecha": doc.fecha_subida.strftime("%d/%m/%Y") if doc.fecha_subida else "N/A"
                })
        
        # Calcular estadísticas
        valor_total = sum(c.get('total', 0) for c in cotizaciones if c.get('estado') == 'aprobada')
        
        # Preparar datos
        datos = {
            "nombre": proyecto.nombre,
            "descripcion": proyecto.descripcion,
            "cliente": proyecto.cliente,
            "estado": proyecto.estado.value if hasattr(proyecto.estado, 'value') else str(proyecto.estado),
            "fecha_inicio": proyecto.fecha_inicio,
            "fecha_fin": proyecto.fecha_fin,
            "cotizaciones": cotizaciones,
            "documentos": documentos_info,
            "valor_total": valor_total
        }
        
        # Generar PDF
        from app.services.pdf_generator import pdf_generator
        from app.core.config import settings
        
        nombre_archivo = f"informe_proyecto_{proyecto.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        pdf_generator.generar_informe_proyecto(
            datos=datos,
            ruta_salida=ruta_salida,
            opciones=opciones or {},
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el PDF"
            )
        
        logger.info(f"✅ PDF generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al generar informe PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar PDF: {str(e)}"
        )