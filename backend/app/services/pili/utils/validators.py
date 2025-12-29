"""
✅ VALIDATORS - Validaciones de datos
"""

import re
from typing import Any, Dict


def validate_area(area: Any) -> tuple[bool, str]:
    """
    Valida área en m².
    
    Args:
        area: Valor a validar
    
    Returns:
        (es_valido, mensaje_error)
    """
    try:
        area_float = float(area)
        if area_float < 10:
            return False, "El área debe ser mayor a 10 m²"
        if area_float > 10000:
            return False, "El área debe ser menor a 10,000 m²"
        return True, ""
    except (ValueError, TypeError):
        return False, "Por favor ingresa un número válido"


def validate_pisos(pisos: Any) -> tuple[bool, str]:
    """
    Valida número de pisos.
    
    Args:
        pisos: Valor a validar
    
    Returns:
        (es_valido, mensaje_error)
    """
    try:
        pisos_int = int(pisos)
        if pisos_int < 1:
            return False, "Debe tener al menos 1 piso"
        if pisos_int > 50:
            return False, "Máximo 50 pisos"
        return True, ""
    except (ValueError, TypeError):
        return False, "Por favor ingresa un número entero válido"


def validate_nombre(nombre: str) -> tuple[bool, str]:
    """
    Valida nombre de cliente.
    
    Args:
        nombre: Nombre a validar
    
    Returns:
        (es_valido, mensaje_error)
    """
    if not nombre or len(nombre.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    
    if len(nombre) > 100:
        return False, "El nombre es demasiado largo (máximo 100 caracteres)"
    
    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    """
    Valida email.
    
    Args:
        email: Email a validar
    
    Returns:
        (es_valido, mensaje_error)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Por favor ingresa un email válido"
    
    return True, ""


def validate_phone(phone: str) -> tuple[bool, str]:
    """
    Valida teléfono.
    
    Args:
        phone: Teléfono a validar
    
    Returns:
        (es_valido, mensaje_error)
    """
    # Eliminar espacios y guiones
    phone_clean = phone.replace(" ", "").replace("-", "")
    
    # Debe tener 9 dígitos (Perú)
    if not phone_clean.isdigit():
        return False, "El teléfono debe contener solo números"
    
    if len(phone_clean) != 9:
        return False, "El teléfono debe tener 9 dígitos"
    
    return True, ""
