"""
Router: Chat IA
Endpoints para interacción con Gemini AI + Gestión de Plantillas
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
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
from pathlib import Path
import logging
import os
import shutil

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
async def generar_cotizacion_rapida(
    request: CotizacionRapidaRequest,
    db: Session = Depends(get_db)
):
    """
    Generar cotización rápida usando IA
    
    El usuario describe lo que necesita y la IA genera la cotización automáticamente
    """
    try:
        logger.info("Generando cotización rápida con IA")
        
        # Generar cotización con Gemini
        cotizacion_data = gemini_service.generar_cotizacion_desde_texto(
            descripcion=request.descripcion,
            contexto_adicional=request.contexto_adicional
        )
        
        # Crear cotización en BD
        numero = generar_numero_cotizacion(db)
        
        nueva_cotizacion = Cotizacion(
            numero=numero,
            cliente=cotizacion_data.get('cliente', 'Cliente No Especificado'),
            proyecto=cotizacion_data.get('proyecto', 'Proyecto Generado por IA'),
            descripcion=request.descripcion,
            observaciones=cotizacion_data.get('observaciones', ''),
            estado='borrador',
            subtotal=0,
            igv=0,
            total=0
        )
        
        db.add(nueva_cotizacion)
        db.flush()
        
        # Crear items
        items_data = cotizacion_data.get('items', [])
        subtotal = 0
        
        for item_data in items_data:
            cantidad = float(item_data.get('cantidad', 1))
            precio = float(item_data.get('precio_unitario', 0))
            
            item = Item(
                cotizacion_id=nueva_cotizacion.id,
                descripcion=item_data.get('descripcion', ''),
                cantidad=cantidad,
                unidad=item_data.get('unidad', 'und'),
                precio_unitario=precio
            )
            
            db.add(item)
            subtotal += cantidad * precio
        
        # Actualizar totales
        nueva_cotizacion.subtotal = subtotal
        nueva_cotizacion.igv = subtotal * 0.18
        nueva_cotizacion.total = subtotal * 1.18
        
        db.commit()
        db.refresh(nueva_cotizacion)
        
        logger.info(f"Cotización rápida creada: {numero}")
        
        return nueva_cotizacion
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al generar cotización rápida: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar cotización: {str(e)}"
        )

@router.post("/conversacional", response_model=ChatResponse)
async def chat_conversacional(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat conversacional para refinar cotizaciones
    
    El usuario puede iterar y mejorar una cotización mediante conversación
    """
    try:
        logger.info("Procesando mensaje de chat conversacional")
        
        # Enviar mensaje a Gemini
        respuesta = gemini_service.chat(
            mensaje=request.mensaje,
            contexto=request.contexto,
            cotizacion_id=request.cotizacion_id
        )
        
        return ChatResponse(
            respuesta=respuesta.get('mensaje', ''),
            sugerencias=respuesta.get('sugerencias', []),
            accion_recomendada=respuesta.get('accion_recomendada')
        )
        
    except Exception as e:
        logger.error(f"Error en chat conversacional: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en chat: {str(e)}"
        )

