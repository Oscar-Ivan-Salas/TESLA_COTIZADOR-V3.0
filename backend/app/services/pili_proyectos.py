"""
🏗️ PILI PROYECTOS - GESTOR INTELIGENTE DE PROYECTOS
📁 RUTA: backend/app/services/pili_proyectos.py

Este módulo especializado maneja la creación y gestión de proyectos
de forma conversacional e inteligente.

🎯 CAPACIDADES:
- ✅ Proyectos Simples (gestión básica)
- ✅ Proyectos PMI Complejos (metodología completa)
- ✅ Conversación inteligente paso a paso
- ✅ Detección automática de complejidad
- ✅ Generación de cronogramas Gantt
- ✅ Gestión de recursos y riesgos
- ✅ Métricas y KPIs

🔄 TIPOS DE PROYECTO:
1. SIMPLE: Nombre, cliente, fases básicas, presupuesto
2. PMI COMPLEJO: Todo lo anterior + Gantt, recursos, riesgos, hitos
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

# Importar el cerebro base de PILI
try:
    from .pili_brain import PILIBrain, SERVICIOS_PILI
except ImportError:
    from pili_brain import PILIBrain, SERVICIOS_PILI

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 🏗️ ESTADOS DEL FLUJO CONVERSACIONAL DE PROYECTOS
# ═══════════════════════════════════════════════════════════════

ESTADOS_PROYECTO = {
    "inicio": "Inicio de conversación",
    "detectando_tipo": "Detectando tipo de proyecto",
    "preguntando_nombre": "Solicitando nombre del proyecto",
    "preguntando_cliente": "Solicitando cliente",
    "preguntando_descripcion": "Solicitando descripción",
    "preguntando_alcance": "Definiendo alcance",
    "preguntando_presupuesto": "Estimando presupuesto",
    "preguntando_duracion": "Estimando duración",
    "definiendo_fases": "Definiendo fases del proyecto",
    "definiendo_recursos": "Asignando recursos (PMI)",
    "analizando_riesgos": "Analizando riesgos (PMI)",
    "creando_gantt": "Creando cronograma Gantt (PMI)",
    "definiendo_hitos": "Definiendo hitos (PMI)",
    "calculando_metricas": "Calculando métricas PMI",
    "listo": "Proyecto completo y listo"
}


# ═══════════════════════════════════════════════════════════════
# 🏗️ CLASE PRINCIPAL: PILIProyectos
# ═══════════════════════════════════════════════════════════════

class PILIProyectos:
    """
    🏗️ Gestor inteligente de proyectos con conversación guiada

    Maneja dos tipos de proyectos:
    1. SIMPLE: Gestión básica con fases estándar
    2. PMI COMPLEJO: Metodología PMI completa con Gantt, recursos, riesgos

    Es conversacional, hace preguntas paso a paso y genera JSON estructurado.
    """

    def __init__(self):
        """Inicializa el gestor de proyectos"""
        self.brain = PILIBrain()
        self.estado_actual = "inicio"
        self.datos_recopilados = {}
        logger.info("🏗️ PILIProyectos inicializado")

    # ──────────────────────────────────────────────────────────────
    # 🎯 MÉTODO PRINCIPAL DE PROCESAMIENTO
    # ──────────────────────────────────────────────────────────────

    def procesar(self, mensaje: str, historial: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Procesa el mensaje del usuario en el contexto de creación de proyecto

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de la conversación

        Returns:
            Respuesta estructurada con siguiente pregunta o proyecto completo
        """

        logger.info(f"📨 Procesando mensaje: {mensaje[:50]}...")

        # Detectar tipo de proyecto si es el primer mensaje
        tipo_proyecto = self._detectar_tipo_proyecto(mensaje, historial)

        # Extraer datos del mensaje
        self._extraer_y_almacenar_datos(mensaje)

        # Determinar el estado y siguiente paso
        if tipo_proyecto == "simple":
            return self._proyecto_simple(mensaje, historial)
        elif tipo_proyecto == "pmi":
            return self._proyecto_pmi(mensaje, historial)
        else:
            # Preguntar qué tipo de proyecto quiere
            return self._preguntar_tipo_proyecto()

    # ──────────────────────────────────────────────────────────────
    # 🔍 DETECCIÓN DE TIPO DE PROYECTO
    # ──────────────────────────────────────────────────────────────

    def _detectar_tipo_proyecto(self, mensaje: str, historial: List) -> str:
        """
        Detecta si el usuario quiere un proyecto simple o PMI complejo

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación

        Returns:
            "simple", "pmi" o "desconocido"
        """

        mensaje_lower = mensaje.lower()

        # Indicadores de proyecto PMI complejo
        indicadores_pmi = [
            "pmi", "complejo", "gantt", "cronograma detallado", "metodología",
            "recursos", "riesgos", "hitos", "métricas", "avanzado",
            "profesional", "ejecutivo", "stakeholders"
        ]

        # Indicadores de proyecto simple
        indicadores_simple = [
            "simple", "básico", "rápido", "sencillo", "pequeño"
        ]

        # Contar matches
        score_pmi = sum(1 for ind in indicadores_pmi if ind in mensaje_lower)
        score_simple = sum(1 for ind in indicadores_simple if ind in mensaje_lower)

        if score_pmi > 0:
            return "pmi"
        elif score_simple > 0:
            return "simple"
        else:
            # Revisar historial
            for msg in historial:
                contenido = msg.get("content", "").lower()
                if any(ind in contenido for ind in indicadores_pmi):
                    return "pmi"
                elif any(ind in contenido for ind in indicadores_simple):
                    return "simple"

            return "desconocido"

    def _preguntar_tipo_proyecto(self) -> Dict[str, Any]:
        """Pregunta al usuario qué tipo de proyecto desea crear"""

        return {
            "accion": "pregunta_tipo_proyecto",
            "estado": "detectando_tipo",
            "mensaje": """¡Perfecto! Voy a ayudarte a crear un proyecto.

📊 **¿Qué tipo de proyecto necesitas?**

**1. 📋 Proyecto Simple**
   - Gestión básica con fases estándar
   - 3-5 fases principales
   - Ideal para proyectos pequeños y medianos
   - Duración y presupuesto estimados

**2. 🎯 Proyecto PMI Complejo**
   - Metodología PMI completa
   - Cronograma Gantt detallado
   - Gestión de recursos y riesgos
   - Hitos y métricas avanzadas
   - Ideal para proyectos grandes y estratégicos

💡 Responde con "**simple**" o "**complejo**" (o "**PMI**")""",
            "botones_sugeridos": [
                "Proyecto Simple",
                "Proyecto PMI Complejo"
            ],
            "datos_recopilados": self.datos_recopilados,
            "puede_generar": False
        }

    # ──────────────────────────────────────────────────────────────
    # 📋 FLUJO: PROYECTO SIMPLE
    # ──────────────────────────────────────────────────────────────

    def _proyecto_simple(self, mensaje: str, historial: List) -> Dict[str, Any]:
        """
        Maneja el flujo conversacional de proyecto simple

        Pasos:
        1. Nombre del proyecto
        2. Cliente
        3. Descripción
        4. Duración estimada
        5. Presupuesto estimado
        6. Fases (3-5 fases)
        7. ✅ GENERAR
        """

        # Determinar qué falta
        nombre = self.datos_recopilados.get("nombre_proyecto")
        cliente = self.datos_recopilados.get("cliente")
        descripcion = self.datos_recopilados.get("descripcion")
        duracion = self.datos_recopilados.get("duracion_dias")
        presupuesto = self.datos_recopilados.get("presupuesto")
        servicio = self.datos_recopilados.get("servicio")

        # PASO 1: Nombre del proyecto
        if not nombre:
            return {
                "accion": "pregunta_nombre",
                "estado": "preguntando_nombre",
                "tipo_proyecto": "simple",
                "mensaje": """✅ Proyecto Simple seleccionado.

📝 **¿Cuál es el nombre del proyecto?**

Ejemplos:
- "Instalación Eléctrica Edificio Los Pinos"
- "Sistema Contraincendios Centro Comercial"
- "Automatización Planta Industrial XYZ"

💡 Escribe el nombre completo del proyecto:""",
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # PASO 2: Cliente
        if not cliente:
            return {
                "accion": "pregunta_cliente",
                "estado": "preguntando_cliente",
                "tipo_proyecto": "simple",
                "mensaje": f"""✅ Proyecto: **{nombre}**

👤 **¿Quién es el cliente?**

Ejemplos:
- "Empresa ABC S.A.C."
- "Juan Pérez"
- "Municipalidad de Huancayo"

💡 Escribe el nombre del cliente:""",
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # PASO 3: Descripción
        if not descripcion:
            return {
                "accion": "pregunta_descripcion",
                "estado": "preguntando_descripcion",
                "tipo_proyecto": "simple",
                "mensaje": f"""✅ Cliente: **{cliente}**

📄 **Describe brevemente el proyecto:**

¿Qué servicios incluye? ¿Cuál es el alcance?

Ejemplos:
- "Instalación eléctrica completa para edificio de 5 pisos"
- "Sistema contraincendios con rociadores y detectores"
- "Automatización industrial con PLC y SCADA"

💡 Describe el proyecto (puedes mencionar servicios, área, características):""",
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # Detectar servicio automáticamente si no está definido
        if not servicio:
            servicio = self.brain.detectar_servicio(descripcion)
            self.datos_recopilados["servicio"] = servicio

        # PASO 4: Duración estimada
        if not duracion:
            # Intentar calcular automáticamente
            datos_extraidos = self.brain.extraer_datos(descripcion, servicio)
            area = datos_extraidos.get("area_m2", 100)

            duracion_sugerida = self._estimar_duracion_simple(area, servicio)

            return {
                "accion": "pregunta_duracion",
                "estado": "preguntando_duracion",
                "tipo_proyecto": "simple",
                "mensaje": f"""✅ Descripción registrada.

⏱️ **¿Cuál es la duración estimada del proyecto?**

Basándome en tu descripción, estimo aproximadamente **{duracion_sugerida} días**.

💡 Puedes:
- Confirmar: "ok", "correcto", "sí"
- Especificar: "45 días", "2 meses", "60 días"

¿Esta duración es correcta o prefieres ajustarla?""",
                "duracion_sugerida": duracion_sugerida,
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # PASO 5: Presupuesto estimado
        if not presupuesto:
            # Generar cotización rápida para estimar presupuesto
            cotizacion = self.brain.generar_cotizacion(descripcion, servicio, "simple")
            presupuesto_sugerido = cotizacion["datos"]["total"]

            return {
                "accion": "pregunta_presupuesto",
                "estado": "preguntando_presupuesto",
                "tipo_proyecto": "simple",
                "mensaje": f"""✅ Duración: **{duracion} días**

💰 **¿Cuál es el presupuesto estimado?**

Basándome en tu descripción, estimo aproximadamente **${presupuesto_sugerido:,.2f} USD**.

💡 Puedes:
- Confirmar: "ok", "correcto", "sí"
- Especificar: "$15000", "20 mil dólares"

¿Este presupuesto es correcto o prefieres ajustarlo?""",
                "presupuesto_sugerido": presupuesto_sugerido,
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # ✅ TODOS LOS DATOS RECOPILADOS - GENERAR PROYECTO
        return self._generar_proyecto_simple()

    # ──────────────────────────────────────────────────────────────
    # 🎯 FLUJO: PROYECTO PMI COMPLEJO
    # ──────────────────────────────────────────────────────────────

    def _proyecto_pmi(self, mensaje: str, historial: List) -> Dict[str, Any]:
        """
        Maneja el flujo conversacional de proyecto PMI complejo

        Pasos:
        1-6. Igual que proyecto simple
        7. Recursos asignados
        8. Análisis de riesgos
        9. Hitos críticos
        10. Métricas PMI
        11. Cronograma Gantt
        12. ✅ GENERAR
        """

        # Primero completar datos básicos (igual que simple)
        nombre = self.datos_recopilados.get("nombre_proyecto")
        cliente = self.datos_recopilados.get("cliente")
        descripcion = self.datos_recopilados.get("descripcion")
        duracion = self.datos_recopilados.get("duracion_dias")
        presupuesto = self.datos_recopilados.get("presupuesto")
        servicio = self.datos_recopilados.get("servicio")

        # Pasos 1-5: Igual que proyecto simple
        if not nombre:
            return {
                "accion": "pregunta_nombre",
                "estado": "preguntando_nombre",
                "tipo_proyecto": "pmi",
                "mensaje": """✅ Proyecto PMI Complejo seleccionado.

📝 **¿Cuál es el nombre del proyecto?**

Ejemplos:
- "Proyecto de Modernización Eléctrica Planta Industrial"
- "Implementación Sistema Integral Contraincendios"
- "Automatización y Control SCADA Refinería"

💡 Escribe el nombre completo del proyecto:""",
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        if not cliente:
            return {
                "accion": "pregunta_cliente",
                "estado": "preguntando_cliente",
                "tipo_proyecto": "pmi",
                "mensaje": f"""✅ Proyecto: **{nombre}**

👤 **¿Quién es el cliente o sponsor del proyecto?**

En proyectos PMI, es importante identificar al sponsor ejecutivo.

💡 Escribe el nombre del cliente/sponsor:""",
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        if not descripcion:
            return {
                "accion": "pregunta_descripcion",
                "estado": "preguntando_descripcion",
                "tipo_proyecto": "pmi",
                "mensaje": f"""✅ Cliente: **{cliente}**

📄 **Describe el alcance completo del proyecto:**

Incluye:
- Servicios a realizar
- Área o magnitud
- Características técnicas
- Objetivos principales

💡 Describe el proyecto de forma detallada:""",
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        if not servicio:
            servicio = self.brain.detectar_servicio(descripcion)
            self.datos_recopilados["servicio"] = servicio

        if not duracion:
            datos_extraidos = self.brain.extraer_datos(descripcion, servicio)
            area = datos_extraidos.get("area_m2", 200)
            duracion_sugerida = self._estimar_duracion_pmi(area, servicio)

            return {
                "accion": "pregunta_duracion",
                "estado": "preguntando_duracion",
                "tipo_proyecto": "pmi",
                "mensaje": f"""✅ Descripción registrada.

⏱️ **¿Cuál es la duración estimada del proyecto?**

Para un proyecto PMI de esta magnitud, estimo aproximadamente **{duracion_sugerida} días**.

💡 Confirma o ajusta la duración:""",
                "duracion_sugerida": duracion_sugerida,
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        if not presupuesto:
            cotizacion = self.brain.generar_cotizacion(descripcion, servicio, "complejo")
            presupuesto_sugerido = cotizacion["datos"]["total"]

            return {
                "accion": "pregunta_presupuesto",
                "estado": "preguntando_presupuesto",
                "tipo_proyecto": "pmi",
                "mensaje": f"""✅ Duración: **{duracion} días**

💰 **¿Cuál es el presupuesto total del proyecto?**

Estimación basada en alcance: **${presupuesto_sugerido:,.2f} USD**

💡 Confirma o ajusta el presupuesto:""",
                "presupuesto_sugerido": presupuesto_sugerido,
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # ──────────────────────────────────────────────────────────
        # PASOS ADICIONALES PMI
        # ──────────────────────────────────────────────────────────

        recursos_confirmados = self.datos_recopilados.get("recursos_confirmados", False)
        riesgos_confirmados = self.datos_recopilados.get("riesgos_confirmados", False)
        hitos_confirmados = self.datos_recopilados.get("hitos_confirmados", False)

        # PASO 6: Recursos
        if not recursos_confirmados:
            recursos_sugeridos = self._generar_recursos_pmi(servicio, presupuesto)

            recursos_texto = "\n".join([
                f"- **{r['rol']}**: {r['cantidad']} persona(s), {r['dedicacion']} dedicación"
                for r in recursos_sugeridos[:5]
            ])

            return {
                "accion": "pregunta_recursos",
                "estado": "definiendo_recursos",
                "tipo_proyecto": "pmi",
                "mensaje": f"""✅ Presupuesto: **${presupuesto:,.2f} USD**

👥 **Recursos del Proyecto:**

He identificado el siguiente equipo:

{recursos_texto}

💡 Responde:
- "ok" o "correcto" para aceptar
- Menciona cambios: "Agregar ingeniero de calidad"

¿El equipo de recursos es correcto?""",
                "recursos_sugeridos": recursos_sugeridos,
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # PASO 7: Riesgos
        if not riesgos_confirmados:
            riesgos_sugeridos = self._generar_riesgos_pmi(servicio)

            riesgos_texto = "\n".join([
                f"- **{r['riesgo']}** (Prob: {r['probabilidad']}, Impacto: {r['impacto']})"
                for r in riesgos_sugeridos[:4]
            ])

            return {
                "accion": "pregunta_riesgos",
                "estado": "analizando_riesgos",
                "tipo_proyecto": "pmi",
                "mensaje": f"""✅ Equipo definido.

⚠️ **Análisis de Riesgos:**

He identificado los siguientes riesgos:

{riesgos_texto}

💡 Responde:
- "ok" para aceptar
- Menciona riesgos adicionales

¿El análisis de riesgos es completo?""",
                "riesgos_sugeridos": riesgos_sugeridos,
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # PASO 8: Hitos
        if not hitos_confirmados:
            hitos_sugeridos = self._generar_hitos_pmi(duracion, servicio)

            hitos_texto = "\n".join([
                f"- **Día {h['dia']}**: {h['nombre']}"
                for h in hitos_sugeridos
            ])

            return {
                "accion": "pregunta_hitos",
                "estado": "definiendo_hitos",
                "tipo_proyecto": "pmi",
                "mensaje": f"""✅ Riesgos identificados.

🎯 **Hitos del Proyecto:**

{hitos_texto}

💡 Responde:
- "ok" para aceptar
- Menciona cambios o hitos adicionales

¿Los hitos son correctos?""",
                "hitos_sugeridos": hitos_sugeridos,
                "datos_recopilados": self.datos_recopilados,
                "puede_generar": False
            }

        # ✅ TODOS LOS DATOS PMI RECOPILADOS - GENERAR PROYECTO
        return self._generar_proyecto_pmi()

    # ──────────────────────────────────────────────────────────────
    # 🔨 GENERACIÓN DE PROYECTOS
    # ──────────────────────────────────────────────────────────────

    def _generar_proyecto_simple(self) -> Dict[str, Any]:
        """Genera el JSON completo de proyecto simple"""

        nombre = self.datos_recopilados["nombre_proyecto"]
        cliente = self.datos_recopilados["cliente"]
        descripcion = self.datos_recopilados["descripcion"]
        duracion = self.datos_recopilados["duracion_dias"]
        presupuesto = self.datos_recopilados["presupuesto"]
        servicio = self.datos_recopilados["servicio"]

        # Usar PILIBrain para generar estructura completa
        proyecto_completo = self.brain.generar_proyecto(
            mensaje=descripcion,
            servicio=servicio,
            complejidad="simple"
        )

        # Sobrescribir con datos recopilados
        proyecto_completo["datos"]["nombre"] = nombre
        proyecto_completo["datos"]["cliente"] = cliente
        proyecto_completo["datos"]["descripcion"] = descripcion
        proyecto_completo["datos"]["duracion_total_dias"] = duracion
        proyecto_completo["datos"]["presupuesto_estimado"] = presupuesto

        # Agregar mensaje de finalización
        proyecto_completo["conversacion"]["mensaje_pili"] = f"""✅ **¡Proyecto Simple Creado!**

📊 **Resumen:**
- 📝 Nombre: {nombre}
- 👤 Cliente: {cliente}
- ⏱️ Duración: {duracion} días
- 💰 Presupuesto: ${presupuesto:,.2f} USD
- 📋 Fases: {len(proyecto_completo['datos']['fases'])}

💡 **¿Qué puedes hacer ahora?**
- 📄 Generar documento Word del proyecto
- ✏️ Editar fases o recursos
- 💬 Hacer ajustes conversando conmigo

¡El proyecto está listo para ser generado!"""

        proyecto_completo["conversacion"]["puede_generar"] = True
        proyecto_completo["tipo_proyecto"] = "simple"

        logger.info(f"✅ Proyecto simple generado: {nombre}")

        return proyecto_completo

    def _generar_proyecto_pmi(self) -> Dict[str, Any]:
        """Genera el JSON completo de proyecto PMI complejo"""

        nombre = self.datos_recopilados["nombre_proyecto"]
        cliente = self.datos_recopilados["cliente"]
        descripcion = self.datos_recopilados["descripcion"]
        duracion = self.datos_recopilados["duracion_dias"]
        presupuesto = self.datos_recopilados["presupuesto"]
        servicio = self.datos_recopilados["servicio"]

        # Usar PILIBrain para generar estructura completa
        proyecto_completo = self.brain.generar_proyecto(
            mensaje=descripcion,
            servicio=servicio,
            complejidad="complejo"
        )

        # Sobrescribir con datos recopilados
        proyecto_completo["datos"]["nombre"] = nombre
        proyecto_completo["datos"]["cliente"] = cliente
        proyecto_completo["datos"]["descripcion"] = descripcion
        proyecto_completo["datos"]["duracion_total_dias"] = duracion
        proyecto_completo["datos"]["presupuesto_estimado"] = presupuesto

        # Agregar datos PMI adicionales
        if "recursos_sugeridos" in self.datos_recopilados:
            proyecto_completo["datos"]["recursos"] = self.datos_recopilados["recursos_sugeridos"]

        if "riesgos_sugeridos" in self.datos_recopilados:
            proyecto_completo["datos"]["riesgos"] = self.datos_recopilados["riesgos_sugeridos"]

        if "hitos_sugeridos" in self.datos_recopilados:
            proyecto_completo["datos"]["hitos"] = self.datos_recopilados["hitos_sugeridos"]

        # Calcular métricas PMI
        metricas_pmi = self._calcular_metricas_pmi(presupuesto, duracion)
        proyecto_completo["datos"]["metricas_pmi"] = metricas_pmi

        # Mensaje de finalización
        proyecto_completo["conversacion"]["mensaje_pili"] = f"""✅ **¡Proyecto PMI Complejo Creado!**

📊 **Resumen Ejecutivo:**
- 📝 Nombre: {nombre}
- 👤 Sponsor: {cliente}
- ⏱️ Duración: {duracion} días
- 💰 Presupuesto: ${presupuesto:,.2f} USD
- 📋 Fases: {len(proyecto_completo['datos']['fases'])}
- 👥 Equipo: {len(proyecto_completo['datos'].get('recursos', []))} roles
- ⚠️ Riesgos: {len(proyecto_completo['datos'].get('riesgos', []))} identificados
- 🎯 Hitos: {len(proyecto_completo['datos'].get('hitos', []))} críticos

📈 **Métricas PMI:**
- ROI Estimado: {metricas_pmi['roi_estimado']}%
- Payback: {metricas_pmi['payback_meses']} meses
- TIR: {metricas_pmi['tir_proyectada']}%

💡 **¿Qué puedes hacer ahora?**
- 📄 Generar documento Word con cronograma Gantt
- 📊 Ver métricas y KPIs detallados
- ✏️ Ajustar recursos, riesgos o hitos
- 💬 Hacer modificaciones conversando conmigo

¡El proyecto PMI está completo y listo!"""

        proyecto_completo["conversacion"]["puede_generar"] = True
        proyecto_completo["tipo_proyecto"] = "pmi_complejo"

        logger.info(f"✅ Proyecto PMI generado: {nombre}")

        return proyecto_completo

    # ──────────────────────────────────────────────────────────────
    # 🔧 MÉTODOS AUXILIARES
    # ──────────────────────────────────────────────────────────────

    def _extraer_y_almacenar_datos(self, mensaje: str):
        """Extrae datos del mensaje y los almacena"""

        mensaje_lower = mensaje.lower()

        # Extraer nombre de proyecto
        if "proyecto" in mensaje_lower or "instalación" in mensaje_lower:
            # Buscar patrones de nombre de proyecto
            patterns = [
                r'proyecto[:\s]+([A-Z][a-zA-ZáéíóúñÑ\s]+)',
                r'([A-Z][a-zA-ZáéíóúñÑ\s]{10,})'  # Texto largo en mayúsculas
            ]
            for pattern in patterns:
                match = re.search(pattern, mensaje)
                if match and not self.datos_recopilados.get("nombre_proyecto"):
                    self.datos_recopilados["nombre_proyecto"] = match.group(1).strip()
                    break

        # Extraer cliente
        if "cliente" in mensaje_lower or "empresa" in mensaje_lower:
            patterns = [
                r'cliente[:\s]+([A-Z][a-zA-ZáéíóúñÑ\s\.]+)',
                r'empresa[:\s]+([A-Z][a-zA-ZáéíóúñÑ\s\.]+)'
            ]
            for pattern in patterns:
                match = re.search(pattern, mensaje)
                if match and not self.datos_recopilados.get("cliente"):
                    self.datos_recopilados["cliente"] = match.group(1).strip()
                    break

        # Extraer duración
        duracion_match = re.search(r'(\d+)\s*días?', mensaje_lower)
        if duracion_match:
            self.datos_recopilados["duracion_dias"] = int(duracion_match.group(1))

        meses_match = re.search(r'(\d+)\s*mes(?:es)?', mensaje_lower)
        if meses_match:
            self.datos_recopilados["duracion_dias"] = int(meses_match.group(1)) * 30

        # Extraer presupuesto
        presupuesto_patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:dólares|usd|soles)',
            r'presupuesto[:\s]+(\d+(?:,\d{3})*(?:\.\d{2})?)'
        ]
        for pattern in presupuesto_patterns:
            match = re.search(pattern, mensaje_lower)
            if match and not self.datos_recopilados.get("presupuesto"):
                presupuesto_str = match.group(1).replace(",", "")
                self.datos_recopilados["presupuesto"] = float(presupuesto_str)
                break

        # Detectar confirmaciones
        confirmaciones = ["ok", "correcto", "sí", "si", "confirmo", "acepto", "está bien"]
        if any(conf in mensaje_lower for conf in confirmaciones):
            # Marcar última pregunta como confirmada
            if "duracion_sugerida" in mensaje_lower or len(self.datos_recopilados.get("duracion_dias", 0)) > 0:
                pass  # Ya está guardado

            if "presupuesto_sugerido" in mensaje_lower:
                pass  # Ya está guardado

            # Confirmar recursos, riesgos, hitos
            if not self.datos_recopilados.get("recursos_confirmados"):
                self.datos_recopilados["recursos_confirmados"] = True
            elif not self.datos_recopilados.get("riesgos_confirmados"):
                self.datos_recopilados["riesgos_confirmados"] = True
            elif not self.datos_recopilados.get("hitos_confirmados"):
                self.datos_recopilados["hitos_confirmados"] = True

        # Guardar descripción si es texto largo (>30 caracteres)
        if len(mensaje) > 30 and not self.datos_recopilados.get("descripcion"):
            # No es una confirmación simple
            if not any(conf in mensaje_lower for conf in confirmaciones):
                self.datos_recopilados["descripcion"] = mensaje

    def _estimar_duracion_simple(self, area: float, servicio: str) -> int:
        """Estima duración para proyecto simple"""

        # Base: 5m² por día
        duracion_base = area / 5

        # Factor por servicio
        factor = 1.0
        if servicio in ["electrico-industrial", "contraincendios"]:
            factor = 1.3
        elif servicio in ["domotica", "redes-cctv"]:
            factor = 1.2

        return max(15, int(duracion_base * factor))

    def _estimar_duracion_pmi(self, area: float, servicio: str) -> int:
        """Estima duración para proyecto PMI (más conservadora)"""

        duracion_simple = self._estimar_duracion_simple(area, servicio)

        # PMI requiere +30% de tiempo para planificación y gestión
        return int(duracion_simple * 1.3)

    def _generar_recursos_pmi(self, servicio: str, presupuesto: float) -> List[Dict[str, Any]]:
        """Genera equipo de recursos para PMI"""

        recursos = [
            {
                "rol": "Director de Proyecto (PMI)",
                "cantidad": 1,
                "dedicacion": "25%",
                "responsabilidad": "Dirección estratégica y gestión de stakeholders"
            },
            {
                "rol": "Jefe de Proyecto",
                "cantidad": 1,
                "dedicacion": "100%",
                "responsabilidad": "Coordinación general y seguimiento PMI"
            },
            {
                "rol": "Ingeniero Residente",
                "cantidad": 1,
                "dedicacion": "100%",
                "responsabilidad": "Ejecución técnica y supervisión en campo"
            },
            {
                "rol": "Ingeniero de Diseño",
                "cantidad": 1,
                "dedicacion": "50%",
                "responsabilidad": "Cálculos técnicos y planos"
            },
            {
                "rol": "Técnicos Especialistas",
                "cantidad": 4,
                "dedicacion": "100%",
                "responsabilidad": "Instalación y montaje"
            },
            {
                "rol": "Inspector de Calidad (PMI)",
                "cantidad": 1,
                "dedicacion": "50%",
                "responsabilidad": "Control de calidad y aseguramiento"
            },
            {
                "rol": "Especialista en Riesgos",
                "cantidad": 1,
                "dedicacion": "25%",
                "responsabilidad": "Gestión de riesgos y contingencias"
            }
        ]

        # Ajustar cantidad según presupuesto
        if presupuesto > 50000:
            recursos.append({
                "rol": "Coordinador de Adquisiciones",
                "cantidad": 1,
                "dedicacion": "50%",
                "responsabilidad": "Gestión de compras y logística"
            })

        return recursos

    def _generar_riesgos_pmi(self, servicio: str) -> List[Dict[str, Any]]:
        """Genera análisis de riesgos PMI"""

        riesgos = [
            {
                "riesgo": "Retrasos en entrega de materiales críticos",
                "probabilidad": "Media",
                "impacto": "Alto",
                "mitigacion": "Compra anticipada con proveedores certificados y backup"
            },
            {
                "riesgo": "Cambios en alcance del cliente",
                "probabilidad": "Alta",
                "impacto": "Alto",
                "mitigacion": "Control estricto de cambios y órdenes de variación"
            },
            {
                "riesgo": "Condiciones climáticas adversas",
                "probabilidad": "Media",
                "impacto": "Medio",
                "mitigacion": "Buffer de tiempo y medidas de protección"
            },
            {
                "riesgo": "Interferencias con otros contratistas",
                "probabilidad": "Media",
                "impacto": "Medio",
                "mitigacion": "Coordinación semanal y cronograma integrado"
            },
            {
                "riesgo": "Fallas técnicas en equipos especializados",
                "probabilidad": "Baja",
                "impacto": "Alto",
                "mitigacion": "Garantías extendidas y stock de repuestos críticos"
            }
        ]

        # Agregar riesgos específicos por servicio
        if servicio in ["electrico-industrial"]:
            riesgos.append({
                "riesgo": "Paros de planta durante instalación",
                "probabilidad": "Media",
                "impacto": "Crítico",
                "mitigacion": "Trabajo en horarios no productivos y plan de contingencia"
            })

        return riesgos

    def _generar_hitos_pmi(self, duracion_dias: int, servicio: str) -> List[Dict[str, Any]]:
        """Genera hitos del proyecto PMI"""

        hitos = [
            {
                "nombre": "Kickoff Meeting y Charter aprobado",
                "dia": 1,
                "descripcion": "Reunión de inicio y aprobación de charter del proyecto"
            },
            {
                "nombre": "Ingeniería de detalle completa",
                "dia": int(duracion_dias * 0.25),
                "descripcion": "Planos, cálculos y especificaciones aprobados"
            },
            {
                "nombre": "50% de ejecución completado",
                "dia": int(duracion_dias * 0.6),
                "descripcion": "Hito de avance medio del proyecto"
            },
            {
                "nombre": "Pruebas FAT completadas",
                "dia": int(duracion_dias * 0.85),
                "descripcion": "Factory Acceptance Tests aprobados"
            },
            {
                "nombre": "Puesta en marcha exitosa",
                "dia": int(duracion_dias * 0.95),
                "descripcion": "Sistema operativo y funcionando"
            },
            {
                "nombre": "Cierre de proyecto y lecciones aprendidas",
                "dia": duracion_dias,
                "descripcion": "Proyecto cerrado oficialmente con documentación"
            }
        ]

        return hitos

    def _calcular_metricas_pmi(self, presupuesto: float, duracion_dias: int) -> Dict[str, Any]:
        """Calcula métricas PMI (ROI, TIR, payback, etc.)"""

        # Cálculos estimados para proyectos eléctricos
        roi_estimado = 22  # %
        payback_meses = max(12, int(presupuesto / 2000))  # Estimación conservadora
        tir_proyectada = roi_estimado + 6  # %

        return {
            "roi_estimado": roi_estimado,
            "payback_meses": payback_meses,
            "tir_proyectada": tir_proyectada,
            "van_estimado": presupuesto * 0.18,  # Estimación VAN
            "indice_rentabilidad": 1.22,
            "cpi_objetivo": 1.0,  # Cost Performance Index
            "spi_objetivo": 1.0,  # Schedule Performance Index
            "margen_contingencia": 10,  # %
            "margen_gestion": 5  # %
        }


# ═══════════════════════════════════════════════════════════════
# 🏭 INSTANCIA SINGLETON
# ═══════════════════════════════════════════════════════════════

# Crear instancia única de PILIProyectos
pili_proyectos = PILIProyectos()

logger.info("🏗️ PILIProyectos listo para gestionar proyectos inteligentemente")


# ═══════════════════════════════════════════════════════════════
# 📚 EJEMPLO DE USO
# ═══════════════════════════════════════════════════════════════

"""
EJEMPLO DE USO:

from app.services.pili_proyectos import pili_proyectos

# Usuario inicia conversación
historial = []

# Paso 1: Usuario pregunta por proyecto
mensaje1 = "Necesito crear un proyecto complejo PMI"
response1 = pili_proyectos.procesar(mensaje1, historial)
print(response1["mensaje"])

# Paso 2: Usuario responde tipo
mensaje2 = "PMI"
response2 = pili_proyectos.procesar(mensaje2, historial)

# Paso 3: Usuario da nombre
mensaje3 = "Instalación Eléctrica Edificio Los Pinos"
response3 = pili_proyectos.procesar(mensaje3, historial)

# ... continúa la conversación hasta que puede_generar = True

# Resultado final: JSON completo del proyecto listo para generar Word/PDF
"""
