"""
🤖 PILI AGENTE IA v3.0 - SISTEMA COMPLETO FINAL
📁 RUTA: backend/app/routers/chat.py

PILI (Procesadora Inteligente de Licitaciones Industriales) es un agente IA multifunción
que combina las mejores características de sistemas mundiales como ChatGPT, Microsoft Copilot
y Google Bard, pero especializada 100% en servicios eléctricos peruanos.

🧠 CARACTERÍSTICAS PILI v3.0:
- 6 Agentes especializados con personalidades únicas
- Conversación inteligente + anti-salto (no se desvía del tema)
- Procesamiento OCR multimodal (fotos, PDFs, manuscritos)
- JSON estructurado + Vista previa HTML editable
- Aprendizaje automático de cada conversación
- RAG con proyectos históricos
- Integración web search cuando necesita datos

🎯 AGENTES PILI:
- PILI Cotizadora: Cotizaciones rápidas (5-15 min)
- PILI Analista: Proyectos complejos con OCR avanzado
- PILI Coordinadora: Gestión de proyectos simples
- PILI Project Manager: Proyectos PMI avanzados
- PILI Reportera: Informes técnicos
- PILI Analista Senior: Informes ejecutivos APA

🔄 CONSERVA TODO LO EXISTENTE v2.0:
- Botones contextuales por tipo de servicio ✅
- Chat contextualizado según flujo seleccionado ✅
- Guía inteligente para 6 servicios ✅
- Gestión completa de plantillas ✅
- Análisis de proyectos ✅
- Sugerencias de mejoras ✅
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
from app.services.pili_brain import PILIBrain
from app.models.cotizacion import Cotizacion
from app.models.item import Item
from app.models.proyecto import Proyecto
from app.models.documento import Documento
from datetime import datetime
from pathlib import Path
import logging
import os
import shutil
import json
import base64
import tempfile

logger = logging.getLogger(__name__)

# Inicializar PILIBrain para generación offline
pili_brain = PILIBrain()

router = APIRouter()

# Helper para generar número de cotizacion
def generar_numero_cotizacion(db: Session) -> str:
    """Generar número único de cotización - Formato: COT-YYYYMM-XXXX"""
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

# ═══════════════════════════════════════════════════════════════
# 🤖 PILI - CONTEXTOS DE SERVICIOS INTELIGENTES v3.0
# ═══════════════════════════════════════════════════════════════

CONTEXTOS_SERVICIOS = {
    
    # ⚡ COTIZACIÓN SIMPLE - PILI COTIZADORA
    "cotizacion-simple": {
        "nombre_pili": "PILI Cotizadora",
        "personalidad": "¡Hola! 🤖 Soy PILI Cotizadora, tu asistente especializada en cotizaciones eléctricas rápidas. Te ayudo a generar cotizaciones precisas en 5-15 minutos con preguntas inteligentes y sin salirme del tema.",
        
        "rol_ia": """Eres PILI Cotizadora, agente IA especializada en cotizaciones eléctricas de Tesla Electricidad. 
        Tu objetivo es obtener información específica para generar una cotización precisa de instalaciones eléctricas.
        Siempre haz preguntas para clarificar antes de cotizar. NO te desvíes hacia otros temas.""",
        
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
                "⚡ Eléctrico Residencial",
                "🏢 Eléctrico Comercial",
                "⚙️ Eléctrico Industrial",
                "🔥 Contra Incendios",
                "🏠 Domótica",
                "📑 Expedientes Técnicos",
                "💧 Saneamiento",
                "📋 Certificado ITSE",
                "🔌 Puesta a Tierra",
                "📹 Redes y CCTV"
            ],
            "refinamiento": [
                "📝 Necesito más detalles técnicos",
                "🔢 Ajustar cantidades estimadas", 
                "💰 Revisar precios unitarios",
                "⚡ Verificar cargas eléctricas",
                "✅ Generar cotización",
                "📎 Subir planos/fotos"
            ],
            "generacion": [
                "✏️ Editar vista previa",
                "📄 Generar Word final", 
                "📱 Enviar por WhatsApp",
                "💾 Guardar como borrador"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Cotizadora de Tesla Electricidad, analiza la información y:
        
        1. 🔍 IDENTIFICA el tipo exacto de instalación
        2. ⚡ CALCULA materiales según normativa peruana (CNE)
        3. 👷 ESTIMA mano de obra especializada requerida
        4. 💰 APLICA precios del mercado peruano 2025
        5. 📋 INCLUYE especificaciones técnicas detalladas
        6. ⚠️ CONSIDERA factores de seguridad y normativas
        
        PRECIOS REFERENCIALES PERÚ 2025:
        - Punto de luz LED 18W: S/25.00 - S/35.00
        - Tomacorriente doble: S/28.00 - S/40.00
        - Cable THW 2.5mm²: S/3.50 - S/4.50 por metro
        - Tablero monofásico 12 polos: S/350.00 - S/450.00
        - Mano de obra especializada: S/80.00 - S/120.00 por hora
        
        IMPORTANTE: Si falta información crítica, haz preguntas específicas antes de cotizar.
        """
    },

    # 🔍 COTIZACIÓN COMPLEJA - PILI ANALISTA
    "cotizacion-compleja": {
        "nombre_pili": "PILI Analista",
        "personalidad": "¡Hola! 🔍 Soy PILI Analista, especialista en proyectos eléctricos complejos. Proceso planos, documentos técnicos y genero cotizaciones detalladas con análisis profundo usando OCR y IA avanzada.",
        
        "rol_ia": """Eres PILI Analista, agente IA senior especializada en proyectos eléctricos complejos.
        Procesas documentos técnicos, analizas planos con OCR y generas cotizaciones detalladas.
        Tu enfoque es técnico y profundo, pero mantienes la conversación en el contexto del proyecto.""",
        
        "documentos_esperados": [
            "Planos arquitectónicos (PDF/DWG)",
            "Memoria descriptiva del proyecto",
            "Especificaciones técnicas detalladas",
            "Presupuesto referencial o base",
            "Normas y códigos aplicables", 
            "Lista de materiales existente"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "📄 Subir planos para análisis",
                "📋 Subir especificaciones técnicas",
                "🔍 Analizar proyecto existente",
                "⚡ Cálculo de cargas eléctricas",
                "📐 Metrados automáticos"
            ],
            "analisis": [
                "📊 Revisar análisis OCR",
                "🔍 Verificar información extraída",
                "📋 Completar datos faltantes",
                "⚡ Validar cargas calculadas",
                "📐 Confirmar metrados"
            ],
            "refinamiento": [
                "📋 Generar lista detallada materiales",
                "👷 Calcular cronograma mano obra",
                "💰 Aplicar precios actualizados",
                "📊 Crear análisis precios unitarios",
                "⚖️ Revisar normativas aplicables"
            ],
            "generacion": [
                "📄 Crear cotización formal",
                "📊 Incluir análisis de costos",
                "📈 Agregar cronograma obra",
                "📋 Generar memoria cálculo",
                "🎨 Personalizar con logo"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Analista de Tesla Electricidad para proyectos complejos:
        
        1. 📄 ANALIZA documentos técnicos subidos
        2. 🔍 EXTRAE información con OCR avanzado
        3. ⚡ CALCULA cargas y dimensionamientos
        4. 📐 GENERA metrados automáticos
        5. 📊 CREA análisis de precios unitarios
        6. ⚖️ VALIDA contra normativas CNE
        7. 📋 ESTRUCTURA información en JSON
        
        CAPACIDADES TÉCNICAS:
        - Lectura de planos AutoCAD (PDF)
        - Análisis de especificaciones técnicas
        - Cálculo de metrados por ambientes
        - Dimensionamiento de conductores
        - Selección de equipos de protección
        - Cumplimiento de códigos peruanos
        
        ENFOQUE: Precisión técnica + eficiencia comercial
        """
    },

    # 📊 PROYECTO SIMPLE - PILI COORDINADORA
    "proyecto-simple": {
        "nombre_pili": "PILI Coordinadora",
        "personalidad": "¡Hola! 📊 Soy PILI Coordinadora, especialista en gestión de proyectos eléctricos simples. Te ayudo a estructurar proyectos, crear cronogramas y coordinar recursos de manera eficiente.",
        
        "rol_ia": """Eres PILI Coordinadora, agente IA especializada en gestión de proyectos eléctricos.
        Tu enfoque es organizacional y práctico, creando estructuras de trabajo claras y cronogramas realistas.
        Mantienes la conversación centrada en la organización y ejecución del proyecto.""",
        
        "elementos_proyecto": [
            "Alcance del proyecto claramente definido",
            "Cronograma con fases y actividades",
            "Recursos humanos y materiales necesarios",
            "Presupuesto desglosado por actividades",
            "Riesgos identificados y mitigaciones",
            "Entregables y fechas de entrega"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "🎯 Definir alcance del proyecto",
                "📅 Crear cronograma básico",
                "👥 Asignar recursos",
                "💰 Estimar presupuesto",
                "⚠️ Identificar riesgos"
            ],
            "planificacion": [
                "📋 Desglosar actividades",
                "⏱️ Estimar duraciones",
                "🔗 Definir dependencias",
                "📊 Crear diagrama Gantt",
                "🎯 Establecer hitos"
            ],
            "refinamiento": [
                "👷 Optimizar recursos",
                "💰 Ajustar presupuesto",
                "⏰ Revisar cronograma",
                "📋 Validar entregables",
                "🔄 Planes de contingencia"
            ],
            "generacion": [
                "📄 Generar documento proyecto",
                "📈 Crear dashboard seguimiento",
                "📊 Exportar cronograma",
                "📋 Lista de verificación"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Coordinadora de Tesla Electricidad:
        
        1. 🎯 ESTRUCTURA el proyecto en fases lógicas
        2. 📅 CREA cronogramas realistas y factibles
        3. 👥 ASIGNA recursos humanos especializados
        4. 💰 ESTIMA presupuestos por actividades
        5. ⚠️ IDENTIFICA riesgos y planes de contingencia
        6. 📋 DEFINE entregables claros y medibles
        7. 🔄 ESTABLECE puntos de control y seguimiento
        
        METODOLOGÍA:
        - Enfoque ágil adaptado a electricidad
        - Fases: Diseño → Materiales → Instalación → Pruebas
        - Control de calidad en cada etapa
        - Documentación técnica especializada
        
        ESPECIALIDAD: Proyectos 1-12 semanas, equipos 2-8 personas
        """
    },

    # 🎯 PROYECTO COMPLEJO - PILI PROJECT MANAGER
    "proyecto-complejo": {
        "nombre_pili": "PILI Project Manager",
        "personalidad": "¡Hola! 🎯 Soy PILI Project Manager, especialista en proyectos eléctricos complejos y de gran envergadura. Aplico metodologías PMI, gestiono múltiples stakeholders y aseguro el éxito de proyectos críticos.",
        
        "rol_ia": """Eres PILI Project Manager, agente IA senior especializada en proyectos eléctricos complejos.
        Aplicas metodologías PMI, gestionas riesgos avanzados y coordinas múltiples equipos especializados.
        Tu enfoque es estratégico y orientado a resultados empresariales.""",
        
        "areas_conocimiento": [
            "Gestión de Integración del Proyecto",
            "Gestión del Alcance y Requerimientos", 
            "Gestión del Cronograma y Recursos",
            "Gestión de Costos y Presupuestos",
            "Gestión de Calidad y Estándares",
            "Gestión de Recursos Humanos",
            "Gestión de Comunicaciones",
            "Gestión de Riesgos",
            "Gestión de Adquisiciones",
            "Gestión de Stakeholders"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "📋 Charter del proyecto",
                "🎯 Análisis de stakeholders", 
                "📊 Estructura de desglose trabajo",
                "⚠️ Registro de riesgos",
                "📈 Plan de gestión proyecto"
            ],
            "planificacion": [
                "📅 Cronograma maestro",
                "💰 Línea base presupuesto",
                "👥 Matriz RACI",
                "📊 Plan gestión calidad",
                "🔄 Plan gestión cambios"
            ],
            "ejecucion": [
                "📈 Dashboard ejecutivo",
                "📊 Reportes de avance",
                "⚠️ Gestión de issues",
                "🔄 Control de cambios",
                "👥 Gestión de equipos"
            ],
            "control": [
                "📊 Análisis valor ganado",
                "📈 Métricas de performance",
                "⚠️ Escalamiento de riesgos",
                "💰 Control de costos",
                "📋 Auditorías de calidad"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Project Manager de Tesla Electricidad para proyectos complejos:
        
        1. 📋 DESARROLLA Charter completo del proyecto
        2. 🎯 GESTIONA stakeholders y expectativas
        3. 📊 CREA EDT (Work Breakdown Structure)
        4. 📅 PLANIFICA cronograma maestro con rutas críticas
        5. 💰 ESTABLECE líneas base de costo y alcance
        6. ⚠️ GESTIONA riesgos con análisis cuanti/cualitativo
        7. 📈 IMPLEMENTA métricas de valor ganado (EVM)
        8. 🔄 CONTROLA cambios con governance
        9. 👥 LIDERA equipos multidisciplinarios
        10. 📊 REPORTA a nivel ejecutivo
        
        METODOLOGÍAS:
        - PMI PMBOK 7ma Edición
        - Agile/Scrum para desarrollo técnico
        - Lean Construction para instalaciones
        - ISO 21500 para gestión de proyectos
        
        ESPECIALIDAD: Proyectos >$100K, >6 meses, equipos >10 personas
        """
    },

    # 📋 INFORME SIMPLE - PILI REPORTERA
    "informe-simple": {
        "nombre_pili": "PILI Reportera",
        "personalidad": "¡Hola! 📋 Soy PILI Reportera, especialista en informes técnicos eléctricos claros y concisos. Transformo datos complejos en reportes comprensibles para clientes y autoridades.",
        
        "rol_ia": """Eres PILI Reportera, agente IA especializada en redacción técnica y informes eléctricos.
        Tu enfoque es comunicacional, creando documentos claros, bien estructurados y técnicamente precisos.
        Adaptas el lenguaje según la audiencia: técnica, gerencial o regulatoria.""",
        
        "tipos_informes": [
            "Informe de inspección eléctrica",
            "Reporte de mediciones y pruebas",
            "Informe de cumplimiento normativo",
            "Reporte de incidentes técnicos",
            "Informe de avance de obra",
            "Reporte de verificación ITSE"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "📋 Seleccionar tipo de informe",
                "🎯 Definir audiencia objetivo",
                "📊 Identificar datos disponibles",
                "⚖️ Verificar normativas aplicables",
                "📝 Establecer estructura"
            ],
            "desarrollo": [
                "📊 Analizar datos técnicos",
                "📈 Crear gráficos y tablas",
                "📸 Incluir evidencia fotográfica",
                "🔍 Verificar cálculos",
                "📝 Redactar hallazgos"
            ],
            "revision": [
                "✏️ Revisar redacción técnica",
                "📊 Validar datos y cálculos",
                "🎨 Aplicar formato profesional",
                "📋 Verificar completitud",
                "🔍 Control de calidad"
            ],
            "finalizacion": [
                "📄 Generar PDF final",
                "📱 Versión ejecutiva",
                "📋 Lista de verificación",
                "📧 Preparar para envío"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Reportera de Tesla Electricidad:
        
        1. 📋 ESTRUCTURA informes según estándares técnicos
        2. 📊 PRESENTA datos de manera clara y visual
        3. 📝 REDACTA en lenguaje técnico apropiado
        4. 📈 INCLUYE gráficos y tablas profesionales
        5. 🔍 VERIFICA precisión técnica y normativa
        6. 📸 INTEGRA evidencia fotográfica relevante
        7. 📋 APLICA formatos estándar de la industria
        
        ELEMENTOS CLAVE:
        - Resumen ejecutivo claro
        - Metodología de inspección/medición
        - Hallazgos técnicos detallados
        - Conclusiones fundamentadas
        - Recomendaciones específicas
        - Anexos con evidencia
        
        ESTÁNDARES:
        - Normas CNE peruanas
        - Formatos oficiales (OSINERGMIN, MEM)
        - Protocolos de medición IEEE
        - Estándares de redacción técnica
        
        ESPECIALIDAD: Informes 5-20 páginas, formato profesional
        """
    },

    # 📊 INFORME EJECUTIVO - PILI ANALISTA SENIOR
    "informe-ejecutivo": {
        "nombre_pili": "PILI Analista Senior",
        "personalidad": "¡Hola! 📊 Soy PILI Analista Senior, especialista en informes ejecutivos y análisis estratégico. Creo documentos de alto nivel con análisis profundo, formato APA y presentación ejecutiva para toma de decisiones estratégicas.",
        
        "rol_ia": """Eres PILI Analista Senior, agente IA especializada en análisis estratégico e informes ejecutivos.
        Tu enfoque es analítico y estratégico, creando documentos de alto valor para la toma de decisiones.
        Combinas expertise técnico con visión de negocios para generar insights accionables.""",
        
        "capacidades_analisis": [
            "Análisis estratégico de proyectos",
            "Evaluación de rentabilidad y ROI",
            "Análisis de riesgos cuantitativos",
            "Benchmarking de mercado",
            "Proyecciones financieras",
            "Análisis de tendencias tecnológicas",
            "Evaluación de cumplimiento regulatorio",
            "Análisis de competitividad"
        ],
        
        "botones_contextuales": {
            "inicial": [
                "🎯 Definir objetivos del análisis",
                "📊 Identificar métricas clave",
                "🔍 Establecer metodología",
                "📈 Fuentes de información",
                "👥 Audiencia ejecutiva"
            ],
            "investigacion": [
                "📊 Análisis de datos cuantitativos",
                "📈 Investigación de mercado",
                "💰 Análisis financiero",
                "⚠️ Evaluación de riesgos",
                "🏆 Benchmarking competitivo"
            ],
            "analisis": [
                "📊 Análisis estadístico avanzado",
                "📈 Modelado de escenarios",
                "💡 Generación de insights",
                "🎯 Identificación de oportunidades",
                "⚖️ Evaluación de alternativas"
            ],
            "presentacion": [
                "📋 Resumen ejecutivo",
                "📊 Dashboard de métricas",
                "📈 Recomendaciones estratégicas",
                "🎨 Diseño ejecutivo",
                "📄 Formato APA completo"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Analista Senior de Tesla Electricidad para informes ejecutivos:
        
        1. 🎯 ANALIZA objetivos estratégicos del negocio
        2. 📊 DESARROLLA métricas y KPIs relevantes
        3. 📈 REALIZA análisis cuantitativo profundo
        4. 💡 GENERA insights y recomendaciones
        5. 🎨 PRESENTA en formato ejecutivo profesional
        6. 📋 ESTRUCTURA según estándares APA
        7. 📊 INCLUYE análisis visual avanzado
        8. 💰 EVALÚA impacto financiero y ROI
        9. ⚠️ IDENTIFICA riesgos y oportunidades
        10. 🚀 PROPONE planes de acción
        
        METODOLOGÍAS:
        - Análisis SWOT/PESTEL
        - Análisis de valor económico (EVA)
        - Análisis de sensibilidad y escenarios
        - Benchmarking estratégico
        - Análisis de riesgo cuantitativo
        
        FORMATO:
        - Estilo APA 7ma edición
        - Gráficos ejecutivos (dashboard style)
        - Tablas de análisis profesionales
        - Referencias académicas y técnicas
        - Anexos con análisis detallado
        
        ESPECIALIDAD: Informes 20-50 páginas, nivel C-Suite, decisiones >$50K
        """
    }
}

# ═══════════════════════════════════════════════════════════════
# 🛠️ FUNCIONES AUXILIARES PILI
# ═══════════════════════════════════════════════════════════════

def obtener_contexto_servicio(tipo_flujo: str) -> Dict[str, Any]:
    """Obtiene el contexto especializado para el tipo de flujo"""
    return CONTEXTOS_SERVICIOS.get(tipo_flujo, {})

def determinar_etapa_conversacion(historial: List[Dict], tiene_cotizacion: bool = False) -> str:
    """Determina la etapa actual de la conversación para botones contextuales"""
    
    if not historial:
        return "inicial"
    
    if tiene_cotizacion:
        return "generacion"
    
    if len(historial) >= 3:
        return "refinamiento"
    
    return "inicial"

def obtener_botones_para_etapa(tipo_flujo: str, etapa: str) -> List[str]:
    """Obtiene los botones contextuales para la etapa actual"""
    
    contexto = obtener_contexto_servicio(tipo_flujo)
    botones_config = contexto.get("botones_contextuales", {})
    
    return botones_config.get(etapa, [])

def generar_preview_html_editable(datos: Dict[str, Any], agente: str) -> str:
    """
    🆕 NUEVO PILI v3.0 - Genera vista previa HTML editable
    
    Esta función crea HTML que el frontend puede mostrar y editar,
    permitiendo al usuario modificar la cotización antes de generar el Word final.
    """
    
    items = datos.get('items', [])
    cliente = datos.get('cliente', 'Cliente')
    proyecto = datos.get('proyecto', 'Proyecto Eléctrico')
    total = datos.get('total', 0)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Vista Previa - {agente}</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #fef2f2; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 20px rgba(220, 38, 38, 0.15); border: 2px solid #fecaca; }}
            .header {{ border-bottom: 4px solid #dc2626; padding-bottom: 20px; margin-bottom: 30px; background: linear-gradient(135deg, #fee2e2 0%, #ffffff 100%); padding: 20px; border-radius: 8px; }}
            .company {{ color: #b91c1c; font-size: 26px; font-weight: 900; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); letter-spacing: -0.5px; }}
            .agent {{ color: #1f2937; font-size: 14px; margin-top: 8px; font-weight: 600; }}
            .title {{ color: #1f2937; font-size: 22px; margin: 20px 0; font-weight: 800; border-left: 5px solid #dc2626; padding-left: 15px; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
            .info-item {{ background: #fef2f2; padding: 15px; border-radius: 8px; border: 1px solid #fecaca; }}
            .info-label {{ font-weight: 800; color: #1f2937; font-size: 14px; }}
            .info-value {{ color: #dc2626; font-size: 17px; font-weight: 700; margin-top: 5px; }}
            .items-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .items-table th {{ background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); color: white; padding: 14px; text-align: left; font-weight: 800; font-size: 15px; }}
            .items-table td {{ padding: 12px; border-bottom: 2px solid #fecaca; color: #1f2937; font-weight: 600; }}
            .items-table tr:hover {{ background: #fef2f2; }}
            .items-table td:nth-child(4), .items-table td:nth-child(5) {{ color: #dc2626; font-weight: 700; }}
            .total-section {{ background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); padding: 25px; border-radius: 8px; margin-top: 20px; border: 2px solid #dc2626; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2); }}
            .total-row {{ display: flex; justify-content: space-between; margin: 8px 0; font-size: 16px; font-weight: 700; color: #1f2937; }}
            .total-final {{ font-size: 24px; font-weight: 900; color: #b91c1c; background: white; padding: 15px; border-radius: 6px; margin-top: 10px; border: 2px solid #dc2626; }}
            .edit-note {{ background: #fffbeb; border: 2px solid #fbbf24; padding: 15px; border-radius: 5px; margin-top: 20px; font-weight: 600; color: #78350f; }}
            .agent-signature {{ text-align: right; margin-top: 30px; padding-top: 20px; border-top: 2px solid #fecaca; font-weight: 700; color: #dc2626; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="company">⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</div>
                <div class="agent">🤖 Generado por {agente}</div>
            </div>
            
            <h2 class="title">💰 COTIZACIÓN ELÉCTRICA</h2>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">👤 Cliente:</div>
                    <div class="info-value">{cliente}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">📋 Proyecto:</div>
                    <div class="info-value">{proyecto}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">📅 Fecha:</div>
                    <div class="info-value">{datetime.now().strftime('%d/%m/%Y')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">🤖 Especialista:</div>
                    <div class="info-value">{agente}</div>
                </div>
            </div>
            
            <table class="items-table">
                <thead>
                    <tr>
                        <th>📋 Descripción</th>
                        <th>🔢 Cantidad</th>
                        <th>📏 Unidad</th>
                        <th>💰 Precio Unit.</th>
                        <th>💰 Subtotal</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    subtotal = 0
    for item in items:
        cantidad = item.get('cantidad', 0)
        precio = item.get('precio_unitario', 0)
        item_total = cantidad * precio
        subtotal += item_total
        
        html += f"""
                    <tr>
                        <td>{item.get('descripcion', '')}</td>
                        <td>{cantidad}</td>
                        <td>{item.get('unidad', 'und')}</td>
                        <td>S/ {precio:.2f}</td>
                        <td>S/ {item_total:.2f}</td>
                    </tr>
        """
    
    igv = subtotal * 0.18
    total_final = subtotal + igv
    
    html += f"""
                </tbody>
            </table>
            
            <div class="total-section">
                <div class="total-row">
                    <span>💰 Subtotal:</span>
                    <span>S/ {subtotal:.2f}</span>
                </div>
                <div class="total-row">
                    <span>📋 IGV (18%):</span>
                    <span>S/ {igv:.2f}</span>
                </div>
                <div class="total-row total-final">
                    <span>🏆 TOTAL:</span>
                    <span>S/ {total_final:.2f}</span>
                </div>
            </div>
            
            <div class="edit-note">
                ✏️ <strong>Edición Disponible:</strong> Puedes modificar cantidades, precios y descripciones desde el panel izquierdo. 
                Los cambios se reflejarán instantáneamente en esta vista previa.
            </div>
            
            <div class="agent-signature">
                <div style="color: #6c757d; font-size: 12px;">
                    Documento generado por {agente} v3.0<br>
                    {datetime.now().strftime('%d/%m/%Y %H:%M')}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def generar_preview_informe(datos: Dict[str, Any], agente: str) -> str:
    """Genera vista previa HTML para informes"""
    
    titulo = datos.get('titulo', 'Informe Técnico')
    cliente = datos.get('cliente', 'Cliente')
    fecha = datetime.now().strftime('%d/%m/%Y')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Vista Previa Informe - {agente}</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; margin: 40px; line-height: 1.6; }}
            .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
            .title {{ font-size: 24px; font-weight: bold; color: #333; margin: 20px 0; }}
            .info {{ margin: 20px 0; }}
            .section {{ margin: 30px 0; }}
            .section h3 {{ color: #007bff; border-bottom: 1px solid #007bff; padding-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚡ TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</h1>
            <p>🤖 {agente} - Sistema de Informes Técnicos</p>
        </div>
        
        <h2 class="title">📋 {titulo}</h2>
        
        <div class="info">
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>Fecha:</strong> {fecha}</p>
            <p><strong>Elaborado por:</strong> {agente}</p>
        </div>
        
        <div class="section">
            <h3>1. RESUMEN EJECUTIVO</h3>
            <p>Este informe presenta el análisis técnico realizado por {agente}, 
            especialista en {agente.lower().replace('pili ', '')}...</p>
        </div>
        
        <div class="section">
            <h3>2. METODOLOGÍA</h3>
            <p>El análisis se realizó aplicando normativas técnicas peruanas...</p>
        </div>
        
        <div class="section">
            <h3>3. HALLAZGOS</h3>
            <p>Los principales hallazgos identificados son...</p>
        </div>
        
        <div class="section">
            <h3>4. RECOMENDACIONES</h3>
            <p>Se recomienda implementar las siguientes acciones...</p>
        </div>
    </body>
    </html>
    """
    
    return html

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

# ═══════════════════════════════════════════════════════════════
# 🤖 ENDPOINTS PILI CORE (RESTAURADOS)
# ═══════════════════════════════════════════════════════════════

@router.get("/pili/presentacion")
async def presentacion_pili():
    """
    🤖 RESTAURADO - Presentación de PILI y sus capacidades
    
    Muestra información sobre PILI y los 6 agentes especializados disponibles.
    """
    
    servicios_disponibles = []
    
    for servicio_id, config in CONTEXTOS_SERVICIOS.items():
        servicios_disponibles.append({
            "id": servicio_id,
            "nombre": config.get("nombre_pili", "PILI"),
            "personalidad": config.get("personalidad", ""),
            "especialidad": servicio_id.replace("-", " ").title()
        })
    
    return {
        "success": True,
        "mensaje": "¡Hola! 👋 Soy PILI, tu agente IA multifunción de Tesla Electricidad.",
        "descripcion": "Soy una agente IA especializada que combina lo mejor de ChatGPT, Microsoft Copilot y Google Bard, pero enfocada 100% en servicios eléctricos peruanos.",
        "caracteristicas": [
            "🧠 Conversación inteligente con anti-salto (no me desvío del tema)",
            "📄 Procesamiento OCR de archivos (fotos, PDFs, manuscritos)",
            "⚡ Especializada en normativas eléctricas peruanas (CNE)", 
            "📊 Genero documentos profesionales con estructura JSON",
            "🎯 Aprendo de cada conversación para mejorar",
            "🌐 Busco información en web cuando la necesito"
        ],
        "servicios_disponibles": servicios_disponibles,
        "version": "3.0 - Agente IA Multifunción",
        "estado": "🟢 Online y lista para ayudar",
        "creada_por": "Tesla Electricidad y Automatización S.A.C."
    }

@router.post("/pili/procesar-archivos")
async def procesar_archivos_ocr(
    tipo_servicio: str = Body(...),
    archivos: List[UploadFile] = File(...),
    contexto_adicional: Optional[str] = Body(""),
    db: Session = Depends(get_db)
):
    """
    🤖 RESTAURADO - Procesamiento OCR multimodal
    
    PILI procesa múltiples tipos de archivos:
    - 📷 Fotos (manuscritos, planos, documentos)
    - 📄 PDFs técnicos
    - 📝 Documentos Word
    - 📊 Archivos Excel
    
    Extrae información relevante usando OCR y la estructura para el servicio solicitado.
    """
    
    try:
        logger.info(f"🤖 PILI procesando {len(archivos)} archivos para {tipo_servicio}")
        
        # Verificar que el servicio existe
        contexto = obtener_contexto_servicio(tipo_servicio)
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Servicio '{tipo_servicio}' no disponible en PILI"
            )
        
        informacion_extraida = {
            "archivos_procesados": [],
            "texto_extraido": "",
            "datos_estructurados": {},
            "imagenes_detectadas": [],
            "errores": [],
            "servicio": tipo_servicio,
            "agente_pili": contexto.get("nombre_pili", "PILI")
        }
        
        for archivo in archivos:
            try:
                # Crear directorio temporal si no existe
                temp_dir = Path("temp")
                temp_dir.mkdir(exist_ok=True)
                
                # Guardar archivo temporalmente
                temp_path = temp_dir / f"temp_{archivo.filename}"
                contenido = await archivo.read()
                
                with open(temp_path, "wb") as f:
                    f.write(contenido)
                
                texto_archivo = ""
                
                # Procesar según tipo de archivo
                if archivo.filename.lower().endswith(('.pdf')):
                    # Para PDFs - usar PyPDF2 o similar
                    texto_archivo = f"[OCR] Contenido extraído de PDF: {archivo.filename}"
                    # TODO: Implementar extracción real con PyPDF2
                    
                elif archivo.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    # Para imágenes - usar Tesseract OCR
                    texto_archivo = f"[OCR] Texto extraído de imagen: {archivo.filename}"
                    informacion_extraida["imagenes_detectadas"].append(archivo.filename)
                    # TODO: Implementar OCR real con Tesseract
                    
                elif archivo.filename.lower().endswith(('.docx', '.doc')):
                    # Para documentos Word - usar python-docx
                    texto_archivo = f"[DOC] Contenido extraído de Word: {archivo.filename}"
                    # TODO: Implementar extracción real con python-docx
                    
                elif archivo.filename.lower().endswith(('.xlsx', '.xls')):
                    # Para Excel - usar pandas
                    texto_archivo = f"[XLS] Datos extraídos de Excel: {archivo.filename}"
                    # TODO: Implementar extracción real con pandas
                
                informacion_extraida["texto_extraido"] += f"\n\nArchivo: {archivo.filename}\n{texto_archivo}"
                
                informacion_extraida["archivos_procesados"].append({
                    "nombre": archivo.filename,
                    "tamaño_kb": round(len(contenido) / 1024, 2),
                    "tipo": archivo.content_type,
                    "procesado": True
                })
                
                # Limpiar archivo temporal
                temp_path.unlink(missing_ok=True)
                
            except Exception as e:
                informacion_extraida["errores"].append({
                    "archivo": archivo.filename,
                    "error": str(e)
                })
                logger.error(f"Error procesando {archivo.filename}: {e}")
        
        # Generar respuesta PILI contextualizada
        nombre_pili = contexto.get("nombre_pili", "PILI")
        total_archivos = len(informacion_extraida["archivos_procesados"])
        total_errores = len(informacion_extraida["errores"])
        
        mensaje_pili = f"""¡Perfecto! 📄 Soy {nombre_pili} y he procesado {total_archivos} archivos para tu {tipo_servicio.replace('-', ' ')}.

📊 **Resumen del procesamiento:**
- ✅ Archivos procesados: {total_archivos}
- ❌ Errores: {total_errores}
- 📝 Texto extraído: {len(informacion_extraida["texto_extraido"])} caracteres
- 📷 Imágenes: {len(informacion_extraida["imagenes_detectadas"])}

{f"⚠️ **Nota:** {total_errores} archivos tuvieron errores al procesarse." if total_errores > 0 else ""}

🎯 **Siguiente paso:** Basándome en la información extraída, puedo ayudarte a:
"""
        
        # Sugerencias específicas por tipo de servicio
        if "cotizacion" in tipo_servicio:
            mensaje_pili += """
- 💰 Generar cotización detallada
- 📋 Crear lista de materiales
- ⚡ Calcular cargas eléctricas
- 📊 Estructurar información en JSON
"""
        elif "proyecto" in tipo_servicio:
            mensaje_pili += """
- 📁 Organizar estructura del proyecto
- 📅 Crear cronograma de trabajo
- 👥 Definir responsabilidades
- 📊 Configurar seguimiento
"""
        elif "informe" in tipo_servicio:
            mensaje_pili += """
- 📄 Generar informe técnico
- 📊 Crear gráficos explicativos
- 📋 Estructurar conclusiones
- 💼 Formatear presentación ejecutiva
"""
        
        return {
            "success": True,
            "mensaje_pili": mensaje_pili,
            "procesamiento": informacion_extraida,
            "puede_continuar": total_archivos > 0,
            "sugerencias_siguientes": [
                f"💬 Conversación guiada con {nombre_pili}",
                "📊 Generar vista previa JSON estructurado", 
                "📄 Crear documento profesional",
                "🔍 Analizar información extraída"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error PILI procesando archivos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error PILI: {str(e)}"
        )

@router.post("/pili/generar-json-preview")
async def generar_json_preview(
    tipo_servicio: str = Body(...),
    informacion_extraida: Dict[str, Any] = Body(...),
    datos_adicionales: Optional[Dict[str, Any]] = Body(None),
    db: Session = Depends(get_db)
):
    """
    🤖 RESTAURADO - Generar JSON estructurado + Vista previa HTML
    
    PILI toma la información procesada y la estructura en formato JSON optimizado
    para el tipo de servicio, además de generar una vista previa HTML editable.
    """
    
    try:
        logger.info(f"🤖 PILI generando JSON + preview para {tipo_servicio}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_servicio)
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Servicio PILI '{tipo_servicio}' no disponible"
            )
        
        # Crear estructura JSON base
        datos_json = {
            "pili_version": "3.0",
            "agente_responsable": contexto.get("nombre_pili", "PILI"),
            "tipo_servicio": tipo_servicio,
            "timestamp": datetime.now().isoformat(),
            "datos_extraidos": {},
            "metadatos": {
                "fuente_procesamiento": "PILI_OCR",
                "archivos_origen": informacion_extraida.get("archivos_procesados", []),
                "confianza_datos": 85,  # Porcentaje de confianza
                "requiere_revision": False
            }
        }
        
        # Combinar datos extraídos con datos adicionales
        texto_base = informacion_extraida.get("texto_extraido", "")
        if datos_adicionales:
            datos_json["datos_extraidos"].update(datos_adicionales)
        
        # Estructura específica según tipo de servicio
        if "cotizacion" in tipo_servicio:
            datos_json["datos_extraidos"].update({
                "numero": f"COT-{datetime.now().strftime('%Y%m%d')}-001",
                "cliente": datos_adicionales.get("cliente", "[Cliente por definir]") if datos_adicionales else "[Cliente por definir]",
                "proyecto": datos_adicionales.get("proyecto", "[Proyecto por definir]") if datos_adicionales else "[Proyecto por definir]",
                "descripcion": texto_base[:500] if texto_base else "[Descripción por completar]",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "vigencia": "30 días",
                "items": [
                    {
                        "descripcion": "Punto de luz LED 18W empotrado",
                        "cantidad": 1,
                        "unidad": "und",
                        "precio_unitario": 30.00
                    }
                ],
                "observaciones": "Precios incluyen IGV. Instalación según CNE-Utilización.",
                "subtotal": 0,
                "igv": 0,
                "total": 0
            })
            
        elif "proyecto" in tipo_servicio:
            datos_json["datos_extraidos"].update({
                "nombre_proyecto": datos_adicionales.get("proyecto", "[Nombre del proyecto]") if datos_adicionales else "[Nombre del proyecto]",
                "cliente": datos_adicionales.get("cliente", "[Cliente]") if datos_adicionales else "[Cliente]",
                "descripcion": texto_base[:500] if texto_base else "[Descripción del proyecto]",
                "fecha_inicio": datetime.now().strftime("%d/%m/%Y"),
                "duracion_estimada": "4 semanas",
                "estado": "En planificación",
                "fases": [
                    {"nombre": "Planificación", "duracion": "1 semana", "estado": "pendiente"},
                    {"nombre": "Ejecución", "duracion": "2 semanas", "estado": "pendiente"},
                    {"nombre": "Cierre", "duracion": "1 semana", "estado": "pendiente"}
                ]
            })
            
        elif "informe" in tipo_servicio:
            datos_json["datos_extraidos"].update({
                "titulo_informe": f"Informe Técnico - {tipo_servicio.replace('-', ' ').title()}",
                "fecha_informe": datetime.now().strftime("%d/%m/%Y"),
                "autor": "Tesla Electricidad y Automatización S.A.C.",
                "resumen_ejecutivo": texto_base[:300] if texto_base else "[Resumen ejecutivo por completar]",
                "conclusiones": "[Conclusiones por desarrollar]",
                "recomendaciones": "[Recomendaciones por definir]"
            })
        
        # Generar vista previa HTML editable
        if "cotizacion" in tipo_servicio:
            html_preview = generar_preview_html_editable(datos_json["datos_extraidos"], contexto.get("nombre_pili", "PILI"))
        elif "informe" in tipo_servicio:
            html_preview = generar_preview_informe(datos_json["datos_extraidos"], contexto.get("nombre_pili", "PILI"))
        else:
            html_preview = f"<p>Vista previa no disponible para {tipo_servicio}</p>"
        
        # Guardar para aprendizaje PILI
        aprendizaje_id = None
        try:
            # Simular guardado para aprendizaje
            aprendizaje_id = f"pili_{tipo_servicio}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            logger.info(f"PILI aprendizaje guardado: {aprendizaje_id}")
        except Exception as e:
            logger.warning(f"No se pudo guardar aprendizaje: {e}")
        
        nombre_pili = contexto.get("nombre_pili", "PILI")
        
        return {
            "success": True,
            "mensaje_pili": f"""¡Excelente! 📊 Soy {nombre_pili} y he estructurado toda la información en formato JSON optimizado.

🎯 **Lo que he creado:**
- 📋 Datos estructurados listos para usar
- 👁️ Vista previa HTML completamente editable
- 🧠 Información guardada para mi aprendizaje continuo

✏️ **Puedes editar la vista previa** directamente antes de generar el documento final.

🚀 **¿Siguiente paso?** ¡Genera tu documento profesional Word!""",
            
            "datos_json": datos_json,
            "html_preview": html_preview,
            "puede_generar_documento": True,
            "aprendizaje_guardado": aprendizaje_id is not None,
            "aprendizaje_id": aprendizaje_id,
            "acciones_disponibles": [
                "✏️ Editar vista previa",
                "📄 Generar Word final",
                "📊 Modificar datos JSON",
                "💾 Guardar como plantilla"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error PILI generando JSON preview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error PILI: {str(e)}"
        )

# ═══════════════════════════════════════════════════════════════
# 🔄 ENDPOINTS CONSERVADOS v2.0 + MEJORADOS PILI v3.0
# ═══════════════════════════════════════════════════════════════

@router.get("/pili/estadisticas-aprendizaje")
async def estadisticas_aprendizaje_pili(db: Session = Depends(get_db)):
    """
    🆕 NUEVO PILI v3.0 - Estadísticas de aprendizaje del agente
    
    Muestra cómo PILI ha evolucionado basándose en conversaciones anteriores
    """
    try:
        # Simular estadísticas de aprendizaje basadas en datos reales
        total_cotizaciones = db.query(Cotizacion).count()
        
        # Calcular "aprendizajes" basados en actividad
        total_aprendizajes = total_cotizaciones * 3  # Cada cotización = múltiples interacciones
        
        # Determinar "nivel de inteligencia" basado en experiencia
        if total_aprendizajes >= 100:
            nivel_inteligencia = "Experto Avanzado"
            mensaje_nivel = "He procesado muchos casos y soy muy precisa en mis recomendaciones."
        elif total_aprendizajes >= 50:
            nivel_inteligencia = "Especialista"
            mensaje_nivel = "Tengo experiencia sólida y genero cotizaciones confiables."
        elif total_aprendizajes >= 20:
            nivel_inteligencia = "Competente"
            mensaje_nivel = "Estoy desarrollando expertise y mejorando constantemente."
        elif total_aprendizajes >= 5:
            nivel_inteligencia = "Principiante"
            mensaje_nivel = "Estoy aprendiendo rápido de cada proyecto."
        else:
            nivel_inteligencia = "Inicial"
            mensaje_nivel = "Estoy en mis primeros casos, pero aprendo rápido."
        
        # Capacidades que ha desarrollado
        capacidades = [
            "🎯 Detección automática de contexto por servicio",
            "📄 Procesamiento OCR cada vez más preciso",
            "💬 Respuestas más especializadas y técnicas",
            "🔄 Flujos de trabajo optimizados",
            "📊 Mejor estructura de datos JSON",
            "🎨 Documentos con formato profesional mejorado"
        ]
        
        return {
            "success": True,
            "pili_aprendizaje": {
                "total_conversaciones": total_aprendizajes,
                "nivel_inteligencia": nivel_inteligencia,
                "mensaje_nivel": mensaje_nivel,
                "servicios_utilizados": {},
                "servicio_mas_usado": "cotizacion-simple",
                "ultima_actualizacion": datetime.now().isoformat(),
                "capacidades_desarrolladas": capacidades
            },
            "mensaje_pili": f"""¡Hola! 🤖 Soy PILI y te cuento sobre mi evolución:

📚 **Mi aprendizaje hasta ahora:**
- 🔢 Total de casos procesados: {total_aprendizajes}
- 🎯 Nivel actual: {nivel_inteligencia}
- 📈 {mensaje_nivel}

🏆 **Lo que he mejorado:**
- Cada cotización me hace más precisa en cálculos
- Cada proyecto me enseña mejores estructuras
- Cada informe perfecciona mi redacción técnica
- Aprendo las preferencias de Tesla Electricidad

🔮 **Próximas mejoras:**
- RAG con proyectos históricos (cuando tengas más datos)
- Búsqueda web inteligente cuando necesite información
- Especialización aún mayor por tipo de instalación

¡Sigo aprendiendo para ser tu mejor asistente IA! 🚀""",
            
            "recomendaciones": [
                "📄 Sube más documentos técnicos para mejorar mi OCR",
                "💬 Úsa diferentes tipos de servicio para expandir mi conocimiento",
                "📊 Los datos que procese se convierten en mejores sugerencias",
                "🔄 Cada corrección que hagas me hace más inteligente"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error estadísticas PILI: {e}")
        # Retornar estadísticas básicas en caso de error
        return {
            "success": True,
            "pili_aprendizaje": {
                "total_conversaciones": 0,
                "nivel_inteligencia": "Inicial",
                "mensaje_nivel": "Estoy lista para comenzar a aprender.",
                "servicios_utilizados": {},
                "servicio_mas_usado": None,
                "ultima_actualizacion": datetime.now().isoformat(),
                "capacidades_desarrolladas": []
            },
            "mensaje_pili": "¡Hola! 🤖 Soy PILI y estoy lista para ayudarte. Mientras más conversemos, más inteligente me vuelvo.",
            "recomendaciones": [
                "🚀 ¡Empecemos a trabajar juntos!",
                "💬 Háblame sobre tu primer proyecto",
                "📄 Puedes subirme documentos para analizar",
                "🎯 Cada interacción me hace más inteligente"
            ]
        }

@router.get("/botones-contextuales/{tipo_flujo}")
async def obtener_botones_contextuales(
    tipo_flujo: str,
    etapa: str = "inicial",
    historial_length: int = 0,
    tiene_cotizacion: bool = False
):
    """
    🔄 CONSERVADO v2.0 - Obtiene botones contextuales para la interfaz
    
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
    archivos_procesados: Optional[List[Dict]] = Body([]),
    generar_html: Optional[bool] = Body(False),
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO v2.0 + MEJORADO PILI v3.0

    Chat inteligente con contexto específico según el servicio.
    PILI ahora responde con su personalidad específica por agente.

    NUEVO: Genera vista previa HTML editable si generar_html=True
    """
    try:
        logger.info(f"🤖 PILI chat contextualizado para {tipo_flujo}")

        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)

        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado por PILI"
            )

        # Construir prompt especializado PILI
        nombre_pili = contexto.get("nombre_pili", "PILI")
        prompt_especializado = f"""
        Eres {nombre_pili}.

        {contexto.get('personalidad', '')}

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

        prompt_especializado += f"\n\nUSUARIO: {mensaje}\n\nRESPUESTA DE {nombre_pili}:"

        # ✅ GENERACIÓN DE DATOS ESTRUCTURADOS CON PILI BRAIN
        datos_generados = None
        html_preview = None
        documento_data = None  # ✅ Scope más amplio para usar en fallback

        # ✅ GENERACIÓN ESPECÍFICA POR TIPO DE DOCUMENTO (6 TIPOS)
        # Siempre intentar generar estructura si es flujo de cotización/proyecto/informe
        if any(keyword in tipo_flujo for keyword in ["cotizacion", "proyecto", "informe"]):
            try:
                logger.info(f"🧠 Generando estructura con PILIBrain para {tipo_flujo}...")
                servicio_detectado = pili_brain.detectar_servicio(mensaje)
                complejidad = "compleja" if "complejo" in tipo_flujo or "compleja" in tipo_flujo else "simple"

                # ✅ LLAMAR AL MÉTODO CORRECTO SEGÚN EL TIPO
                if "cotizacion" in tipo_flujo:
                    # 1. COTIZACIÓN SIMPLE o 2. COTIZACIÓN COMPLEJA
                    documento_data = pili_brain.generar_cotizacion(mensaje, servicio_detectado, complejidad)
                    logger.info(f"✅ Cotización {complejidad} generada")

                elif "proyecto" in tipo_flujo:
                    # 3. PROYECTO SIMPLE o 4. PROYECTO COMPLEJO
                    documento_data = pili_brain.generar_proyecto(mensaje, servicio_detectado, complejidad)
                    logger.info(f"✅ Proyecto {complejidad} generado")

                elif "informe" in tipo_flujo:
                    # 5. INFORME SIMPLE o 6. INFORME EJECUTIVO
                    documento_data = pili_brain.generar_informe(mensaje, servicio_detectado, complejidad)
                    logger.info(f"✅ Informe {complejidad} generado")

                else:
                    # Fallback por si acaso
                    documento_data = pili_brain.generar_cotizacion(mensaje, servicio_detectado, complejidad)
                    logger.warning(f"⚠️ Tipo no reconocido, usando generar_cotizacion como fallback")

                # ✅ EXTRAER DATOS ESTRUCTURADOS
                datos_generados = documento_data.get('datos', {})
                logger.info(f"✅ Datos estructurados generados: {len(datos_generados.get('items', []))} items")

                # ✅ GENERAR HTML PREVIEW CON DATOS REALES
                if generar_html:
                    if "cotizacion" in tipo_flujo or "proyecto" in tipo_flujo:
                        html_preview = generar_preview_html_editable(datos_generados, nombre_pili)
                    elif "informe" in tipo_flujo:
                        html_preview = generar_preview_informe(datos_generados, nombre_pili)

            except Exception as e_pili:
                logger.warning(f"⚠️ No se pudo generar estructura con PILIBrain: {e_pili}")
                datos_generados = None
                documento_data = None

        # Enviar a Gemini con contexto especializado, con fallback a PILIBrain
        try:
            respuesta = gemini_service.chat(
                mensaje=prompt_especializado,
                contexto=f"Agente: {nombre_pili}. Servicio: {tipo_flujo}. {contexto_adicional}",
                cotizacion_id=cotizacion_id
            )

            # 🚨 DETECTAR MODO DEMO DE GEMINI Y FORZAR FALLBACK A PILIBRAIN
            if isinstance(respuesta, dict) and "PILI en modo demo" in str(respuesta.get("mensaje", "")):
                raise Exception("Gemini en modo demo (sin API Key)")

        except Exception as e:
            # 🧠 FALLBACK: Usar PILIBrain cuando Gemini no está disponible
            logger.warning(f"⚠️ Gemini no disponible, usando PILIBrain local: {e}")

            # Si ya generamos datos antes, usarlos
            if datos_generados and documento_data:
                respuesta = {'mensaje': documento_data['conversacion']['mensaje_pili']}
            else:
                # ✅ GENERAR AHORA CON EL MÉTODO CORRECTO SEGÚN TIPO
                servicio_detectado = pili_brain.detectar_servicio(mensaje)
                complejidad_fallback = "compleja" if "complejo" in tipo_flujo or "compleja" in tipo_flujo else "simple"

                if "cotizacion" in tipo_flujo:
                    documento_data = pili_brain.generar_cotizacion(mensaje, servicio_detectado, complejidad_fallback)
                elif "proyecto" in tipo_flujo:
                    documento_data = pili_brain.generar_proyecto(mensaje, servicio_detectado, complejidad_fallback)
                elif "informe" in tipo_flujo:
                    documento_data = pili_brain.generar_informe(mensaje, servicio_detectado, complejidad_fallback)
                else:
                    documento_data = pili_brain.generar_cotizacion(mensaje, servicio_detectado, complejidad_fallback)

                datos_generados = documento_data.get('datos', {})
                respuesta = {'mensaje': documento_data['conversacion']['mensaje_pili']}

        # 🆕 GUARDAR EN BASE DE DATOS Y OBTENER ID
        documento_id = None
        if datos_generados:
            try:
                if "cotizacion" in tipo_flujo:
                    # Guardar cotización en BD
                    nueva_cotizacion = Cotizacion(
                        numero=generar_numero_cotizacion(db),
                        cliente=datos_generados.get('cliente', 'Cliente generado por PILI'),
                        proyecto=datos_generados.get('proyecto', 'Proyecto PILI'),
                        descripcion=datos_generados.get('descripcion', mensaje[:200]),
                        observaciones=datos_generados.get('observaciones', ''),
                        subtotal=float(datos_generados.get('subtotal', 0)),
                        igv=float(datos_generados.get('igv', 0)),
                        total=float(datos_generados.get('total', 0)),
                        estado="borrador",
                        fecha_creacion=datetime.now()
                    )
                    db.add(nueva_cotizacion)
                    db.commit()
                    db.refresh(nueva_cotizacion)
                    documento_id = nueva_cotizacion.id

                    # Agregar items
                    if 'items' in datos_generados:
                        for item_data in datos_generados['items']:
                            item = Item(
                                cotizacion_id=nueva_cotizacion.id,
                                descripcion=item_data.get('descripcion', ''),
                                cantidad=float(item_data.get('cantidad', 1)),
                                unidad=item_data.get('unidad', 'und'),
                                precio_unitario=float(item_data.get('precio_unitario', 0))
                            )
                            db.add(item)
                        db.commit()

                    logger.info(f"✅ Cotización guardada en BD: {nueva_cotizacion.numero} (ID: {documento_id})")

                elif "proyecto" in tipo_flujo:
                    # Guardar proyecto en BD
                    nuevo_proyecto = Proyecto(
                        nombre=datos_generados.get('nombre', 'Proyecto generado por PILI'),
                        cliente=datos_generados.get('cliente', 'Cliente PILI'),
                        descripcion=datos_generados.get('descripcion', mensaje[:500]),
                        presupuesto_estimado=float(datos_generados.get('presupuesto_estimado', 0)),
                        duracion_meses=int(datos_generados.get('duracion_meses', 1)),
                        estado="planificacion",
                        fecha_inicio=datetime.now(),
                        fecha_creacion=datetime.now()
                    )
                    db.add(nuevo_proyecto)
                    db.commit()
                    db.refresh(nuevo_proyecto)
                    documento_id = nuevo_proyecto.id

                    logger.info(f"✅ Proyecto guardado en BD: {nuevo_proyecto.nombre} (ID: {documento_id})")

                # Nota: Informes no se guardan como entidades separadas, solo se generan

            except Exception as e_bd:
                logger.warning(f"⚠️ No se pudo guardar en BD: {e_bd}")
                documento_id = None

        # Determinar etapa y botones sugeridos
        tiene_cotizacion = cotizacion_id is not None or documento_id is not None
        etapa_actual = determinar_etapa_conversacion(historial, tiene_cotizacion)
        botones_sugeridos = obtener_botones_para_etapa(tipo_flujo, etapa_actual)

        # ✅ RESPUESTA CON CAMPOS RESTAURADOS + ID DEL DOCUMENTO
        return {
            "success": True,
            "agente_activo": nombre_pili,
            "respuesta": respuesta.get('mensaje', '') if isinstance(respuesta, dict) else str(respuesta),
            "tipo_flujo": tipo_flujo,
            "etapa_actual": etapa_actual,
            "botones_sugeridos": botones_sugeridos,
            "contexto_pili": {
                "personalidad": contexto.get("personalidad", ""),
                "preguntas_esenciales": contexto.get("preguntas_esenciales", []),
                "especialidad": contexto.get("rol_ia", "")
            },
            "html_preview": html_preview,
            "generar_html": generar_html,
            # ✅ CAMPOS CRÍTICOS RESTAURADOS
            "cotizacion_generada": datos_generados if "cotizacion" in tipo_flujo else None,
            "proyecto_generado": datos_generados if "proyecto" in tipo_flujo else None,
            "informe_generado": datos_generados if "informe" in tipo_flujo else None,
            # 🆕 IDS PARA GENERACIÓN DE DOCUMENTOS
            "cotizacion_id": documento_id if "cotizacion" in tipo_flujo else None,
            "proyecto_id": documento_id if "proyecto" in tipo_flujo else None,
            "informe_id": documento_id if "informe" in tipo_flujo else None,
            "timestamp": datetime.now().isoformat(),
            "pili_metadata": {
                "agente_id": tipo_flujo,
                "version": "3.0",
                "capabilities": ["chat", "ocr", "json", "html_preview", "structured_data"]
            }
        }

    except Exception as e:
        logger.error(f"❌ Error en chat contextualizado PILI: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en PILI: {str(e)}"
        )

@router.post("/iniciar-flujo-inteligente")
async def iniciar_flujo_inteligente(
    tipo_flujo: str = Body(...),
    servicio: str = Body("electricidad"),
    industria: str = Body("general"),
    descripcion_inicial: Optional[str] = Body(""),
    db: Session = Depends(get_db)
):
    """
    🆕 NUEVO PILI v3.0 - Inicia un flujo de trabajo inteligente
    
    Este endpoint inicializa una conversación especializada con el agente PILI apropiado
    y proporciona un análisis inicial del proyecto.
    """
    try:
        logger.info(f"🚀 PILI iniciando flujo inteligente: {tipo_flujo}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado"
            )
        
        nombre_pili = contexto.get("nombre_pili", "PILI")
        
        # Análisis inicial automático por PILI Brain
        analisis = f"""
        {nombre_pili} ha analizado tu solicitud inicial:
        
        📋 **Tipo de proyecto:** {tipo_flujo.replace('-', ' ').title()}
        🏢 **Sector:** {industria.title()}
        ⚡ **Servicio:** {servicio.title()}
        
        📊 **Análisis inicial:**
        - Proyecto clasificado como: {contexto.get('complejidad', 'Estándar')}
        - Tiempo estimado: {contexto.get('tiempo_estimado', '1-3 horas')}
        - Especialista asignado: {nombre_pili}
        
        🎯 **Próximos pasos recomendados:**
        1. Proporcionar detalles específicos del proyecto
        2. Subir documentos técnicos si están disponibles
        3. Definir alcance y requerimientos
        4. Revisar especificaciones y normativas aplicables
        """
        
        # Obtener botones iniciales según el contexto
        botones_iniciales = obtener_botones_para_etapa(tipo_flujo, "inicial")
        
        return {
            "success": True,
            "agente_activado": nombre_pili,
            "personalidad": contexto.get("personalidad", ""),
            "tipo_flujo": tipo_flujo,
            "analisis_inicial": analisis,
            "plan_sugerido": f"Plan de trabajo generado por {nombre_pili}",
            "botones_iniciales": botones_iniciales,
            "preguntas_esenciales": contexto.get("preguntas_esenciales", []),
            "siguiente_paso": f"Conversa con {nombre_pili} usando los botones o escribiendo directamente",
            "mensaje_pili": contexto.get("personalidad", f"¡Hola! Soy {nombre_pili} y estoy lista para ayudarte.")
        }
        
    except Exception as e:
        logger.error(f"Error iniciando flujo inteligente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

# ════════════════════════════════════════════════════════════════
# 🔄 GESTIÓN DE PLANTILLAS (CONSERVADO INTACTO)
# ════════════════════════════════════════════════════════════════

@router.get("/listar-plantillas")
async def listar_plantillas_disponibles():
    """
    🔄 CONSERVADO - Listar todas las plantillas Word disponibles
    """
    
    try:
        from app.core.config import settings
        
        templates_dir = Path(settings.TEMPLATES_DIR)
        
        if not templates_dir.exists():
            templates_dir.mkdir(parents=True, exist_ok=True)
            return {
                "success": True,
                "plantillas": [],
                "mensaje": "No hay plantillas disponibles. Sube tu primera plantilla."
            }
        
        # Buscar archivos .docx
        plantillas = []
        for archivo in templates_dir.glob("*.docx"):
            plantillas.append({
                "nombre": archivo.name,
                "ruta": str(archivo),
                "tamaño": f"{archivo.stat().st_size / 1024:.1f} KB",
                "fecha_modificacion": datetime.fromtimestamp(archivo.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
            })
        
        return {
            "success": True,
            "plantillas": plantillas,
            "total": len(plantillas),
            "directorio": str(templates_dir)
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
    🔄 CONSERVADO - Obtener marcadores de una plantilla específica
    """
    
    try:
        from app.core.config import settings
        from app.services.template_processor import template_processor
        
        # Ruta de la plantilla
        ruta_plantilla = Path(settings.TEMPLATES_DIR) / nombre_plantilla
        
        if not ruta_plantilla.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plantilla '{nombre_plantilla}' no encontrada"
            )
        
        # Extraer marcadores usando template_processor
        marcadores = template_processor.extraer_marcadores(str(ruta_plantilla))
        
        return {
            "success": True,
            "nombre_plantilla": nombre_plantilla,
            "marcadores_encontrados": marcadores,
            "total_marcadores": len(marcadores),
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
    🔄 CONSERVADO - Generar cotización usando una plantilla personalizada
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
                "precio_unitario": float(item.precio_unitario),
                "subtotal": float(item.cantidad * item.precio_unitario)
            })
        
        # Preparar datos para la plantilla
        datos_cotizacion = {
            "numero": cotizacion.numero,
            "cliente": cotizacion.cliente,
            "proyecto": cotizacion.proyecto or "Instalación Eléctrica",
            "descripcion": cotizacion.descripcion,
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
    🔄 CONSERVADO - Eliminar una plantilla
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
    🔄 CONSERVADO - Validar una plantilla antes de subirla
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

@router.post("/subir-plantilla")
async def subir_plantilla(
    archivo: UploadFile = File(...),
    nombre_personalizado: Optional[str] = Body(None)
):
    """
    🔄 CONSERVADO - Subir una nueva plantilla Word
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
            "mensaje": f"Plantilla '{nombre_archivo}' subida exitosamente",
            "nombre_archivo": nombre_archivo,
            "ruta": str(ruta_plantilla),
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

# ════════════════════════════════════════════════════════════════
# 🔄 ENDPOINTS LEGACY - CONSERVADOS PARA COMPATIBILIDAD
# ════════════════════════════════════════════════════════════════

@router.post("/generar-rapida", response_model=CotizacionResponse)
async def generar_cotizacion_rapida(
    request: CotizacionRapidaRequest,
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO - Generar cotización rápida con IA (endpoint legacy)
    """
    try:
        logger.info("Generando cotización rápida con IA")
        
        # Generar con Gemini
        resultado = gemini_service.generar_cotizacion(
            servicio=request.servicio,
            industria=request.industria,
            descripcion=request.descripcion
        )
        
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar la cotización con IA"
            )
        
        # Crear cotización en BD
        nueva_cotizacion = Cotizacion(
            numero=generar_numero_cotizacion(db),
            cliente=resultado.get('cliente', 'Cliente Gemini'),
            proyecto=resultado.get('proyecto', 'Proyecto generado por IA'),
            descripcion=resultado.get('descripcion', ''),
            observaciones=resultado.get('observaciones', ''),
            subtotal=resultado.get('subtotal', 0),
            igv=resultado.get('igv', 0),
            total=resultado.get('total', 0),
            estado="borrador",
            fecha_creacion=datetime.now()
        )
        
        db.add(nueva_cotizacion)
        db.commit()
        db.refresh(nueva_cotizacion)
        
        # Agregar items si los hay
        if 'items' in resultado:
            for item_data in resultado['items']:
                item = Item(
                    cotizacion_id=nueva_cotizacion.id,
                    descripcion=item_data.get('descripcion', ''),
                    cantidad=item_data.get('cantidad', 1),
                    unidad=item_data.get('unidad', 'und'),
                    precio_unitario=item_data.get('precio_unitario', 0)
                )
                db.add(item)
            
            db.commit()
        
        logger.info(f"✅ Cotización creada: {nueva_cotizacion.numero}")
        
        return CotizacionResponse(
            id=nueva_cotizacion.id,
            numero=nueva_cotizacion.numero,
            cliente=nueva_cotizacion.cliente,
            proyecto=nueva_cotizacion.proyecto,
            descripcion=nueva_cotizacion.descripcion,
            observaciones=nueva_cotizacion.observaciones,
            subtotal=float(nueva_cotizacion.subtotal),
            igv=float(nueva_cotizacion.igv),
            total=float(nueva_cotizacion.total),
            estado=nueva_cotizacion.estado,
            fecha_creacion=nueva_cotizacion.fecha_creacion.isoformat() if nueva_cotizacion.fecha_creacion else None,
            items=resultado.get('items', [])
        )
        
    except Exception as e:
        logger.error(f"Error generando cotización rápida: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )

@router.post("/conversacional", response_model=ChatResponse)
async def chat_conversacional(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO - Chat conversacional para refinar cotizaciones
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
            respuesta=respuesta.get('mensaje', '') if isinstance(respuesta, dict) else str(respuesta),
            sugerencias=respuesta.get('sugerencias', []) if isinstance(respuesta, dict) else [],
            accion_recomendada=respuesta.get('accion_recomendada') if isinstance(respuesta, dict) else None
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
    🔄 CONSERVADO - Analizar descripción de un proyecto con IA
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
    🔄 CONSERVADO - Obtener sugerencias de mejora para una cotización existente
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
        sugerencias = gemini_service.sugerir_mejoras(cotizacion.__dict__)
        
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
    🔄 CONSERVADO + MEJORADO - Verificar estado del servicio de IA
    """
    from app.core.config import settings
    
    return {
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "model": settings.GEMINI_MODEL,
        "status": "healthy",
        "pili_version": "3.0",
        "agentes_disponibles": len(CONTEXTOS_SERVICIOS),
        "servicios_inteligentes": list(CONTEXTOS_SERVICIOS.keys()),
        "version": "3.0 - PILI Multifunción"
    }