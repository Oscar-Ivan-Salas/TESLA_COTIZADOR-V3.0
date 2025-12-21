"""
Router para generación directa de documentos
Sin necesidad de guardar en base de datos
🆕 INTEGRADO CON PARSER HTML Y PLANTILLAS PROFESIONALES
"""
from fastapi import APIRouter, HTTPException, Body, Query
from fastapi.responses import FileResponse
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Obtener directorio de almacenamiento
from app.core.config import get_generated_directory
storage_path = get_generated_directory()

@router.post("/generar-documento-directo")
async def generar_documento_directo(
    datos: Dict = Body(...),
    formato: str = Query("word", regex="^(word|pdf)$"),
    html_editado: Optional[str] = Body(None),
    tipo_plantilla: Optional[str] = Body(None)
):
    """
    🆕 MEJORADO: Genera documento Word o PDF profesional

    Puede recibir:
    1. HTML editado por usuario → parsea → genera documento profesional
    2. JSON directo → genera documento profesional

    Args:
        datos: Datos JSON de la cotización/proyecto/informe
        formato: "word" o "pdf"
        html_editado: (Opcional) HTML editado por el usuario
        tipo_plantilla: (Opcional) Tipo específico de documento:
            - "cotizacion-simple" | "cotizacion-compleja"
            - "proyecto-simple" | "proyecto-complejo"
            - "informe-tecnico" | "informe-ejecutivo"

    Returns:
        Archivo descargable Word/PDF profesional
    """
    try:
        logger.info(f"📄 Generando documento {formato.upper()} profesional")
        
        # 🔍 DEBUG: Ver datos JSON recibidos del frontend
        logger.info(f"🔍 DEBUG - Datos JSON recibidos del frontend:")
        logger.info(f"  - cliente: {datos.get('cliente')}")
        logger.info(f"  - proyecto: {datos.get('proyecto')}")
        logger.info(f"  - numero: {datos.get('numero')}")
        logger.info(f"  - items: {len(datos.get('items', []))} items")

        # ═══════════════════════════════════════════════════════════
        # PASO 1: PARSEAR HTML EDITADO SI SE RECIBIÓ
        # ═══════════════════════════════════════════════════════════
        if html_editado:
            logger.info("🔍 Parseando HTML editado por usuario...")
            from app.services.html_parser import html_parser

            # Parsear HTML → JSON
            datos_parseados = html_parser.parsear_html_editado(
                html=html_editado,
                tipo_documento=tipo_plantilla or "cotizacion"
            )
            
            logger.info(f"🔍 DEBUG - Datos parseados del HTML:")
            logger.info(f"  - cliente: {datos_parseados.get('cliente')}")
            logger.info(f"  - proyecto: {datos_parseados.get('proyecto')}")

            # ✅ CRÍTICO: Priorizar datos JSON del frontend sobre HTML parseado
            # HTML parseado primero, luego JSON lo sobrescribe
            # Esto asegura que los datos correctos del frontend NO sean reemplazados por strings vacíos del HTML
            datos = {**datos_parseados, **datos}  # JSON sobrescribe HTML ✅
            logger.info(f"✅ HTML parseado: {len(datos_parseados)} campos extraídos")
            
            logger.info(f"🔍 DEBUG - Datos FINALES después de fusión:")
            logger.info(f"  - cliente: {datos.get('cliente')}")
            logger.info(f"  - proyecto: {datos.get('proyecto')}")

        # ═══════════════════════════════════════════════════════════
        # PASO 2: DETERMINAR TIPO DE DOCUMENTO
        # ═══════════════════════════════════════════════════════════
        if not tipo_plantilla:
            # Auto-detectar tipo
            if "fases" in datos or "cronograma" in datos or "metricas_pmi" in datos:
                tipo_plantilla = "proyecto-simple"
            elif "resumen" in datos and "conclusiones" in datos:
                tipo_plantilla = "informe-tecnico"
            else:
                tipo_plantilla = "cotizacion-simple"

        logger.info(f"📋 Tipo de documento: {tipo_plantilla}")

        # ═══════════════════════════════════════════════════════════
        # PASO 3: GENERAR DOCUMENTO PROFESIONAL
        # ═══════════════════════════════════════════════════════════
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if formato == "word":
            # Importar generador HTML→Word profesional
            from app.services.html_to_word_generator import html_to_word_generator

            filename = f"{tipo_plantilla}_{timestamp}.docx"
            filepath = storage_path / filename

            # Seleccionar método de generación según tipo
            if "cotizacion-simple" in tipo_plantilla:
                ruta_generada = html_to_word_generator.generar_cotizacion_simple(
                    datos=datos,
                    ruta_salida=filepath
                )
            elif "cotizacion-compleja" in tipo_plantilla:
                ruta_generada = html_to_word_generator.generar_cotizacion_compleja(
                    datos=datos,
                    ruta_salida=filepath
                )
            elif "proyecto-simple" in tipo_plantilla:
                ruta_generada = html_to_word_generator.generar_proyecto_simple(
                    datos=datos,
                    ruta_salida=filepath
                )
            elif "proyecto-complejo" in tipo_plantilla or "pmi" in tipo_plantilla.lower():
                ruta_generada = html_to_word_generator.generar_proyecto_complejo(
                    datos=datos,
                    ruta_salida=filepath
                )
            elif "informe-tecnico" in tipo_plantilla:
                ruta_generada = html_to_word_generator.generar_informe_tecnico(
                    datos=datos,
                    ruta_salida=filepath
                )
            elif "informe-ejecutivo" in tipo_plantilla or "apa" in tipo_plantilla.lower():
                ruta_generada = html_to_word_generator.generar_informe_ejecutivo(
                    datos=datos,
                    ruta_salida=filepath
                )
            else:
                # Fallback a cotización simple
                logger.warning(f"Tipo no reconocido '{tipo_plantilla}', usando cotización simple")
                ruta_generada = html_to_word_generator.generar_cotizacion_simple(
                    datos=datos,
                    ruta_salida=filepath
                )

            archivo = str(ruta_generada)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        else:  # PDF
            # Usar generador PDF
            from app.services.pdf_generator import pdf_generator

            filename = f"{tipo_plantilla}_{timestamp}.pdf"
            filepath = storage_path / filename
            archivo = str(filepath)

            # Determinar tipo para PDF
            if "proyecto" in tipo_plantilla:
                pdf_generator.generar_informe_proyecto(datos=datos, ruta_salida=archivo)
            elif "informe" in tipo_plantilla:
                pdf_generator.generar_informe_simple(datos=datos, ruta_salida=archivo)
            else:
                pdf_generator.generar_cotizacion(datos=datos, ruta_salida=archivo)

            media_type = "application/pdf"

        logger.info(f"✅ Documento profesional generado: {filename}")

        return FileResponse(
            path=archivo,
            media_type=media_type,
            filename=filename,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )

    except Exception as e:
        logger.error(f"❌ Error generando documento: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT V2: GENERACIÓN LIMPIA SIN HTML PARSING
# ============================================================================

@router.post("/generar-documento-v2")
async def generar_documento_v2(
    datos: Dict = Body(...),
    formato: str = Query("word", regex="^(word|pdf)$"),
    guardar_bd: bool = Query(False)
):
    """
    🆕 GENERACIÓN V2: Flujo limpio JSON → Word/PDF
    
    Flujo:
    1. Recibir JSON limpio del frontend (SIN HTML)
    2. Guardar en ChromaDB para RAG de PILI
    3. Generar Word con python-docx
    4. Convertir a PDF si necesario
    5. Retornar archivo
    
    Args:
        datos: Datos JSON completos de la cotización
        formato: 'word' o 'pdf'
        guardar_bd: Si guardar en BD relacional (futuro)
    """
    try:
        logger.info(f"📄 Generación V2 - Formato: {formato}")
        logger.info(f"📦 Datos recibidos: {datos.get('numero')}")
        
        # Importar servicios V2
        from app.services.word_generator_v2 import word_generator_v2
        from app.services.pdf_generator_v2 import pdf_generator_v2
        from app.services.vector_db import get_vector_db
        
        # PASO 1: Guardar en ChromaDB para RAG de PILI
        logger.info("🔍 Guardando en ChromaDB para RAG...")
        try:
            vector_db = get_vector_db()  # Lazy initialization
            vector_db.agregar_cotizacion(
                cotizacion_id=datos.get('numero', f"COT-{datetime.now().timestamp()}"),
                datos=datos
            )
        except Exception as e:
            logger.warning(f"⚠️ Error al guardar en ChromaDB (no crítico): {e}")
        
        # PASO 2: Generar Word con python-docx
        logger.info("📝 Generando documento Word con python-docx...")
        ruta_word = word_generator_v2.generar_cotizacion(datos)
        
        # PASO 3: Generar PDF si se solicita
        if formato == 'pdf':
            logger.info("📄 Convirtiendo a PDF...")
            try:
                ruta_pdf = pdf_generator_v2.convertir_word_a_pdf(ruta_word)
                ruta_final = ruta_pdf
                media_type = "application/pdf"
            except Exception as e:
                logger.error(f"❌ Error al convertir a PDF: {e}")
                logger.info("📝 Retornando Word en su lugar")
                ruta_final = ruta_word
                media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            ruta_final = ruta_word
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        # PASO 4: Retornar archivo
        logger.info(f"✅ Documento V2 generado exitosamente: {ruta_final.name}")
        
        return FileResponse(
            path=str(ruta_final),
            media_type=media_type,
            filename=ruta_final.name,
            headers={"Content-Disposition": f'attachment; filename="{ruta_final.name}"'}
        )
        
    except Exception as e:
        logger.error(f"❌ Error en generación V2: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

