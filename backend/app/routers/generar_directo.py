"""
Router para generación directa de documentos
Sin necesidad de guardar en base de datos
"""
from fastapi import APIRouter, HTTPException, Body, Query
from fastapi.responses import FileResponse
from typing import Dict
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
    formato: str = Query("word", regex="^(word|pdf)$")
):
    """
    Genera documento Word o PDF directamente desde datos JSON
    
    Args:
        datos: Datos de la cotización/proyecto/informe
        formato: "word" o "pdf"
    
    Returns:
        Archivo descargable
    """
    try:
        logger.info(f"📄 Generando documento {formato.upper()} directo")
        
        # Importar generadores
        from app.services.word_generator import word_generator
        from app.services.pdf_generator import pdf_generator
        
        # Determinar tipo
        tipo_documento = "cotizacion"
        if "fases" in datos or "cronograma" in datos:
            tipo_documento = "proyecto"
        elif "secciones" in datos:
            tipo_documento = "informe"
        
        # Generar archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato == "word":
            filename = f"{tipo_documento}_{timestamp}.docx"
            filepath = storage_path / filename
            
            if hasattr(word_generator, 'generar_desde_json_pili'):
                # 🛠️ FIX: Empaquetar datos para estructura PILI
                datos_pili = {
                    "datos_extraidos": datos,
                    "agente_responsable": "PILI (Generación Directa)",
                    "tipo_servicio": "cotizacion-simple",
                    "timestamp": datetime.now().isoformat()
                }
                
                resultado = word_generator.generar_desde_json_pili(
                    datos_json=datos_pili,
                    tipo_documento=tipo_documento,
                    ruta_salida=str(filepath)
                )
                # Extraer ruta del resultado
                archivo = resultado.get("ruta_archivo", str(filepath)) if isinstance(resultado, dict) else str(filepath)
            else:
                archivo = str(filepath)
                word_generator.generar_cotizacion(datos=datos, ruta_salida=archivo)
            
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            filename = f"{tipo_documento}_{timestamp}.pdf"
            filepath = storage_path / filename
            archivo = str(filepath)
            pdf_generator.generar_cotizacion(datos=datos, ruta_salida=archivo)
            media_type = "application/pdf"
        
        logger.info(f"✅ Documento generado: {filename}")
        
        return FileResponse(
            path=archivo,
            media_type=media_type,
            filename=filename,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
