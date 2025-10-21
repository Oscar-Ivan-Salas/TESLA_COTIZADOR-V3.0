"""
Router: Cotizaciones
Endpoints para CRUD de cotizaciones
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.models.cotizacion import Cotizacion
from app.models.item import Item
from app.schemas.cotizacion import (
    CotizacionCreate,
    CotizacionUpdate,
    CotizacionResponse
)
from datetime import datetime
from pathlib import Path
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

# ============================================
# GENERACIÓN DE DOCUMENTOS (WORD Y PDF)
# ============================================

@router.post("/{cotizacion_id}/generar-word")
async def generar_word(
    cotizacion_id: int,
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Generar documento Word de la cotización
    
    Body (JSON):
    {
        "opciones": {
            "mostrarPreciosUnitarios": true,
            "mostrarPreciosTotales": true,
            "mostrarIGV": true,
            "mostrarSubtotal": true,
            "mostrarLogo": true
        },
        "logo_base64": "data:image/png;base64,..."
    }
    """
    from app.services.word_generator import word_generator
    
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        # Preparar ruta de salida
        from app.core.config import settings
        import os
        
        nombre_archivo = f"cotizacion_{cotizacion.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        logger.info(f"Generando Word para cotización {cotizacion_id} en {ruta_salida}")

        # Generar documento con opciones y logo
        ruta_archivo = word_generator.generar_cotizacion(
            datos=cotizacion.to_dict(),
            ruta_salida=ruta_salida,
            opciones=opciones,
            logo_base64=logo_base64
        )
        
        logger.info(f"Archivo Word generado en {ruta_archivo}")

        # Retornar archivo directamente
        from fastapi.responses import FileResponse
        return FileResponse(
            path=ruta_archivo,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        logger.error(f"Error al generar Word para cotización {cotizacion_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar Word: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Error al generar Word: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar Word: {str(e)}"
        )

@router.post("/{cotizacion_id}/generar-pdf")
async def generar_pdf(
    cotizacion_id: int,
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Generar documento PDF de la cotización
    
    Body (JSON):
    {
        "opciones": {
            "mostrarPreciosUnitarios": true,
            "mostrarPreciosTotales": true,
            "mostrarIGV": true,
            "mostrarSubtotal": true,
            "mostrarLogo": true
        },
        "logo_base64": "data:image/png;base64,..."
    }
    """
    from app.services.pdf_generator import pdf_generator
    
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        # Generar documento con opciones y logo
        ruta_archivo = pdf_generator.generar_cotizacion(
            cotizacion=cotizacion.to_dict(),
            opciones=opciones,
            logo_base64=logo_base64
        )
        
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

# ============================================
# ENDPOINTS ADICIONALES
# ============================================

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


# ============================================
# ENDPOINT DE DIAGNÓSTICO TEMPORAL
# ============================================
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.cotizacion import Cotizacion
from fastapi import APIRouter, Depends, HTTPException, status

# Suponiendo que tu router se llama 'router' en este archivo
# Si tiene otro nombre, ajústalo.
@router.get("/test-db/{cotizacion_id}", tags=["TEMP - Diagnóstico"])
def test_database_connection(cotizacion_id: int, db: Session = Depends(get_db)):
    """
    Endpoint de prueba para verificar únicamente la conexión a la BD
    y la lectura de una cotización.
    """
    print(f"--- INICIANDO PRUEBA DE BD PARA COTIZACIÓN ID: {cotizacion_id} ---")
    try:
        cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
        if not cotizacion:
            print("--- PRUEBA FALLIDA: No se encontró la cotización. ---")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una cotización con el ID {cotizacion_id}"
            )
        
        print("--- ¡ÉXITO! Conexión a BD y lectura correctas. ---")
        return {
            "status": "¡Conexión y lectura de BD exitosa!",
            "cotizacion_id": cotizacion.id,
            "cliente": cotizacion.cliente,
            "total": cotizacion.total
        }
    except Exception as e:
        print(f"--- PRUEBA FALLIDA: Error durante la consulta a la BD: {e} ---")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al consultar la base de datos: {str(e)}"
        )