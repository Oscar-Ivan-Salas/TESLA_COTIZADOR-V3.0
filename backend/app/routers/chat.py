"""
Router: Chat IA
Endpoints para interacción con Gemini AI
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.cotizacion import (
    CotizacionRapidaRequest,
    ChatRequest,
    ChatResponse,
    CotizacionResponse
)
from app.services.gemini_service import gemini_service
from app.models.cotizacion import Cotizacion
from app.models.item import Item
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def generar_numero_cotizacion(db: Session) -> str:
    """Generar número único de cotización"""
    fecha = datetime.now()
    prefijo = f"COT-{fecha.strftime('%Y%m')}"
    
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
# ENDPOINTS DE CHAT IA
# ============================================

@router.post("/generar-rapida", response_model=CotizacionResponse)
def generar_cotizacion_rapida(
    request: CotizacionRapidaRequest,
    db: Session = Depends(get_db)
):
    """
    Generar cotización rápida usando IA a partir de una descripción
    
    El usuario solo proporciona:
    - Descripción del proyecto
    - Nombre del cliente
    - Nombre del proyecto (opcional)
    
    La IA genera automáticamente todos los items con precios
    """
    try:
        logger.info(f"Generando cotización rápida para cliente: {request.cliente}")
        
        # Llamar a Gemini para generar cotización
        cotizacion_data = gemini_service.generar_cotizacion_rapida(
            descripcion_proyecto=request.descripcion_proyecto,
            cliente=request.cliente,
            proyecto=request.proyecto
        )
        
        # Generar número de cotización
        numero = generar_numero_cotizacion(db)
        
        # Crear cotización en la base de datos
        nueva_cotizacion = Cotizacion(
            numero=numero,
            cliente=cotizacion_data.get('cliente', request.cliente),
            proyecto=cotizacion_data.get('proyecto', request.proyecto or f"Proyecto {request.cliente}"),
            descripcion=cotizacion_data.get('descripcion', request.descripcion_proyecto),
            estado="borrador",
            items=cotizacion_data.get('items', [])
        )
        
        # Crear items
        if cotizacion_data.get('items'):
            for item_data in cotizacion_data['items']:
                item = Item(
                    descripcion=item_data.get('descripcion', ''),
                    cantidad=float(item_data.get('cantidad', 1.0)),
                    precio_unitario=float(item_data.get('precio_unitario', 0.0)),
                    total=float(item_data.get('cantidad', 1.0)) * float(item_data.get('precio_unitario', 0.0))
                )
                nueva_cotizacion.items_rel.append(item)
        
        # Calcular totales
        nueva_cotizacion.calcular_totales()
        
        # Guardar en base de datos
        db.add(nueva_cotizacion)
        db.commit()
        db.refresh(nueva_cotizacion)
        
        logger.info(f"Cotización generada: {numero} con {len(nueva_cotizacion.items_rel)} items")
        
        return nueva_cotizacion
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al generar cotización rápida: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar cotización: {str(e)}"
        )

@router.post("/conversacional", response_model=ChatResponse)
def chat_conversacional(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat conversacional con IA para refinar cotizaciones
    
    Permite al usuario conversar con la IA para:
    - Modificar items existentes
    - Agregar nuevos items
    - Eliminar items
    - Ajustar precios
    - Cambiar descripciones
    """
    try:
        logger.info(f"Chat conversacional: {request.mensaje[:50]}...")
        
        # Obtener cotización actual si existe
        cotizacion_actual = None
        if request.cotizacion_id:
            cotizacion = db.query(Cotizacion).filter(
                Cotizacion.id == request.cotizacion_id
            ).first()
            
            if cotizacion:
                cotizacion_actual = cotizacion.to_dict()
        
        # Preparar contexto
        contexto = []
        if request.contexto:
            contexto = [
                {"role": msg.role, "content": msg.content}
                for msg in request.contexto
            ]
        
        # Llamar a Gemini
        respuesta_ia = gemini_service.chat_conversacional(
            mensaje=request.mensaje,
            contexto=contexto,
            cotizacion_actual=cotizacion_actual
        )
        
        # Procesar respuesta
        respuesta_texto = respuesta_ia.get('respuesta', 'Lo siento, no pude procesar tu mensaje.')
        accion = respuesta_ia.get('accion', 'ninguna')
        cambios = respuesta_ia.get('cambios', {})
        sugerencias = respuesta_ia.get('sugerencias', [])
        
        # Si hay cambios y existe una cotización
        cotizacion_actualizada = None
        
        if accion != 'ninguna' and request.cotizacion_id:
            cotizacion = db.query(Cotizacion).filter(
                Cotizacion.id == request.cotizacion_id
            ).first()
            
            if cotizacion:
                # Aplicar cambios según acción
                if accion == 'modificar_cotizacion' and cambios:
                    if 'items' in cambios:
                        # Eliminar items anteriores
                        db.query(Item).filter(Item.cotizacion_id == cotizacion.id).delete()
                        
                        # Crear nuevos items
                        for item_data in cambios['items']:
                            item = Item(
                                descripcion=item_data.get('descripcion', ''),
                                cantidad=float(item_data.get('cantidad', 1.0)),
                                precio_unitario=float(item_data.get('precio_unitario', 0.0)),
                                total=float(item_data.get('cantidad', 1.0)) * float(item_data.get('precio_unitario', 0.0)),
                                cotizacion_id=cotizacion.id
                            )
                            db.add(item)
                    
                    if 'descripcion' in cambios:
                        cotizacion.descripcion = cambios['descripcion']
                    
                    # Recalcular totales
                    cotizacion.calcular_totales()
                    
                    db.commit()
                    db.refresh(cotizacion)
                    
                    cotizacion_actualizada = cotizacion
                
                elif accion == 'agregar_item' and cambios.get('items'):
                    # Agregar nuevos items
                    for item_data in cambios['items']:
                        item = Item(
                            descripcion=item_data.get('descripcion', ''),
                            cantidad=float(item_data.get('cantidad', 1.0)),
                            precio_unitario=float(item_data.get('precio_unitario', 0.0)),
                            total=float(item_data.get('cantidad', 1.0)) * float(item_data.get('precio_unitario', 0.0)),
                            cotizacion_id=cotizacion.id
                        )
                        db.add(item)
                    
                    cotizacion.calcular_totales()
                    db.commit()
                    db.refresh(cotizacion)
                    
                    cotizacion_actualizada = cotizacion
        
        # Construir respuesta
        response = ChatResponse(
            respuesta=respuesta_texto,
            cotizacion=cotizacion_actualizada,
            sugerencias=sugerencias if sugerencias else None
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error en chat conversacional: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en chat: {str(e)}"
        )

