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
    Calcula cotización ITSE según categoría, área y pisos.
    Usa precios reales del YAML (TUPA + Tesla).
    
    Args:
        data: Datos ITSE (categoria, tipo, area, pisos)
    
    Returns:
        Dict con cálculos ITSE reales
    """
    import yaml
    from pathlib import Path
    
    # Cargar configuración YAML
    config_path = Path(__file__).parent.parent / 'config' / 'itse.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    categoria = data.get("categoria", "SALUD")
    area = float(data.get("area", 100))
    pisos = int(data.get("pisos", 1))
    
    # Determinar nivel de riesgo según reglas
    riesgo = _calcular_riesgo_itse(categoria, area, pisos, config)
    
    # Obtener precios según nivel de riesgo
    precios_muni = config['precios_municipales'][riesgo]
    precios_tesla = config['precios_tesla'][riesgo]
    
    costo_tupa = precios_muni['precio']
    costo_tesla_min = precios_tesla['min']
    costo_tesla_max = precios_tesla['max']
    incluye_tesla = precios_tesla['incluye']
    dias = precios_muni['dias']
    
    # Calcular totales
    total_min = costo_tupa + costo_tesla_min
    total_max = costo_tupa + costo_tesla_max
    
    return {
        **data,
        "riesgo": riesgo,
        "costo_tupa": costo_tupa,
        "costo_tesla_min": costo_tesla_min,
        "costo_tesla_max": costo_tesla_max,
        "incluye_tesla": incluye_tesla,
        "total_min": total_min,
        "total_max": total_max,
        "dias": dias,
        "items": [
            {
                "descripcion": f"Derecho Municipal TUPA - Riesgo {riesgo}",
                "cantidad": 1,
                "unidad": "servicio",
                "precio_unitario": costo_tupa,
                "subtotal": costo_tupa
            },
            {
                "descripcion": f"Servicio Técnico TESLA - {incluye_tesla}",
                "cantidad": 1,
                "unidad": "servicio",
                "precio_unitario": costo_tesla_min,
                "subtotal": costo_tesla_min
            }
        ],
        "subtotal": total_min,
        "total": total_min
    }


def _calcular_riesgo_itse(categoria: str, area: float, pisos: int, config: Dict) -> str:
    """
    Calcula nivel de riesgo ITSE según categoría, área y pisos.
    
    Returns:
        Nivel de riesgo: BAJO, MEDIO, ALTO, MUY_ALTO
    """
    reglas = config.get('reglas_calculo_riesgo', {}).get(categoria, [])
    
    for regla in reglas:
        condicion = regla['condicion']
        
        # Evaluar condición (simple)
        if 'area > 1000' in condicion and area > 1000:
            return regla['resultado']
        elif 'area > 500' in condicion and area > 500:
            return regla['resultado']
        elif 'area > 300' in condicion and area > 300:
            return regla['resultado']
        elif 'pisos >= 3' in condicion and pisos >= 3:
            return regla['resultado']
        elif 'pisos >= 2' in condicion and pisos >= 2:
            return regla['resultado']
        elif 'area <= 500' in condicion and area <= 500:
            return regla['resultado']
        elif 'area <= 300' in condicion and area <= 300:
            return regla['resultado']
    
    # Default según categoría
    categoria_info = config.get('categorias', {}).get(categoria, {})
    return categoria_info.get('riesgo_default', 'MEDIO')



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
