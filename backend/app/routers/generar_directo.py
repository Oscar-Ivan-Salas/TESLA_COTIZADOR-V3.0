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

            # Mezclar con datos originales (prioridad a datos parseados)
            datos = {**datos, **datos_parseados}
            logger.info(f"✅ HTML parseado: {len(datos_parseados)} campos extraídos")

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
            # ✅ USAR GENERADOR PROFESIONAL CON BD DE CLIENTES
            from app.services.word_generator import WordGenerator

            word_gen = WordGenerator()

            # Determinar nombre del cliente para el archivo
            cliente_nombre = "Cliente"
            if isinstance(datos.get("cliente"), dict):
                cliente_nombre = datos["cliente"].get("nombre", "Cliente")
            elif isinstance(datos.get("cliente"), str):
                cliente_nombre = datos["cliente"]

            # Sanitizar nombre para archivo
            cliente_nombre_limpio = cliente_nombre.replace(" ", "_").replace("/", "_")[:30]

            filename = f"{tipo_plantilla}_{cliente_nombre_limpio}_{timestamp}.docx"
            filepath = storage_path / filename

            # ✅ GENERAR CON WORD_GENERATOR PROFESIONAL
            logger.info(f"📄 Generando documento Word profesional con datos: {datos.get('numero', 'N/A')}")
            logger.info(f"👤 Cliente: {cliente_nombre}")

            # Preparar datos en formato JSON esperado por word_generator
            datos_json = {
                "tipo_documento": datos.get("tipo_documento", "cotizacion"),
                "puede_generar": True,
                "datos_extraidos": {
                    "numero": datos.get("numero", f"DOC-{timestamp}"),
                    "fecha": datos.get("fecha", datetime.now().strftime("%d/%m/%Y")),
                    "cliente": datos.get("cliente", {}),
                    "proyecto": datos.get("proyecto", ""),
                    "descripcion": datos.get("descripcion", ""),
                    "items": datos.get("items", []),
                    "subtotal": float(datos.get("subtotal", 0)),
                    "igv": float(datos.get("igv", 0)),
                    "total": float(datos.get("total", 0)),
                    "observaciones": datos.get("observaciones", "Precios incluyen IGV. Válido por 30 días."),
                    "vigencia": datos.get("vigencia", "30 días")
                }
            }

            # Generar documento profesional
            resultado = word_gen.generar_desde_json_pili(
                datos_json=datos_json,
                tipo_documento=datos.get("tipo_documento", "cotizacion"),
                opciones=datos.get("opciones_personalizacion"),
                logo_base64=datos.get("logo_base64"),
                ruta_salida=str(filepath),
                db=None  # Por ahora sin BD, generación directa
            )

            archivo = str(filepath)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        else:  # PDF
            # ✅ USAR GENERADOR PDF PROFESIONAL
            from app.services.pdf_generator import PDFGenerator

            pdf_gen = PDFGenerator()

            # Determinar nombre del cliente para el archivo
            cliente_nombre = "Cliente"
            if isinstance(datos.get("cliente"), dict):
                cliente_nombre = datos["cliente"].get("nombre", "Cliente")
            elif isinstance(datos.get("cliente"), str):
                cliente_nombre = datos["cliente"]

            # Sanitizar nombre para archivo
            cliente_nombre_limpio = cliente_nombre.replace(" ", "_").replace("/", "_")[:30]

            filename = f"{tipo_plantilla}_{cliente_nombre_limpio}_{timestamp}.pdf"
            filepath = storage_path / filename
            archivo = str(filepath)

            logger.info(f"📄 Generando PDF profesional")
            logger.info(f"👤 Cliente: {cliente_nombre}")

            # Generar PDF profesional
            pdf_gen.generar_cotizacion(
                datos=datos,
                ruta_salida=archivo
            )

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
