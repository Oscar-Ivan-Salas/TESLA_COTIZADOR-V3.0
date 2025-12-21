"""
🎯 PILI COTIZADORA LANGCHAIN
Agente inteligente para cotizaciones simples y complejas

Maneja 10 servicios eléctricos con conversación natural
"""

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, List, Optional
import logging
import re
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class PILICotizadoraLangChain:
    """
    Agente LangChain para cotizaciones inteligentes

    Soporta:
    - Cotizaciones simples (3-5 items)
    - Cotizaciones complejas (10+ items con normativas)

    10 Servicios:
    1. Instalaciones Eléctricas
    2. Certificados ITSE
    3. Puestas a Tierra
    4. Sistemas Contra Incendios
    5. Domótica
    6. CCTV
    7. Redes de Datos
    8. Automatización Industrial
    9. Saneamiento
    10. Expedientes Técnicos
    """

    def __init__(self, gemini_api_key: str):
        """Inicializa agente con Gemini"""

        # LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=gemini_api_key,
            temperature=0.3,
            convert_system_message_to_human=True
        )

        # Herramientas especializadas
        self.tools = self._crear_herramientas()

        # Prompt del agente
        self.prompt = self._crear_prompt()

        # Crear agente
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        # Executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=8,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )

        logger.info("✅ PILICotizadora LangChain inicializada")

    def _crear_herramientas(self) -> List[Tool]:
        """Crea herramientas especializadas para cotizaciones"""

        return [
            Tool(
                name="calcular_carga_electrica",
                func=self._calcular_carga_electrica,
                description="""
                Calcula carga eléctrica según CNE Perú.
                Input: {"area_m2": float, "tipo": "residencial|comercial|industrial"}
                Output: {"carga_va": float, "conductor": "AWG", "normativa": str}
                """
            ),
            Tool(
                name="calcular_igv",
                func=lambda monto: round(float(monto) * 0.18, 2),
                description="Calcula IGV 18% Perú. Input: monto (float). Output: igv (float)"
            ),
            Tool(
                name="generar_items_instalacion_electrica",
                func=self._generar_items_instalacion,
                description="""
                Genera items para instalación eléctrica residencial.
                Input: {"area_m2": float, "puntos_luz": int, "tomacorrientes": int}
                Output: Lista de items con descripción, cantidad, unidad, precio_unitario
                """
            ),
            Tool(
                name="generar_items_itse",
                func=self._generar_items_itse,
                description="""
                Genera items para certificado ITSE.
                Input: {"tipo_local": "comercio|industria|oficina", "area_m2": float}
                Output: Lista de items ITSE
                """
            ),
            Tool(
                name="validar_completitud",
                func=self._validar_completitud,
                description="""
                Valida si tenemos todos los datos para generar cotización.
                Input: {"cliente": str, "items": list, "servicio": str}
                Output: {"completo": bool, "faltantes": list}
                """
            ),
            Tool(
                name="formatear_cotizacion_json",
                func=self._formatear_cotizacion,
                description="""
                Formatea datos en JSON estructurado para generación de documento.
                Input: datos de cotización
                Output: JSON estructurado completo
                """
            )
        ]

    def _calcular_carga_electrica(self, input_str: str) -> str:
        """Calcula carga eléctrica según CNE"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            area_m2 = float(data.get("area_m2", 100))
            tipo = data.get("tipo", "residencial").lower()

            # Carga según tipo (CNE 2011)
            if tipo == "residencial":
                carga_va_m2 = 20  # 20 VA/m²
            elif tipo == "comercial":
                carga_va_m2 = 30
            else:  # industrial
                carga_va_m2 = 40

            carga_total = area_m2 * carga_va_m2

            # Conductor según carga
            if carga_total < 3000:
                conductor = "14 AWG"
            elif carga_total < 5000:
                conductor = "12 AWG"
            else:
                conductor = "10 AWG"

            resultado = {
                "carga_va": carga_total,
                "conductor_recomendado": conductor,
                "normativa": "CNE 2011 Art. 50.102"
            }

            return json.dumps(resultado, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error calculando carga: {e}")
            return json.dumps({"error": str(e)})

    def _generar_items_instalacion(self, input_str: str) -> str:
        """Genera items para instalación eléctrica"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            area_m2 = float(data.get("area_m2", 100))
            puntos_luz = int(data.get("puntos_luz", 15))
            tomacorrientes = int(data.get("tomacorrientes", 10))

            items = [
                {
                    "descripcion": f"Tablero eléctrico monofásico {int(puntos_luz + tomacorrientes) // 2} polos",
                    "cantidad": 1,
                    "unidad": "und",
                    "precio_unitario": 450.00
                },
                {
                    "descripcion": "Punto de luz empotrado con cable 14 AWG",
                    "cantidad": puntos_luz,
                    "unidad": "pto",
                    "precio_unitario": 35.00
                },
                {
                    "descripcion": "Tomacorriente doble con línea a tierra",
                    "cantidad": tomacorrientes,
                    "unidad": "und",
                    "precio_unitario": 25.00
                },
                {
                    "descripcion": "Cable THW 14 AWG",
                    "cantidad": int(area_m2 * 0.8),
                    "unidad": "m",
                    "precio_unitario": 2.50
                },
                {
                    "descripcion": "Tubería PVC-P 20mm",
                    "cantidad": int(area_m2 * 0.6),
                    "unidad": "m",
                    "precio_unitario": 1.80
                }
            ]

            return json.dumps(items, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando items: {e}")
            return json.dumps([])

    def _generar_items_itse(self, input_str: str) -> str:
        """Genera items para ITSE"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            tipo_local = data.get("tipo_local", "comercio").lower()
            area_m2 = float(data.get("area_m2", 100))

            # Precio base según tipo y área
            if tipo_local == "comercio":
                precio_base = 800 + (area_m2 * 2)
            elif tipo_local == "industria":
                precio_base = 1200 + (area_m2 * 3)
            else:  # oficina
                precio_base = 600 + (area_m2 * 1.5)

            items = [
                {
                    "descripcion": "Inspección técnica de seguridad básica",
                    "cantidad": 1,
                    "unidad": "serv",
                    "precio_unitario": precio_base * 0.5
                },
                {
                    "descripcion": "Plano de ubicación y arquitectura",
                    "cantidad": 1,
                    "unidad": "doc",
                    "precio_unitario": 150.00
                },
                {
                    "descripcion": "Memoria descriptiva y cálculos",
                    "cantidad": 1,
                    "unidad": "doc",
                    "precio_unitario": 200.00
                },
                {
                    "descripcion": "Tramitación y certificación ITSE",
                    "cantidad": 1,
                    "unidad": "trám",
                    "precio_unitario": precio_base * 0.5
                }
            ]

            return json.dumps(items, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando items ITSE: {e}")
            return json.dumps([])

    def _validar_completitud(self, input_str: str) -> str:
        """Valida si datos están completos"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str

            faltantes = []

            if not data.get("cliente"):
                faltantes.append("datos del cliente (nombre, RUC)")

            if not data.get("items") or len(data.get("items", [])) == 0:
                faltantes.append("items de cotización")

            if not data.get("servicio"):
                faltantes.append("tipo de servicio")

            resultado = {
                "completo": len(faltantes) == 0,
                "faltantes": faltantes
            }

            return json.dumps(resultado, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"completo": False, "error": str(e)})

    def _formatear_cotizacion(self, input_str: str) -> str:
        """Formatea cotización en JSON estructurado"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str

            items = data.get("items", [])
            subtotal = sum(item.get("cantidad", 0) * item.get("precio_unitario", 0) for item in items)
            igv = subtotal * 0.18
            total = subtotal + igv

            cotizacion = {
                "tipo_documento": "cotizacion",
                "puede_generar": True,
                "datos_extraidos": {
                    "numero": f"COT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    "fecha": datetime.now().strftime("%d/%m/%Y"),
                    "cliente": data.get("cliente", {}),
                    "proyecto": data.get("proyecto", "Servicio Eléctrico"),
                    "servicio": data.get("servicio", "instalacion-electrica"),
                    "items": items,
                    "subtotal": round(subtotal, 2),
                    "igv": round(igv, 2),
                    "total": round(total, 2),
                    "observaciones": "Precios incluyen IGV. Instalación según CNE 2011.",
                    "vigencia": "30 días"
                }
            }

            return json.dumps(cotizacion, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Error formateando: {e}")
            return json.dumps({"error": str(e)})

    def _crear_prompt(self) -> PromptTemplate:
        """Crea prompt para el agente"""

        template = """Eres PILI Cotizadora, experta en cotizaciones eléctricas en Perú.

