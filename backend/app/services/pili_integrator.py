"""
PILI INTEGRATOR - SERVICIO DE INTEGRACION COMPLETO
RUTA: backend/app/services/pili_integrator.py

Este servicio es el PUENTE CRITICO que conecta todos los componentes de PILI:
- PILIBrain (generacion de JSON)
- WordGenerator (generacion de Word)
- PDFGenerator (generacion de PDF)
- Plantillas Modelo (fallback offline)
- GeminiService (IA externa opcional)

FLUJO COMPLETO:
Usuario -> Chat -> PILIBrain/Gemini -> JSON -> Generador -> Documento

MODOS DE OPERACION:
1. ONLINE: Usa Gemini para respuestas conversacionales + PILIBrain para JSON
2. OFFLINE: Usa PILIBrain puro para todo
3. FALLBACK: Usa plantillas modelo predefinidas

VERSION: 3.0 PRODUCTION READY
"""

import logging
import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Imports de servicios existentes
try:
    from app.services.pili_brain import PILIBrain, pili_brain
    from app.services.word_generator import word_generator
    from app.services.pdf_generator import pdf_generator
    from app.templates.documentos.plantillas_modelo import obtener_plantilla
    from app.core.config import settings, validate_gemini_key
    SERVICIOS_DISPONIBLES = True
except ImportError as e:
    logging.warning(f"Error importando servicios: {e}")
    SERVICIOS_DISPONIBLES = False

# Import condicional de Gemini
try:
    from app.services.gemini_service import gemini_service
    GEMINI_DISPONIBLE = True
except ImportError:
    GEMINI_DISPONIBLE = False
    gemini_service = None

logger = logging.getLogger(__name__)


