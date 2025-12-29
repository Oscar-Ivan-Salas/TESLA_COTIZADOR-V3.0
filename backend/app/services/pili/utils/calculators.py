"""
🧮 CALCULATORS - Cálculos de cotizaciones y proyectos
"""

from typing import Dict, Any, List


def calculate_simple_quote(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula cotización simple.
    
    Args:
        data: Datos del proyecto (debe incluir area_m2, servicio)
    
    Returns:
        Dict con cálculos (items, subtotal, igv, total)
    """
    area = data.get("area_m2", 100)
    servicio = data.get("servicio", "electrico-residencial")
    
    # Precios base por m² según servicio
    precios_base = {
        "electrico-residencial": 50,
        "electrico-comercial": 75,
        "electrico-industrial": 100,
        "pozo-tierra": 30,
        "contraincendios": 80,
        "domotica": 120,
        "cctv": 60,
        "redes": 40,
        "saneamiento": 55,
        "automatizacion-industrial": 150
    }
    
    precio_por_m2 = precios_base.get(servicio, 50)
    
    # Cálculo
    subtotal = area * precio_por_m2
    igv = subtotal * 0.18
    total = subtotal + igv
    
    return {
        **data,
        "items": [
            {
                "descripcion": f"Instalación {servicio}",
                "cantidad": area,
                "unidad": "m²",
                "precio_unitario": precio_por_m2,
                "subtotal": subtotal
            }
        ],
        "subtotal": subtotal,
        "igv": igv,
        "total": total
    }


def calculate_complex_quote(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula cotización compleja con múltiples items.
    
    Args:
        data: Datos del proyecto
    
    Returns:
        Dict con cálculos detallados
    """
    # Por ahora usa cálculo simple
    # En el futuro se puede agregar lógica más compleja
    result = calculate_simple_quote(data)
    
    # Agregar items adicionales para cotización compleja
    result["items"].append({
        "descripcion": "Materiales especiales",
        "cantidad": 1,
        "unidad": "global",
        "precio_unitario": 500,
        "subtotal": 500
    })
    
    # Recalcular totales
    result["subtotal"] += 500
    result["igv"] = result["subtotal"] * 0.18
    result["total"] = result["subtotal"] + result["igv"]
    
    return result


def calculate_itse_quote(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula cotización ITSE según categoría y tipo.
    
    Args:
        data: Datos ITSE (categoria, tipo, area_m2, pisos)
    
    Returns:
        Dict con cálculos ITSE
    """
    categoria = data.get("categoria", "SALUD")
    tipo = data.get("tipo", "Hospital")
    area = data.get("area_m2", 100)
    pisos = data.get("pisos", 1)
    
    # Precios base ITSE
    precios_base_itse = {
        "SALUD": {"Hospital": 800, "Clínica": 600, "Centro de Salud": 400},
        "EDUCACION": {"Universidad": 700, "Colegio": 500, "Instituto": 450},
        "COMERCIO": {"Centro Comercial": 900, "Tienda": 400, "Supermercado": 700},
        "HOSPEDAJE": {"Hotel": 750, "Hostal": 500, "Apart-hotel": 650},
        "INDUSTRIA": {"Fábrica": 1000, "Almacén": 600, "Taller": 500}
    }
    
    precio_base = precios_base_itse.get(categoria, {}).get(tipo, 500)
    
    # Factor por área
    factor_area = 1.0
    if area > 500:
        factor_area = 1.2
    elif area > 1000:
        factor_area = 1.5
    
    # Factor por pisos
    factor_pisos = 1.0 + (pisos - 1) * 0.1
    
    # Cálculo
    subtotal = precio_base * factor_area * factor_pisos
    igv = subtotal * 0.18
    total = subtotal + igv
    
    return {
        **data,
        "items": [
            {
                "descripcion": f"Certificado ITSE - {categoria} - {tipo}",
                "cantidad": 1,
                "unidad": "servicio",
                "precio_unitario": subtotal,
                "subtotal": subtotal
            }
        ],
        "subtotal": subtotal,
        "igv": igv,
        "total": total,
        "detalles": {
            "precio_base": precio_base,
            "factor_area": factor_area,
            "factor_pisos": factor_pisos
        }
    }


def calculate_project_budget(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula presupuesto de proyecto.
    
    Args:
        data: Datos del proyecto
    
    Returns:
        Dict con presupuesto calculado
    """
    # Por ahora retorna datos básicos
    # En el futuro se puede agregar lógica de WBS, etc.
    return {
        **data,
        "presupuesto_estimado": data.get("presupuesto", 10000),
        "duracion_dias": data.get("duracion", 30)
    }
