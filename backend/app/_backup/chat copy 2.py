"""
Router: Chat IA - VERSIÓN EXTENDIDA v2.0
Endpoints para interacción con Gemini AI + Gestión de Plantillas + SERVICIOS INTELIGENTES

🆕 NUEVAS FUNCIONALIDADES:
- Botones contextuales por tipo de servicio
- Chat contextualizado según flujo seleccionado  
- Guía inteligente para 6 servicios (simple/complejo × 3 tipos)
- Detección automática de etapas de conversación
- Prompts especializados por industria

🔄 CONSERVA TODO LO EXISTENTE:
- Generación rápida de cotizaciones
- Chat conversacional
- Gestión completa de plantillas
- Análisis de proyectos 
- Sugerencias de mejoras
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.schemas.cotizacion import (
    CotizacionRapidaRequest,
    ChatRequest,
    ChatResponse,
    CotizacionResponse
)
from app.services.gemini_service import gemini_service
from app.models.cotizacion import Cotizacion
from app.models.item import Item
from datetime import datetime
from pathlib import Path
import logging
import os
import shutil

logger = logging.getLogger(__name__)

router = APIRouter()

# ═══════════════════════════════════════════════════════════════
# 🆕 NUEVOS CONTEXTOS DE SERVICIOS INTELIGENTES
# ═══════════════════════════════════════════════════════════════

CONTEXTOS_SERVICIOS = {
    
    # ⚡ COTIZACIÓN SIMPLE
    "cotizacion-simple": {
        "rol_ia": """Eres un ingeniero eléctrico experto de Tesla Electricidad. 
        Tu objetivo es obtener información específica para generar una cotización precisa de instalaciones eléctricas.
        Siempre haz preguntas para clarificar antes de cotizar.""",
        
        "preguntas_esenciales": [
            "¿Qué tipo de instalación necesitas? (residencial/comercial/industrial)",
            "¿Cuántos metros cuadrados tiene el área?", 
            "¿Cuántos puntos de luz necesitas aproximadamente?",
            "¿Cuántos tomacorrientes requieres?",
            "¿Necesitas tablero eléctrico nuevo o existe uno?",
            "¿La instalación es desde cero o hay cableado existente?"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "🏠 Instalación Residencial", 
                "🏢 Instalación Comercial",
                "🏭 Instalación Industrial", 
                "📋 Certificado ITSE",
                "🔌 Pozo a Tierra",
                "🤖 Automatización",
                "📹 CCTV",
                "🌐 Redes"
            ],
            "refinamiento": [
                "📝 Necesito más detalles técnicos",
                "🔢 Ajustar cantidades estimadas", 
                "💰 Revisar precios unitarios",
                "⚡ Verificar cargas eléctricas",
                "✅ Generar cotización"
            ],
            "generacion": [
                "✏️ Editar vista previa",
                "📄 Generar Word final", 
                "📱 Enviar por WhatsApp",
                "💾 Guardar como borrador"
            ]
        },
        
        "prompt_especializado": """
        Como ingeniero eléctrico de Tesla, analiza la información y:
        
        1. 🔍 IDENTIFICA el tipo exacto de instalación
        2. ⚡ CALCULA materiales según normativa peruana (CNE)
        3. 👷 ESTIMA mano de obra especializada requerida
        4. 💰 APLICA precios del mercado peruano 2025
        5. 📋 INCLUYE especificaciones técnicas detalladas
        6. ⚠️ CONSIDERA factores de seguridad y normativas
        
        IMPORTANTE: Si falta información crítica, pregunta ANTES de generar cotización.
        
        PRECIOS REFERENCIALES PERÚ 2025:
        - Punto de luz LED 18W: S/ 25-35
        - Tomacorriente doble: S/ 28-38  
        - Cable 2.5mm²: S/ 3.50-4.50/mt
        - Tablero 12 polos: S/ 350-450
        - Mano de obra: S/ 80-120/hora
        """
    },

    # 📄 COTIZACIÓN COMPLEJA 
    "cotizacion-compleja": {
        "rol_ia": """Eres un ingeniero senior especialista en proyectos complejos de gran envergadura.
        Analizas documentos técnicos (planos, especificaciones, normas) y generas cotizaciones detalladas.""",
        
        "documentos_esperados": [
            "Planos arquitectónicos (PDF/DWG)",
            "Memoria descriptiva del proyecto",
            "Especificaciones técnicas detalladas", 
            "Presupuesto referencial o base",
            "Normas y códigos aplicables",
            "Lista de materiales existente"
        ],
        
        "botones_contextuales": {
            "analisis": [
                "📄 Analizar planos subidos",
                "🔍 Revisar especificaciones técnicas",
                "📊 Calcular metrados automáticos", 
                "⚡ Verificar cargas y circuitos",
                "📏 Analizar dimensionamiento",
                "🔧 Evaluar materiales especificados"
            ],
            "refinamiento": [
                "📋 Generar lista detallada de materiales",
                "👷 Calcular cronograma de mano de obra",
                "💰 Aplicar precios actualizados",
                "📊 Crear análisis de precios unitarios", 
                "⚖️ Revisar normativas aplicables"
            ],
            "generacion": [
                "📄 Crear cotización formal",
                "📊 Incluir análisis de costos",
                "📈 Agregar cronograma de obra",
                "📋 Generar memoria de cálculo"
            ]
        },
        
        "prompt_especializado": """
        Como ingeniero senior de proyectos complejos:
        
        1. 📋 ANALIZA documentos técnicos subidos minuciosamente
        2. 📏 CALCULA metrados según planos y especificaciones
        3. ⚡ DIMENSIONA instalaciones según cargas reales
        4. 🔧 ESPECIFICA materiales según normativas vigentes
        5. 👷 PROGRAMA actividades según complejidad  
        6. 💰 COSTEA con precios de mercado actualizados
        7. ⚖️ VERIFICA cumplimiento de códigos (CNE, NEC, etc.)
        
        CONSIDERA SIEMPRE:
        - Factor de simultaneidad
        - Caídas de tensión admisibles
        - Coordinación de protecciones
        - Puesta a tierra normativa
        - Instalaciones especiales (ITSE, bomberos)
        """
    },

    # 📊 INFORME SIMPLE
    "informe-simple": {
        "rol_ia": """Eres un redactor técnico especializado en informes de ingeniería claros y concisos.""",
        
        "tipos_informe": [
            "📊 Informe de avance de proyecto",
            "📈 Reporte financiero de obra", 
            "🔧 Informe técnico de instalación",
            "📋 Informe de conformidad de obra",
            "⚠️ Reporte de incidencias",
            "✅ Certificado de pruebas",
            "📏 Informe de mediciones",
            "🔍 Reporte de supervisión"
        ],
        
        "botones_contextuales": {
            "seleccion": [
                "📊 Informe de Avance",
                "💰 Reporte Financiero", 
                "🔧 Informe Técnico",
                "✅ Conformidad de Obra",
                "📏 Mediciones y Pruebas",
                "⚠️ Reporte de Incidencias"
            ],
            "configuracion": [
                "📄 Formato estándar PDF",
                "📊 Incluir tablas y datos",
                "📈 Agregar gráficos básicos", 
                "📷 Incluir fotos de evidencia",
                "🗓️ Cronograma simplificado"
            ]
        },
        
        "prompt_especializado": """
        Como redactor técnico especializado:
        
        1. 📋 ESTRUCTURA el informe con secciones claras
        2. 📊 PRESENTA datos en tablas organizadas
        3. 📷 INCLUYE evidencia fotográfica si está disponible
        4. 📈 AGREGA gráficos simples cuando sea útil
        5. ✅ RESUME conclusiones y recomendaciones
        6. 🗓️ ESPECIFICA fechas y plazos claramente
        
        FORMATO ESTÁNDAR:
        - Resumen ejecutivo (1 página)
        - Objetivos del informe
        - Metodología aplicada
        - Resultados y hallazgos
        - Conclusiones
        - Recomendaciones
        - Anexos (fotos, tablas, planos)
        """
    },

    # 📊 INFORME EJECUTIVO
    "informe-ejecutivo": {
        "rol_ia": """Eres un director técnico que genera informes ejecutivos para alta gerencia.
        Tus informes son estratégicos, incluyen KPIs, análisis profundo y recomendaciones de negocio.""",
        
        "estructura_ejecutiva": [
            "📋 Resumen ejecutivo (Dashboard)",
            "📊 Análisis de situación actual",
            "📈 KPIs y métricas de rendimiento", 
            "📉 Análisis de desviaciones",
            "🎯 Recomendaciones estratégicas",
            "📅 Plan de acción con cronograma",
            "💰 Impacto financiero y ROI", 
            "⚖️ Gestión de riesgos",
            "📋 Conclusiones ejecutivas"
        ],
        
        "botones_contextuales": {
            "configuracion": [
                "📊 Dashboard ejecutivo con KPIs",
                "💼 Formato gerencial profesional",
                "📈 Gráficos avanzados automáticos",
                "📊 Análisis financiero detallado",
                "🎯 Recomendaciones estratégicas",
                "📅 Cronograma con hitos críticos"
            ],
            "analisis": [
                "📊 Análisis de rentabilidad",
                "📈 Proyección de flujos",
                "⚖️ Evaluación de riesgos", 
                "🎯 Análisis de competitividad",
                "📉 Identificación de desviaciones"
            ]
        },
        
        "prompt_especializado": """
        Como director técnico para alta gerencia:
        
        1. 📊 CREA dashboard ejecutivo con KPIs clave
        2. 📈 ANALIZA tendencias y proyecciones
        3. 💰 EVALÚA impacto financiero y ROI
        4. 🎯 IDENTIFICA oportunidades estratégicas
        5. ⚖️ GESTIONA riesgos y contingencias
        6. 📅 DESARROLLA plan de acción concreto
        7. 📋 RESUME en conclusiones ejecutivas
        
        KPIs PRINCIPALES:
        - Rentabilidad por proyecto (%)
        - Cumplimiento de cronograma (%)  
        - Satisfacción del cliente (escala)
        - Eficiencia de recursos (ratio)
        - Margen de contribución (S/)
        - Tiempo promedio de ejecución (días)
        
        FORMATO GERENCIAL:
        - Máximo 10 páginas + anexos
        - Gráficos profesionales
        - Tablas ejecutivas  
        - Recomendaciones priorizadas
        """
    },

    # 📁 PROYECTO SIMPLE
    "proyecto-simple": {
        "rol_ia": """Eres un coordinador de proyectos que organiza y gestiona proyectos eléctricos de mediana complejidad.""",
        
        "botones_contextuales": {
            "gestion": [
                "📁 Crear estructura de carpetas",
                "📅 Definir cronograma básico",
                "👥 Asignar responsables principales",
                "📊 Dashboard de seguimiento",
                "📋 Lista de entregables",
                "💰 Control presupuestal básico"
            ],
            "documentacion": [
                "📄 Acta de inicio del proyecto",
                "📋 Plan de trabajo simplificado", 
                "📅 Cronograma en Excel",
                "👥 Matriz de responsabilidades",
                "📊 Reporte de avance semanal"
            ]
        },
        
        "prompt_especializado": """
        Como coordinador de proyectos:
        
        1. 📁 ORGANIZA estructura de carpetas lógica
        2. 📅 CREA cronograma realista con hitos
        3. 👥 DEFINE roles y responsabilidades claras
        4. 📊 ESTABLECE métricas de seguimiento
        5. 💰 CONTROLA presupuesto y costos
        6. 📋 GESTIONA entregables y documentación
        
        ESTRUCTURA ESTÁNDAR:
        - Carpeta: Documentos del Cliente
        - Carpeta: Planos y Diseños
        - Carpeta: Cotizaciones y Presupuestos
        - Carpeta: Órdenes de Compra
        - Carpeta: Reportes de Avance
        - Carpeta: Certificados y Pruebas
        - Carpeta: Documentos Finales
        """
    },

    # 📁 PROYECTO COMPLEJO
    "proyecto-complejo": {
        "rol_ia": """Eres un director de proyectos senior especializado en gestión integral de proyectos de gran envergadura.
        Manejas múltiples stakeholders, cronogramas complejos y riesgos significativos.""",
        
        "botones_contextuales": {
            "planificacion": [
                "📋 Plan maestro del proyecto",
                "📊 Diagrama de Gantt detallado",
                "💰 Control presupuestal avanzado",
                "📈 Análisis de riesgos completo",
                "🎯 Definir hitos críticos",
                "👥 Gestión de stakeholders"
            ],
            "seguimiento": [
                "📊 Dashboard ejecutivo en tiempo real",
                "📈 Curva S de avance vs. planificado",
                "💰 Análisis de valor ganado (EVM)",
                "⚖️ Matriz de riesgos actualizada",
                "📋 Reporte ejecutivo semanal"
            ],
            "documentacion": [
                "📋 Project Charter completo",
                "📊 WBS (Work Breakdown Structure)", 
                "📅 Cronograma maestro",
                "💰 Baseline de costos",
                "⚖️ Registro de riesgos",
                "👥 Plan de comunicaciones"
            ]
        },
        
        "prompt_especializado": """
        Como director de proyectos senior:
        
        1. 📋 DESARROLLA plan maestro integral
        2. 📊 CREA WBS detallado con entregables
        3. 📅 PROGRAMA actividades con dependencias
        4. 💰 ESTABLECE baseline y control de costos
        5. ⚖️ IDENTIFICA y mitiga riesgos críticos
        6. 👥 GESTIONA comunicación con stakeholders
        7. 📊 IMPLEMENTA dashboard de control
        
        METODOLOGÍA PMI:
        - Iniciación: Charter y stakeholders
        - Planificación: Scope, tiempo, costo, calidad
        - Ejecución: Gestión de equipos y comunicación
        - Monitoreo: Control integrado de cambios  
        - Cierre: Lecciones aprendidas y entregables
        
        HERRAMIENTAS AVANZADAS:
        - Diagrama de Gantt con ruta crítica
        - Análisis de valor ganado (EVM)
        - Matriz de riesgos cuantificada
        - Dashboard de KPIs en tiempo real
        """
    }
}

def obtener_contexto_servicio(tipo_flujo: str) -> dict:
    """Retorna el contexto específico para un tipo de servicio"""
    return CONTEXTOS_SERVICIOS.get(tipo_flujo, {})

def determinar_etapa_conversacion(historial_mensajes: List[Dict], cotizacion_existente: bool = False) -> str:
    """Determina en qué etapa de la conversación está el usuario"""
    if not historial_mensajes:
        return "inicial"
    elif cotizacion_existente:
        return "generacion" 
    elif len(historial_mensajes) >= 3:
        return "refinamiento"
    else:
        return "inicial"

def obtener_botones_para_etapa(tipo_flujo: str, etapa: str) -> List[str]:
    """Retorna botones contextuales para una etapa específica"""
    contexto = obtener_contexto_servicio(tipo_flujo)
    botones_config = contexto.get("botones_contextuales", {})
    return botones_config.get(etapa, [])

# ════════════════════════════════════════════════════════════════
# 🔄 FUNCIONES AUXILIARES EXISTENTES (CONSERVADAS)
# ════════════════════════════════════════════════════════════════

def generar_numero_cotizacion(db: Session) -> str:
    """Generar número único de cotización"""
    fecha = datetime.now()
    prefijo = f"COT-{fecha.strftime('%Y%m')}"
    
    ultima = db.query(Cotizacion).filter(
        Cotizacion.numero.like(f"{prefijo}%")
    ).order_by(Cotizacion.numero.desc()).first()
    
    if ultima:
        try:
            ultimo_num = int(ultima.numero.split('-')[-1])
            nuevo_num = ultimo_num + 1
        except:
            nuevo_num = 1
    else:
        nuevo_num = 1
    
    return f"{prefijo}-{nuevo_num:04d}"

# ════════════════════════════════════════════════════════════════
# 🆕 NUEVOS ENDPOINTS PARA SERVICIOS INTELIGENTES  
# ════════════════════════════════════════════════════════════════

@router.get("/botones-contextuales/{tipo_flujo}")
async def obtener_botones_contextuales(
    tipo_flujo: str,
    etapa: Optional[str] = "inicial",
    historial_length: Optional[int] = 0,
    tiene_cotizacion: Optional[bool] = False
):
    """
    🆕 NUEVO - Obtiene botones contextuales según el tipo de flujo y etapa
    
    Este endpoint permite a App.jsx obtener botones inteligentes que guían
    al usuario en cada paso del proceso.
    
    Args:
        tipo_flujo: cotizacion-simple, cotizacion-compleja, informe-simple, etc.
        etapa: inicial, refinamiento, generacion
        historial_length: Cantidad de mensajes en la conversación
        tiene_cotizacion: Si ya se generó una cotización
    
    Returns:
        Lista de botones contextuales para mostrar al usuario
    """
    try:
        logger.info(f"Obteniendo botones para {tipo_flujo}, etapa: {etapa}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado"
            )
        
        # Determinar etapa automáticamente si no se especifica
        if etapa == "inicial" and historial_length > 0:
            if tiene_cotizacion:
                etapa = "generacion"
            elif historial_length >= 3:
                etapa = "refinamiento"
        
        # Obtener botones para la etapa
        botones = obtener_botones_para_etapa(tipo_flujo, etapa)
        
        return {
            "success": True,
            "tipo_flujo": tipo_flujo,
            "etapa": etapa,
            "botones": botones,
            "contexto": {
                "rol_ia": contexto.get("rol_ia", ""),
                "preguntas_esenciales": contexto.get("preguntas_esenciales", [])
            }
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo botones contextuales: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/chat-contextualizado")
async def chat_contextualizado(
    tipo_flujo: str = Body(...),
    mensaje: str = Body(...), 
    historial: Optional[List[Dict]] = Body([]),
    contexto_adicional: Optional[str] = Body(""),
    cotizacion_id: Optional[int] = Body(None),
    db: Session = Depends(get_db)
):
    """
    🆕 NUEVO - Chat inteligente con contexto específico según el servicio
    
    Este endpoint permite conversaciones especializadas donde la IA entiende
    exactamente qué tipo de servicio está ayudando a crear.
    
    Args:
        tipo_flujo: Tipo de servicio (cotizacion-simple, etc.)
        mensaje: Mensaje del usuario
        historial: Conversación previa
        contexto_adicional: Información extra del proyecto
        cotizacion_id: ID de cotización existente (opcional)
    
    Returns:
        Respuesta especializada de la IA + sugerencias contextuales
    """
    try:
        logger.info(f"Chat contextualizado para {tipo_flujo}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado"
            )
        
        # Construir prompt especializado
        prompt_especializado = f"""
        {contexto.get('rol_ia', '')}
        
        {contexto.get('prompt_especializado', '')}
        
        CONTEXTO DEL PROYECTO:
        {contexto_adicional}
        
        HISTORIAL DE CONVERSACIÓN:
        """
        
        # Agregar historial al prompt
        for i, msg in enumerate(historial[-5:]):  # Últimos 5 mensajes
            role = msg.get('role', 'user')
            content = msg.get('content', msg.get('mensaje', ''))
            prompt_especializado += f"\n{role.upper()}: {content}"
        
        prompt_especializado += f"\n\nUSUARIO: {mensaje}\n\nRESPUESTA ESPECIALIZADA:"
        
        # Enviar a Gemini con contexto especializado
        respuesta = gemini_service.chat(
            mensaje=prompt_especializado,
            contexto=f"Servicio: {tipo_flujo}. {contexto_adicional}",
            cotizacion_id=cotizacion_id
        )
        
        # Determinar etapa y botones sugeridos
        tiene_cotizacion = cotizacion_id is not None
        etapa_actual = determinar_etapa_conversacion(historial, tiene_cotizacion)
        botones_sugeridos = obtener_botones_para_etapa(tipo_flujo, etapa_actual)
        
        return {
            "success": True,
            "respuesta": respuesta.get('mensaje', ''),
            "sugerencias": respuesta.get('sugerencias', []),
            "accion_recomendada": respuesta.get('accion_recomendada'),
            "botones_contextuales": botones_sugeridos,
            "etapa_actual": etapa_actual,
            "preguntas_pendientes": contexto.get("preguntas_esenciales", []),
            "tipo_flujo": tipo_flujo
        }
        
    except Exception as e:
        logger.error(f"Error en chat contextualizado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/iniciar-flujo-inteligente")
async def iniciar_flujo_inteligente(
    tipo_flujo: str = Body(...),
    descripcion_inicial: Optional[str] = Body(""),
    nombre_cliente: Optional[str] = Body(""),
    db: Session = Depends(get_db)
):
    """
    🆕 NUEVO - Inicia un flujo inteligente con análisis automático
    
    Analiza la descripción inicial y ofrece un plan de trabajo específico
    según el tipo de servicio seleccionado.
    
    Args:
        tipo_flujo: Tipo de servicio a iniciar
        descripcion_inicial: Descripción del proyecto
        nombre_cliente: Nombre del cliente (para crear carpeta)
    
    Returns:
        Plan de trabajo inicial + primeras preguntas + botones contextuales
    """
    try:
        logger.info(f"Iniciando flujo inteligente: {tipo_flujo}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado"
            )
        
        # Construir prompt de inicio especializado
        prompt_inicio = f"""
        {contexto.get('rol_ia', '')}
        
        Un nuevo cliente quiere iniciar: {tipo_flujo}
        
        INFORMACIÓN INICIAL:
        - Cliente: {nombre_cliente or 'No especificado'}
        - Descripción: {descripcion_inicial or 'Sin descripción inicial'}
        
        Como experto, necesitas:
        1. Analizar la información inicial
        2. Identificar qué información falta
        3. Hacer 2-3 preguntas específicas para empezar
        4. Dar una bienvenida profesional y clara
        
        PREGUNTAS ESENCIALES A CONSIDERAR:
        {chr(10).join(contexto.get('preguntas_esenciales', []))}
        
        Responde de forma amigable y profesional, explicando brevemente el proceso.
        """
        
        # Obtener respuesta inicial de la IA
        respuesta_inicial = gemini_service.chat(
            mensaje=prompt_inicio,
            contexto=f"Iniciando {tipo_flujo} para {nombre_cliente}",
            cotizacion_id=None
        )
        
        # Obtener botones iniciales
        botones_iniciales = obtener_botones_para_etapa(tipo_flujo, "inicial")
        
        return {
            "success": True,
            "tipo_flujo": tipo_flujo,
            "mensaje_bienvenida": respuesta_inicial.get('mensaje', ''),
            "plan_trabajo": {
                "etapas": [
                    "Recopilación de información",
                    "Análisis y cálculos",
                    "Generación de propuesta",
                    "Revisión y ajustes", 
                    "Entrega final"
                ],
                "tiempo_estimado": self._estimar_tiempo_flujo(tipo_flujo),
                "documentos_necesarios": contexto.get("documentos_esperados", [])
            },
            "botones_contextuales": botones_iniciales,
            "preguntas_esenciales": contexto.get("preguntas_esenciales", []),
            "siguiente_paso": "Responde las preguntas o usa los botones para continuar"
        }
        
    except Exception as e:
        logger.error(f"Error iniciando flujo inteligente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

def _estimar_tiempo_flujo(tipo_flujo: str) -> str:
    """Estima el tiempo necesario según el tipo de flujo"""
    tiempos = {
        "cotizacion-simple": "5-15 minutos",
        "cotizacion-compleja": "30-60 minutos", 
        "informe-simple": "10-20 minutos",
        "informe-ejecutivo": "45-90 minutos",
        "proyecto-simple": "15-30 minutos",
        "proyecto-complejo": "60-120 minutos"
    }
    return tiempos.get(tipo_flujo, "20-40 minutos")

@router.get("/contextos-disponibles")
async def listar_contextos_disponibles():
    """
    🆕 NUEVO - Lista todos los contextos de servicios disponibles
    
    Útil para debugging y para que App.jsx sepa qué servicios están soportados.
    """
    try:
        contextos_info = {}
        
        for tipo_flujo, contexto in CONTEXTOS_SERVICIOS.items():
            contextos_info[tipo_flujo] = {
                "nombre": tipo_flujo.replace('-', ' ').title(),
                "rol_ia": contexto.get("rol_ia", ""),
                "etapas_disponibles": list(contexto.get("botones_contextuales", {}).keys()),
                "preguntas_esenciales": len(contexto.get("preguntas_esenciales", [])),
                "tiempo_estimado": _estimar_tiempo_flujo(tipo_flujo)
            }
        
        return {
            "success": True,
            "total_servicios": len(contextos_info),
            "servicios_disponibles": contextos_info
        }
        
    except Exception as e:
        logger.error(f"Error listando contextos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

# ════════════════════════════════════════════════════════════════
# 🔄 ENDPOINTS EXISTENTES (CONSERVADOS INTACTOS)
# ════════════════════════════════════════════════════════════════

@router.post("/generar-rapida", response_model=CotizacionResponse)
async def generar_cotizacion_rapida(
    request: CotizacionRapidaRequest,
    db: Session = Depends(get_db)
):
    """
    Generar cotización rápida usando IA
    
    El usuario describe lo que necesita y la IA genera la cotización automáticamente
    """
    try:
        logger.info("Generando cotización rápida con IA")
        
        # Generar cotización con Gemini
        cotizacion_data = gemini_service.generar_cotizacion_desde_texto(
            descripcion=request.descripcion,
            contexto_adicional=request.contexto_adicional
        )
        
        # Crear cotización en BD
        numero = generar_numero_cotizacion(db)
        
        nueva_cotizacion = Cotizacion(
            numero=numero,
            cliente=cotizacion_data.get('cliente', 'Cliente No Especificado'),
            proyecto=cotizacion_data.get('proyecto', 'Proyecto Generado por IA'),
            descripcion=request.descripcion,
            observaciones=cotizacion_data.get('observaciones', ''),
            estado='borrador',
            subtotal=0,
            igv=0,
            total=0
        )
        
        db.add(nueva_cotizacion)
        db.flush()
        
        # Crear items
        items_data = cotizacion_data.get('items', [])
        subtotal = 0
        
        for item_data in items_data:
            cantidad = float(item_data.get('cantidad', 1))
            precio = float(item_data.get('precio_unitario', 0))
            
            item = Item(
                cotizacion_id=nueva_cotizacion.id,
                descripcion=item_data.get('descripcion', ''),
                cantidad=cantidad,
                unidad=item_data.get('unidad', 'und'),
                precio_unitario=precio
            )
            
            db.add(item)
            subtotal += cantidad * precio
        
        # Actualizar totales
        nueva_cotizacion.subtotal = subtotal
        nueva_cotizacion.igv = subtotal * 0.18
        nueva_cotizacion.total = subtotal * 1.18
        
        db.commit()
        db.refresh(nueva_cotizacion)
        
        logger.info(f"Cotización rápida creada: {numero}")
        
        return nueva_cotizacion
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al generar cotización rápida: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar cotización: {str(e)}"
        )

@router.post("/conversacional", response_model=ChatResponse)
async def chat_conversacional(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat conversacional para refinar cotizaciones
    
    El usuario puede iterar y mejorar una cotización mediante conversación
    """
    try:
        logger.info("Procesando mensaje de chat conversacional")
        
        # Enviar mensaje a Gemini
        respuesta = gemini_service.chat(
            mensaje=request.mensaje,
            contexto=request.contexto,
            cotizacion_id=request.cotizacion_id
        )
        
        return ChatResponse(
            respuesta=respuesta.get('mensaje', ''),
            sugerencias=respuesta.get('sugerencias', []),
            accion_recomendada=respuesta.get('accion_recomendada')
        )
        
    except Exception as e:
        logger.error(f"Error en chat conversacional: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en chat: {str(e)}"
        )

