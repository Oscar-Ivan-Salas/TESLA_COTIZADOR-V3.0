"""
🤖 PILI MULTI-IA
Sistema de múltiples IAs con fallback automático

Soporta:
- Gemini (Google) - GRATIS 60 req/min
- Groq (Llama 3.1) - GRATIS 30 req/min
- Together AI - GRATIS 60 req/min
- OpenAI GPT-4 - PAGO (producción)
- Claude - PAGO (producción)

Fallback automático si una IA falla o está lenta.
"""

from litellm import completion, acompletion
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class PILIMultiIA:
    """
    Sistema Multi-IA con fallback automático

    DESARROLLO: Usa IAs gratuitas (Gemini, Groq, Together)
    PRODUCCIÓN: Usa IAs de pago con fallback a gratuitas
    """

    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.primary_model = os.getenv("PRIMARY_MODEL", "gemini/gemini-1.5-pro")

        # Modelos de fallback
        fallback_str = os.getenv("FALLBACK_MODELS", "")
        self.fallback_models = [m.strip() for m in fallback_str.split(",") if m.strip()]

        # Configurar API keys
        self._setup_api_keys()

        logger.info(f"🤖 PILI Multi-IA inicializada")
        logger.info(f"📊 Ambiente: {self.environment}")
        logger.info(f"🎯 Modelo primario: {self.primary_model}")
        logger.info(f"🔄 Fallbacks: {len(self.fallback_models)} modelos")

    def _setup_api_keys(self):
        """Configura API keys desde .env"""

        # Gemini (ya configurado)
        if os.getenv("GEMINI_API_KEY"):
            os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
            logger.info("✅ Gemini API configurada")

        # Groq (opcional - gratis)
        if os.getenv("GROQ_API_KEY"):
            os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
            logger.info("✅ Groq API configurada")

        # Together AI (opcional - gratis)
        if os.getenv("TOGETHER_API_KEY"):
            os.environ["TOGETHERAI_API_KEY"] = os.getenv("TOGETHER_API_KEY")
            logger.info("✅ Together AI configurada")

        # OpenAI (opcional - pago)
        if os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            logger.info("✅ OpenAI API configurada")

        # Anthropic Claude (opcional - pago)
        if os.getenv("ANTHROPIC_API_KEY"):
            os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
            logger.info("✅ Anthropic API configurada")

    def chat(
        self,
        mensaje: str,
        historial: List[Dict[str, str]] = None,
        system_prompt: str = None,
        temperature: float = 0.3,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Chat con fallback automático entre múltiples IAs

        Args:
            mensaje: Mensaje del usuario
            historial: Conversación previa [{"role": "user/assistant", "content": "..."}]
            system_prompt: Instrucciones del sistema
            temperature: Creatividad (0.0 = determinístico, 1.0 = creativo)
            max_tokens: Máximo de tokens en respuesta

        Returns:
            {
                "respuesta": str,
                "modelo_usado": str,
                "intento": int,
                "exito": bool,
                "tokens_usados": int
            }
        """

        # Preparar mensajes
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if historial:
            messages.extend(historial)

        messages.append({"role": "user", "content": mensaje})

        # Intentar con modelo primario + fallbacks
        all_models = [self.primary_model] + self.fallback_models

        for idx, model in enumerate(all_models):
            try:
                logger.info(f"🔄 Intento {idx + 1}/{len(all_models)}: {model}")

                response = completion(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=15  # 15 segundos máximo
                )

                logger.info(f"✅ Respuesta exitosa de: {model}")

                return {
                    "respuesta": response.choices[0].message.content,
                    "modelo_usado": model,
                    "intento": idx + 1,
                    "exito": True,
                    "tokens_usados": response.usage.total_tokens if hasattr(response, 'usage') else 0
                }

            except Exception as e:
                logger.warning(f"⚠️ Falló {model}: {str(e)[:100]}")

                # Si es el último modelo, retornar error
                if idx == len(all_models) - 1:
                    logger.error("❌ Todos los modelos fallaron")
                    return {
                        "respuesta": "Lo siento, el servicio está temporalmente no disponible. Intenta en unos momentos.",
                        "modelo_usado": None,
                        "intento": idx + 1,
                        "exito": False,
                        "error": str(e)
                    }

                # Continuar con siguiente modelo
                continue

    async def chat_async(
        self,
        mensaje: str,
        historial: List[Dict[str, str]] = None,
        system_prompt: str = None,
        temperature: float = 0.3,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Versión asíncrona del chat con fallback"""

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if historial:
            messages.extend(historial)

        messages.append({"role": "user", "content": mensaje})

        all_models = [self.primary_model] + self.fallback_models

        for idx, model in enumerate(all_models):
            try:
                logger.info(f"🔄 Async intento {idx + 1}/{len(all_models)}: {model}")

                response = await acompletion(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=15
                )

                logger.info(f"✅ Async exitoso: {model}")

                return {
                    "respuesta": response.choices[0].message.content,
                    "modelo_usado": model,
                    "intento": idx + 1,
                    "exito": True
                }

            except Exception as e:
                logger.warning(f"⚠️ Async falló {model}: {str(e)[:100]}")

                if idx == len(all_models) - 1:
                    return {
                        "respuesta": "Servicio temporalmente no disponible",
                        "modelo_usado": None,
                        "exito": False,
                        "error": str(e)
                    }
                continue

    def get_available_models(self) -> List[str]:
        """Retorna lista de modelos disponibles según API keys configuradas"""

        available = []

        if os.getenv("GEMINI_API_KEY"):
            available.append("gemini/gemini-1.5-pro")

        if os.getenv("GROQ_API_KEY"):
            available.extend([
                "groq/llama-3.1-70b-versatile",
                "groq/mixtral-8x7b-32768"
            ])

        if os.getenv("TOGETHER_API_KEY"):
            available.append("together_ai/meta-llama/Llama-3-70b-chat-hf")

        if os.getenv("OPENAI_API_KEY"):
            available.extend(["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"])

        if os.getenv("ANTHROPIC_API_KEY"):
            available.extend(["claude-3-opus", "claude-3-sonnet"])

        return available
