from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models import Proyecto, Cotizacion, Documento
from app.models.proyecto import EstadoProyecto
from app.schemas.proyecto import (
    ProyectoCreate,
    ProyectoUpdate,
    ProyectoResponse
)

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