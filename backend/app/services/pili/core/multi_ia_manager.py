"""
🌐 MULTI-IA MANAGER - Gestión de múltiples proveedores de IA
"""

import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class MultiIAManager:
    """
    Gestiona múltiples proveedores de IA con fallback automático.
    
    Proveedores soportados:
    - Gemini (Google)
    - Claude (Anthropic)
    - GPT-4 (OpenAI)
    - Groq
    - Together AI
    
    Fallback: PILIBrain (lógica propia offline)
    """
    
    def __init__(self):
        """Inicializa el manager multi-IA"""
        self.providers = {
            'gemini': {
                'enabled': bool(os.getenv('GEMINI_API_KEY')),
                'priority': 1,
                'service': None
            },
            'claude': {
                'enabled': bool(os.getenv('ANTHROPIC_API_KEY')),
                'priority': 2,
                'service': None
            },
            'gpt4': {
                'enabled': bool(os.getenv('OPENAI_API_KEY')),
                'priority': 3,
                'service': None
            }
        }
        
        self._init_providers()
        logger.info(f"🌐 MultiIAManager inicializado")
    
    def _init_providers(self):
        """Inicializa los servicios de IA disponibles"""
        # Gemini
        if self.providers['gemini']['enabled']:
            try:
                from app.services.gemini_service import GeminiService
                self.providers['gemini']['service'] = GeminiService()
                logger.info("✅ Gemini disponible")
            except Exception as e:
                logger.warning(f"⚠️ Gemini no disponible: {e}")
                self.providers['gemini']['enabled'] = False
        
        # Claude (futuro)
        # GPT-4 (futuro)
    
    def generate_response(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Genera respuesta usando el proveedor de IA disponible.
        
        Args:
            prompt: Prompt para la IA
            context: Contexto adicional
            max_tokens: Máximo de tokens
        
        Returns:
            Respuesta de la IA o None si falla
        """
        # Ordenar proveedores por prioridad
        sorted_providers = sorted(
            [(name, info) for name, info in self.providers.items() if info['enabled']],
            key=lambda x: x[1]['priority']
        )
        
        # Intentar con cada proveedor
        for provider_name, provider_info in sorted_providers:
            try:
                logger.info(f"🤖 Intentando con {provider_name}...")
                
                if provider_name == 'gemini':
                    response = self._call_gemini(prompt, context, max_tokens)
                    if response:
                        logger.info(f"✅ Respuesta de {provider_name}")
                        return response
                
                # Otros proveedores aquí...
                
            except Exception as e:
                logger.warning(f"⚠️ {provider_name} falló: {e}")
                continue
        
        logger.warning("⚠️ Ningún proveedor de IA disponible")
        return None
    
    def _call_gemini(
        self,
        prompt: str,
        context: Optional[Dict],
        max_tokens: int
    ) -> Optional[str]:
        """Llama a Gemini"""
        service = self.providers['gemini']['service']
        if not service:
            return None
        
        try:
            # Construir prompt completo
            full_prompt = prompt
            if context:
                full_prompt = f"Contexto: {context}\n\n{prompt}"
            
            # Llamar a Gemini
            response = service.generar_respuesta_simple(full_prompt)
            return response
        
        except Exception as e:
            logger.error(f"Error en Gemini: {e}")
            return None


# Instancia global
_multi_ia_manager = None

def get_multi_ia_manager() -> MultiIAManager:
    """Obtiene instancia global del multi-IA manager"""
    global _multi_ia_manager
    if _multi_ia_manager is None:
        _multi_ia_manager = MultiIAManager()
    return _multi_ia_manager