@router.post("/analizar-proyecto")
def analizar_proyecto_ia(
    descripcion: str
):
    """
    Analizar descripción de un proyecto con IA
    
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

# ════════════════════════════════════════════════════════════════
# ⭐ NUEVOS ENDPOINTS - GESTIÓN DE PLANTILLAS
# ════════════════════════════════════════════════════════════════

@router.post("/subir-plantilla")
async def subir_plantilla(
    archivo: UploadFile = File(...),
    nombre_plantilla: str = Body(...),
    descripcion: Optional[str] = Body(None)
):
    """
    Subir una plantilla Word personalizada
    
    ⭐ NUEVO - Gestión de plantillas personalizadas
    
    La plantilla puede contener marcadores como:
    - {{cliente}}
    - {{proyecto}}
    - {{fecha}}
    - {{numero}}
    - etc.
    
    Args:
        archivo: Archivo .docx de plantilla
        nombre_plantilla: Nombre descriptivo
        descripcion: Descripción de la plantilla
    
    Returns:
        Información de la plantilla subida
    """
    
    try:
        from app.core.config import settings
        
        logger.info(f"Subiendo plantilla: {nombre_plantilla}")
        
        # Validar que sea archivo Word
        if not archivo.filename.endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se permiten archivos .docx"
            )
        
        # Crear directorio de plantillas si no existe
        templates_dir = Path(settings.TEMPLATES_DIR)
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre único para el archivo
        nombre_archivo = f"{nombre_plantilla.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_plantilla = templates_dir / nombre_archivo
        
        # Guardar archivo
        with open(ruta_plantilla, "wb") as buffer:
            contenido = await archivo.read()
            buffer.write(contenido)
        
        # Extraer marcadores de la plantilla
        from app.services.template_processor import template_processor
        
        marcadores = template_processor.extraer_marcadores(str(ruta_plantilla))
        
        logger.info(f"✅ Plantilla subida: {nombre_archivo}")
        logger.info(f"Marcadores encontrados: {len(marcadores)}")
        
        return {
            "success": True,
            "nombre_plantilla": nombre_plantilla,
            "archivo": nombre_archivo,
            "ruta": str(ruta_plantilla),
            "descripcion": descripcion,
            "marcadores_encontrados": marcadores,
            "total_marcadores": len(marcadores),
            "mensaje": f"Plantilla '{nombre_plantilla}' subida exitosamente. Se encontraron {len(marcadores)} marcadores."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al subir plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir plantilla: {str(e)}"
        )

@router.get("/listar-plantillas")
async def listar_plantillas():
    """
    Listar todas las plantillas disponibles
    
    ⭐ NUEVO - Ver plantillas disponibles
    
    Returns:
        Lista de plantillas con información
    """
    
    try:
        from app.core.config import settings
        
        templates_dir = Path(settings.TEMPLATES_DIR)
        
        if not templates_dir.exists():
            return {
                "total": 0,
                "plantillas": []
            }
        
        plantillas = []
        
        for archivo in templates_dir.glob("*.docx"):
            try:
                from app.services.template_processor import template_processor
                
                # Extraer marcadores
                marcadores = template_processor.extraer_marcadores(str(archivo))
                
                plantillas.append({
                    "nombre": archivo.stem,
                    "archivo": archivo.name,
                    "ruta": str(archivo),
                    "tamano_kb": round(archivo.stat().st_size / 1024, 2),
                    "fecha_creacion": datetime.fromtimestamp(archivo.stat().st_ctime).strftime("%d/%m/%Y %H:%M"),
                    "total_marcadores": len(marcadores),
                    "marcadores": marcadores
                })
                
            except Exception as e:
                logger.warning(f"Error al procesar plantilla {archivo.name}: {str(e)}")
                continue
        
        return {
            "total": len(plantillas),
            "plantillas": plantillas
        }
        
    except Exception as e:
        logger.error(f"Error al listar plantillas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar plantillas: {str(e)}"
        )

@router.get("/plantilla/{nombre_archivo}/marcadores")
async def obtener_marcadores_plantilla(
    nombre_archivo: str
):
    """
    Obtener marcadores de una plantilla específica
    
    ⭐ NUEVO - Ver qué marcadores tiene una plantilla
    
    Args:
        nombre_archivo: Nombre del archivo de plantilla
    
    Returns:
        Lista de marcadores encontrados
    """
    
    try:
        from app.core.config import settings
        from app.services.template_processor import template_processor
        
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_archivo
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_archivo}' no encontrada"
            )
        
        marcadores = template_processor.extraer_marcadores(str(ruta_plantilla))
        
        return {
            "plantilla": nombre_archivo,
            "total_marcadores": len(marcadores),
            "marcadores": marcadores,
            "marcadores_comunes": [
                "{{cliente}}", "{{proyecto}}", "{{fecha}}", "{{numero}}",
                "{{descripcion}}", "{{subtotal}}", "{{igv}}", "{{total}}"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener marcadores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/usar-plantilla/{cotizacion_id}")
async def generar_cotizacion_con_plantilla(
    cotizacion_id: int,
    nombre_plantilla: str = Body(...),
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Generar cotización usando una plantilla personalizada
    
    ⭐ NUEVO - Usar plantilla del usuario
    
    El chat puede decir: "usa mi plantilla de informe"
    Y este endpoint procesa esa solicitud
    
    Args:
        cotizacion_id: ID de la cotización
        nombre_plantilla: Nombre del archivo de plantilla
        opciones: Opciones adicionales
        logo_base64: Logo en base64
    
    Returns:
        Archivo Word generado desde plantilla
    """
    
    try:
        # Obtener cotización
        cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
        
        if not cotizacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cotización no encontrada"
            )
        
        logger.info(f"Generando cotización {cotizacion.numero} con plantilla: {nombre_plantilla}")
        
        from app.core.config import settings
        from app.services.template_processor import template_processor
        
        # Ruta de la plantilla
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_plantilla
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_plantilla}' no encontrada"
            )
        
        # Obtener items de la cotización
        items_db = db.query(Item).filter(Item.cotizacion_id == cotizacion_id).all()
        
        items = []
        for item in items_db:
            items.append({
                "descripcion": item.descripcion,
                "cantidad": float(item.cantidad),
                "unidad": item.unidad,
                "precio_unitario": float(item.precio_unitario)
            })
        
        # Preparar datos
        datos_cotizacion = {
            "numero": cotizacion.numero,
            "cliente": cotizacion.cliente,
            "proyecto": cotizacion.proyecto,
            "descripcion": cotizacion.descripcion or "",
            "observaciones": cotizacion.observaciones or "",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "subtotal": float(cotizacion.subtotal) if cotizacion.subtotal else 0,
            "igv": float(cotizacion.igv) if cotizacion.igv else 0,
            "total": float(cotizacion.total) if cotizacion.total else 0,
            "items": items
        }
        
        # Generar documento con plantilla
        nombre_salida = f"cotizacion_{cotizacion.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_salida)
        
        ruta_generada = template_processor.procesar_plantilla(
            ruta_plantilla=str(ruta_plantilla),
            datos_cotizacion=datos_cotizacion,
            ruta_salida=ruta_salida,
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_generada):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el documento"
            )
        
        logger.info(f"✅ Cotización generada con plantilla: {nombre_salida}")
        
        return FileResponse(
            path=ruta_generada,
            filename=nombre_salida,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al usar plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.delete("/eliminar-plantilla/{nombre_archivo}")
async def eliminar_plantilla(
    nombre_archivo: str
):
    """
    Eliminar una plantilla
    
    ⭐ NUEVO - Gestión de plantillas
    
    Args:
        nombre_archivo: Nombre del archivo a eliminar
    
    Returns:
        Confirmación de eliminación
    """
    
    try:
        from app.core.config import settings
        
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_archivo
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_archivo}' no encontrada"
            )
        
        # Eliminar archivo
        ruta_plantilla.unlink()
        
        logger.info(f"✅ Plantilla eliminada: {nombre_archivo}")
        
        return {
            "success": True,
            "mensaje": f"Plantilla '{nombre_archivo}' eliminada exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/validar-plantilla")
