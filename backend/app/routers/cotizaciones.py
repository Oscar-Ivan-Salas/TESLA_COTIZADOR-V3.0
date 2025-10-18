"""
Router: Cotizaciones
Endpoints para CRUD de cotizaciones
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.cotizacion import Cotizacion
from app.models.item import Item
from app.schemas.cotizacion import (
    CotizacionCreate,
    CotizacionUpdate,
    CotizacionResponse
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def generar_numero_cotizacion(db: Session) -> str:
    """
    Generar número único de cotización
    Formato: COT-YYYYMM-XXXX
    """
    fecha = datetime.now()
    prefijo = f"COT-{fecha.strftime('%Y%m')}"
    
    # Buscar última cotización del mes
    ultima = db.query(Cotizacion).filter(
        Cotizacion.numero.like(f"{prefijo}%")
    ).order_by(Cotizacion.numero.desc()).first()
    
    if ultima:
        # Extraer número secuencial
        try:
            ultimo_num = int(ultima.numero.split('-')[-1])
            nuevo_num = ultimo_num + 1
        except:
            nuevo_num = 1
    else:
        nuevo_num = 1
    
    return f"{prefijo}-{nuevo_num:04d}"

# ============================================
# ENDPOINTS DE COTIZACIONES
# ============================================

@router.get("/", response_model=List[CotizacionResponse])
def listar_cotizaciones(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    cliente: Optional[str] = Query(None, description="Filtrar por cliente"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    proyecto_id: Optional[int] = Query(None, description="Filtrar por proyecto"),
    db: Session = Depends(get_db)
):
    """
    Listar todas las cotizaciones con paginación y filtros
    """
    try:
        query = db.query(Cotizacion)
        
        # Filtros
        if cliente:
            query = query.filter(Cotizacion.cliente.ilike(f"%{cliente}%"))
        
        if estado:
            query = query.filter(Cotizacion.estado == estado)
        
        if proyecto_id:
            query = query.filter(Cotizacion.proyecto_id == proyecto_id)
        
        # Paginación
        cotizaciones = query.order_by(Cotizacion.fecha_creacion.desc()).offset(skip).limit(limit).all()
        
        return cotizaciones
        
    except Exception as e:
        logger.error(f"Error al listar cotizaciones: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar cotizaciones: {str(e)}"
        )

@router.get("/{cotizacion_id}", response_model=CotizacionResponse)
def obtener_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una cotización por ID
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    return cotizacion

@router.post("/", response_model=CotizacionResponse, status_code=status.HTTP_201_CREATED)
def crear_cotizacion(
    cotizacion_data: CotizacionCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva cotización
    """
    try:
        # Generar número de cotización
        numero = generar_numero_cotizacion(db)
        
        # Crear cotización
        nueva_cotizacion = Cotizacion(
            numero=numero,
            cliente=cotizacion_data.cliente,
            proyecto=cotizacion_data.proyecto,
            descripcion=cotizacion_data.descripcion,
            estado=cotizacion_data.estado,
            items=cotizacion_data.items,
            proyecto_id=cotizacion_data.proyecto_id
        )
        
        # Calcular totales
        if cotizacion_data.items:
            nueva_cotizacion.calcular_totales()
            
            # Crear items en la tabla items
            for item_data in cotizacion_data.items:
                item = Item(
                    descripcion=item_data.get('descripcion', ''),
                    cantidad=float(item_data.get('cantidad', 0)),
                    precio_unitario=float(item_data.get('precio_unitario', 0)),
                    total=float(item_data.get('cantidad', 0)) * float(item_data.get('precio_unitario', 0))
                )
                nueva_cotizacion.items_rel.append(item)
        
        db.add(nueva_cotizacion)
        db.commit()
        db.refresh(nueva_cotizacion)
        
        logger.info(f"Cotización creada: {numero} - Cliente: {nueva_cotizacion.cliente}")
        
        return nueva_cotizacion
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear cotización: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cotización: {str(e)}"
        )

@router.put("/{cotizacion_id}", response_model=CotizacionResponse)
def actualizar_cotizacion(
    cotizacion_id: int,
    cotizacion_data: CotizacionUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una cotización existente
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        # Actualizar campos
        update_data = cotizacion_data.model_dump(exclude_unset=True)
        
        for campo, valor in update_data.items():
            if campo == 'items' and valor is not None:
                # Eliminar items antiguos
                db.query(Item).filter(Item.cotizacion_id == cotizacion_id).delete()
                
                # Crear nuevos items
                for item_data in valor:
                    item = Item(
                        descripcion=item_data.get('descripcion', ''),
                        cantidad=float(item_data.get('cantidad', 0)),
                        precio_unitario=float(item_data.get('precio_unitario', 0)),
                        total=float(item_data.get('cantidad', 0)) * float(item_data.get('precio_unitario', 0)),
                        cotizacion_id=cotizacion_id
                    )
                    db.add(item)
            else:
                setattr(cotizacion, campo, valor)
        
        # Recalcular totales
        cotizacion.calcular_totales()
        
        db.commit()
        db.refresh(cotizacion)
        
        logger.info(f"Cotización actualizada: {cotizacion.numero}")
        
        return cotizacion
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar cotización: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cotización: {str(e)}"
        )

@router.delete("/{cotizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una cotización
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        numero = cotizacion.numero
        db.delete(cotizacion)
        db.commit()
        
        logger.warning(f"Cotización eliminada: {numero}")
        
        return None
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar cotización: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cotización: {str(e)}"
        )

@router.post("/{cotizacion_id}/generar-word")
def generar_word(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Generar documento Word de la cotización
    """
    from app.services.word_generator import word_generator
    
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        # Generar documento
        ruta_archivo = word_generator.generar_cotizacion(cotizacion.to_dict())
        
        from pathlib import Path
        nombre_archivo = Path(ruta_archivo).name
        
        return {
            "success": True,
            "message": "Documento Word generado exitosamente",
            "ruta_archivo": ruta_archivo,
            "nombre_archivo": nombre_archivo,
            "url_descarga": f"/api/descargas/{nombre_archivo}"
        }
        
    except Exception as e:
        logger.error(f"Error al generar Word: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar Word: {str(e)}"
        )

@router.post("/{cotizacion_id}/generar-pdf")
def generar_pdf(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Generar documento PDF de la cotización
    """
    from app.services.pdf_generator import pdf_generator
    
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        # Generar documento
        ruta_archivo = pdf_generator.generar_cotizacion(cotizacion.to_dict())
        
        from pathlib import Path
        nombre_archivo = Path(ruta_archivo).name
        
        return {
            "success": True,
            "message": "Documento PDF generado exitosamente",
            "ruta_archivo": ruta_archivo,
            "nombre_archivo": nombre_archivo,
            "url_descarga": f"/api/descargas/{nombre_archivo}"
        }
        
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar PDF: {str(e)}"
        )

@router.get("/{cotizacion_id}/items")
def obtener_items_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los items de una cotización
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    return {
        "cotizacion_id": cotizacion_id,
        "numero_cotizacion": cotizacion.numero,
        "items": [item.to_dict() for item in cotizacion.items_rel]
    }