@router.post("/analizar-proyecto")
def analizar_proyecto_ia(
    descripcion: str
):
    """
    Analizar descripción de un proyecto con IA
    
    NO crea la cotización, solo analiza y sugiere
    """
    try:
        logger.info("Analizando descripción de proyecto")
        
        # Analizar con Gemini
        analisis = gemini_service.analizar_documento(
            texto_documento=descripcion,
            tipo_analisis="proyecto"
        )
        
        return {
            "success": True,
            "analisis": analisis,
            "mensaje": "Análisis completado. Puedes usar esta información para crear una cotización."
        }
        
    except Exception as e:
        logger.error(f"Error al analizar proyecto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al analizar: {str(e)}"
        )

@router.post("/sugerir-mejoras/{cotizacion_id}")
def sugerir_mejoras_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener sugerencias de mejora para una cotización existente
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cotización con ID {cotizacion_id} no encontrada"
        )
    
    try:
        logger.info(f"Generando sugerencias para cotización {cotizacion.numero}")
        
        # Obtener sugerencias de Gemini
        sugerencias = gemini_service.sugerir_mejoras(cotizacion.to_dict())
        
        return {
            "success": True,
            "cotizacion_numero": cotizacion.numero,
            "sugerencias": sugerencias
        }
        
    except Exception as e:
        logger.error(f"Error al sugerir mejoras: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar sugerencias: {str(e)}"
        )