class PILIIntegrator:
    """
    Servicio integrador que conecta todos los componentes de PILI
    para produccion.

    Este es el CEREBRO CENTRAL que:
    1. Recibe solicitudes del usuario
    2. Decide que servicio usar (Gemini/PILIBrain/Plantillas)
    3. Genera el JSON estructurado
    4. Crea el documento final (Word/PDF)
    5. Retorna el resultado completo
    """

    def __init__(self):
        """Inicializa el integrador con todos los servicios"""
        self.pili_brain = pili_brain if SERVICIOS_DISPONIBLES else None
        self.word_generator = word_generator if SERVICIOS_DISPONIBLES else None
        self.pdf_generator = pdf_generator if SERVICIOS_DISPONIBLES else None
        self.gemini_service = gemini_service if GEMINI_DISPONIBLE else None

        # Estado de servicios
        self.estado_servicios = {
            "pili_brain": self.pili_brain is not None,
            "word_generator": self.word_generator is not None,
            "pdf_generator": self.pdf_generator is not None,
            "gemini": GEMINI_DISPONIBLE and validate_gemini_key(),
            "plantillas": SERVICIOS_DISPONIBLES
        }

        logger.info("=" * 60)
        logger.info("PILI INTEGRATOR INICIADO")
        logger.info("=" * 60)
        for servicio, estado in self.estado_servicios.items():
            status = "ACTIVO" if estado else "NO DISPONIBLE"
            logger.info(f"  {servicio}: {status}")
        logger.info("=" * 60)

    # ==================================================================
    # METODO PRINCIPAL: PROCESAR SOLICITUD COMPLETA
    # ==================================================================

    async def procesar_solicitud_completa(
        self,
        mensaje: str,
        tipo_flujo: str,
        historial: List[Dict] = None,
        generar_documento: bool = False,
        formato_salida: str = "word",
        logo_base64: Optional[str] = None,
        opciones: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Procesa una solicitud completa del usuario.

        Este es el METODO PRINCIPAL que maneja todo el flujo:
        1. Analiza el mensaje y tipo de flujo
        2. Genera respuesta conversacional
        3. Detecta servicio y extrae datos
        4. Genera JSON estructurado
        5. Opcionalmente crea documento

        Args:
            mensaje: Mensaje del usuario
            tipo_flujo: cotizacion-simple, proyecto-complejo, etc.
            historial: Historial de conversacion
            generar_documento: Si debe generar archivo
            formato_salida: "word" o "pdf"
            logo_base64: Logo en base64
            opciones: Opciones adicionales

        Returns:
            Dict con respuesta, JSON, y opcionalmente ruta de documento
        """
        try:
            logger.info(f"Procesando solicitud: {tipo_flujo}")
            historial = historial or []

            # Resultado base
            resultado = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "tipo_flujo": tipo_flujo,
                "modo": self._determinar_modo_operacion()
            }

            # Paso 1: Detectar tipo de documento y complejidad
            tipo_documento, complejidad = self._parsear_tipo_flujo(tipo_flujo)
            resultado["tipo_documento"] = tipo_documento
            resultado["complejidad"] = complejidad

            # Paso 2: Detectar servicio del mensaje
            servicio = self.pili_brain.detectar_servicio(mensaje) if self.pili_brain else "electrico-residencial"
            resultado["servicio_detectado"] = servicio

            # Paso 3: Generar respuesta conversacional
            respuesta_chat = await self._generar_respuesta_chat(
                mensaje, tipo_flujo, historial, servicio
            )
            resultado["respuesta"] = respuesta_chat["texto"]
            resultado["agente_pili"] = respuesta_chat["agente"]

            # Paso 4: Generar JSON estructurado
            json_estructurado = self._generar_json_estructurado(
                mensaje, servicio, tipo_documento, complejidad
            )
            resultado["datos_generados"] = json_estructurado

            # Paso 5: Generar vista previa HTML
            html_preview = self._generar_html_preview(json_estructurado, tipo_documento)
            resultado["html_preview"] = html_preview

            # Paso 6: Generar documento si se solicita
            if generar_documento:
                ruta_documento = await self._generar_documento_final(
                    json_estructurado,
                    tipo_documento,
                    complejidad,
                    formato_salida,
                    logo_base64,
                    opciones
                )
                resultado["documento_generado"] = ruta_documento
                resultado["nombre_archivo"] = os.path.basename(ruta_documento) if ruta_documento else None

            # Paso 7: Determinar botones contextuales
            resultado["botones_sugeridos"] = self._obtener_botones_contextuales(
                tipo_flujo, len(historial), generar_documento
            )

            logger.info(f"Solicitud procesada exitosamente: {tipo_flujo}")
            return resultado

        except Exception as e:
            logger.error(f"Error procesando solicitud: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # ==================================================================
    # METODOS DE GENERACION DE DOCUMENTOS
    # ==================================================================

    async def generar_cotizacion(
        self,
        mensaje: str,
        servicio: str = None,
        complejidad: str = "simple",
        formato: str = "word",
        logo_base64: str = None,
        opciones: Dict = None
    ) -> Dict[str, Any]:
        """
        Genera una cotizacion completa.

        Returns:
            Dict con datos JSON y ruta del documento
        """
        try:
            # Detectar servicio si no se proporciona
            if not servicio:
                servicio = self.pili_brain.detectar_servicio(mensaje) if self.pili_brain else "electrico-residencial"

            # Generar JSON
            if self.pili_brain:
                json_data = self.pili_brain.generar_cotizacion(mensaje, servicio, complejidad)
            else:
                json_data = obtener_plantilla("cotizacion", complejidad, servicio)

            # Generar documento
            ruta = await self._generar_documento_final(
                json_data.get("datos", json_data.get("datos_extraidos", {})),
                "cotizacion",
                complejidad,
                formato,
                logo_base64,
                opciones
            )

            return {
                "success": True,
                "datos": json_data,
                "documento": ruta,
                "servicio": servicio,
                "complejidad": complejidad
            }

        except Exception as e:
            logger.error(f"Error generando cotizacion: {e}")
            return {"success": False, "error": str(e)}

    async def generar_proyecto(
        self,
        mensaje: str,
        servicio: str = None,
        complejidad: str = "simple",
        formato: str = "word",
        logo_base64: str = None,
        opciones: Dict = None
    ) -> Dict[str, Any]:
        """
        Genera un proyecto completo.
        """
        try:
            if not servicio:
                servicio = self.pili_brain.detectar_servicio(mensaje) if self.pili_brain else "electrico-residencial"

            # Generar JSON
            if self.pili_brain:
                json_data = self.pili_brain.generar_proyecto(mensaje, servicio, complejidad)
            else:
                json_data = obtener_plantilla("proyecto", complejidad, servicio)

            # Generar documento
            ruta = await self._generar_documento_final(
                json_data.get("datos", json_data.get("datos_extraidos", {})),
                "proyecto",
                complejidad,
                formato,
                logo_base64,
                opciones
            )

            return {
                "success": True,
                "datos": json_data,
                "documento": ruta,
                "servicio": servicio,
                "complejidad": complejidad
            }

        except Exception as e:
            logger.error(f"Error generando proyecto: {e}")
            return {"success": False, "error": str(e)}

    async def generar_informe(
        self,
        mensaje: str,
        servicio: str = None,
        complejidad: str = "simple",
        formato: str = "word",
        logo_base64: str = None,
        opciones: Dict = None
    ) -> Dict[str, Any]:
        """
        Genera un informe completo.
        """
        try:
            if not servicio:
                servicio = self.pili_brain.detectar_servicio(mensaje) if self.pili_brain else "electrico-residencial"

            # Generar JSON
            if self.pili_brain:
                json_data = self.pili_brain.generar_informe(mensaje, servicio, complejidad)
            else:
                json_data = obtener_plantilla("informe", complejidad, servicio)

            # Generar documento
            ruta = await self._generar_documento_final(
                json_data.get("datos", json_data.get("datos_extraidos", {})),
                "informe",
                complejidad,
                formato,
                logo_base64,
                opciones
            )

            return {
                "success": True,
                "datos": json_data,
                "documento": ruta,
                "servicio": servicio,
                "complejidad": complejidad
            }

        except Exception as e:
            logger.error(f"Error generando informe: {e}")
            return {"success": False, "error": str(e)}

    # ==================================================================
    # METODOS INTERNOS
    # ==================================================================

    def _determinar_modo_operacion(self) -> str:
        """Determina el modo de operacion actual"""
        if self.estado_servicios["gemini"]:
            return "ONLINE_COMPLETO"
        elif self.estado_servicios["pili_brain"]:
            return "OFFLINE_PILI"
        elif self.estado_servicios["plantillas"]:
            return "FALLBACK_PLANTILLAS"
        else:
            return "ERROR_SIN_SERVICIOS"

    def _parsear_tipo_flujo(self, tipo_flujo: str) -> Tuple[str, str]:
        """Parsea el tipo de flujo en tipo_documento y complejidad"""
        tipo_flujo_lower = tipo_flujo.lower()

        if "cotizacion" in tipo_flujo_lower:
            tipo_documento = "cotizacion"
        elif "proyecto" in tipo_flujo_lower:
            tipo_documento = "proyecto"
        elif "informe" in tipo_flujo_lower:
            tipo_documento = "informe"
        else:
            tipo_documento = "cotizacion"

        if "complej" in tipo_flujo_lower or "ejecutiv" in tipo_flujo_lower or "pmi" in tipo_flujo_lower:
            complejidad = "complejo"
        else:
            complejidad = "simple"

        return tipo_documento, complejidad

    async def _generar_respuesta_chat(
        self,
        mensaje: str,
        tipo_flujo: str,
        historial: List[Dict],
        servicio: str
    ) -> Dict[str, str]:
        """Genera respuesta conversacional"""

        # Determinar agente PILI
        agentes = {
            "cotizacion-simple": "PILI Cotizadora",
            "cotizacion-compleja": "PILI Analista",
            "proyecto-simple": "PILI Coordinadora",
            "proyecto-complejo": "PILI Project Manager",
            "informe-simple": "PILI Reportera",
            "informe-ejecutivo": "PILI Analista Senior"
        }
        agente = agentes.get(tipo_flujo, "PILI Asistente")

        # Intentar usar Gemini para respuesta conversacional
        if self.estado_servicios["gemini"] and self.gemini_service:
            try:
                respuesta_gemini = await self.gemini_service.chat_conversacional(
                    mensaje=mensaje,
                    historial=historial,
                    contexto=f"Tipo de servicio: {servicio}, Flujo: {tipo_flujo}"
                )
                if respuesta_gemini.get("success"):
                    return {
                        "texto": respuesta_gemini.get("respuesta", ""),
                        "agente": agente
                    }
            except Exception as e:
                logger.warning(f"Error en Gemini, usando fallback: {e}")

        # Fallback: generar respuesta con PILI Brain
        return self._generar_respuesta_pili_local(mensaje, servicio, agente)

    def _generar_respuesta_pili_local(
        self,
        mensaje: str,
        servicio: str,
        agente: str
    ) -> Dict[str, str]:
        """Genera respuesta local cuando Gemini no esta disponible"""

        # Extraer datos del mensaje
        datos = self.pili_brain.extraer_datos(mensaje, servicio) if self.pili_brain else {}
        info_servicio = self.pili_brain.servicios.get(servicio, {}) if self.pili_brain else {}

        # Construir respuesta
        respuesta = f"He analizado tu solicitud para **{info_servicio.get('nombre', 'servicio electrico')}**.\n\n"

        if datos.get("area_m2"):
            respuesta += f"- Area detectada: {datos['area_m2']} m2\n"
        if datos.get("num_pisos", 1) > 1:
            respuesta += f"- Pisos: {datos['num_pisos']}\n"
        if datos.get("cantidad_puntos"):
            respuesta += f"- Puntos: {datos['cantidad_puntos']}\n"

        respuesta += f"\nHe preparado los calculos segun **{info_servicio.get('normativa', 'normativa vigente')}**.\n"
        respuesta += "\nPuedes revisar la vista previa y editar los items si necesitas ajustes."

        return {
            "texto": respuesta,
            "agente": agente
        }

    def _generar_json_estructurado(
        self,
        mensaje: str,
        servicio: str,
        tipo_documento: str,
        complejidad: str
    ) -> Dict[str, Any]:
        """Genera JSON estructurado para el documento"""

        # Intentar con PILIBrain
        if self.pili_brain:
            if tipo_documento == "cotizacion":
                return self.pili_brain.generar_cotizacion(mensaje, servicio, complejidad).get("datos", {})
            elif tipo_documento == "proyecto":
                return self.pili_brain.generar_proyecto(mensaje, servicio, complejidad).get("datos", {})
            elif tipo_documento == "informe":
                return self.pili_brain.generar_informe(mensaje, servicio, complejidad).get("datos", {})

        # Fallback a plantillas
        plantilla = obtener_plantilla(tipo_documento, complejidad, servicio)
        return plantilla.get("datos_extraidos", {})

    async def _generar_documento_final(
        self,
        datos: Dict[str, Any],
        tipo_documento: str,
        complejidad: str,
        formato: str,
        logo_base64: str,
        opciones: Dict
    ) -> Optional[str]:
        """Genera el documento final (Word o PDF)"""

        try:
            # Configurar opciones por defecto
            opciones = opciones or {}
            opciones["complejidad"] = complejidad

            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_base = f"{tipo_documento}_{complejidad}_{timestamp}"

            if formato.lower() == "pdf":
                if self.pdf_generator:
                    ruta = os.path.join(
                        str(settings.GENERATED_DIR),
                        f"{nombre_base}.pdf"
                    )
                    self.pdf_generator.generar_cotizacion(
                        datos=datos,
                        ruta_salida=ruta,
                        opciones=opciones,
                        logo_base64=logo_base64
                    )
                    return ruta
            else:
                if self.word_generator:
                    ruta = self.word_generator.generar_desde_json_pili(
                        datos_json=datos,
                        tipo_documento=tipo_documento,
                        opciones=opciones
                    )
                    return ruta

            return None

        except Exception as e:
            logger.error(f"Error generando documento: {e}")
            return None

    def _generar_html_preview(self, datos: Dict[str, Any], tipo_documento: str) -> str:
        """Genera vista previa HTML del documento"""

        if tipo_documento == "cotizacion":
            return self._html_preview_cotizacion(datos)
        elif tipo_documento == "proyecto":
            return self._html_preview_proyecto(datos)
        elif tipo_documento == "informe":
            return self._html_preview_informe(datos)
        else:
            return "<div>Vista previa no disponible</div>"

    def _html_preview_cotizacion(self, datos: Dict) -> str:
        """HTML preview para cotizacion"""
        items = datos.get("items", [])
        items_html = ""
        subtotal = 0

        for item in items:
            total_item = item.get("total", item.get("cantidad", 0) * item.get("precio_unitario", 0))
            subtotal += total_item
            items_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{item.get('descripcion', '')}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{item.get('cantidad', 0)}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">${item.get('precio_unitario', 0):.2f}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">${total_item:.2f}</td>
            </tr>
            """

        igv = datos.get("igv", subtotal * 0.18)
        total = datos.get("total", subtotal + igv)

        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #c41e3a; margin: 0;">TESLA ELECTRICIDAD</h2>
                <p style="color: #666; margin: 5px 0;">Automatizacion y Servicios Electricos</p>
            </div>

            <h3 style="color: #333;">COTIZACION: {datos.get('numero', 'COT-XXXXX')}</h3>

            <table style="width: 100%; margin-bottom: 15px;">
                <tr>
                    <td><strong>Cliente:</strong> {datos.get('cliente', 'N/A')}</td>
                    <td><strong>Fecha:</strong> {datos.get('fecha', 'N/A')}</td>
                </tr>
                <tr>
                    <td colspan="2"><strong>Proyecto:</strong> {datos.get('proyecto', 'N/A')}</td>
                </tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <thead>
                    <tr style="background: #c41e3a; color: white;">
                        <th style="padding: 10px; border: 1px solid #ddd;">Descripcion</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Cant.</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">P. Unit.</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>

            <div style="text-align: right;">
                <p><strong>Subtotal:</strong> ${subtotal:.2f}</p>
                <p><strong>IGV (18%):</strong> ${igv:.2f}</p>
                <p style="font-size: 1.2em; color: #c41e3a;"><strong>TOTAL: ${total:.2f}</strong></p>
            </div>

            <div style="margin-top: 20px; padding: 10px; background: #f5f5f5; font-size: 0.9em;">
                <strong>Vigencia:</strong> {datos.get('vigencia', '30 dias')}
            </div>
        </div>
        """

    def _html_preview_proyecto(self, datos: Dict) -> str:
        """HTML preview para proyecto"""
        fases = datos.get("fases", [])
        fases_html = ""

        for fase in fases:
            fases_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{fase.get('nombre', '')}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{fase.get('duracion_dias', 0)} dias</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{fase.get('entregable', '')}</td>
            </tr>
            """

        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #c41e3a;">PROYECTO: {datos.get('nombre', 'N/A')}</h2>

            <table style="width: 100%; margin-bottom: 15px;">
                <tr>
                    <td><strong>Codigo:</strong> {datos.get('codigo', 'N/A')}</td>
                    <td><strong>Cliente:</strong> {datos.get('cliente', 'N/A')}</td>
                </tr>
                <tr>
                    <td><strong>Inicio:</strong> {datos.get('fecha_inicio', 'N/A')}</td>
                    <td><strong>Fin:</strong> {datos.get('fecha_fin', 'N/A')}</td>
                </tr>
                <tr>
                    <td><strong>Duracion:</strong> {datos.get('duracion_total_dias', 0)} dias</td>
                    <td><strong>Presupuesto:</strong> ${datos.get('presupuesto_estimado', 0):,.2f}</td>
                </tr>
            </table>

            <h4>FASES DEL PROYECTO</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #333; color: white;">
                        <th style="padding: 10px;">Fase</th>
                        <th style="padding: 10px;">Duracion</th>
                        <th style="padding: 10px;">Entregable</th>
                    </tr>
                </thead>
                <tbody>
                    {fases_html}
                </tbody>
            </table>
        </div>
        """

    def _html_preview_informe(self, datos: Dict) -> str:
        """HTML preview para informe"""
        secciones = datos.get("secciones", [])
        secciones_html = ""

        for seccion in secciones:
            secciones_html += f"""
            <div style="margin-bottom: 15px;">
                <h4 style="color: #333; margin-bottom: 5px;">{seccion.get('titulo', '')}</h4>
                <p style="color: #666; font-size: 0.9em;">{seccion.get('contenido', '')[:200]}...</p>
            </div>
            """

        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #c41e3a;">{datos.get('titulo', 'INFORME')}</h2>

            <table style="width: 100%; margin-bottom: 15px;">
                <tr>
                    <td><strong>Codigo:</strong> {datos.get('codigo', 'N/A')}</td>
                    <td><strong>Fecha:</strong> {datos.get('fecha', 'N/A')}</td>
                </tr>
                <tr>
                    <td><strong>Cliente:</strong> {datos.get('cliente', 'N/A')}</td>
                    <td><strong>Formato:</strong> {datos.get('formato', 'Tecnico')}</td>
                </tr>
            </table>

            <h4>CONTENIDO</h4>
            {secciones_html}
        </div>
        """

    def _obtener_botones_contextuales(
        self,
        tipo_flujo: str,
        num_mensajes: int,
        documento_generado: bool
    ) -> List[str]:
        """Obtiene botones contextuales segun el estado"""

        if documento_generado:
            return [
                "Editar datos",
                "Regenerar documento",
                "Descargar Word",
                "Descargar PDF",
                "Enviar por email",
                "Nueva solicitud"
            ]
        elif num_mensajes >= 3:
            return [
                "Generar documento",
                "Ajustar items",
                "Modificar cantidades",
                "Revisar precios",
                "Agregar observaciones"
            ]
        else:
            if "cotizacion" in tipo_flujo:
                return [
                    "Residencial",
                    "Comercial",
                    "Industrial",
                    "Contraincendios",
                    "Domotica",
                    "CCTV/Redes"
                ]
            elif "proyecto" in tipo_flujo:
                return [
                    "Definir alcance",
                    "Establecer cronograma",
                    "Asignar recursos",
                    "Estimar presupuesto"
                ]
            else:
                return [
                    "Informe tecnico",
                    "Informe ejecutivo",
                    "Analisis de datos",
                    "Resumen de proyecto"
                ]

    # ==================================================================
    # METODOS DE UTILIDAD
    # ==================================================================

    def obtener_estado(self) -> Dict[str, Any]:
        """Retorna el estado actual del integrador"""
        return {
            "version": "3.0",
            "modo": self._determinar_modo_operacion(),
            "servicios": self.estado_servicios,
            "timestamp": datetime.now().isoformat()
        }

    def listar_servicios_disponibles(self) -> List[str]:
        """Lista los servicios PILI disponibles"""
        if self.pili_brain:
            return list(self.pili_brain.servicios.keys())
        return [
            "electrico-residencial",
            "electrico-comercial",
            "electrico-industrial",
            "contraincendios",
            "domotica",
            "expedientes",
            "saneamiento",
            "itse",
            "pozo-tierra",
            "redes-cctv"
        ]

    def listar_tipos_documento(self) -> List[Dict[str, str]]:
        """Lista los tipos de documento disponibles"""
        return [
            {"tipo": "cotizacion", "complejidad": "simple", "nombre": "Cotizacion Simple"},
            {"tipo": "cotizacion", "complejidad": "complejo", "nombre": "Cotizacion Compleja"},
            {"tipo": "proyecto", "complejidad": "simple", "nombre": "Proyecto Simple"},
            {"tipo": "proyecto", "complejidad": "complejo", "nombre": "Proyecto PMI"},
            {"tipo": "informe", "complejidad": "simple", "nombre": "Informe Tecnico"},
            {"tipo": "informe", "complejidad": "complejo", "nombre": "Informe Ejecutivo"}
        ]


# ==================================================================
# INSTANCIA GLOBAL
# ==================================================================

pili_integrator = PILIIntegrator()

def get_pili_integrator() -> PILIIntegrator:
    """Obtiene la instancia del integrador"""
    return pili_integrator


# ==================================================================
# FUNCIONES DE CONVENIENCIA
# ==================================================================

async def procesar_mensaje_chat(
    mensaje: str,
    tipo_flujo: str = "cotizacion-simple",
    historial: List[Dict] = None
) -> Dict[str, Any]:
    """Funcion de conveniencia para procesar mensaje de chat"""
    return await pili_integrator.procesar_solicitud_completa(
        mensaje=mensaje,
        tipo_flujo=tipo_flujo,
        historial=historial,
        generar_documento=False
    )


async def generar_documento_rapido(
    mensaje: str,
    tipo_documento: str = "cotizacion",
    complejidad: str = "simple",
    formato: str = "word"
) -> Dict[str, Any]:
    """Funcion de conveniencia para generar documento rapidamente"""
    if tipo_documento == "cotizacion":
        return await pili_integrator.generar_cotizacion(mensaje, None, complejidad, formato)
    elif tipo_documento == "proyecto":
        return await pili_integrator.generar_proyecto(mensaje, None, complejidad, formato)
    else:
        return await pili_integrator.generar_informe(mensaje, None, complejidad, formato)


logger.info("PILI Integrator cargado y listo para produccion")
