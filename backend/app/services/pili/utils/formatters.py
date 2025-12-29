"""
📝 FORMATTERS - Formateo de datos
"""

from datetime import datetime
from typing import Any


def format_currency(amount: float) -> str:
    """
    Formatea monto como moneda peruana.
    
    Args:
        amount: Monto a formatear
    
    Returns:
        String formateado (ej: "S/ 1,500.00")
    """
    return f"S/ {amount:,.2f}"


def format_date(date: datetime = None) -> str:
    """
    Formatea fecha en formato peruano.
    
    Args:
        date: Fecha a formatear (default: hoy)
    
    Returns:
        String formateado (ej: "28/12/2024")
    """
    if date is None:
        date = datetime.now()
    
    return date.strftime("%d/%m/%Y")


def format_area(area: float) -> str:
    """
    Formatea área con unidad.
    
    Args:
        area: Área en m²
    
    Returns:
        String formateado (ej: "150.5 m²")
    """
    return f"{area:,.1f} m²"


def format_percentage(value: float) -> str:
    """
    Formatea porcentaje.
    
    Args:
        value: Valor decimal (ej: 0.18 para 18%)
    
    Returns:
        String formateado (ej: "18%")
    """
    return f"{value * 100:.0f}%"


def format_document_number(prefix: str, timestamp: datetime = None) -> str:
    """
    Genera número de documento formateado.
    
    Args:
        prefix: Prefijo (ej: "COT", "PROY", "INF")
        timestamp: Fecha/hora (default: ahora)
    
    Returns:
        Número formateado (ej: "COT-20241228-1530")
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    return f"{prefix}-{timestamp.strftime('%Y%m%d-%H%M')}"


def format_phone(phone: str) -> str:
    """
    Formatea teléfono peruano.
    
    Args:
        phone: Teléfono (9 dígitos)
    
    Returns:
        String formateado (ej: "999 888 777")
    """
    phone_clean = phone.replace(" ", "").replace("-", "")
    
    if len(phone_clean) == 9:
        return f"{phone_clean[:3]} {phone_clean[3:6]} {phone_clean[6:]}"
    
    return phone_clean
