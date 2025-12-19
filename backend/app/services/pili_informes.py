"""
🧠 PILI INFORMES - GENERACIÓN CONVERSACIONAL DE INFORMES PROFESIONALES
📁 RUTA: backend/app/services/pili_informes.py

Módulo especializado en la generación conversacional de informes técnicos y ejecutivos (APA).
PILI guía al usuario paso a paso para recopilar toda la información necesaria.

🎯 CAPACIDADES:
- ✅ Generación conversacional de informes técnicos
- ✅ Generación conversacional de informes ejecutivos (formato APA)
- ✅ Validación de formato profesional
- ✅ Guía paso a paso inteligente
- ✅ Detección automática de tipo de informe
- ✅ Generación de JSON estructurado listo para Word/PDF

📊 TIPOS DE INFORMES:
1. INFORME TÉCNICO:
   - Título del informe
   - Introducción
   - Objetivos
   - Metodología
   - Resultados
   - Conclusiones
   - Recomendaciones
   - Anexos técnicos

2. INFORME EJECUTIVO (APA):
   - Todo lo de técnico +
   - Formato APA 7ma edición
   - Abstract/Resumen ejecutivo
   - Referencias bibliográficas
   - Tablas y figuras numeradas
   - Análisis financiero (ROI, TIR, payback)
   - KPIs y métricas

🔄 FLUJO CONVERSACIONAL:
1. Usuario solicita informe
2. PILI detecta tipo (técnico/ejecutivo)
3. PILI pregunta paso a paso
4. Usuario responde
5. PILI valida y solicita más info si falta
6. PILI genera JSON estructurado
7. Sistema crea documento Word/PDF profesional
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 📊 PLANTILLAS DE SECCIONES DE INFORMES
# ═══════════════════════════════════════════════════════════════

SECCIONES_INFORME_TECNICO = [
    "titulo",
    "introduccion",
    "objetivos",
    "metodologia",
    "resultados",
    "conclusiones",
    "recomendaciones",
    "anexos"
]

SECCIONES_INFORME_EJECUTIVO = [
    "titulo",
    "abstract",  # Resumen ejecutivo
    "introduccion",
    "objetivos",
    "metodologia",
    "analisis_situacion",
    "resultados",
    "analisis_financiero",
    "metricas_kpis",
    "evaluacion_riesgos",
    "conclusiones",
    "recomendaciones",
    "referencias",  # Bibliografía en formato APA
    "anexos"
]


# ═══════════════════════════════════════════════════════════════
# 🧠 CLASE PRINCIPAL: PILIInformes
# ═══════════════════════════════════════════════════════════════

class PILIInformes:
    """
    🧠 Cerebro especializado de PILI para generación conversacional de informes

    Guía al usuario paso a paso para crear informes técnicos y ejecutivos
    de manera conversacional, validando formato profesional.
    """

    def __init__(self):
        """Inicializa el módulo de informes de PILI"""
        self.tipo_informe = None
        self.datos_recopilados = {}
        self.paso_actual = 0
        self.pasos_completados = []
        logger.info("📄 PILIInformes inicializado")

    # ──────────────────────────────────────────────────────────────
    # 🎯 MÉTODO PRINCIPAL: PROCESAR MENSAJE
    # ──────────────────────────────────────────────────────────────

    def procesar(
        self,
        mensaje: str,
        historial: List[Dict[str, str]] = None,
        datos_contexto: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario y guía la generación del informe

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación (opcional)
            datos_contexto: Datos de contexto (proyecto, cotización, etc.)

        Returns:
            Diccionario con respuesta y estado del informe
        """
        historial = historial or []
        datos_contexto = datos_contexto or {}

        # 1. Detectar tipo de informe si no está definido
        if not self.tipo_informe:
            self.tipo_informe = self._detectar_tipo_informe(mensaje)
            logger.info(f"📊 Tipo de informe detectado: {self.tipo_informe}")

        # 2. Procesar según tipo de informe
        if self.tipo_informe == "ejecutivo":
            return self._informe_ejecutivo_apa(mensaje, historial, datos_contexto)
        else:
            return self._informe_tecnico(mensaje, historial, datos_contexto)

    # ──────────────────────────────────────────────────────────────
    # 🔍 DETECCIÓN DE TIPO DE INFORME
    # ──────────────────────────────────────────────────────────────

    def _detectar_tipo_informe(self, mensaje: str) -> str:
        """
        Detecta si el usuario quiere informe técnico o ejecutivo

        Args:
            mensaje: Mensaje del usuario

        Returns:
            "tecnico" o "ejecutivo"
        """
        mensaje_lower = mensaje.lower()

        # Palabras clave para informe ejecutivo
        keywords_ejecutivo = [
            "ejecutivo", "apa", "gerencia", "directorio", "alta dirección",
            "roi", "tir", "payback", "financiero", "estratégico", "kpi",
            "métricas", "dashboard", "análisis financiero"
        ]

        # Palabras clave para informe técnico
        keywords_tecnico = [
            "técnico", "ingeniería", "cálculo", "diseño", "especificaciones",
            "metodología", "normativa", "estándar"
        ]

        # Contar coincidencias
        score_ejecutivo = sum(1 for kw in keywords_ejecutivo if kw in mensaje_lower)
        score_tecnico = sum(1 for kw in keywords_tecnico if kw in mensaje_lower)

        if score_ejecutivo > score_tecnico:
            return "ejecutivo"
        else:
            # Por defecto: técnico
            return "tecnico"

    # ──────────────────────────────────────────────────────────────
    # 📄 INFORME TÉCNICO - CONVERSACIONAL
    # ──────────────────────────────────────────────────────────────

    def _informe_tecnico(
        self,
        mensaje: str,
        historial: List[Dict[str, str]],
        datos_contexto: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera informe técnico de manera conversacional

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación
            datos_contexto: Datos de contexto

        Returns:
            Diccionario con respuesta y estado
        """
        # Definir pasos del informe técnico
        pasos = [
            {
                "clave": "titulo",
                "pregunta": "📝 **Comencemos con el título del informe técnico.**\n\n¿Cuál es el título completo del informe?\n\n*Ejemplo:* \"Informe Técnico de Instalación Eléctrica en Edificio Multifamiliar\"",
                "validacion": self._validar_titulo
            },
            {
                "clave": "introduccion",
                "pregunta": "📖 **Introducción**\n\n¿Cuál es el contexto y antecedentes del proyecto? Describe brevemente:\n- ¿Qué motivó este proyecto?\n- ¿Cuál es la situación actual?\n- ¿Qué problema se busca resolver?",
                "validacion": self._validar_texto_largo
            },
            {
                "clave": "objetivos",
                "pregunta": "🎯 **Objetivos del Informe**\n\nIndica los objetivos principales del informe (puedes listar varios):\n\n*Ejemplo:*\n1. Evaluar la viabilidad técnica del sistema eléctrico\n2. Diseñar el sistema según CNE Suministro 2011\n3. Presentar especificaciones técnicas detalladas",
                "validacion": self._validar_objetivos
            },
            {
                "clave": "metodologia",
                "pregunta": "🔬 **Metodología**\n\n¿Qué metodología se utilizó para desarrollar el proyecto?\n\n*Incluye:*\n- Proceso de diseño\n- Normativas aplicadas\n- Herramientas y software utilizados\n- Métodos de cálculo",
                "validacion": self._validar_texto_largo
            },
            {
                "clave": "resultados",
                "pregunta": "📊 **Resultados Obtenidos**\n\n¿Cuáles son los resultados principales del proyecto?\n\n*Puede incluir:*\n- Cálculos realizados\n- Diseños desarrollados\n- Especificaciones definidas\n- Pruebas efectuadas",
                "validacion": self._validar_texto_largo
            },
            {
                "clave": "conclusiones",
                "pregunta": "✅ **Conclusiones**\n\nIndica las conclusiones principales del informe (lista al menos 3):\n\n*Ejemplo:*\n1. El sistema cumple con la normativa CNE vigente\n2. Los cálculos garantizan funcionamiento seguro\n3. El proyecto es técnicamente viable",
                "validacion": self._validar_lista
            },
            {
                "clave": "recomendaciones",
                "pregunta": "💡 **Recomendaciones**\n\n¿Qué recomendaciones tienes para la implementación? (lista al menos 2)\n\n*Ejemplo:*\n1. Iniciar trabajos en temporada seca\n2. Contratar personal certificado\n3. Implementar control de calidad estricto",
                "validacion": self._validar_lista
            },
            {
                "clave": "anexos",
                "pregunta": "📎 **Anexos (Opcional)**\n\n¿Qué anexos incluirá el informe?\n\n*Opcional - puedes responder \"ninguno\" o listar:*\n- Planos\n- Cálculos detallados\n- Especificaciones técnicas\n- Certificados\n\nO escribe **\"ninguno\"** si no habrá anexos.",
                "validacion": self._validar_anexos,
                "opcional": True
            }
        ]

        # Procesar paso actual
        return self._procesar_paso(mensaje, pasos, historial, datos_contexto, "tecnico")

    # ──────────────────────────────────────────────────────────────
    # 📊 INFORME EJECUTIVO APA - CONVERSACIONAL
    # ──────────────────────────────────────────────────────────────

    def _informe_ejecutivo_apa(
        self,
        mensaje: str,
        historial: List[Dict[str, str]],
        datos_contexto: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera informe ejecutivo en formato APA de manera conversacional

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación
            datos_contexto: Datos de contexto

        Returns:
            Diccionario con respuesta y estado
        """
        # Definir pasos del informe ejecutivo APA
        pasos = [
            {
                "clave": "titulo",
                "pregunta": "📝 **Comencemos con el título del informe ejecutivo.**\n\n¿Cuál es el título completo?\n\n*Ejemplo:* \"Análisis de Viabilidad Técnico-Económica del Sistema Eléctrico para Edificio Corporativo\"",
                "validacion": self._validar_titulo
            },
            {
                "clave": "abstract",
                "pregunta": "📋 **Abstract / Resumen Ejecutivo**\n\nRedacta un resumen ejecutivo breve (150-250 palabras) que incluya:\n- Problema u oportunidad\n- Metodología aplicada\n- Hallazgos principales\n- Recomendaciones clave\n\n*Este es el resumen que leerán los ejecutivos primero.*",
                "validacion": self._validar_abstract
            },
            {
                "clave": "introduccion",
                "pregunta": "📖 **Introducción y Contexto Organizacional**\n\nDescribe:\n- Contexto del negocio\n- Problemática identificada\n- Justificación del proyecto\n- Alcance del análisis",
                "validacion": self._validar_texto_largo
            },
            {
                "clave": "objetivos",
                "pregunta": "🎯 **Objetivos Estratégicos**\n\nIndica los objetivos del informe (mínimo 3):\n\n*Ejemplo:*\n1. Evaluar viabilidad técnico-económica\n2. Analizar retorno de inversión (ROI)\n3. Proponer plan de implementación estratégico",
                "validacion": self._validar_objetivos
            },
            {
                "clave": "analisis_situacion",
                "pregunta": "🔍 **Análisis de Situación Actual**\n\nDescribe la situación actual:\n- Estado de la infraestructura\n- Problemas o deficiencias identificadas\n- Oportunidades de mejora\n- Impacto en el negocio",
                "validacion": self._validar_texto_largo
            },
            {
                "clave": "metodologia",
                "pregunta": "🔬 **Metodología de Análisis**\n\n¿Qué metodología se aplicó?\n\n*Incluye:*\n- Framework utilizado (ej: PMI, PRINCE2)\n- Normativas técnicas\n- Herramientas de análisis financiero\n- Métodos de evaluación",
                "validacion": self._validar_texto_largo
            },
            {
                "clave": "analisis_financiero",
                "pregunta": "💰 **Análisis Financiero**\n\nProporciona datos financieros clave:\n- Inversión total estimada (USD)\n- ROI esperado (%)\n- Periodo de retorno / Payback (meses)\n- TIR proyectada (%)\n\n*Formato:* Inversión: 50000, ROI: 25, Payback: 18, TIR: 30",
                "validacion": self._validar_datos_financieros
            },
            {
                "clave": "metricas_kpis",
                "pregunta": "📊 **Métricas y KPIs**\n\nDefine los indicadores clave de desempeño:\n\n*Ejemplo:*\n- Eficiencia energética: +35%\n- Reducción de costos: 20%\n- Nivel de satisfacción: 95%\n- Tiempo de implementación: 60 días",
                "validacion": self._validar_texto_largo
            },
            {
                "clave": "evaluacion_riesgos",
                "pregunta": "⚠️ **Evaluación de Riesgos**\n\nIdentifica riesgos principales y planes de mitigación (lista al menos 3):\n\n*Formato:*\nRiesgo 1: [descripción] | Probabilidad: [Alta/Media/Baja] | Impacto: [Alto/Medio/Bajo] | Mitigación: [plan]",
                "validacion": self._validar_riesgos
            },
            {
                "clave": "conclusiones",
                "pregunta": "✅ **Conclusiones Ejecutivas**\n\nIndica conclusiones clave orientadas a la toma de decisiones (mínimo 4):\n\n*Ejemplo:*\n1. El proyecto es altamente viable financieramente\n2. El ROI de 25% justifica la inversión\n3. Los riesgos son manejables con los planes propuestos\n4. Se recomienda aprobación e implementación inmediata",
                "validacion": self._validar_lista
            },
            {
                "clave": "recomendaciones",
                "pregunta": "💡 **Recomendaciones Estratégicas**\n\n¿Qué recomendaciones estratégicas propones? (mínimo 3)\n\n*Ejemplo:*\n1. Aprobar inversión en el Q1 2025\n2. Implementar por fases para mitigar riesgos\n3. Establecer comité de dirección para seguimiento\n4. Evaluar opciones de financiamiento",
                "validacion": self._validar_lista
            },
            {
                "clave": "referencias",
                "pregunta": "📚 **Referencias Bibliográficas (Formato APA)**\n\nLista las referencias bibliográficas en formato APA 7ma edición:\n\n*Ejemplo:*\n- Ministerio de Energía y Minas. (2011). CNE Suministro 2011. Lima, Perú.\n- Project Management Institute. (2021). PMBOK Guide 7th Edition. PMI.\n\n*Proporciona al menos 3 referencias.*",
                "validacion": self._validar_referencias
            },
            {
                "clave": "anexos",
                "pregunta": "📎 **Anexos (Opcional)**\n\n¿Qué anexos incluirá el informe?\n\n*Opcional - lista anexos o responde \"ninguno\":*\n- Anexo A: Cálculos financieros detallados\n- Anexo B: Análisis de sensibilidad\n- Anexo C: Matriz de riesgos completa\n\nO escribe **\"ninguno\"** si no habrá anexos.",
                "validacion": self._validar_anexos,
                "opcional": True
            }
        ]

        # Procesar paso actual
        return self._procesar_paso(mensaje, pasos, historial, datos_contexto, "ejecutivo")

    # ──────────────────────────────────────────────────────────────
    # 🔄 PROCESAMIENTO DE PASOS
    # ──────────────────────────────────────────────────────────────

    def _procesar_paso(
        self,
        mensaje: str,
        pasos: List[Dict[str, Any]],
        historial: List[Dict[str, str]],
        datos_contexto: Dict[str, Any],
        tipo: str
    ) -> Dict[str, Any]:
        """
        Procesa el paso actual del flujo conversacional

        Args:
            mensaje: Mensaje del usuario
            pasos: Lista de pasos definidos
            historial: Historial de conversación
            datos_contexto: Datos de contexto
            tipo: Tipo de informe ("tecnico" o "ejecutivo")

        Returns:
            Diccionario con respuesta y estado
        """
        # Si es el primer mensaje, iniciar flujo
        if self.paso_actual == 0 and not historial:
            return self._iniciar_flujo(pasos, tipo)

        # Si el usuario ya respondió, validar y guardar
        if self.paso_actual > 0 and self.paso_actual <= len(pasos):
            paso_previo = pasos[self.paso_actual - 1]
            clave = paso_previo["clave"]
            validacion = paso_previo["validacion"]

            # Validar respuesta
            es_valido, mensaje_validacion = validacion(mensaje)

            if not es_valido:
                # Respuesta inválida, pedir de nuevo
                return {
                    "accion": "solicitar_info",
                    "tipo_informe": tipo,
                    "paso_actual": self.paso_actual,
                    "total_pasos": len(pasos),
                    "seccion": clave,
                    "mensaje_pili": f"⚠️ **Validación:**\n\n{mensaje_validacion}\n\n{paso_previo['pregunta']}",
                    "puede_continuar": False,
                    "datos_recopilados": self.datos_recopilados
                }

            # Guardar dato válido
            self.datos_recopilados[clave] = mensaje.strip()
            self.pasos_completados.append(clave)
            logger.info(f"✅ Paso {self.paso_actual} completado: {clave}")

        # Avanzar al siguiente paso
        self.paso_actual += 1

        # Si terminamos todos los pasos, generar informe
        if self.paso_actual > len(pasos):
            return self._generar_informe_final(tipo, datos_contexto)

        # Mostrar siguiente pregunta
        paso_siguiente = pasos[self.paso_actual - 1]
        progreso = int((self.paso_actual / len(pasos)) * 100)

        return {
            "accion": "solicitar_info",
            "tipo_informe": tipo,
            "paso_actual": self.paso_actual,
            "total_pasos": len(pasos),
            "progreso_porcentaje": progreso,
            "seccion": paso_siguiente["clave"],
            "mensaje_pili": f"**📊 Progreso: {self.paso_actual}/{len(pasos)} ({progreso}%)**\n\n{paso_siguiente['pregunta']}",
            "puede_continuar": True,
            "datos_recopilados": self.datos_recopilados
        }

    def _iniciar_flujo(self, pasos: List[Dict[str, Any]], tipo: str) -> Dict[str, Any]:
        """
        Inicia el flujo conversacional

        Args:
            pasos: Lista de pasos
            tipo: Tipo de informe

        Returns:
            Mensaje de bienvenida y primera pregunta
        """
        self.paso_actual = 1

        tipo_nombre = "Informe Ejecutivo (APA)" if tipo == "ejecutivo" else "Informe Técnico"

        mensaje_intro = f"""¡Perfecto! Voy a ayudarte a crear un **{tipo_nombre}** profesional. 📄

**🎯 Sobre este tipo de informe:**
"""

        if tipo == "ejecutivo":
            mensaje_intro += """
- ✅ Formato APA 7ma edición
- ✅ Abstract / Resumen ejecutivo
- ✅ Análisis financiero (ROI, TIR, Payback)
- ✅ KPIs y métricas estratégicas
- ✅ Referencias bibliográficas
- ✅ Orientado a alta dirección

**📋 Proceso:**
Te haré {total_pasos} preguntas para recopilar toda la información necesaria. Puedes responder de manera detallada y conversacional.

¡Comencemos! 🚀

---

""".format(total_pasos=len(pasos))
        else:
            mensaje_intro += """
- ✅ Formato técnico profesional
- ✅ Análisis metodológico
- ✅ Resultados y conclusiones técnicas
- ✅ Recomendaciones prácticas
- ✅ Orientado a ingenieros y técnicos

**📋 Proceso:**
Te haré {total_pasos} preguntas para recopilar toda la información necesaria. Puedes responder de manera detallada y conversacional.

¡Comencemos! 🚀

---

""".format(total_pasos=len(pasos))

        primer_paso = pasos[0]
        mensaje_intro += f"**📊 Progreso: 1/{len(pasos)} (0%)**\n\n{primer_paso['pregunta']}"

        return {
            "accion": "solicitar_info",
            "tipo_informe": tipo,
            "paso_actual": 1,
            "total_pasos": len(pasos),
            "progreso_porcentaje": 0,
            "seccion": primer_paso["clave"],
            "mensaje_pili": mensaje_intro,
            "puede_continuar": True,
            "datos_recopilados": {}
        }

    # ──────────────────────────────────────────────────────────────
    # ✅ FUNCIONES DE VALIDACIÓN
    # ──────────────────────────────────────────────────────────────

    def _validar_titulo(self, texto: str) -> Tuple[bool, str]:
        """Valida que el título sea apropiado"""
        texto = texto.strip()

        if len(texto) < 10:
            return False, "El título es muy corto. Debe tener al menos 10 caracteres y ser descriptivo."

        if len(texto) > 200:
            return False, "El título es muy largo. Debe ser conciso (máximo 200 caracteres)."

        return True, "Título válido"

    def _validar_texto_largo(self, texto: str) -> Tuple[bool, str]:
        """Valida texto largo (secciones narrativas)"""
        texto = texto.strip()

        if len(texto) < 50:
            return False, "La respuesta es muy breve. Por favor, proporciona una descripción más detallada (al menos 50 caracteres)."

        return True, "Texto válido"

    def _validar_objetivos(self, texto: str) -> Tuple[bool, str]:
        """Valida lista de objetivos"""
        texto = texto.strip()

        # Detectar si hay al menos 2 objetivos (numerados o con guiones)
        patrones_lista = [
            r'\d+\.',  # 1. 2. 3.
            r'-\s',    # - item
            r'\*\s',   # * item
        ]

        tiene_lista = any(re.search(patron, texto) for patron in patrones_lista)

        if not tiene_lista and len(texto.split('\n')) < 2:
            return False, "Por favor, lista al menos 2 objetivos. Puedes usar formato numerado (1., 2.) o con guiones (-)."

        if len(texto) < 30:
            return False, "Los objetivos son muy breves. Describe cada objetivo de manera clara."

        return True, "Objetivos válidos"

    def _validar_lista(self, texto: str) -> Tuple[bool, str]:
        """Valida lista genérica (conclusiones, recomendaciones, etc.)"""
        texto = texto.strip()

        # Detectar si hay al menos 2 items
        patrones_lista = [
            r'\d+\.',  # 1. 2. 3.
            r'-\s',    # - item
            r'\*\s',   # * item
        ]

        tiene_lista = any(re.search(patron, texto) for patron in patrones_lista)
        num_lineas = len([l for l in texto.split('\n') if l.strip()])

        if not tiene_lista and num_lineas < 2:
            return False, "Por favor, lista al menos 2 items. Puedes usar formato numerado (1., 2.) o con guiones (-)."

        if len(texto) < 30:
            return False, "La lista es muy breve. Describe cada item de manera clara."

        return True, "Lista válida"

    def _validar_abstract(self, texto: str) -> Tuple[bool, str]:
        """Valida abstract/resumen ejecutivo"""
        texto = texto.strip()
        num_palabras = len(texto.split())

        if num_palabras < 50:
            return False, "El abstract es muy breve. Debe tener entre 150-250 palabras para ser un resumen ejecutivo completo."

        if num_palabras > 400:
            return False, "El abstract es muy extenso. Debe ser conciso (150-250 palabras) para facilitar lectura rápida."

        return True, "Abstract válido"

    def _validar_datos_financieros(self, texto: str) -> Tuple[bool, str]:
        """Valida datos financieros"""
        texto_lower = texto.lower()

        # Buscar números
        numeros = re.findall(r'\d+\.?\d*', texto)

        if len(numeros) < 3:
            return False, "Por favor, proporciona los datos financieros completos: Inversión, ROI, Payback y TIR.\n\nEjemplo: Inversión: 50000, ROI: 25, Payback: 18, TIR: 30"

        # Verificar que tenga las métricas clave
        metricas_requeridas = ["inversión", "roi", "payback", "tir"]
        metricas_encontradas = sum(1 for m in metricas_requeridas if m in texto_lower)

        if metricas_encontradas < 3:
            return False, "Asegúrate de incluir: Inversión total, ROI (%), Payback (meses) y TIR (%).\n\nEjemplo: Inversión: 50000 USD, ROI: 25%, Payback: 18 meses, TIR: 30%"

        return True, "Datos financieros válidos"

    def _validar_riesgos(self, texto: str) -> Tuple[bool, str]:
        """Valida análisis de riesgos"""
        texto_lower = texto.lower()

        # Buscar al menos 2 riesgos listados
        patrones_lista = [
            r'\d+\.',  # 1. 2. 3.
            r'riesgo\s*\d+',  # riesgo 1, riesgo 2
            r'-\s',    # - item
        ]

        tiene_lista = any(re.search(patron, texto_lower) for patron in patrones_lista)
        num_lineas = len([l for l in texto.split('\n') if l.strip()])

        if not tiene_lista and num_lineas < 2:
            return False, "Lista al menos 2 riesgos con formato:\nRiesgo 1: [descripción] | Probabilidad: [Alta/Media/Baja] | Impacto: [Alto/Medio/Bajo] | Mitigación: [plan]"

        # Verificar que mencione probabilidad e impacto
        tiene_probabilidad = any(p in texto_lower for p in ["probabilidad", "alta", "media", "baja"])
        tiene_impacto = any(i in texto_lower for i in ["impacto", "alto", "medio", "bajo"])

        if not (tiene_probabilidad and tiene_impacto):
            return False, "Incluye para cada riesgo: Probabilidad (Alta/Media/Baja) e Impacto (Alto/Medio/Bajo).\n\nEjemplo:\nRiesgo 1: Retrasos en materiales | Probabilidad: Media | Impacto: Alto | Mitigación: Compra anticipada"

        return True, "Riesgos válidos"

    def _validar_referencias(self, texto: str) -> Tuple[bool, str]:
        """Valida referencias bibliográficas en formato APA"""
        texto = texto.strip()

        # Verificar que haya al menos 3 referencias (líneas no vacías o items numerados)
        lineas_validas = [l for l in texto.split('\n') if l.strip() and len(l.strip()) > 20]

        if len(lineas_validas) < 3:
            return False, "Proporciona al menos 3 referencias bibliográficas en formato APA.\n\nEjemplo:\n- Apellido, N. (Año). Título. Editorial.\n- Ministerio de Energía. (2011). CNE Suministro. Lima, Perú."

        # Verificar formato básico APA (debe tener año entre paréntesis)
        tiene_formato_apa = any(re.search(r'\(\d{4}\)', l) for l in lineas_validas)

        if not tiene_formato_apa:
            return False, "Las referencias deben seguir formato APA (incluir año entre paréntesis).\n\nEjemplo: Apellido, N. (2023). Título del documento. Editorial."

        return True, "Referencias válidas"

    def _validar_anexos(self, texto: str) -> Tuple[bool, str]:
        """Valida anexos (campo opcional)"""
        texto_lower = texto.strip().lower()

        # Si dice "ninguno", "no", "sin anexos", etc., es válido
        sin_anexos = any(palabra in texto_lower for palabra in ["ninguno", "no", "sin anexos", "n/a"])

        if sin_anexos or len(texto.strip()) == 0:
            return True, "Sin anexos"

        # Si tiene anexos, validar que tenga al menos descripción mínima
        if len(texto) < 20:
            return False, "Si vas a incluir anexos, describe cada uno brevemente.\n\nEjemplo:\n- Anexo A: Cálculos detallados\n- Anexo B: Planos\n\nO responde 'ninguno' si no habrá anexos."

        return True, "Anexos válidos"

    # ──────────────────────────────────────────────────────────────
    # 📄 GENERACIÓN DE INFORME FINAL
    # ──────────────────────────────────────────────────────────────

    def _generar_informe_final(
        self,
        tipo: str,
        datos_contexto: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera el JSON estructurado final del informe

        Args:
            tipo: Tipo de informe ("tecnico" o "ejecutivo")
            datos_contexto: Datos de contexto

        Returns:
            JSON estructurado del informe listo para generar Word/PDF
        """
        # Parsear datos financieros si es ejecutivo
        datos_financieros = {}
        if tipo == "ejecutivo" and "analisis_financiero" in self.datos_recopilados:
            datos_financieros = self._parsear_datos_financieros(
                self.datos_recopilados["analisis_financiero"]
            )

        # Construir JSON estructurado
        informe = {
            "accion": "informe_generado",
            "tipo_informe": tipo,
            "formato": "APA 7ma edición" if tipo == "ejecutivo" else "Técnico estándar",
            "datos": {
                "titulo": self.datos_recopilados.get("titulo", "Informe Técnico"),
                "codigo": f"INF-{datetime.now().strftime('%Y%m%d')}-{tipo[:3].upper()}",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "autor": "Tesla Electricidad y Automatización S.A.C.",
                "cliente": datos_contexto.get("cliente", "Cliente Demo"),

                # Secciones del informe
                "abstract": self.datos_recopilados.get("abstract"),
                "introduccion": self.datos_recopilados.get("introduccion"),
                "objetivos": self._parsear_lista(self.datos_recopilados.get("objetivos", "")),
                "metodologia": self.datos_recopilados.get("metodologia"),
                "analisis_situacion": self.datos_recopilados.get("analisis_situacion"),
                "resultados": self.datos_recopilados.get("resultados"),
                "conclusiones": self._parsear_lista(self.datos_recopilados.get("conclusiones", "")),
                "recomendaciones": self._parsear_lista(self.datos_recopilados.get("recomendaciones", "")),

                # Secciones específicas de ejecutivo
                "analisis_financiero": datos_financieros if tipo == "ejecutivo" else None,
                "metricas_kpis": self.datos_recopilados.get("metricas_kpis") if tipo == "ejecutivo" else None,
                "evaluacion_riesgos": self._parsear_riesgos(self.datos_recopilados.get("evaluacion_riesgos", "")) if tipo == "ejecutivo" else None,
                "referencias": self._parsear_lista(self.datos_recopilados.get("referencias", "")) if tipo == "ejecutivo" else None,

                # Anexos
                "anexos": self._parsear_lista(self.datos_recopilados.get("anexos", "")) if self.datos_recopilados.get("anexos") else [],

                # Metadata
                "datos_contexto": datos_contexto,
                "datos_recopilados_completos": self.datos_recopilados
            },
            "conversacion": {
                "mensaje_pili": self._generar_mensaje_final(tipo),
                "puede_generar": True
            }
        }

        logger.info(f"📄 Informe {tipo} generado exitosamente")
        return informe

    def _parsear_lista(self, texto: str) -> List[str]:
        """Convierte texto con lista en array"""
        if not texto:
            return []

        items = []

        # Separar por líneas
        lineas = texto.split('\n')

        for linea in lineas:
            linea = linea.strip()

            # Eliminar prefijos numerados o con guiones
            linea = re.sub(r'^\d+\.\s*', '', linea)
            linea = re.sub(r'^-\s*', '', linea)
            linea = re.sub(r'^\*\s*', '', linea)
            linea = re.sub(r'^•\s*', '', linea)

            if linea:
                items.append(linea)

        return items

    def _parsear_datos_financieros(self, texto: str) -> Dict[str, Any]:
        """Parsea datos financieros del texto"""
        # Extraer números
        numeros = re.findall(r'(\d+\.?\d*)', texto)
        texto_lower = texto.lower()

        datos = {
            "inversion_total": 0,
            "roi_porcentaje": 0,
            "payback_meses": 0,
            "tir_porcentaje": 0
        }

        # Intentar extraer cada métrica
        if "inversión" in texto_lower or "inversion" in texto_lower:
            match = re.search(r'(?:inversión|inversion)[:\s]*(\d+\.?\d*)', texto_lower)
            if match:
                datos["inversion_total"] = float(match.group(1))

        if "roi" in texto_lower:
            match = re.search(r'roi[:\s]*(\d+\.?\d*)', texto_lower)
            if match:
                datos["roi_porcentaje"] = float(match.group(1))

        if "payback" in texto_lower:
            match = re.search(r'payback[:\s]*(\d+\.?\d*)', texto_lower)
            if match:
                datos["payback_meses"] = int(match.group(1))

        if "tir" in texto_lower:
            match = re.search(r'tir[:\s]*(\d+\.?\d*)', texto_lower)
            if match:
                datos["tir_porcentaje"] = float(match.group(1))

        # Si no encontramos valores específicos, usar los primeros 4 números en orden
        if datos["inversion_total"] == 0 and len(numeros) >= 4:
            datos["inversion_total"] = float(numeros[0])
            datos["roi_porcentaje"] = float(numeros[1])
            datos["payback_meses"] = int(float(numeros[2]))
            datos["tir_porcentaje"] = float(numeros[3])

        return datos

    def _parsear_riesgos(self, texto: str) -> List[Dict[str, str]]:
        """Parsea análisis de riesgos"""
        riesgos = []

        # Dividir por líneas o por "Riesgo N:"
        partes = re.split(r'(?:^|\n)(?:riesgo\s*\d+[:\.]||\d+\.)', texto, flags=re.IGNORECASE)

        for parte in partes:
            parte = parte.strip()
            if len(parte) < 10:
                continue

            # Intentar extraer componentes
            riesgo_dict = {
                "descripcion": "",
                "probabilidad": "",
                "impacto": "",
                "mitigacion": ""
            }

            # Buscar separador "|" o ":"
            if "|" in parte:
                componentes = parte.split("|")
                if len(componentes) >= 1:
                    riesgo_dict["descripcion"] = componentes[0].strip()
                if len(componentes) >= 2:
                    prob_texto = componentes[1].lower()
                    if "alta" in prob_texto:
                        riesgo_dict["probabilidad"] = "Alta"
                    elif "media" in prob_texto:
                        riesgo_dict["probabilidad"] = "Media"
                    elif "baja" in prob_texto:
                        riesgo_dict["probabilidad"] = "Baja"
                if len(componentes) >= 3:
                    imp_texto = componentes[2].lower()
                    if "alto" in imp_texto:
                        riesgo_dict["impacto"] = "Alto"
                    elif "medio" in imp_texto:
                        riesgo_dict["impacto"] = "Medio"
                    elif "bajo" in imp_texto:
                        riesgo_dict["impacto"] = "Bajo"
                if len(componentes) >= 4:
                    riesgo_dict["mitigacion"] = componentes[3].strip()
            else:
                # Sin separadores, usar toda la parte como descripción
                riesgo_dict["descripcion"] = parte

            if riesgo_dict["descripcion"]:
                riesgos.append(riesgo_dict)

        return riesgos

    def _generar_mensaje_final(self, tipo: str) -> str:
        """Genera mensaje final de confirmación"""
        tipo_nombre = "Informe Ejecutivo (APA)" if tipo == "ejecutivo" else "Informe Técnico"

        mensaje = f"""✅ ¡Excelente! He recopilado toda la información para tu **{tipo_nombre}**.

📄 **Resumen del Informe:**
- Título: {self.datos_recopilados.get('titulo', 'N/A')}
- Formato: {'APA 7ma edición' if tipo == 'ejecutivo' else 'Técnico profesional'}
- Secciones: {len([k for k in self.datos_recopilados.keys() if self.datos_recopilados[k]])}
"""

        if tipo == "ejecutivo":
            mensaje += """
**✨ Incluye:**
- Abstract / Resumen ejecutivo
- Análisis financiero completo
- KPIs y métricas estratégicas
- Evaluación de riesgos
- Referencias bibliográficas en formato APA
"""
        else:
            mensaje += """
**✨ Incluye:**
- Introducción y objetivos
- Metodología aplicada
- Resultados técnicos
- Conclusiones y recomendaciones
"""

        mensaje += """
💡 **¿Qué puedes hacer ahora?**
- 📄 **Generar documento Word** profesional
- 📊 **Exportar a PDF** con formato
- ✏️ **Editar** cualquier sección
- 💬 **Hacer ajustes** conversando conmigo

¡Tu informe está listo para generarse! 🚀
"""

        return mensaje

    # ──────────────────────────────────────────────────────────────
    # 🔧 UTILIDADES
    # ──────────────────────────────────────────────────────────────

    def reiniciar(self):
        """Reinicia el estado del flujo conversacional"""
        self.tipo_informe = None
        self.datos_recopilados = {}
        self.paso_actual = 0
        self.pasos_completados = []
        logger.info("🔄 PILIInformes reiniciado")


# ═══════════════════════════════════════════════════════════════
# 🏭 INSTANCIA SINGLETON
# ═══════════════════════════════════════════════════════════════

# Crear instancia única de PILIInformes
pili_informes = PILIInformes()

logger.info("📄 PILIInformes listo para generar informes profesionales")
