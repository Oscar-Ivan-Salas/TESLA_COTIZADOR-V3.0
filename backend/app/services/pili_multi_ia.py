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

        # Si NO hay API keys configuradas, ir directo a modo offline
        if not any([
            os.getenv("GEMINI_API_KEY"),
            os.getenv("GROQ_API_KEY"),
            os.getenv("TOGETHER_API_KEY"),
            os.getenv("OPENAI_API_KEY"),
            os.getenv("ANTHROPIC_API_KEY")
        ]):
            logger.warning("⚠️ No hay API keys configuradas")
            logger.info("🔧 Activando MODO OFFLINE directamente")
            return self._modo_offline(mensaje, historial)

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

                # Si es el último modelo, usar MODO OFFLINE
                if idx == len(all_models) - 1:
                    logger.error("❌ Todos los modelos fallaron")
                    logger.info("🔧 Activando MODO OFFLINE (lógica propia)")

                    # Usar lógica offline como último recurso
                    return self._modo_offline(mensaje, historial)

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
                    logger.error("❌ Todos los modelos fallaron (async)")
                    logger.info("🔧 Activando MODO OFFLINE (lógica propia)")

                    # Usar modo offline en async también
                    return self._modo_offline(mensaje, historial)

                continue

    def _modo_offline(self, mensaje: str, historial: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        🔧 MODO OFFLINE - Lógica propia cuando NO hay IAs disponibles

        Usa reglas y templates para responder sin conectarse a ninguna IA.
        Esto garantiza que PILI NUNCA se quede paralizado.
        """

        mensaje_lower = mensaje.lower()

        # ==========================================
        # DETECCIÓN DE INTENCIÓN (sin IA)
        # ==========================================

        # 1. COTIZACIÓN
        if any(palabra in mensaje_lower for palabra in ["cotiz", "presupuesto", "cuanto cuesta", "precio"]):
            respuesta = self._offline_cotizacion(mensaje)

        # 2. PROYECTO
        elif any(palabra in mensaje_lower for palabra in ["proyecto", "gantt", "cronograma", "pmi"]):
            respuesta = self._offline_proyecto(mensaje)

        # 3. INFORME
        elif any(palabra in mensaje_lower for palabra in ["informe", "reporte", "documento", "analisis"]):
            respuesta = self._offline_informe(mensaje)

        # 4. SALUDO
        elif any(palabra in mensaje_lower for palabra in ["hola", "buenos días", "buenas tardes", "hey", "hi"]):
            respuesta = """¡Hola! Soy PILI, tu asistente de Tesla Electricidad.

🔧 **MODO OFFLINE ACTIVADO** - Trabajando con lógica local.

Puedo ayudarte con:
• **Cotizaciones** - Instalaciones eléctricas, ITSE, automatización
• **Proyectos** - Planificación, cronogramas, presupuestos
• **Informes** - Técnicos y ejecutivos

¿Qué necesitas hoy?"""

        # 5. DESPEDIDA
        elif any(palabra in mensaje_lower for palabra in ["adios", "chau", "gracias", "hasta luego"]):
            respuesta = """¡Hasta pronto! Fue un gusto ayudarte.

Si necesitas algo más, aquí estaré. 👋"""

        # 6. RESPUESTA GENÉRICA
        else:
            respuesta = """Entiendo que necesitas ayuda, pero necesito más información.

🔧 **Modo Offline Activado** - Conectividad limitada.

Por favor, especifica:
• ¿Necesitas una **cotización**?
• ¿Quieres crear un **proyecto**?
• ¿Necesitas un **informe**?

Cuéntame más detalles para ayudarte mejor."""

        return {
            "respuesta": respuesta,
            "modelo_usado": "PILI_OFFLINE",
            "intento": 1,
            "exito": True,
            "modo": "offline",
            "aviso": "⚠️ Usando lógica local - IAs no disponibles"
        }

    def _offline_cotizacion(self, mensaje: str) -> str:
        """Respuesta offline para cotizaciones"""
        return """Perfecto, te ayudo con la cotización usando mi lógica local.

🔧 **MODO OFFLINE** - Necesito algunos datos:

**Para Instalación Eléctrica:**
1. ¿Cuál es el nombre del cliente?
2. ¿Qué área en m² tiene el proyecto?
3. ¿Cuántos puntos de luz necesitas?
4. ¿Cuántos tomacorrientes?

**Servicios disponibles:**
• Instalaciones Eléctricas
• Certificados ITSE
• Puestas a Tierra
• Sistemas Contra Incendios
• Domótica
• CCTV
• Redes de Datos
• Automatización Industrial

Por favor proporciona estos datos y generaré la cotización."""

    def _offline_proyecto(self, mensaje: str) -> str:
        """Respuesta offline para proyectos"""
        return """Entiendo que necesitas crear un proyecto.

🔧 **MODO OFFLINE** - Dame estos datos:

**Información del Proyecto:**
1. Nombre del proyecto
2. Cliente
3. Tipo (eléctrico, automatización, etc.)
4. Presupuesto estimado (S/)
5. Duración (meses)

**Generaré:**
• Cronograma Gantt
• Análisis de costos
• Identificación de riesgos
• Plan de trabajo

Proporciona los datos y creo el proyecto."""

    def _offline_informe(self, mensaje: str) -> str:
        """Respuesta offline para informes"""
        return """Perfecto, te ayudo con el informe.

🔧 **MODO OFFLINE** - Necesito:

**Datos del Informe:**
1. Tipo: ¿Técnico o Ejecutivo APA?
2. Tema principal
3. Cliente/Destinatario
4. Objetivos del informe

**Incluiré:**
• Resumen ejecutivo
• Análisis técnico
• Conclusiones y recomendaciones
• Bibliografía (si es APA)

Dame los datos para generar el informe."""

    def get_available_models(self) -> List[str]:
        """Retorna lista de modelos disponibles según API keys configuradas"""

        available = []

        # SIEMPRE incluir modo offline como fallback final
        available.append("PILI_OFFLINE (Modo Local)")

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