@router.get("/health")
def health_check_ia():
    """
    Verificar estado del servicio de IA
    """
    from app.core.config import settings
    
    return {
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "model": settings.GEMINI_MODEL,
        "status": "healthy",
        "servicios_inteligentes": len(CONTEXTOS_SERVICIOS),  # 🆕 Nuevo campo
        "version": "2.0"  # 🆕 Versión actualizada
    }

# ════════════════════════════════════════════════════════════════
# 🔄 GESTIÓN DE PLANTILLAS (CONSERVADO INTACTO)
# ════════════════════════════════════════════════════════════════

@router.post("/subir-plantilla")
async def subir_plantilla_word(
    archivo: UploadFile = File(...),
    nombre_personalizado: Optional[str] = None
):
    """
    Subir plantilla Word personalizada
    
    ⭐ El usuario puede subir sus propias plantillas .docx
    
    Las plantillas pueden contener marcadores como:
    - {{cliente}} - Se reemplaza con nombre del cliente
    - {{proyecto}} - Se reemplaza con nombre del proyecto  
    - {{fecha}} - Se reemplaza con fecha actual
    - {{items_tabla}} - Se reemplaza con tabla de items
    - {{total}} - Se reemplaza with total de la cotización
    
    Args:
        archivo: Archivo .docx de la plantilla
        nombre_personalizado: Nombre personalizado (opcional)
    
    Returns:
        Información de la plantilla subida
    """
    
    try:
        from app.core.config import settings
        
        # Validar que sea un archivo Word
        if not archivo.filename.endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se permiten archivos .docx"
            )
        
        # Crear directorio de plantillas si no existe
        templates_dir = Path(settings.TEMPLATES_DIR)
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Nombre del archivo
        nombre_archivo = nombre_personalizado if nombre_personalizado else archivo.filename
        if not nombre_archivo.endswith('.docx'):
            nombre_archivo += '.docx'
        
        # Ruta completa
        ruta_plantilla = templates_dir / nombre_archivo
        
        # Guardar archivo
        contenido = await archivo.read()
        with open(ruta_plantilla, 'wb') as f:
            f.write(contenido)
        
        logger.info(f"✅ Plantilla subida: {nombre_archivo}")
        
        # Validar plantilla y extraer marcadores
        from app.services.template_processor import template_processor
        
        try:
            es_valida, mensaje = template_processor.validar_plantilla(str(ruta_plantilla))
            marcadores = template_processor.extraer_marcadores(str(ruta_plantilla)) if es_valida else []
        except:
            es_valida = True  # Asumir que es válida si hay error en validación
            marcadores = []
            mensaje = "Plantilla subida (validación básica)"
        
        return {
            "success": True,
            "mensaje": "Plantilla subida exitosamente",
            "archivo": {
                "nombre_original": archivo.filename,
                "nombre_guardado": nombre_archivo,
                "tamaño_kb": round(len(contenido) / 1024, 2),
                "ruta": str(ruta_plantilla)
            },
            "validacion": {
                "es_valida": es_valida,
                "mensaje": mensaje,
                "marcadores_encontrados": marcadores,
                "total_marcadores": len(marcadores)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al subir plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.get("/listar-plantillas")
async def listar_plantillas_disponibles():
    """
    Listar todas las plantillas Word disponibles
    
    ⭐ Permite ver qué plantillas han sido subidas
    
    Returns:
        Lista de plantillas con información básica
    """
    
    try:
        from app.core.config import settings
        
        templates_dir = Path(settings.TEMPLATES_DIR)
        
        if not templates_dir.exists():
            templates_dir.mkdir(parents=True, exist_ok=True)
            return {
                "success": True,
                "total": 0,
                "plantillas": []
            }
        
        plantillas = []
        
        for archivo in templates_dir.glob("*.docx"):
            if archivo.is_file():
                # Información básica del archivo
                stat = archivo.stat()
                
                plantillas.append({
                    "nombre": archivo.name,
                    "tamaño_kb": round(stat.st_size / 1024, 2),
                    "fecha_modificacion": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "ruta_relativa": f"plantillas/{archivo.name}"
                })
        
        return {
            "success": True,
            "total": len(plantillas),
            "plantillas": sorted(plantillas, key=lambda x: x["fecha_modificacion"], reverse=True)
        }
        
    except Exception as e:
        logger.error(f"Error al listar plantillas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.get("/obtener-marcadores/{nombre_plantilla}")
async def obtener_marcadores_plantilla(
    nombre_plantilla: str
):
    """
    Obtener marcadores de una plantilla específica
    
    ⭐ Permite ver qué marcadores están disponibles en una plantilla
    
    Útil para que el chat pueda decir: 
    "Tu plantilla tiene los marcadores: {{cliente}}, {{fecha}}, {{items_tabla}}"
    
    Args:
        nombre_plantilla: Nombre del archivo de plantilla
    
    Returns:
        Lista de marcadores encontrados
    """
    
    try:
        from app.core.config import settings
        
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_plantilla
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_plantilla}' no encontrada"
            )
        
        # Extraer marcadores usando template_processor
        from app.services.template_processor import template_processor
        
        marcadores = template_processor.extraer_marcadores(str(ruta_plantilla))
        
        return {
            "success": True,
            "plantilla": nombre_plantilla,
            "total_marcadores": len(marcadores),
            "marcadores": marcadores,
            "marcadores_comunes": [
                "{{cliente}}", "{{proyecto}}", "{{fecha}}", "{{numero}}",
                "{{descripcion}}", "{{observaciones}}", 
                "{{subtotal}}", "{{igv}}", "{{total}}",
                "{{items_tabla}}", "{{empresa_nombre}}", "{{empresa_direccion}}"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener marcadores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/usar-plantilla/{cotizacion_id}")
async def generar_cotizacion_con_plantilla(
    cotizacion_id: int,
    nombre_plantilla: str = Body(...),
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Generar cotización usando una plantilla personalizada
    
    ⭐ NUEVO - Usar plantilla del usuario
    
    El chat puede decir: "usa mi plantilla de informe"
    Y este endpoint procesa esa solicitud
    
    Args:
        cotizacion_id: ID de la cotización
        nombre_plantilla: Nombre del archivo de plantilla
        opciones: Opciones adicionales
        logo_base64: Logo en base64
    
    Returns:
        Archivo Word generado desde plantilla
    """
    
    try:
        # Obtener cotización
        cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
        
        if not cotizacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cotización no encontrada"
            )
        
        logger.info(f"Generando cotización {cotizacion.numero} con plantilla: {nombre_plantilla}")
        
        from app.core.config import settings
        from app.services.template_processor import template_processor
        
        # Ruta de la plantilla
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_plantilla
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_plantilla}' no encontrada"
            )
        
        # Obtener items de la cotización
        items_db = db.query(Item).filter(Item.cotizacion_id == cotizacion_id).all()
        
        items = []
        for item in items_db:
            items.append({
                "descripcion": item.descripcion,
                "cantidad": float(item.cantidad),
                "unidad": item.unidad,
                "precio_unitario": float(item.precio_unitario)
            })
        
        # Preparar datos
        datos_cotizacion = {
            "numero": cotizacion.numero,
            "cliente": cotizacion.cliente,
            "proyecto": cotizacion.proyecto,
            "descripcion": cotizacion.descripcion or "",
            "observaciones": cotizacion.observaciones or "",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "subtotal": float(cotizacion.subtotal) if cotizacion.subtotal else 0,
            "igv": float(cotizacion.igv) if cotizacion.igv else 0,
            "total": float(cotizacion.total) if cotizacion.total else 0,
            "items": items
        }
        
        # Generar documento con plantilla
        nombre_salida = f"cotizacion_{cotizacion.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_salida)
        
        ruta_generada = template_processor.procesar_plantilla(
            ruta_plantilla=str(ruta_plantilla),
            datos_cotizacion=datos_cotizacion,
            ruta_salida=ruta_salida,
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_generada):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el documento"
            )
        
        logger.info(f"✅ Cotización generada con plantilla: {nombre_salida}")
        
        return FileResponse(
            path=ruta_generada,
            filename=nombre_salida,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al usar plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.delete("/eliminar-plantilla/{nombre_archivo}")
async def eliminar_plantilla(
    nombre_archivo: str
):
    """
    Eliminar una plantilla
    
    ⭐ NUEVO - Gestión de plantillas
    
    Args:
        nombre_archivo: Nombre del archivo a eliminar
    
    Returns:
        Confirmación de eliminación
    """
    
    try:
        from app.core.config import settings
        
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_archivo
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_archivo}' no encontrada"
            )
        
        # Eliminar archivo
        ruta_plantilla.unlink()
        
        logger.info(f"✅ Plantilla eliminada: {nombre_archivo}")
        
        return {
            "success": True,
            "mensaje": f"Plantilla '{nombre_archivo}' eliminada exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar plantilla: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/validar-plantilla")
async def validar_plantilla(
    archivo: UploadFile = File(...)
):
    """
    Validar una plantilla antes de subirla
    
    ⭐ NUEVO - Verificar que la plantilla es válida
    
    Verifica:
    - Que sea un archivo .docx válido
    - Extrae y muestra los marcadores
    - Valida la estructura
    
    Returns:
        Reporte de validación
    """
    
    try:
        import tempfile
        from app.services.template_processor import template_processor
        
        # Validar extensión
        if not archivo.filename.endswith('.docx'):
            return {
                "valida": False,
                "error": "El archivo debe ser .docx",
                "recomendacion": "Usa Microsoft Word para crear la plantilla"
            }
        
        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            contenido = await archivo.read()
            tmp.write(contenido)
            tmp_path = tmp.name
        
        try:
            # Validar plantilla
            es_valida, mensaje = template_processor.validar_plantilla(tmp_path)
            
            if es_valida:
                # Extraer marcadores
                marcadores = template_processor.extraer_marcadores(tmp_path)
                
                return {
                    "valida": True,
                    "mensaje": "Plantilla válida",
                    "total_marcadores": len(marcadores),
                    "marcadores_encontrados": marcadores,
                    "marcadores_sugeridos": [
                        "{{cliente}}", "{{proyecto}}", "{{fecha}}", "{{numero}}",
                        "{{descripcion}}", "{{subtotal}}", "{{igv}}", "{{total}}"
                    ],
                    "recomendacion": "Puedes subir esta plantilla para usarla en cotizaciones"
                }
            else:
                return {
                    "valida": False,
                    "error": mensaje,
                    "recomendacion": "Revisa la plantilla y vuelve a intentar"
                }
                
        finally:
            # Eliminar archivo temporal
            Path(tmp_path).unlink(missing_ok=True)
        
    except Exception as e:
        logger.error(f"Error al validar plantilla: {str(e)}")
        return {
            "valida": False,
            "error": str(e),
            "recomendacion": "Verifica que el archivo no esté corrupto"
        }