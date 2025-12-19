"""
🎯 PILI COTIZADORA - Especialista en Cotizaciones Inteligentes
📁 RUTA: backend/app/services/pili_cotizadora.py

PILI Cotizadora es el agente especializado en generar cotizaciones profesionales
para los 10 servicios de Tesla Electricidad con conversación guiada paso a paso.

🔧 SERVICIOS MANEJADOS (10):
1. ⚡ Instalaciones Eléctricas (Residencial/Comercial/Industrial)
2. 📋 Certificados ITSE
3. 🔌 Puestas a Tierra (Pozos SPT)
4. 🔥 Sistemas Contra Incendios
5. 🏠 Domótica y Automatización
6. 📹 CCTV
7. 🌐 Redes de Datos
8. ⚙️ Automatización Industrial
9. 🚰 Saneamiento (Agua y Desagüe)
10. 📄 Expedientes Técnicos

🎯 CAPACIDADES:
- ✅ Conversación guiada paso a paso
- ✅ Preguntas específicas por servicio
- ✅ Validación de respuestas
- ✅ Cálculos automáticos según normativas
- ✅ Detección automática de servicio
- ✅ Generación de JSON estructurado
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Importar el cerebro base para reutilizar lógica
from app.services.pili_brain import PILIBrain, SERVICIOS_PILI

logger = logging.getLogger(__name__)


class PILICotizadora:
    """
    🎯 Especialista PILI en Cotizaciones

    Guía al usuario conversacionalmente para obtener toda la información
    necesaria y generar cotizaciones profesionales para 10 servicios.
    """

    def __init__(self):
        """Inicializa PILI Cotizadora"""
        self.brain = PILIBrain()
        self.servicios = SERVICIOS_PILI
        logger.info("🎯 PILI Cotizadora inicializada - 10 servicios activos")

    def procesar(self, mensaje: str, historial: List[Dict]) -> Dict[str, Any]:
        """
        Procesa mensaje del usuario y guía la cotización

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación

        Returns:
            Respuesta con pregunta siguiente o cotización generada
        """
        # 1. DETECTAR SERVICIO
        servicio = self._detectar_servicio_contexto(mensaje, historial)

        if not servicio:
            # Preguntar qué servicio necesita
            return self._preguntar_servicio()

        # 2. EXTRAER DATOS DEL HISTORIAL
        datos_recopilados = self._extraer_datos_historial(historial, mensaje)
        datos_recopilados["servicio"] = servicio

        # 3. VERIFICAR QUÉ DATOS FALTAN Y HACER PREGUNTAS
        pregunta = self._siguiente_pregunta(servicio, datos_recopilados)

        if pregunta:
            # AÚN FALTAN DATOS
            return pregunta

        # 4. YA TENEMOS TODO - GENERAR COTIZACIÓN
        return self._generar_cotizacion_final(servicio, datos_recopilados)

    def _detectar_servicio_contexto(self, mensaje: str, historial: List[Dict]) -> Optional[str]:
        """Detecta servicio usando mensaje actual e historial"""

        # Primero intentar detectar del mensaje actual
        servicio = self.brain.detectar_servicio(mensaje)

        # Si ya hay servicio en el historial, mantenerlo
        for msg in reversed(historial):
            contenido = msg.get("content", "").lower()

            # Buscar si ya eligió un servicio
            if "eléctric" in contenido or "electrico" in contenido or "instalacion" in contenido:
                if "residencial" in contenido or "casa" in contenido or "vivienda" in contenido:
                    return "electrico-residencial"
                elif "comercial" in contenido or "tienda" in contenido or "oficina" in contenido:
                    return "electrico-comercial"
                elif "industrial" in contenido or "fábrica" in contenido or "planta" in contenido:
                    return "electrico-industrial"

            if "itse" in contenido or "certificación" in contenido or "certificado" in contenido:
                return "itse"

            if "pozo" in contenido or "tierra" in contenido or "puesta" in contenido:
                return "pozo-tierra"

            if "contraincendio" in contenido or "incendio" in contenido or "sprinkler" in contenido:
                return "contraincendios"

            if "domótica" in contenido or "domotica" in contenido or "smart" in contenido:
                return "domotica"

            if "cctv" in contenido or "cámara" in contenido or "vigilancia" in contenido:
                return "redes-cctv"

            if "red" in contenido and ("datos" in contenido or "ethernet" in contenido):
                return "redes-cctv"

            if "saneamiento" in contenido or "agua" in contenido or "desagüe" in contenido:
                return "saneamiento"

            if "expediente" in contenido or "licencia" in contenido or "trámite" in contenido:
                return "expedientes"

        return servicio if servicio else None

    def _preguntar_servicio(self) -> Dict[str, Any]:
        """Pregunta qué servicio necesita cotizar"""
        return {
            "accion": "solicitar_info",
            "mensaje_pili": "¡Hola! Soy **PILI Cotizadora**, especialista en cotizaciones eléctricas. ⚡\n\n¿Qué servicio necesitas cotizar?",
            "botones": [
                "⚡ Instalación Eléctrica",
                "📋 Certificado ITSE",
                "🔌 Pozo a Tierra",
                "🔥 Contra Incendios",
                "🏠 Domótica",
                "📹 CCTV",
                "🌐 Redes de Datos",
                "⚙️ Automatización",
                "🚰 Saneamiento",
                "📄 Expediente Técnico"
            ],
            "campo_esperado": "servicio",
            "puede_generar": False
        }

    def _extraer_datos_historial(self, historial: List[Dict], mensaje_actual: str) -> Dict[str, Any]:
        """Extrae todos los datos ya recopilados del historial"""
        datos = {}

        # Combinar historial + mensaje actual
        todos_mensajes = " ".join([msg.get("content", "") for msg in historial]) + " " + mensaje_actual

        # Extraer con regex los datos clave
        datos["cliente"] = self._extraer_cliente(todos_mensajes)
        datos["area_m2"] = self._extraer_numero(todos_mensajes, ["metros", "m2", "m²", "área"])
        datos["puntos_luz"] = self._extraer_numero(todos_mensajes, ["puntos de luz", "luces", "luminarias"])
        datos["tomacorrientes"] = self._extraer_numero(todos_mensajes, ["tomacorrientes", "tomas", "enchufes"])
        datos["pisos"] = self._extraer_numero(todos_mensajes, ["pisos", "niveles", "plantas"])
        datos["tipo_instalacion"] = self._extraer_tipo(todos_mensajes)
        datos["descripcion"] = self._extraer_descripcion(todos_mensajes)

        return datos

    def _extraer_numero(self, texto: str, keywords: List[str]) -> Optional[float]:
        """Extrae un número asociado a palabras clave"""
        for keyword in keywords:
            # Buscar patrón: número + keyword o keyword + número
            patron1 = rf'(\d+(?:\.\d+)?)\s*{keyword}'
            patron2 = rf'{keyword}\s*(\d+(?:\.\d+)?)'

            match = re.search(patron1, texto, re.IGNORECASE)
            if not match:
                match = re.search(patron2, texto, re.IGNORECASE)

            if match:
                return float(match.group(1))

        return None

    def _extraer_cliente(self, texto: str) -> Optional[str]:
        """Extrae nombre del cliente"""
        # Buscar patrón: "cliente: X" o "para X"
        patron = r'(?:cliente|para|de)\s+([A-ZÁÉÍÓÚ][a-záéíóúñ\s]+(?:[A-ZÁÉÍÓÚ][a-záéíóúñ\s]+)*)'
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _extraer_tipo(self, texto: str) -> Optional[str]:
        """Extrae tipo de instalación"""
        texto_lower = texto.lower()
        if any(word in texto_lower for word in ["residencial", "casa", "vivienda", "departamento"]):
            return "residencial"
        elif any(word in texto_lower for word in ["comercial", "tienda", "local", "oficina"]):
            return "comercial"
        elif any(word in texto_lower for word in ["industrial", "fábrica", "planta"]):
            return "industrial"
        return None

    def _extraer_descripcion(self, texto: str) -> str:
        """Extrae descripción general del proyecto"""
        # Tomar las primeras 200 caracteres que no sean preguntas
        lineas = [l for l in texto.split(".") if "?" not in l and len(l) > 20]
        return lineas[0][:200] if lineas else "Proyecto eléctrico"

    def _siguiente_pregunta(self, servicio: str, datos: Dict) -> Optional[Dict]:
        """
        Determina cuál es la siguiente pregunta a hacer según el servicio

        Returns:
            None si ya tiene todos los datos, o dict con la pregunta
        """

        # SERVICIO: INSTALACIONES ELÉCTRICAS
        if servicio.startswith("electrico"):

            if not datos.get("tipo_instalacion"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📊 ¿Es instalación **residencial**, **comercial** o **industrial**?",
                    "botones": ["🏠 Residencial", "🏢 Comercial", "🏭 Industrial"],
                    "campo_esperado": "tipo_instalacion",
                    "puede_generar": False
                }

            if not datos.get("area_m2"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": f"📐 ¿Cuántos **metros cuadrados (m²)** tiene el área a instalar?\n\n_Ejemplo: 150 m² o 150 metros_",
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            if not datos.get("puntos_luz"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "💡 ¿Cuántos **puntos de luz** necesitas?\n\n_Ejemplo: 20 puntos de luz_",
                    "campo_esperado": "puntos_luz",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            if not datos.get("tomacorrientes"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "🔌 ¿Cuántos **tomacorrientes** necesitas?\n\n_Ejemplo: 15 tomacorrientes_",
                    "campo_esperado": "tomacorrientes",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            # Ya tenemos todo
            return None

        # SERVICIO: ITSE
        elif servicio == "itse":

            if not datos.get("tipo_local"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "🏢 ¿Qué tipo de local es?\n\n_Ejemplo: Restaurante, Consultorio, Tienda, Oficina_",
                    "campo_esperado": "tipo_local",
                    "puede_generar": False
                }

            if not datos.get("area_m2"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📐 ¿Cuántos **metros cuadrados (m²)** tiene el local?\n\n_Ejemplo: 80 m²_",
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            return None

        # SERVICIO: POZO A TIERRA
        elif servicio == "pozo-tierra":

            if not datos.get("tipo_instalacion"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "⚡ ¿Es para instalación **residencial**, **comercial** o **industrial**?",
                    "botones": ["🏠 Residencial", "🏢 Comercial", "🏭 Industrial"],
                    "campo_esperado": "tipo_instalacion",
                    "puede_generar": False
                }

            if not datos.get("potencia_instalada"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "⚡ ¿Cuál es la **potencia instalada** aproximada?\n\n_Ejemplo: 10 kW, 50 kW, 200 kW_",
                    "campo_esperado": "potencia_instalada",
                    "puede_generar": False
                }

            return None

        # SERVICIO: CONTRA INCENDIOS
        elif servicio == "contraincendios":

            if not datos.get("area_m2"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📐 ¿Cuántos **metros cuadrados (m²)** tiene el área a proteger?",
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            if not datos.get("riesgo"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "🔥 ¿Cuál es el **nivel de riesgo**?",
                    "botones": ["Riesgo Leve", "Riesgo Ordinario", "Riesgo Alto"],
                    "campo_esperado": "riesgo",
                    "puede_generar": False
                }

            return None

        # SERVICIOS SIMPLES (CCTV, Redes, Domótica, Saneamiento, Expedientes)
        else:

            if not datos.get("area_m2") and servicio in ["domotica", "redes-cctv", "saneamiento"]:
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📐 ¿Cuántos **metros cuadrados (m²)** tiene el área?",
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            if not datos.get("descripcion"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📝 Por favor describe brevemente el proyecto:\n\n_Ejemplo: Sistema de CCTV para vigilancia perimetral_",
                    "campo_esperado": "descripcion",
                    "puede_generar": False
                }

            return None

    def _generar_cotizacion_final(self, servicio: str, datos: Dict) -> Dict[str, Any]:
        """
        Genera la cotización final con todos los datos

        Returns:
            JSON estructurado con la cotización completa
        """

        logger.info(f"💰 Generando cotización para servicio: {servicio}")

        # Usar el brain para generar la estructura base
        cotizacion = self.brain.generar_cotizacion(
            servicio=servicio,
            datos=datos
        )

        # Enriquecer con información adicional
        cotizacion["conversacion"] = {
            "mensaje_pili": f"✅ ¡Excelente! He generado tu cotización para **{self.servicios.get(servicio, {}).get('nombre', servicio)}**.\n\n"
                          f"📊 Total: **S/ {cotizacion['datos_cotizacion']['total']:,.2f}**\n\n"
                          f"Puedes revisar la vista previa y descargar el documento.",
            "puede_generar": True
        }

        return cotizacion


# ═══════════════════════════════════════════════════════════════
# INSTANCIA GLOBAL
# ═══════════════════════════════════════════════════════════════

pili_cotizadora = PILICotizadora()
