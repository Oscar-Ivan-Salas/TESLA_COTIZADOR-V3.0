"""
🏭 SPECIALIST FACTORY - Crea specialists según servicio
"""

import logging
from typing import Dict, Any
from .universal_specialist import UniversalSpecialist

logger = logging.getLogger(__name__)


class SpecialistFactory:
    """
    Factory para crear specialists.
    
    Crea el specialist apropiado según el servicio y tipo de documento.
    """
    
    # Mapeo de servicios disponibles
    AVAILABLE_SERVICES = [
        'itse',
        'electricidad',
        'pozo-tierra',
        'contraincendios',
        'domotica',
        'cctv',
        'redes',
        'saneamiento',
        'automatizacion-industrial',
        'expedientes'
    ]
    
    @staticmethod
    def create(service_name: str, document_type: str = "cotizacion-simple"):
        """
        Crea un specialist.
        
        Args:
            service_name: Nombre del servicio
            document_type: Tipo de documento (default: cotizacion-simple)
        
        Returns:
            Specialist configurado
        
        Raises:
            ValueError: Si el servicio no existe
        """
        if service_name not in SpecialistFactory.AVAILABLE_SERVICES:
            logger.error(f"❌ Servicio no disponible: {service_name}")
            raise ValueError(f"Servicio '{service_name}' no disponible")
        
        logger.info(f"🏭 Creando specialist: {service_name}/{document_type}")
        
        # Por ahora todos usan UniversalSpecialist
        # En el futuro se pueden crear specialists especializados
        return UniversalSpecialist(service_name, document_type)
    
    @staticmethod
    def list_services() -> list:
        """
        Lista todos los servicios disponibles.
        
        Returns:
            Lista de nombres de servicios
        """
        return SpecialistFactory.AVAILABLE_SERVICES.copy()


# Instancia global
_factory = SpecialistFactory()

def get_specialist_factory() -> SpecialistFactory:
    """Obtiene instancia global del factory"""
    return _factory
