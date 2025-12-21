"""
📁 PILI PROYECTOS LANGCHAIN
Agente inteligente para gestión de proyectos simples y PMI complejos
"""

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PILIProyectosLangChain:
    """
    Agente LangChain para proyectos

    Soporta:
    - Proyectos Simples (5 pasos)
    - Proyectos PMI Complejos (8 pasos + Gantt + Riesgos + KPIs)
    """

    def __init__(self, gemini_api_key: str):
        """Inicializa agente con Gemini"""

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=gemini_api_key,
            temperature=0.3,
            convert_system_message_to_human=True
        )

        self.tools = self._crear_herramientas()
        self.prompt = self._crear_prompt()

        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True
        )

        logger.info("✅ PILIProyectos LangChain inicializada")

    def _crear_herramientas(self) -> List[Tool]:
        """Herramientas PMI especializadas"""

        return [
            Tool(
                name="generar_cronograma_gantt",
                func=self._generar_gantt,
                description="""
                Genera cronograma Gantt automático.
                Input: {"fases": [{"nombre": str, "duracion_semanas": int}]}
                Output: Gantt con fechas calculadas
                """
            ),
            Tool(
                name="calcular_roi",
                func=self._calcular_roi,
                description="""
                Calcula ROI del proyecto.
                Input: {"inversion": float, "beneficio_anual": float, "años": int}
                Output: {"roi_%": float, "payback_años": float}
                """
            ),
            Tool(
                name="analizar_riesgos",
                func=self._analizar_riesgos,
                description="""
                Analiza riesgos del proyecto.
                Input: {"descripcion_proyecto": str, "presupuesto": float}
                Output: Lista de riesgos con probabilidad e impacto
                """
            ),
            Tool(
                name="calcular_presupuesto",
                func=self._calcular_presupuesto,
                description="""
                Calcula presupuesto estimado según tipo y duración.
                Input: {"tipo": "electrico|automatizacion|otro", "duracion_meses": int}
                Output: {"presupuesto_estimado": float, "desglose": dict}
                """
            ),
            Tool(
                name="generar_kpis",
                func=self._generar_kpis,
                description="""
                Genera KPIs del proyecto.
                Input: {"tipo_proyecto": str, "presupuesto": float, "duracion_meses": int}
                Output: Lista de KPIs con metas
                """
            ),
            Tool(
                name="formatear_proyecto_json",
                func=self._formatear_proyecto,
                description="""
                Formatea proyecto en JSON estructurado.
                Input: datos completos del proyecto
                Output: JSON final para generación de documento
                """
            )
        ]

    def _generar_gantt(self, input_str: str) -> str:
        """Genera cronograma Gantt"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            fases = data.get("fases", [])

            fecha_inicio = datetime.now()
            gantt = []

            fecha_actual = fecha_inicio

            for idx, fase in enumerate(fases):
                duracion_semanas = fase.get("duracion_semanas", 2)
                fecha_fin = fecha_actual + timedelta(weeks=duracion_semanas)

                gantt.append({
                    "id": idx + 1,
                    "nombre": fase.get("nombre", f"Fase {idx + 1}"),
                    "fecha_inicio": fecha_actual.strftime("%d/%m/%Y"),
                    "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
                    "duracion_semanas": duracion_semanas,
                    "progreso": 0
                })

                fecha_actual = fecha_fin + timedelta(days=1)

            resultado = {
                "gantt": gantt,
                "duracion_total_semanas": sum(f.get("duracion_semanas", 0) for f in fases),
                "fecha_fin_proyecto": fecha_actual.strftime("%d/%m/%Y")
            }

            return json.dumps(resultado, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando Gantt: {e}")
            return json.dumps({"error": str(e)})

    def _calcular_roi(self, input_str: str) -> str:
        """Calcula ROI"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            inversion = float(data.get("inversion", 0))
            beneficio_anual = float(data.get("beneficio_anual", 0))
            años = int(data.get("años", 3))

            beneficio_total = beneficio_anual * años
            roi_porcentaje = ((beneficio_total - inversion) / inversion) * 100 if inversion > 0 else 0

            payback = inversion / beneficio_anual if beneficio_anual > 0 else 0

            resultado = {
                "roi_porcentaje": round(roi_porcentaje, 2),
                "payback_años": round(payback, 2),
                "beneficio_total": round(beneficio_total, 2),
                "ganancia_neta": round(beneficio_total - inversion, 2)
            }

            return json.dumps(resultado, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error calculando ROI: {e}")
            return json.dumps({"error": str(e)})

    def _analizar_riesgos(self, input_str: str) -> str:
        """Analiza riesgos del proyecto"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            desc = data.get("descripcion_proyecto", "").lower()
            presupuesto = float(data.get("presupuesto", 0))

            riesgos = [
                {
                    "riesgo": "Retrasos en permisos municipales",
                    "probabilidad": 0.6,
                    "impacto": 0.7,
                    "severidad": "Media-Alta",
                    "mitigacion": "Tramitar permisos anticipadamente"
                },
                {
                    "riesgo": "Sobrecosto en materiales",
                    "probabilidad": 0.5,
                    "impacto": 0.6,
                    "severidad": "Media",
                    "mitigacion": "Pactar precios con proveedores"
                },
                {
                    "riesgo": "Falta de personal especializado",
                    "probabilidad": 0.4,
                    "impacto": 0.8,
                    "severidad": "Alta",
                    "mitigacion": "Contratar con anticipación"
                }
            ]

            # Agregar riesgo financiero si presupuesto es alto
            if presupuesto > 50000:
                riesgos.append({
                    "riesgo": "Problemas de flujo de caja",
                    "probabilidad": 0.3,
                    "impacto": 0.9,
                    "severidad": "Alta",
                    "mitigacion": "Pagos escalonados con cliente"
                })

            return json.dumps(riesgos, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error analizando riesgos: {e}")
            return json.dumps([])

    def _calcular_presupuesto(self, input_str: str) -> str:
        """Calcula presupuesto estimado"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            tipo = data.get("tipo", "electrico").lower()
            duracion_meses = int(data.get("duracion_meses", 3))

            # Costos base mensuales según tipo
            if tipo == "electrico":
                costo_mensual = 8000
            elif tipo == "automatizacion":
                costo_mensual = 12000
            else:
                costo_mensual = 6000

            materiales = costo_mensual * duracion_meses * 0.5
            mano_obra = costo_mensual * duracion_meses * 0.35
            gastos_generales = costo_mensual * duracion_meses * 0.15

            total = materiales + mano_obra + gastos_generales

            resultado = {
                "presupuesto_estimado": round(total, 2),
                "desglose": {
                    "materiales": round(materiales, 2),
                    "mano_obra": round(mano_obra, 2),
                    "gastos_generales": round(gastos_generales, 2)
                },
                "duracion_meses": duracion_meses
            }

            return json.dumps(resultado, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error calculando presupuesto: {e}")
            return json.dumps({"error": str(e)})

    def _generar_kpis(self, input_str: str) -> str:
        """Genera KPIs del proyecto"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            presupuesto = float(data.get("presupuesto", 0))
            duracion_meses = int(data.get("duracion_meses", 3))

            kpis = [
                {
                    "kpi": "Variación del Cronograma (SV)",
                    "meta": "≤ 5% de desviación",
                    "formula": "(Trabajo Realizado - Trabajo Planificado) / Trabajo Planificado"
                },
                {
                    "kpi": "Variación del Costo (CV)",
                    "meta": f"≤ S/ {presupuesto * 0.1:.2f}",
                    "formula": "Presupuesto - Costo Real"
                },
                {
                    "kpi": "Índice de Desempeño del Costo (CPI)",
                    "meta": "≥ 0.95",
                    "formula": "Valor Ganado / Costo Real"
                },
                {
                    "kpi": "Satisfacción del Cliente",
                    "meta": "≥ 4.5/5.0",
                    "formula": "Encuesta post-proyecto"
                },
                {
                    "kpi": "Cumplimiento de Calidad",
                    "meta": "100% de inspecciones aprobadas",
                    "formula": "Inspecciones Aprobadas / Total Inspecciones"
                }
            ]

            return json.dumps(kpis, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando KPIs: {e}")
            return json.dumps([])

    def _formatear_proyecto(self, input_str: str) -> str:
        """Formatea proyecto en JSON estructurado"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str

            proyecto = {
                "tipo_documento": "proyecto",
                "complejidad": data.get("complejidad", "simple"),
                "puede_generar": True,
                "datos_extraidos": {
                    "nombre": data.get("nombre", "Proyecto Eléctrico"),
                    "cliente": data.get("cliente", {}),
                    "descripcion": data.get("descripcion", ""),
                    "objetivos": data.get("objetivos", []),
                    "presupuesto": data.get("presupuesto", 0),
                    "duracion_meses": data.get("duracion_meses", 3),
                    "fecha": datetime.now().strftime("%d/%m/%Y"),
                    "gantt": data.get("gantt", []),
                    "riesgos": data.get("riesgos", []),
                    "kpis": data.get("kpis", []),
                    "roi": data.get("roi", {}),
                    "observaciones": "Proyecto gestionado con metodología PMI"
                }
            }

            return json.dumps(proyecto, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Error formateando proyecto: {e}")
            return json.dumps({"error": str(e)})

    def _crear_prompt(self) -> PromptTemplate:
        """Prompt para proyectos"""

        template = """Eres PILI Proyectos, experta en gestión de proyectos según PMI.

OBJETIVO: Guiar al usuario para crear proyectos profesionales.

TIPOS DE PROYECTOS:
1. SIMPLE (5 pasos): Nombre, cliente, descripción, duración, presupuesto
2. PMI COMPLEJO (8 pasos): Todo lo anterior + Gantt, riesgos, KPIs, ROI

METODOLOGÍA:
1. Pregunta si quiere proyecto simple o PMI complejo
2. Guía paso a paso (pregunta UNO POR UNO)
3. Usa herramientas para cálculos automáticos
4. Al final, usa "formatear_proyecto_json" para generar JSON

REGLAS:
- Responde en español profesional
- Sé claro y organizado
- Usa herramientas para análisis técnicos
- No inventes datos, pregunta al usuario

HERRAMIENTAS:
{tools}

NOMBRES: {tool_names}

Usuario: {input}

RAZONAMIENTO:
{agent_scratchpad}"""

        return PromptTemplate.from_template(template)

    def procesar(
        self,
        mensaje: str,
        historial: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Procesa mensaje del usuario"""
        try:
            resultado = self.agent_executor.invoke({"input": mensaje})

            respuesta_raw = resultado["output"]

            # Verificar JSON
            puede_generar = False
            datos_proyecto = None

            if "{" in respuesta_raw and "puede_generar" in respuesta_raw:
                try:
                    import re
                    json_match = re.search(r'\{[\s\S]*\}', respuesta_raw)
                    if json_match:
                        datos_proyecto = json.loads(json_match.group())
                        puede_generar = datos_proyecto.get("puede_generar", False)
                        respuesta_limpia = respuesta_raw.replace(json_match.group(), "").strip()
                        if not respuesta_limpia:
                            respuesta_limpia = "✅ Proyecto generado exitosamente."
                    else:
                        respuesta_limpia = respuesta_raw
                except:
                    respuesta_limpia = respuesta_raw
            else:
                respuesta_limpia = respuesta_raw

            return {
                "respuesta": respuesta_limpia,
                "puede_generar": puede_generar,
                "datos_proyecto": datos_proyecto
            }

        except Exception as e:
            logger.error(f"Error en procesar: {e}")
            return {
                "respuesta": f"Disculpa, error: {str(e)}",
                "puede_generar": False,
                "datos_proyecto": None
            }
