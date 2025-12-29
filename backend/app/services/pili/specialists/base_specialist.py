"""
🎯 BASE SPECIALIST - Clase base para specialists
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseSpecialist(ABC):
    """
    Clase base abstracta para todos los specialists.
    
    Define la interfaz común que todos los specialists deben implementar.
    """
    
    def __init__(self, service_name: str, document_type: str):
        """
        Inicializa el specialist.
        
        Args:
            service_name: Nombre del servicio (ej: 'itse', 'electricidad')
            document_type: Tipo de documento (ej: 'cotizacion-simple')
        """
        self.service_name = service_name
        self.document_type = document_type
        logger.info(f"🎯 {self.__class__.__name__} inicializado: {service_name}/{document_type}")
    
    @abstractmethod
    def process_message(self, message: str, state: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario.
        
        Args:
            message: Mensaje del usuario
            state: Estado de conversación (opcional)
        
        Returns:
            Dict con respuesta y estado actualizado
        """
        pass
    
    @abstractmethod
    def get_initial_message(self) -> Dict[str, Any]:
        """
        Obtiene el mensaje inicial para comenzar conversación.
        
        Returns:
            Dict con mensaje inicial y botones
        """
        pass
    
    def _create_response(
        self,
        texto: str,
        botones: list = None,
        stage: str = None,
        state: Dict = None,
        progreso: str = None
    ) -> Dict[str, Any]:
        """
        Crea una respuesta estandarizada.
        
        Args:
            texto: Texto de respuesta
            botones: Lista de botones (opcional)
            stage: Etapa actual (opcional)
            state: Estado actualizado (opcional)
            progreso: Indicador de progreso (opcional)
        
        Returns:
            Dict con respuesta estandarizada
        """
        response = {
            "texto": texto,
            "botones": botones or [],
            "stage": stage or "initial",
            "state": state or {},
        }
        
        if progreso:
            response["progreso"] = progreso
        
        return response
