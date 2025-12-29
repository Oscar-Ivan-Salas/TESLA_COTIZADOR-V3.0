"""
🔄 FALLBACK MANAGER - Gestión de fallbacks offline
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class FallbackManager:
    """
    Gestiona fallbacks cuando no hay conexión a IA.
    
    Proporciona:
    - Cálculos básicos
    - Generación de estructura
    - Datos demo
    """
    
    def __init__(self):
        """Inicializa el fallback manager"""
        logger.info("🔄 FallbackManager inicializado")
    
    def extract_data(self, message: str, document_type: str) -> Dict[str, Any]:
        """
        Extrae datos del mensaje sin IA (fallback).
        
        Args:
            message: Mensaje del usuario
            document_type: Tipo de documento
        
        Returns:
            Dict con datos extraídos (básicos)
        """
        logger.info(f"🔄 Fallback: Extrayendo datos sin IA")
        
        # Datos básicos por defecto
        data = {
            "numero": self._generate_document_number(document_type),
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "mensaje_original": message
        }
        
        # Intentar extraer área si está en el mensaje
        area = self._extract_area(message)
        if area:
            data["area_m2"] = area
        
        # Intentar extraer nombre si está en el mensaje
        nombre = self._extract_name(message)
        if nombre:
            data["cliente"] = nombre
        
        logger.info(f"✅ Datos extraídos (fallback): {list(data.keys())}")
        return data
    
    def _generate_document_number(self, document_type: str) -> str:
        """Genera número de documento"""
        prefix = {
            "cotizacion-simple": "COT",
            "cotizacion-compleja": "COT",
            "proyecto-simple": "PROY",
            "proyecto-complejo-pmi": "PROY",
            "informe-tecnico": "INF",
            "informe-ejecutivo-apa": "INF"
        }.get(document_type, "DOC")
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"{prefix}-{timestamp}"
    
    def _extract_area(self, message: str) -> float:
        """Intenta extraer área del mensaje"""
        import re
        
        # Buscar patrones como "150m2", "150 m2", "150 metros"
        patterns = [
            r'(\d+\.?\d*)\s*m2',
            r'(\d+\.?\d*)\s*m²',
            r'(\d+\.?\d*)\s*metros',
            r'(\d+\.?\d*)\s*metro'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    def _extract_name(self, message: str) -> str:
        """Intenta extraer nombre del mensaje"""
        # Buscar palabras capitalizadas (posibles nombres)
        import re
        
        # Buscar después de palabras clave
        keywords = ['cliente', 'nombre', 'para', 'sr', 'sra', 'señor', 'señora']
        
        for keyword in keywords:
            pattern = f'{keyword}\\s+([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*)'
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def calculate_simple_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula cotización simple (fallback).
        
        Args:
            data: Datos del proyecto
        
        Returns:
            Dict con cálculos básicos
        """
        area = data.get("area_m2", 100)
        
        # Cálculo básico por m²
        precio_por_m2 = 50  # Precio base
        
        subtotal = area * precio_por_m2
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return {
            **data,
            "items": [
                {
                    "descripcion": "Instalación eléctrica básica",
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


# Instancia global
_fallback_manager = None

def get_fallback_manager() -> FallbackManager:
    """Obtiene instancia global del fallback manager"""
    global _fallback_manager
    if _fallback_manager is None:
        _fallback_manager = FallbackManager()
    return _fallback_manager
