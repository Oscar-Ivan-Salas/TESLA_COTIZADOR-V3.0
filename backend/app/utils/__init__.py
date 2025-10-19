"""
Utilidades del sistema
"""
from app.utils.ocr import ocr_processor, OCRProcessor
from app.utils.helpers import (
    generar_slug,
    limpiar_texto,
    extraer_numeros,
    formatear_moneda,
    calcular_igv,
    validar_ruc,
    validar_email,
    validar_telefono_peru,
    fecha_actual,
    fecha_formato_largo,
    parsear_fecha,
    obtener_extension,
    formatear_tamano_archivo,
    numero_a_texto,
    redondear_decimal
)

__all__ = [
    "ocr_processor",
    "OCRProcessor",
    "generar_slug",
    "limpiar_texto",
    "extraer_numeros",
    "formatear_moneda",
    "calcular_igv",
    "validar_ruc",
    "validar_email",
    "validar_telefono_peru",
    "fecha_actual",
    "fecha_formato_largo",
    "parsear_fecha",
    "obtener_extension",
    "formatear_tamano_archivo",
    "numero_a_texto",
    "redondear_decimal"
]