OBJETIVO: Guiar al usuario paso a paso para generar cotización profesional.

SERVICIOS QUE MANEJAS:
1. Instalaciones Eléctricas (residencial, comercial, industrial)
2. Certificados ITSE
3. Puestas a Tierra
4. Sistemas Contra Incendios
5. Domótica y Automatización
6. CCTV
7. Redes de Datos
8. Automatización Industrial
9. Saneamiento
10. Expedientes Técnicos

METODOLOGÍA:
1. Detecta el servicio que necesita
2. Pregunta datos UNO POR UNO (no muchas preguntas juntas)
3. Usa herramientas para cálculos y generación de items
4. Cuando tengas todos los datos, usa "formatear_cotizacion_json" para generar JSON final

REGLAS:
- Responde en español peruano profesional
- Sé amable y claro
- No inventes precios, usa las herramientas
- Si no sabes algo, pregunta al usuario

HERRAMIENTAS DISPONIBLES:
{tools}

NOMBRES DE HERRAMIENTAS: {tool_names}

CONVERSACIÓN ACTUAL:
Usuario: {input}

RAZONAMIENTO:
{agent_scratchpad}"""

        return PromptTemplate.from_template(template)

    def procesar(
        self,
        mensaje: str,
        historial: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Procesa mensaje del usuario

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación

        Returns:
            {
                "respuesta": str,
                "puede_generar": bool,
                "datos_cotizacion": dict (si puede_generar=True)
            }
        """
        try:
            # Ejecutar agente
            resultado = self.agent_executor.invoke({
                "input": mensaje
            })

            respuesta_raw = resultado["output"]

            # Verificar si generó JSON de cotización
            puede_generar = False
            datos_cotizacion = None

            if "{" in respuesta_raw and "puede_generar" in respuesta_raw:
                try:
                    # Extraer JSON
                    json_match = re.search(r'\{[\s\S]*\}', respuesta_raw)
                    if json_match:
                        datos_cotizacion = json.loads(json_match.group())
                        puede_generar = datos_cotizacion.get("puede_generar", False)

                        # Respuesta sin el JSON
                        respuesta_limpia = respuesta_raw.replace(json_match.group(), "").strip()
                        if not respuesta_limpia:
                            respuesta_limpia = "✅ Cotización generada exitosamente. Revisa los detalles."
                    else:
                        respuesta_limpia = respuesta_raw
                except:
                    respuesta_limpia = respuesta_raw
            else:
                respuesta_limpia = respuesta_raw

            return {
                "respuesta": respuesta_limpia,
                "puede_generar": puede_generar,
                "datos_cotizacion": datos_cotizacion
            }

        except Exception as e:
            logger.error(f"Error en procesar: {e}")
            return {
                "respuesta": f"Disculpa, hubo un error: {str(e)}. ¿Puedes reformular tu pregunta?",
                "puede_generar": False,
                "datos_cotizacion": None
            }
