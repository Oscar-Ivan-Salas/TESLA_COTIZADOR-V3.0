"""
🎯 PILI ORCHESTRATOR INTELIGENTE - INTEGRACIÓN DE 3 ESPECIALISTAS
📁 RUTA: services/pili_orchestrator.py

ORQUESTA 3 ESPECIALISTAS PILI:
✅ pili_cotizadora.py - Cotizaciones inteligentes para 10 servicios
✅ pili_proyectos.py - Proyectos simples y complejos PMI
✅ pili_informes.py - Informes técnicos y ejecutivos APA

INTEGRA CON SERVICIOS EXISTENTES:
✅ file_processor.py (tu versión)
✅ gemini_service.py (tu versión)
✅ rag_service.py (tu versión)
✅ template_processor.py (tu versión)
✅ word_generator.py (tu versión)
✅ pdf_generator.py (tu versión)

ESTE ARCHIVO ES EL COORDINADOR MAESTRO QUE UNE TODO EL SISTEMA PILI.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import json

# Imports de los 3 especialistas PILI
try:
    from .pili_cotizadora import pili_cotizadora
    from .pili_proyectos import pili_proyectos
    from .pili_informes import pili_informes
    logger_temp = logging.getLogger(__name__)
    logger_temp.info("✅ Especialistas PILI importados correctamente")
except ImportError as e:
    logging.warning(f"⚠️ Error importando especialistas PILI: {e}")
    pili_cotizadora = None
    pili_proyectos = None
    pili_informes = None

# Imports de tus servicios existentes
try:
    from .gemini_service import gemini_service
    from .file_processor import file_processor
    from .rag_service import rag_service
    from .template_processor import template_processor
    from .word_generator import word_generator
    from .pdf_generator import pdf_generator
except ImportError as e:
    logging.warning(f"Importing with fallback: {e}")
    # Fallback imports
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))

        import gemini_service
        import file_processor
        import rag_service
        import template_processor
        import word_generator
        import pdf_generator
    except:
        logging.error("Could not import services")

logger = logging.getLogger(__name__)

class PILIOrchestrator:
    """
    🎯 ORQUESTADOR INTELIGENTE - Coordina 3 especialistas PILI

    Orquesta los 3 especialistas PILI:
    - PILICotizadora: Guía conversacional para cotizaciones de 10 servicios
    - PILIProyectos: Creación de proyectos simples y complejos PMI
    - PILIInformes: Generación de informes técnicos y ejecutivos APA

    Además se integra con servicios existentes para generación de documentos.
    """

    def __init__(self):
        """Inicializa orquestador con los 3 especialistas PILI"""

        self.servicios = {}
        self.modo_demo = False

        # Conectar los 3 especialistas PILI
        self.cotizadora = pili_cotizadora
        self.proyectos = pili_proyectos
        self.informes = pili_informes

        # Conectar con tus servicios existentes
        self._conectar_servicios_existentes()

        logger.info("✅ PILI Orchestrator con 3 especialistas inicializado")
    
    def _conectar_servicios_existentes(self):
        """Conecta con tus servicios sin modificarlos"""
        
        # Conectar Gemini Service (tu versión)
        try:
            if 'gemini_service' in globals():
                self.servicios['gemini'] = gemini_service
                logger.info("✅ Conectado con tu GeminiService")
            else:
                self.servicios['gemini'] = None
                self.modo_demo = True
                logger.info("⚠️ GeminiService no disponible - modo demo")
        except Exception as e:
            logger.warning(f"GeminiService error: {e}")
            self.servicios['gemini'] = None
            self.modo_demo = True
        
        # Conectar File Processor (tu versión)
        try:
            if 'file_processor' in globals():
                self.servicios['file_processor'] = file_processor
                logger.info("✅ Conectado con tu FileProcessor")
            else:
                self.servicios['file_processor'] = None
        except Exception as e:
            logger.warning(f"FileProcessor error: {e}")
            self.servicios['file_processor'] = None
        
        # Conectar RAG Service (tu versión)
        try:
            if 'rag_service' in globals():
                self.servicios['rag'] = rag_service
                logger.info("✅ Conectado con tu RAGService")
            else:
                self.servicios['rag'] = None
        except Exception as e:
            logger.warning(f"RAGService error: {e}")
            self.servicios['rag'] = None
        
        # Conectar Template Processor (tu versión)
        try:
            if 'template_processor' in globals():
                self.servicios['template'] = template_processor
                logger.info("✅ Conectado con tu TemplateProcessor")
            else:
                self.servicios['template'] = None
        except Exception as e:
            logger.warning(f"TemplateProcessor error: {e}")
            self.servicios['template'] = None
        
        # Conectar Word Generator (tu versión)
        try:
            if 'word_generator' in globals():
                self.servicios['word'] = word_generator
                logger.info("✅ Conectado con tu WordGenerator")
            else:
                self.servicios['word'] = None
        except Exception as e:
            logger.warning(f"WordGenerator error: {e}")
            self.servicios['word'] = None
        
        # Conectar PDF Generator (tu versión)
        try:
            if 'pdf_generator' in globals():
                self.servicios['pdf'] = pdf_generator
                logger.info("✅ Conectado con tu PDFGenerator")
            else:
                self.servicios['pdf'] = None
        except Exception as e:
            logger.warning(f"PDFGenerator error: {e}")
            self.servicios['pdf'] = None

    # ═══════════════════════════════════════════════════════════════
    # 🎯 MÉTODO PRINCIPAL - ENRUTA A ESPECIALISTAS PILI
    # ═══════════════════════════════════════════════════════════════

    def procesar(
        self,
        mensaje: str,
        historial: List[Dict[str, str]],
        tipo_flujo: str
    ) -> Dict[str, Any]:
        """
        🎯 MÉTODO PRINCIPAL - Enruta al especialista PILI correcto

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación
            tipo_flujo: Tipo de flujo (cotizacion-simple, proyecto-pmi, informe-tecnico, etc.)

        Returns:
            Respuesta del especialista correspondiente

        Tipos de flujo soportados:
            - cotizacion-simple, cotizacion-rapida, cotizacion-compleja → PILICotizadora
            - proyecto-simple, proyecto-complejo, proyecto-pmi → PILIProyectos
            - informe-simple, informe-tecnico, informe-ejecutivo → PILIInformes
        """

        logger.info(f"🎯 Orquestador recibió mensaje para flujo: {tipo_flujo}")

        try:
            # ENRUTAR A PILI COTIZADORA (10 servicios)
            if any(keyword in tipo_flujo.lower() for keyword in ["cotizacion", "cotizar", "presupuesto"]):
                if self.cotizadora:
                    logger.info("📋 Enrutando a PILICotizadora...")
                    return self.cotizadora.procesar(mensaje, historial)
                else:
                    return {
                        "accion": "error",
                        "mensaje_pili": "❌ PILICotizadora no está disponible",
                        "error": "Módulo pili_cotizadora no cargado"
                    }

            # ENRUTAR A PILI PROYECTOS (simple y PMI)
            elif any(keyword in tipo_flujo.lower() for keyword in ["proyecto"]):
                if self.proyectos:
                    logger.info("📁 Enrutando a PILIProyectos...")
                    return self.proyectos.procesar(mensaje, historial, tipo_flujo)
                else:
                    return {
                        "accion": "error",
                        "mensaje_pili": "❌ PILIProyectos no está disponible",
                        "error": "Módulo pili_proyectos no cargado"
                    }

            # ENRUTAR A PILI INFORMES (técnico y ejecutivo APA)
            elif any(keyword in tipo_flujo.lower() for keyword in ["informe"]):
                if self.informes:
                    logger.info("📄 Enrutando a PILIInformes...")
                    return self.informes.procesar(mensaje, historial, tipo_flujo)
                else:
                    return {
                        "accion": "error",
                        "mensaje_pili": "❌ PILIInformes no está disponible",
                        "error": "Módulo pili_informes no cargado"
                    }

            # FLUJO DESCONOCIDO
            else:
                logger.warning(f"⚠️ Tipo de flujo desconocido: {tipo_flujo}")
                return {
                    "accion": "error",
                    "mensaje_pili": f"No sé cómo procesar el flujo: {tipo_flujo}.\n\n"
                                   "Tipos válidos:\n"
                                   "- cotizacion-simple, cotizacion-compleja\n"
                                   "- proyecto-simple, proyecto-pmi\n"
                                   "- informe-tecnico, informe-ejecutivo",
                    "flujo_solicitado": tipo_flujo
                }

        except Exception as e:
            logger.error(f"❌ Error en orquestador: {e}")
            import traceback
            traceback.print_exc()
            return {
                "accion": "error",
                "mensaje_pili": f"Error procesando tu solicitud: {str(e)}",
                "error": str(e)
            }

    # ═══════════════════════════════════════════════════════════════
    # 🎯 MÉTODOS AUXILIARES - GENERACIÓN COMPLETA
    # ═══════════════════════════════════════════════════════════════

    async def procesar_cotizacion_completa(
        self,
        descripcion: str,
        archivos: Optional[List] = None,
        tipo_salida: str = "word",  # "word" o "pdf"
        cliente: str = "Cliente",
        usar_plantilla: bool = False,
        logo_base64: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        🎯 FLUJO COTIZACIÓN COMPLETA usando tus servicios existentes
        
        1. Procesa archivos (si hay) con TU file_processor
        2. Genera respuesta con TU gemini_service  
        3. Crea documento con TU word_generator o pdf_generator
        """
        
        try:
            resultado = {
                "exito": True,
                "timestamp": datetime.now().isoformat(),
                "tipo_procesamiento": "cotizacion_completa",
                "pasos_realizados": []
            }
            
            # PASO 1: Procesar archivos (si hay)
            contenido_archivos = ""
            if archivos and len(archivos) > 0 and self.servicios['file_processor']:
                logger.info("📄 Procesando archivos con tu FileProcessor...")
                
                for archivo in archivos:
                    try:
                        # Usar TU file_processor existente
                        resultado_archivo = await self.servicios['file_processor'].procesar_archivo(
                            archivo['path'], archivo['nombre']
                        )
                        
                        if resultado_archivo.get('exito'):
                            contenido_archivos += f"\n--- {archivo['nombre']} ---\n"
                            contenido_archivos += resultado_archivo.get('contenido_texto', '')
                            
                    except Exception as e:
                        logger.warning(f"Error procesando archivo: {e}")
                
                resultado["pasos_realizados"].append("procesar_archivos")
            
            # PASO 2: Generar cotización con IA (tu Gemini)
            if self.servicios['gemini']:
                logger.info("🤖 Generando cotización con tu GeminiService...")
                
                try:
                    # Usar TU gemini_service existente
                    prompt_completo = f"""
Descripción del proyecto: {descripcion}

Cliente: {cliente}

Archivos analizados:
{contenido_archivos}

Genera una cotización profesional para instalación eléctrica en Perú.
"""
                    
                    respuesta_ia = await self.servicios['gemini'].generar_cotizacion(
                        descripcion_proyecto=prompt_completo,
                        contexto_documentos=[contenido_archivos] if contenido_archivos else None,
                        historial_chat=[]
                    )
                    
                    resultado["respuesta_ia"] = respuesta_ia
                    resultado["pasos_realizados"].append("generar_ia")
                    
                except Exception as e:
                    logger.error(f"Error con Gemini: {e}")
                    # Fallback a respuesta demo
                    respuesta_ia = self._generar_cotizacion_demo(descripcion, cliente)
                    resultado["respuesta_ia"] = respuesta_ia
                    resultado["modo_demo"] = True
            else:
                # Modo demo
                respuesta_ia = self._generar_cotizacion_demo(descripcion, cliente)
                resultado["respuesta_ia"] = respuesta_ia
                resultado["modo_demo"] = True
            
            # PASO 3: Generar documento final
            if respuesta_ia.get('exito') and respuesta_ia.get('cotizacion'):
                logger.info(f"📄 Generando documento {tipo_salida} con tus generadores...")
                
                datos_cotizacion = respuesta_ia['cotizacion']
                
                if tipo_salida == "pdf" and self.servicios['pdf']:
                    # Usar TU pdf_generator
                    try:
                        documento_resultado = self.servicios['pdf'].generar_cotizacion(
                            datos_cotizacion=datos_cotizacion,
                            opciones={"cliente": cliente},
                            logo_base64=logo_base64
                        )
                        resultado["documento_generado"] = documento_resultado
                        resultado["pasos_realizados"].append("generar_pdf")
                    except Exception as e:
                        logger.error(f"Error generando PDF: {e}")
                        resultado["error_documento"] = str(e)
                        
                elif self.servicios['word']:
                    # Usar TU word_generator (default)
                    try:
                        documento_resultado = self.servicios['word'].generar_cotizacion(
                            datos_cotizacion=datos_cotizacion,
                            opciones={"cliente": cliente},
                            logo_base64=logo_base64
                        )
                        resultado["documento_generado"] = documento_resultado
                        resultado["pasos_realizados"].append("generar_word")
                    except Exception as e:
                        logger.error(f"Error generando Word: {e}")
                        resultado["error_documento"] = str(e)
                
                else:
                    resultado["error_documento"] = f"Generador {tipo_salida} no disponible"
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en procesamiento completo: {e}")
            return {
                "exito": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def procesar_proyecto_completo(
        self,
        descripcion: str,
        cliente: str = "Cliente",
        tipo_salida: str = "word"
    ) -> Dict[str, Any]:
        """
        🎯 FLUJO PROYECTO COMPLETO usando tus servicios existentes
        """
        
        try:
            # Similar al de cotización pero usando métodos de proyecto
            if self.servicios['word'] and hasattr(self.servicios['word'], 'generar_informe_proyecto'):
                
                datos_proyecto = {
                    "cliente": cliente,
                    "descripcion": descripcion,
                    "fecha": datetime.now().strftime("%d/%m/%Y"),
                    "tipo": "Proyecto Eléctrico"
                }
                
                resultado_doc = self.servicios['word'].generar_informe_proyecto(
                    datos_proyecto=datos_proyecto
                )
                
                return {
                    "exito": True,
                    "tipo_procesamiento": "proyecto_completo",
                    "documento_generado": resultado_doc,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "exito": False,
                    "error": "WordGenerator no tiene método generar_informe_proyecto",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "exito": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def chat_inteligente(
        self,
        mensaje: str,
        contexto: Optional[Dict[str, Any]] = None,
        historial: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        🎯 CHAT INTELIGENTE usando tu GeminiService existente
        """
        
        if self.servicios['gemini']:
            try:
                respuesta = await self.servicios['gemini'].chat_conversacional(
                    mensaje=mensaje,
                    historial=historial or [],
                    contexto=contexto
                )
                
                return {
                    "exito": True,
                    "respuesta": respuesta.get('respuesta', ''),
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error en chat: {e}")
                return {
                    "exito": False,
                    "error": str(e),
                    "respuesta": "Error en el chat. Verifica tu configuración de Gemini.",
                    "timestamp": datetime.now().isoformat()
                }
        else:
            # Modo demo
            return {
                "exito": True,
                "respuesta": f"DEMO: Recibí tu mensaje '{mensaje[:50]}...' - Configura GEMINI_API_KEY para chat real.",
                "modo_demo": True,
                "timestamp": datetime.now().isoformat()
            }
    
    def _generar_cotizacion_demo(self, descripcion: str, cliente: str) -> Dict[str, Any]:
        """Genera cotización demo cuando Gemini no está disponible"""
        
        return {
            "exito": True,
            "cotizacion": {
                "cliente": cliente,
                "proyecto": f"Proyecto para {descripcion[:30]}...",
                "numero": f"DEMO-{datetime.now().strftime('%Y%m%d')}-001",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "items": [
                    {
                        "id": 1,
                        "descripcion": f"Instalación eléctrica - {descripcion[:40]}",
                        "cantidad": 1,
                        "precio_unitario": 1500.00,
                        "total": 1500.00
                    }
                ],
                "subtotal": 1500.00,
                "igv": 270.00,
                "total": 1770.00,
                "observaciones": "Cotización DEMO - Configura GEMINI_API_KEY para cotizaciones reales con IA",
                "vigencia": "30 días"
            },
            "modo_demo": True
        }

    # ═══════════════════════════════════════════════════════════════
    # 🎯 MÉTODOS UTILITARIOS
    # ═══════════════════════════════════════════════════════════════
    
    def obtener_estado(self) -> Dict[str, Any]:
        """Obtiene estado de todos los servicios y especialistas PILI"""

        estado = {
            "pili_orchestrator": "✅ ACTIVO",
            "modo_demo": self.modo_demo,
            "especialistas_pili": {},
            "servicios_conectados": {},
            "total_servicios": len(self.servicios)
        }

        # Estado de los 3 especialistas PILI
        estado["especialistas_pili"]["cotizadora"] = "✅ ACTIVO" if self.cotizadora else "❌ NO DISPONIBLE"
        estado["especialistas_pili"]["proyectos"] = "✅ ACTIVO" if self.proyectos else "❌ NO DISPONIBLE"
        estado["especialistas_pili"]["informes"] = "✅ ACTIVO" if self.informes else "❌ NO DISPONIBLE"

        # Estado de servicios auxiliares
        for nombre, servicio in self.servicios.items():
            if servicio is not None:
                estado["servicios_conectados"][nombre] = "✅ CONECTADO"
            else:
                estado["servicios_conectados"][nombre] = "❌ NO DISPONIBLE"

        return estado
    
    def listar_capacidades(self) -> Dict[str, Any]:
        """Lista capacidades de los 3 especialistas PILI y servicios"""

        capacidades = {
            "especialistas_pili": {},
            "flujos_completos": [],
            "generadores_disponibles": [],
            "procesadores_disponibles": []
        }

        # Capacidades de los 3 especialistas PILI
        if self.cotizadora:
            capacidades["especialistas_pili"]["cotizadora"] = {
                "activo": True,
                "servicios": [
                    "Instalaciones Eléctricas (Residencial/Comercial/Industrial)",
                    "Certificados ITSE",
                    "Puestas a Tierra",
                    "Sistemas Contra Incendios",
                    "Domótica",
                    "CCTV",
                    "Redes de Datos",
                    "Automatización",
                    "Saneamiento",
                    "Expedientes Técnicos"
                ],
                "descripcion": "Guía conversacional paso a paso para 10 servicios"
            }

        if self.proyectos:
            capacidades["especialistas_pili"]["proyectos"] = {
                "activo": True,
                "tipos": ["Proyecto Simple (5 pasos)", "Proyecto Complejo PMI (8 pasos + Gantt)"],
                "descripcion": "Creación de proyectos con metodología PMI"
            }

        if self.informes:
            capacidades["especialistas_pili"]["informes"] = {
                "activo": True,
                "tipos": ["Informe Técnico (8 secciones)", "Informe Ejecutivo APA (13 secciones)"],
                "descripcion": "Generación de informes profesionales con formato APA 7"
            }

        # Verificar flujos completos disponibles
        if self.servicios['gemini'] and self.servicios['word']:
            capacidades["flujos_completos"].append("cotizacion_completa_word")

        if self.servicios['gemini'] and self.servicios['pdf']:
            capacidades["flujos_completos"].append("cotizacion_completa_pdf")

        if self.servicios['word']:
            capacidades["generadores_disponibles"].append("word_documents")

        if self.servicios['pdf']:
            capacidades["generadores_disponibles"].append("pdf_documents")

        if self.servicios['file_processor']:
            capacidades["procesadores_disponibles"].append("file_analysis")

        if self.servicios['template']:
            capacidades["procesadores_disponibles"].append("template_processing")

        return capacidades

# ═══════════════════════════════════════════════════════════════
# 🎯 INSTANCIA GLOBAL PARA TU SISTEMA
# ═══════════════════════════════════════════════════════════════

# Crear instancia que se conecta con tus servicios
try:
    pili_orchestrator = PILIOrchestrator()
    logger.info("✅ PILI Orchestrator conectado con tu sistema existente")
except Exception as e:
    logger.error(f"❌ Error conectando PILI Orchestrator: {e}")
    pili_orchestrator = None

def get_pili_orchestrator():
    """Obtiene el orquestrador conectado con tu sistema"""
    global pili_orchestrator
    if pili_orchestrator is None:
        try:
            pili_orchestrator = PILIOrchestrator()
        except Exception as e:
            logger.error(f"Error creando PILIOrchestrator: {e}")
    return pili_orchestrator

# ═══════════════════════════════════════════════════════════════
# 🎯 EJEMPLOS DE USO CON LOS 3 ESPECIALISTAS PILI
# ═══════════════════════════════════════════════════════════════

"""
EJEMPLO 1: USO DEL ORQUESTADOR CON LOS 3 ESPECIALISTAS

from services.pili_orchestrator import get_pili_orchestrator

# Crear instancia del orquestador
orchestrator = get_pili_orchestrator()

# Ver estado de los 3 especialistas
print(orchestrator.obtener_estado())
# Output:
# {
#   "especialistas_pili": {
#     "cotizadora": "✅ ACTIVO",
#     "proyectos": "✅ ACTIVO",
#     "informes": "✅ ACTIVO"
#   },
#   "servicios_conectados": {...}
# }

# Ver capacidades de los especialistas
print(orchestrator.listar_capacidades())

# ═════════════════════════════════════════════════════════

EJEMPLO 2: COTIZACIÓN CON PILI COTIZADORA (10 SERVICIOS)

historial = []

# Usuario inicia conversación
respuesta = orchestrator.procesar(
    mensaje="Necesito cotizar una instalación eléctrica",
    historial=historial,
    tipo_flujo="cotizacion-simple"
)
# → PILICotizadora pregunta: "¿Es residencial, comercial o industrial?"

historial.append({"role": "user", "content": "Necesito cotizar una instalación eléctrica"})
historial.append({"role": "assistant", "content": respuesta["mensaje_pili"]})

# Usuario responde
respuesta = orchestrator.procesar(
    mensaje="Residencial",
    historial=historial,
    tipo_flujo="cotizacion-simple"
)
# → PILICotizadora pregunta: "¿Cuántos m² tiene el área?"

# ... continúa preguntando paso a paso hasta tener todos los datos ...

# Cuando tiene todo:
# respuesta["accion"] == "cotizacion_generada"
# respuesta["puede_generar"] == True
# respuesta["datos_cotizacion"] == {...}  # JSON completo

# ═════════════════════════════════════════════════════════

EJEMPLO 3: PROYECTO CON PILI PROYECTOS (SIMPLE O PMI)

# Proyecto simple (5 pasos)
respuesta = orchestrator.procesar(
    mensaje="Quiero crear un proyecto",
    historial=[],
    tipo_flujo="proyecto-simple"
)
# → PILIProyectos pregunta: "¿Cuál es el nombre del proyecto?"

# Proyecto complejo PMI (8 pasos + Gantt + recursos)
respuesta = orchestrator.procesar(
    mensaje="Proyecto de automatización industrial",
    historial=[],
    tipo_flujo="proyecto-pmi"
)
# → PILIProyectos usa metodología PMI completa

# ═════════════════════════════════════════════════════════

EJEMPLO 4: INFORME CON PILI INFORMES (TÉCNICO O EJECUTIVO APA)

# Informe técnico (8 secciones)
respuesta = orchestrator.procesar(
    mensaje="Necesito un informe técnico",
    historial=[],
    tipo_flujo="informe-tecnico"
)
# → PILIInformes pregunta por introducción, objetivos, metodología, etc.

# Informe ejecutivo APA (13 secciones con análisis financiero)
respuesta = orchestrator.procesar(
    mensaje="Informe ejecutivo para la gerencia",
    historial=[],
    tipo_flujo="informe-ejecutivo"
)
# → PILIInformes usa formato APA 7 con análisis ROI, TIR, Payback

# ═════════════════════════════════════════════════════════

EJEMPLO 5: MÉTODOS AUXILIARES (GENERACIÓN COMPLETA)

# Generar cotización completa con IA + documento Word
resultado = await orchestrator.procesar_cotizacion_completa(
    descripcion="Instalación casa 120m²",
    cliente="Juan Pérez",
    tipo_salida="word"
)

# Chat inteligente
chat = await orchestrator.chat_inteligente(
    mensaje="¿Cuánto cuesta instalar 10 puntos de luz?"
)
"""