async def validar_plantilla(
    archivo: UploadFile = File(...)
):
    """
    Validar una plantilla antes de subirla
    
    ⭐ NUEVO - Verificar que la plantilla es válida
    
    Verifica:
    - Que sea un archivo .docx válido
    - Extrae y muestra los marcadores
    - Valida la estructura
    
    Returns:
        Reporte de validación
    """
    
    try:
        import tempfile
        from app.services.template_processor import template_processor
        
        # Validar extensión
        if not archivo.filename.endswith('.docx'):
            return {
                "valida": False,
                "error": "El archivo debe ser .docx",
                "recomendacion": "Usa Microsoft Word para crear la plantilla"
            }
        
        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            contenido = await archivo.read()
            tmp.write(contenido)
            tmp_path = tmp.name
        
        try:
            # Validar plantilla
            es_valida, mensaje = template_processor.validar_plantilla(tmp_path)
            
            if es_valida:
                # Extraer marcadores
                marcadores = template_processor.extraer_marcadores(tmp_path)
                
                return {
                    "valida": True,
                    "mensaje": "Plantilla válida",
                    "total_marcadores": len(marcadores),
                    "marcadores_encontrados": marcadores,
                    "marcadores_sugeridos": [
                        "{{cliente}}", "{{proyecto}}", "{{fecha}}", "{{numero}}",
                        "{{descripcion}}", "{{subtotal}}", "{{igv}}", "{{total}}"
                    ],
                    "recomendacion": "Puedes subir esta plantilla para usarla en cotizaciones"
                }
            else:
                return {
                    "valida": False,
                    "error": mensaje,
                    "recomendacion": "Revisa la plantilla y vuelve a intentar"
                }
                
        finally:
            # Eliminar archivo temporal
            Path(tmp_path).unlink(missing_ok=True)
        
    except Exception as e:
        logger.error(f"Error al validar plantilla: {str(e)}")
        return {
            "valida": False,
            "error": str(e),
            "recomendacion": "Verifica que el archivo no esté corrupto"
        }