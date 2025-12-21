"""
📄 PILI INFORMES LANGCHAIN
Agente inteligente para generación de informes técnicos y ejecutivos APA

Soporta:
- Informes Técnicos (estructurados con análisis profesional)
- Informes Ejecutivos APA (formato académico/profesional)
"""

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class PILIInformesLangChain:
    """
    Agente LangChain para informes profesionales

    Soporta:
    - Informes Técnicos (análisis, conclusiones, recomendaciones)
    - Informes Ejecutivos APA (formato académico/investigación)
    """

    def __init__(self, gemini_api_key: str):
        """Inicializa agente con Gemini"""

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=gemini_api_key,
            temperature=0.4,  # Un poco más creativo para redacción
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

        logger.info("✅ PILIInformes LangChain inicializada")

    def _crear_herramientas(self) -> List[Tool]:
        """Herramientas especializadas para informes"""

        return [
            Tool(
                name="generar_resumen_ejecutivo",
                func=self._generar_resumen_ejecutivo,
                description="""
                Genera resumen ejecutivo profesional.
                Input: {"tema": str, "objetivos": list, "conclusiones_clave": list}
                Output: Resumen ejecutivo estructurado (200-300 palabras)
                """
            ),
            Tool(
                name="generar_analisis_tecnico",
                func=self._generar_analisis_tecnico,
                description="""
                Genera análisis técnico detallado.
                Input: {"tipo_proyecto": str, "datos": dict, "aspectos_clave": list}
                Output: Análisis técnico con subsecciones
                """
            ),
            Tool(
                name="generar_conclusiones_recomendaciones",
                func=self._generar_conclusiones,
                description="""
                Genera conclusiones y recomendaciones.
                Input: {"hallazgos": list, "objetivos": list}
                Output: Conclusiones numeradas + recomendaciones accionables
                """
            ),
            Tool(
                name="generar_bibliografia_apa",
                func=self._generar_bibliografia_apa,
                description="""
                Genera bibliografía en formato APA 7ma edición.
                Input: {"tipo_fuentes": list}  # "normas_electricas", "pmi", "ieee", etc.
                Output: Lista de referencias en formato APA correcto
                """
            ),
            Tool(
                name="estructurar_informe_tecnico",
                func=self._estructurar_informe_tecnico,
                description="""
                Estructura completa de informe técnico.
                Input: datos del informe
                Output: Estructura con todas las secciones
                """
            ),
            Tool(
                name="estructurar_informe_ejecutivo_apa",
                func=self._estructurar_informe_apa,
                description="""
                Estructura completa de informe ejecutivo APA.
                Input: datos del informe
                Output: Estructura formato APA con portada, índice, secciones
                """
            ),
            Tool(
                name="formatear_informe_json",
                func=self._formatear_informe,
                description="""
                Formatea informe en JSON estructurado.
                Input: datos completos del informe
                Output: JSON final para generación de documento
                """
            )
        ]

    def _generar_resumen_ejecutivo(self, input_str: str) -> str:
        """Genera resumen ejecutivo"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            tema = data.get("tema", "Proyecto Técnico")
            objetivos = data.get("objetivos", [])
            conclusiones = data.get("conclusiones_clave", [])

            resumen = {
                "titulo": "Resumen Ejecutivo",
                "parrafos": [
                    f"El presente informe técnico sobre '{tema}' tiene como propósito analizar y documentar los aspectos técnicos, económicos y operativos del proyecto.",

                    f"Los objetivos principales incluyen: {', '.join(objetivos[:3]) if objetivos else 'análisis técnico completo, evaluación económica y recomendaciones de implementación'}.",

                    f"Entre las conclusiones clave se encuentran: {', '.join(conclusiones[:2]) if conclusiones else 'viabilidad técnica confirmada y rentabilidad proyectada positiva'}.",

                    "Se recomienda proceder con la implementación siguiendo las fases propuestas y los lineamientos técnicos establecidos en este documento."
                ],
                "palabras_clave": ["análisis técnico", "viabilidad", "implementación", "recomendaciones"]
            }

            return json.dumps(resumen, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando resumen: {e}")
            return json.dumps({"error": str(e)})

    def _generar_analisis_tecnico(self, input_str: str) -> str:
        """Genera análisis técnico detallado"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            tipo = data.get("tipo_proyecto", "electrico").lower()
            datos_proyecto = data.get("datos", {})

            analisis = {
                "titulo": "Análisis Técnico",
                "subsecciones": []
            }

            # 1. Contexto Técnico
            analisis["subsecciones"].append({
                "titulo": "1. Contexto y Alcance Técnico",
                "contenido": f"El proyecto corresponde a una intervención de tipo {tipo}, que requiere consideraciones técnicas específicas según normativas vigentes (CNE 2011, RNE, etc.)."
            })

            # 2. Especificaciones Técnicas
            if tipo == "electrico":
                analisis["subsecciones"].append({
                    "titulo": "2. Especificaciones Eléctricas",
                    "contenido": "Sistema eléctrico diseñado conforme al Código Nacional de Electricidad (CNE 2011). Incluye tableros, circuitos derivados, protecciones termomagnéticas y sistema de puesta a tierra.",
                    "detalles": [
                        "Tensión de servicio: 220V monofásico / 380V trifásico",
                        "Conductores: THW/THHN calibre según cálculo de carga",
                        "Protecciones: Interruptores termomagnéticos según IEC 60898",
                        "Puesta a tierra: Resistencia < 25 Ohm según CNE"
                    ]
                })
            elif tipo == "automatizacion":
                analisis["subsecciones"].append({
                    "titulo": "2. Especificaciones de Automatización",
                    "contenido": "Sistema de automatización industrial con controladores lógicos programables (PLC) y supervisión SCADA.",
                    "detalles": [
                        "Controlador: PLC con comunicación Ethernet/IP",
                        "I/O: Módulos digitales y analógicos según proceso",
                        "HMI: Pantalla táctil para operación local",
                        "SCADA: Software de supervisión centralizada"
                    ]
                })
            else:
                analisis["subsecciones"].append({
                    "titulo": "2. Especificaciones Técnicas Generales",
                    "contenido": "El proyecto cumple con estándares técnicos internacionales y normativas locales aplicables."
                })

            # 3. Metodología de Implementación
            analisis["subsecciones"].append({
                "titulo": "3. Metodología de Implementación",
                "contenido": "La ejecución del proyecto sigue metodología PMI (Project Management Institute) con enfoque ágil adaptado.",
                "fases": [
                    "Fase 1: Ingeniería de detalle y planificación",
                    "Fase 2: Adquisición de materiales y equipos",
                    "Fase 3: Implementación en sitio",
                    "Fase 4: Pruebas y puesta en marcha",
                    "Fase 5: Capacitación y entrega"
                ]
            })

            # 4. Consideraciones Técnicas Críticas
            analisis["subsecciones"].append({
                "titulo": "4. Consideraciones Críticas",
                "puntos": [
                    "Cumplimiento normativo: Todos los componentes cumplen normativas peruanas e internacionales",
                    "Seguridad: Diseño prioriza seguridad de personas y equipos",
                    "Mantenibilidad: Sistema diseñado para facilitar mantenimiento preventivo",
                    "Escalabilidad: Arquitectura permite futuras ampliaciones"
                ]
            })

            return json.dumps(analisis, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando análisis: {e}")
            return json.dumps({"error": str(e)})

    def _generar_conclusiones(self, input_str: str) -> str:
        """Genera conclusiones y recomendaciones"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            hallazgos = data.get("hallazgos", [])
            objetivos = data.get("objetivos", [])

            resultado = {
                "conclusiones": [
                    {
                        "numero": 1,
                        "texto": "El proyecto es técnicamente viable y cumple con todas las normativas aplicables (CNE 2011, RNE, estándares internacionales)."
                    },
                    {
                        "numero": 2,
                        "texto": "La metodología propuesta garantiza una implementación ordenada, segura y eficiente del proyecto."
                    },
                    {
                        "numero": 3,
                        "texto": "Los riesgos identificados son manejables mediante las estrategias de mitigación propuestas."
                    },
                    {
                        "numero": 4,
                        "texto": "El análisis costo-beneficio indica un retorno de inversión favorable en el plazo proyectado."
                    }
                ],
                "recomendaciones": [
                    {
                        "numero": 1,
                        "tipo": "Inmediata",
                        "texto": "Proceder con la fase de ingeniería de detalle y elaboración de planos definitivos.",
                        "prioridad": "Alta"
                    },
                    {
                        "numero": 2,
                        "tipo": "Corto plazo",
                        "texto": "Iniciar proceso de adquisición de materiales y equipos críticos para evitar retrasos.",
                        "prioridad": "Alta"
                    },
                    {
                        "numero": 3,
                        "tipo": "Durante ejecución",
                        "texto": "Implementar sistema de control de calidad en cada fase del proyecto.",
                        "prioridad": "Media"
                    },
                    {
                        "numero": 4,
                        "tipo": "Post-implementación",
                        "texto": "Establecer programa de mantenimiento preventivo para garantizar vida útil de equipos.",
                        "prioridad": "Media"
                    }
                ]
            }

            # Agregar hallazgos personalizados si existen
            if hallazgos:
                for i, hallazgo in enumerate(hallazgos[:2], start=5):
                    resultado["conclusiones"].append({
                        "numero": i,
                        "texto": hallazgo
                    })

            return json.dumps(resultado, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando conclusiones: {e}")
            return json.dumps({"error": str(e)})

    def _generar_bibliografia_apa(self, input_str: str) -> str:
        """Genera bibliografía en formato APA 7ma edición"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str
            tipo_fuentes = data.get("tipo_fuentes", ["normas_electricas"])

            bibliografia = []

            # Normas eléctricas peruanas
            if "normas_electricas" in tipo_fuentes or "electrico" in str(tipo_fuentes).lower():
                bibliografia.extend([
                    {
                        "referencia": "Ministerio de Energía y Minas. (2011). *Código Nacional de Electricidad - Utilización* (CNE 2011). Dirección General de Electricidad.",
                        "tipo": "normativa"
                    },
                    {
                        "referencia": "Ministerio de Vivienda, Construcción y Saneamiento. (2006). *Reglamento Nacional de Edificaciones* (RNE). Norma EM.010 Instalaciones Eléctricas Interiores.",
                        "tipo": "normativa"
                    }
                ])

            # PMI y gestión de proyectos
            if "pmi" in tipo_fuentes or "proyectos" in str(tipo_fuentes).lower():
                bibliografia.extend([
                    {
                        "referencia": "Project Management Institute. (2021). *A Guide to the Project Management Body of Knowledge* (PMBOK® Guide) (7th ed.). PMI Publications.",
                        "tipo": "metodologia"
                    },
                    {
                        "referencia": "Schwalbe, K. (2018). *Information Technology Project Management* (9th ed.). Cengage Learning.",
                        "tipo": "libro"
                    }
                ])

            # Estándares IEEE
            if "ieee" in tipo_fuentes or "estandares" in str(tipo_fuentes).lower():
                bibliografia.extend([
                    {
                        "referencia": "Institute of Electrical and Electronics Engineers. (2020). *IEEE Standard for Electrical Installations* (IEEE Std 3001-2020).",
                        "tipo": "estandar"
                    }
                ])

            # Automatización
            if "automatizacion" in tipo_fuentes or "scada" in str(tipo_fuentes).lower():
                bibliografia.extend([
                    {
                        "referencia": "Bolton, W. (2015). *Programmable Logic Controllers* (6th ed.). Newnes.",
                        "tipo": "libro"
                    },
                    {
                        "referencia": "Siemens AG. (2022). *SIMATIC PLC Programming Guide*. Siemens Industry Documentation.",
                        "tipo": "manual"
                    }
                ])

            # Si no hay referencias específicas, agregar generales
            if not bibliografia:
                bibliografia = [
                    {
                        "referencia": "Ministerio de Energía y Minas. (2011). *Código Nacional de Electricidad - Utilización* (CNE 2011). Dirección General de Electricidad.",
                        "tipo": "normativa"
                    },
                    {
                        "referencia": "Project Management Institute. (2021). *A Guide to the Project Management Body of Knowledge* (PMBOK® Guide) (7th ed.). PMI Publications.",
                        "tipo": "metodologia"
                    }
                ]

            return json.dumps({
                "titulo": "Referencias Bibliográficas",
                "formato": "APA 7ma Edición",
                "referencias": bibliografia,
                "nota": "Referencias organizadas alfabéticamente según apellido del autor o nombre de la institución."
            }, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error generando bibliografía: {e}")
            return json.dumps({"referencias": []})

    def _estructurar_informe_tecnico(self, input_str: str) -> str:
        """Estructura completa de informe técnico"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str

            estructura = {
                "tipo": "informe_tecnico",
                "portada": {
                    "titulo": data.get("titulo", "Informe Técnico"),
                    "empresa": "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",
                    "cliente": data.get("cliente", {}),
                    "fecha": datetime.now().strftime("%d de %B de %Y"),
                    "elaborado_por": "Departamento de Ingeniería"
                },
                "secciones": [
                    {
                        "numero": "1",
                        "titulo": "Resumen Ejecutivo",
                        "contenido_key": "resumen_ejecutivo"
                    },
                    {
                        "numero": "2",
                        "titulo": "Introducción",
                        "subsecciones": ["Antecedentes", "Objetivos", "Alcance"]
                    },
                    {
                        "numero": "3",
                        "titulo": "Análisis Técnico",
                        "contenido_key": "analisis_tecnico"
                    },
                    {
                        "numero": "4",
                        "titulo": "Metodología",
                        "subsecciones": ["Enfoque metodológico", "Fases del proyecto", "Cronograma"]
                    },
                    {
                        "numero": "5",
                        "titulo": "Resultados y Hallazgos",
                        "contenido": "Descripción de resultados obtenidos del análisis"
                    },
                    {
                        "numero": "6",
                        "titulo": "Conclusiones y Recomendaciones",
                        "contenido_key": "conclusiones_recomendaciones"
                    },
                    {
                        "numero": "7",
                        "titulo": "Anexos",
                        "items": ["Planos técnicos", "Especificaciones técnicas", "Cotizaciones"]
                    }
                ]
            }

            return json.dumps(estructura, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error estructurando informe técnico: {e}")
            return json.dumps({"error": str(e)})

    def _estructurar_informe_apa(self, input_str: str) -> str:
        """Estructura completa de informe ejecutivo APA"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str

            estructura = {
                "tipo": "informe_ejecutivo_apa",
                "portada_apa": {
                    "titulo": data.get("titulo", "Informe Ejecutivo"),
                    "subtitulo": data.get("subtitulo", "Análisis Técnico y Propuesta de Implementación"),
                    "autor": "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",
                    "institucion": "Departamento de Ingeniería",
                    "fecha": datetime.now().strftime("%d de %B de %Y")
                },
                "contenido_preliminar": [
                    {
                        "elemento": "Resumen Ejecutivo",
                        "pagina": "ii",
                        "longitud": "200-300 palabras"
                    },
                    {
                        "elemento": "Índice General",
                        "pagina": "iii",
                        "generado_automaticamente": True
                    },
                    {
                        "elemento": "Índice de Tablas",
                        "pagina": "iv",
                        "si_aplica": True
                    },
                    {
                        "elemento": "Índice de Figuras",
                        "pagina": "v",
                        "si_aplica": True
                    }
                ],
                "cuerpo_principal": [
                    {
                        "capitulo": 1,
                        "titulo": "Introducción",
                        "subsecciones": [
                            "1.1 Antecedentes",
                            "1.2 Justificación",
                            "1.3 Objetivos",
                            "1.4 Alcance y Limitaciones"
                        ]
                    },
                    {
                        "capitulo": 2,
                        "titulo": "Marco Teórico",
                        "subsecciones": [
                            "2.1 Fundamentos Técnicos",
                            "2.2 Normativas Aplicables",
                            "2.3 Estado del Arte"
                        ]
                    },
                    {
                        "capitulo": 3,
                        "titulo": "Metodología",
                        "subsecciones": [
                            "3.1 Diseño de la Investigación",
                            "3.2 Procedimientos",
                            "3.3 Herramientas y Técnicas"
                        ]
                    },
                    {
                        "capitulo": 4,
                        "titulo": "Análisis y Resultados",
                        "subsecciones": [
                            "4.1 Diagnóstico Actual",
                            "4.2 Análisis Técnico",
                            "4.3 Evaluación Económica"
                        ]
                    },
                    {
                        "capitulo": 5,
                        "titulo": "Conclusiones y Recomendaciones",
                        "subsecciones": [
                            "5.1 Conclusiones",
                            "5.2 Recomendaciones",
                            "5.3 Trabajo Futuro"
                        ]
                    }
                ],
                "contenido_final": [
                    {
                        "elemento": "Referencias Bibliográficas",
                        "formato": "APA 7ma Edición",
                        "contenido_key": "bibliografia_apa"
                    },
                    {
                        "elemento": "Apéndices",
                        "items": [
                            "Apéndice A: Cálculos Técnicos",
                            "Apéndice B: Planos y Diagramas",
                            "Apéndice C: Especificaciones Técnicas"
                        ]
                    }
                ],
                "formato": {
                    "fuente": "Times New Roman 12pt",
                    "interlineado": "Doble espacio",
                    "margenes": "2.54 cm (1 pulgada) todos los lados",
                    "numeracion": "Números arábigos en esquina superior derecha",
                    "sangria": "1.27 cm (0.5 pulgadas) primera línea de párrafo"
                }
            }

            return json.dumps(estructura, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error estructurando informe APA: {e}")
            return json.dumps({"error": str(e)})

    def _formatear_informe(self, input_str: str) -> str:
        """Formatea informe en JSON estructurado"""
        try:
            data = json.loads(input_str) if isinstance(input_str, str) else input_str

            tipo_informe = data.get("tipo_informe", "tecnico")  # tecnico o ejecutivo_apa

            informe = {
                "tipo_documento": "informe",
                "subtipo": tipo_informe,
                "puede_generar": True,
                "datos_extraidos": {
                    "titulo": data.get("titulo", "Informe Técnico Profesional"),
                    "cliente": data.get("cliente", {}),
                    "proyecto": data.get("proyecto", ""),
                    "fecha": datetime.now().strftime("%d/%m/%Y"),
                    "autor": "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",

                    # Contenido estructurado
                    "resumen_ejecutivo": data.get("resumen_ejecutivo", {}),
                    "introduccion": data.get("introduccion", {}),
                    "analisis_tecnico": data.get("analisis_tecnico", {}),
                    "metodologia": data.get("metodologia", {}),
                    "conclusiones_recomendaciones": data.get("conclusiones_recomendaciones", {}),
                    "bibliografia": data.get("bibliografia", []),

                    # Metadata
                    "tipo_proyecto": data.get("tipo_proyecto", "electrico"),
                    "presupuesto": data.get("presupuesto", 0),
                    "duracion_meses": data.get("duracion_meses", 3),

                    # Estructura del documento
                    "estructura": data.get("estructura", {}),

                    "observaciones": f"Informe {'ejecutivo APA' if tipo_informe == 'ejecutivo_apa' else 'técnico'} generado profesionalmente"
                }
            }

            return json.dumps(informe, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Error formateando informe: {e}")
            return json.dumps({"error": str(e)})

    def _crear_prompt(self) -> PromptTemplate:
        """Prompt para informes"""

        template = """Eres PILI Informes, experta en redacción de informes técnicos y ejecutivos.

OBJETIVO: Guiar al usuario para crear informes profesionales (Técnico o Ejecutivo APA).

TIPOS DE INFORMES:
1. TÉCNICO: Informe estructurado para proyectos (resumen, análisis, conclusiones, anexos)
2. EJECUTIVO APA: Informe formato académico/investigación (portada APA, índice, capítulos, bibliografía APA 7ma ed.)

METODOLOGÍA:
1. Pregunta qué tipo de informe necesita (Técnico o Ejecutivo APA)
2. Guía paso a paso (pregunta UNO POR UNO los datos necesarios)
3. Usa herramientas para generar secciones profesionales
4. Al final, usa "formatear_informe_json" para generar JSON

REGLAS:
- Responde en español profesional y formal
- Usa terminología técnica apropiada
- Para informes APA, sigue estrictamente formato APA 7ma edición
- No inventes datos técnicos, pregunta al usuario
- Genera contenido coherente y bien estructurado

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
            datos_informe = None

            if "{" in respuesta_raw and "puede_generar" in respuesta_raw:
                try:
                    import re
                    json_match = re.search(r'\{[\s\S]*\}', respuesta_raw)
                    if json_match:
                        datos_informe = json.loads(json_match.group())
                        puede_generar = datos_informe.get("puede_generar", False)
                        respuesta_limpia = respuesta_raw.replace(json_match.group(), "").strip()
                        if not respuesta_limpia:
                            respuesta_limpia = "✅ Informe generado exitosamente."
                    else:
                        respuesta_limpia = respuesta_raw
                except:
                    respuesta_limpia = respuesta_raw
            else:
                respuesta_limpia = respuesta_raw

            return {
                "respuesta": respuesta_limpia,
                "puede_generar": puede_generar,
                "datos_informe": datos_informe
            }

        except Exception as e:
            logger.error(f"Error en procesar: {e}")
            return {
                "respuesta": f"Disculpa, error: {str(e)}",
                "puede_generar": False,
                "datos_informe": None
            }