@router.post("/analizar-proyecto")
def analizar_proyecto_texto(
    descripcion: str,
    db: Session = Depends(get_db)
):
    """
    Analizar descripción de proyecto y sugerir estructura de cotización
    
    NO crea la cotización, solo analiza y sugiere
    """
    try:
        logger.info("Analizando descripción de proyecto")
        
        # Analizar con Gemini
        analisis = gemini_service.analizar_documento(
            texto_documento=descripcion,
            tipo_analisis="proyecto"
        )
        
        return {
            "success": True,
            "analisis": analisis,
            "mensaje": "Análisis completado. Puedes usar esta información para crear una cotización."
        }
        
    except Exception as e:
        logger.error(f"Error al analizar proyecto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al analizar: {str(e)}"
        )

@router.post("/sugerir-mejoras/{cotizacion_id}")
def sugerir_mejoras_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener sugerencias de mejora para una cotización existente
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        logger.info(f"Generando sugerencias para cotización {cotizacion.numero}")
        
        # Obtener sugerencias de Gemini
        sugerencias = gemini_service.sugerir_mejoras(cotizacion.to_dict())
        
        return {
            "success": True,
            "cotizacion_numero": cotizacion.numero,
            "sugerencias": sugerencias
        }
        
    except Exception as e:
        logger.error(f"Error al sugerir mejoras: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar sugerencias: {str(e)}"
        )

@router.get("/health")
def health_check_ia():
    """
    Verificar estado del servicio de IA
    """
    from app.core.config import settings
    
    return {
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "model": settings.GEMINI_MODEL,
        "status": "ready" if gemini_service.model else "not_configured"
    }