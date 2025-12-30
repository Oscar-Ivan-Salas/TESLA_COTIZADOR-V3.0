"""
🔌 ADAPTER DE COMPATIBILIDAD LEGACY
Permite usar UniversalSpecialist con interfaz legacy
"""

from typing import Dict, Any, Optional
from ..specialist import UniversalSpecialist
import logging

logger = logging.getLogger(__name__)


class LegacySpecialistAdapter:
    """
    Adapta UniversalSpecialist a interfaz legacy.
    
    Mantiene compatibilidad con código existente mientras
    usa la nueva arquitectura modular.
    """
    
    def __init__(self, service_name: str, document_type: str = "cotizacion-simple"):
        """
        Inicializa el adapter.
        
        Args:
            service_name: Nombre del servicio (ej: 'itse', 'electricidad')
            document_type: Tipo de documento (default: 'cotizacion-simple')
        """
        self.service_name = service_name
        self.specialist = UniversalSpecialist(service_name, document_type)
        logger.info(f"✅ LegacyAdapter inicializado para {service_name}")
    
    def process_message(self, message: str, state: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Procesa mensaje con interfaz compatible con código legacy.
        
        Args:
            message: Mensaje del usuario
            state: Estado de conversación (opcional)
        
        Returns:
            Dict con formato legacy:
            {
                'texto': str,
                'botones': List[Dict],
                'stage': str,
                'conversation_state': Dict,
                'datos_generados': Dict
            }
        """
        try:
            # Procesar con UniversalSpecialist
            response = self.specialist.process_message(message, state)
            
            # Adaptar formato de respuesta a legacy
            adapted_response = {
                'texto': response.get('texto', ''),
                'botones': response.get('botones', []),
                'stage': response.get('stage', 'initial'),
                'conversation_state': response.get('state', {}),
                'datos_generados': response.get('state', {}).get('data', {}),
                'progreso': response.get('progreso', '')
            }
            
            logger.debug(f"Mensaje procesado: stage={adapted_response['stage']}")
            return adapted_response
            
        except Exception as e:
            logger.error(f"❌ Error en adapter: {e}")
            return {
                'texto': f'Error procesando mensaje: {str(e)}',
                'botones': [],
                'stage': 'error',
                'conversation_state': state or {},
                'datos_generados': {}
            }


class LocalSpecialistFactory:
    """
    Factory compatible con código legacy.
    
    Crea especialistas usando la nueva arquitectura modular
    pero con interfaz legacy.
    
    ✅ FIX: Usa patrón Singleton para reutilizar instancias
    """
    
    # Cache de instancias por servicio
    _instances = {}
    
    @staticmethod
    def create(service_name: str, document_type: str = "cotizacion-simple"):
        """
        Crea un especialista con interfaz legacy.
        ✅ FIX: Reutiliza instancia existente en lugar de crear nueva
        
        Args:
            service_name: Nombre del servicio
            document_type: Tipo de documento (opcional)
        
        Returns:
            LegacySpecialistAdapter configurado (reutilizado si existe)
        """
        # Crear clave única para cache
        cache_key = f"{service_name}_{document_type}"
        
        # Si ya existe, reutilizar
        if cache_key in LocalSpecialistFactory._instances:
            logger.info(f"♻️ Reutilizando especialista existente: {service_name}")
            return LocalSpecialistFactory._instances[cache_key]
        
        # Si no existe, crear nuevo y cachear
        logger.info(f"🏭 Factory creando NUEVO especialista: {service_name}")
        instance = LegacySpecialistAdapter(service_name, document_type)
        LocalSpecialistFactory._instances[cache_key] = instance
        return instance
    
    @staticmethod
    def clear_cache():
        """Limpia el cache de instancias"""
        LocalSpecialistFactory._instances = {}
        logger.info("🗑️ Cache de especialistas limpiado")
