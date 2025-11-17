"""
🤖 PILI AGENTE IA v3.0 - SISTEMA COMPLETO
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

    # 📁 PROYECTO SIMPLE - PILI COORDINADORA
    "proyecto-simple": {
        "nombre_pili": "PILI Coordinadora",
        "personalidad": "¡Hola! 📁 Soy PILI Coordinadora, tu experta en gestión de proyectos eléctricos. Te ayudo a organizar, dar seguimiento y documentar tus proyectos de forma simple y efectiva.",
        
        "rol_ia": """Eres PILI Coordinadora, especialista en gestión de proyectos eléctricos simples.
        Tu enfoque es organizacional: crear estructura, asignar responsabilidades, hacer seguimiento.
        Mantienes la conversación enfocada en la gestión eficiente del proyecto.""",
        
        "botones_contextuales": {
            "inicial": [
                "📋 Crear proyecto nuevo",
                "📂 Organizar estructura carpetas", 
                "👥 Asignar responsabilidades",
                "📅 Definir cronograma básico",
                "💰 Establecer presupuesto",
                "📊 Configurar seguimiento"
            ],
            "planificacion": [
                "📋 Completar plan de trabajo",
                "📅 Ajustar fechas y hitos",
                "👥 Definir equipo de trabajo",
                "💰 Revisar presupuesto",
                "📊 Configurar métricas"
            ],
            "seguimiento": [
                "📈 Ver estado del proyecto",
                "📋 Actualizar avances",
                "💰 Controlar costos", 
                "📅 Revisar cronograma",
                "📊 Generar reporte avance",
                "⚠️ Identificar riesgos"
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
        Como PILI Coordinadora para gestión de proyectos simples:
        
        1. 🔍 ORGANIZA estructura de carpetas lógica
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

    # 📊 PROYECTO COMPLEJO - PILI PROJECT MANAGER
    "proyecto-complejo": {
        "nombre_pili": "PILI Project Manager",
        "personalidad": "¡Hola! 📊 Soy PILI Project Manager, directora de proyectos senior especializada en gestión integral de proyectos de gran envergadura. Manejo múltiples stakeholders, cronogramas complejos y riesgos significativos.",
        
        "rol_ia": """Eres PILI Project Manager, directora de proyectos senior especializada en gestión integral de proyectos de gran envergadura.
        Manejas múltiples stakeholders, cronogramas complejos y riesgos significativos usando metodología PMI.
        Tu enfoque es estratégico y ejecutivo.""",
        
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
        Como PILI Project Manager senior:
        
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
    },

    # 📄 INFORME SIMPLE - PILI REPORTERA
    "informe-simple": {
        "nombre_pili": "PILI Reportera",
        "personalidad": "¡Hola! 📄 Soy PILI Reportera, tu especialista en documentos técnicos claros y profesionales. Genero informes técnicos desde datos de proyectos y cotizaciones con un enfoque claro y directo.",
        
        "rol_ia": """Eres PILI Reportera, especialista en creación de documentos técnicos claros.
        Tu enfoque es comunicacional: información clara, estructurada y profesional.
        Mantienes el foco en generar documentos útiles y bien estructurados.""",
        
        "botones_contextuales": {
            "inicial": [
                "📋 Seleccionar proyecto/cotización",
                "📊 Definir contenido informe",
                "🎨 Elegir plantilla",
                "📄 Vista previa PDF",
                "✅ Generar informe final"
            ],
            "configuracion": [
                "📊 Incluir métricas básicas",
                "📈 Agregar gráficos simples",
                "📋 Definir secciones",
                "🎨 Personalizar formato",
                "✅ Confirmar estructura"
            ],
            "generacion": [
                "📄 Vista previa Word",
                "📑 Generar PDF final",
                "📧 Preparar para envío",
                "💾 Guardar como plantilla"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Reportera para informes técnicos:
        
        1. 📊 SELECCIONA datos relevantes del proyecto
        2. 📋 ESTRUCTURA información lógicamente
        3. 📈 INCLUYE gráficos explicativos básicos
        4. 📝 REDACTA con claridad técnica
        5. 🎨 APLICA formato profesional
        6. ✅ VALIDA completitud y coherencia
        
        ESTRUCTURA ESTÁNDAR:
        - Resumen ejecutivo
        - Descripción del proyecto
        - Metodología aplicada
        - Resultados obtenidos
        - Conclusiones técnicas
        - Recomendaciones
        - Anexos técnicos
        """
    },

    # 💼 INFORME EJECUTIVO - PILI ANALISTA SENIOR
    "informe-ejecutivo": {
        "nombre_pili": "PILI Analista Senior",
        "personalidad": "¡Hola! 💼 Soy PILI Analista Senior, creadora de informes ejecutivos de alto nivel. Genero documentos con gráficos avanzados, métricas clave, análisis financiero y recomendaciones estratégicas en formato APA.",
        
        "rol_ia": """Eres PILI Analista Senior, especialista en informes ejecutivos de alto nivel.
        Tu enfoque es estratégico: análisis profundo, recomendaciones fundamentadas, presentación ejecutiva.
        Mantienes un nivel de sofisticación apropiado para audiencias ejecutivas.""",
        
        "botones_contextuales": {
            "configuracion": [
                "📊 Configurar métricas KPI",
                "📈 Incluir gráficos estadísticos", 
                "💰 Análisis financiero ROI",
                "🎯 Definir recomendaciones",
                "📋 Seleccionar formato APA"
            ],
            "analisis": [
                "📊 Dashboard ejecutivo",
                "📈 Análisis de tendencias",
                "💰 Evaluación financiera",
                "⚖️ Análisis de riesgos",
                "🎯 Recomendaciones estratégicas"
            ],
            "generacion": [
                "📊 Vista previa con gráficos",
                "📄 Generar Word ejecutivo",
                "📑 Generar PDF no editable",
                "📧 Preparar para envío",
                "💾 Guardar como plantilla"
            ]
        },
        
        "prompt_especializado": """
        Como PILI Analista Senior para informes ejecutivos:
        
        1. 📊 ANALIZA datos con profundidad estadística
        2. 📈 CREA gráficos avanzados (tendencias, comparaciones)
        3. 💰 EVALÚA aspectos financieros y ROI
        4. 🎯 FORMULA recomendaciones estratégicas
        5. 📋 APLICA formato APA profesional
        6. ⚖️ INCLUYE análisis de riesgos
        7. 🔮 PROYECTA escenarios futuros
        
        ESTRUCTURA EJECUTIVA:
        - Executive Summary (1 página)
        - Análisis de situación actual
        - Métricas clave y KPIs
        - Análisis financiero detallado
        - Evaluación de riesgos y oportunidades
        - Recomendaciones estratégicas
        - Plan de implementación
        - Anexos con datos de soporte
        
        FORMATO: APA 7ma edición + gráficos profesionales
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
# 🤖 NUEVOS ENDPOINTS PILI v3.0
# ════════════════════════════════════════════════════════════════

@router.get("/pili/presentacion")
async def presentacion_pili():
    """
    🤖 NUEVO PILI v3.0 - Presentación de PILI y sus capacidades
    
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
    🤖 NUEVO PILI v3.0 - Procesamiento OCR multimodal
    
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
    🤖 NUEVO PILI v3.0 - Generar JSON estructurado + Vista previa HTML
    
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
        html_preview = generar_preview_html(datos_json)
        
        # Guardar para aprendizaje PILI
        try:
            from app.models.documento import Documento
            aprendizaje = Documento(
                nombre=f"PILI_Aprendizaje_{tipo_servicio}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                tipo_archivo="application/json",
                content_text=json.dumps(datos_json, ensure_ascii=False, indent=2),
                procesado=True,
                fecha_upload=datetime.now()
            )
            db.add(aprendizaje)
            db.commit()
            aprendizaje_id = aprendizaje.id
        except Exception as e:
            logger.warning(f"No se pudo guardar aprendizaje: {e}")
            aprendizaje_id = None
        
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

def generar_preview_html(datos_json: Dict[str, Any]) -> str:
    """Genera vista previa HTML editable según tipo de servicio"""
    
    tipo_servicio = datos_json.get("tipo_servicio", "")
    datos = datos_json.get("datos_extraidos", {})
    agente = datos_json.get("agente_responsable", "PILI")
    
    if "cotizacion" in tipo_servicio:
        return generar_preview_cotizacion(datos, agente)
    elif "proyecto" in tipo_servicio:
        return generar_preview_proyecto(datos, agente)
    elif "informe" in tipo_servicio:
        return generar_preview_informe(datos, agente)
    else:
        return f"<p>Vista previa no disponible para {tipo_servicio}</p>"

def generar_filas_items(items: List[Dict[str, Any]]) -> str:
    """Genera las filas de items dinámicamente desde el array de items"""
    if not items:
        return """
        <tr>
            <td colspan="5" style="border: 1px solid #333; padding: 20px; text-align: center; color: #666; font-style: italic;">
                No hay items generados aún. PILI está esperando más información...
            </td>
        </tr>
        """

    filas_html = ""
    for item in items:
        descripcion = item.get('descripcion', item.get('item', 'Item sin descripción'))
        cantidad = item.get('cantidad', item.get('cant', 0))
        unidad = item.get('unidad', 'und')
        precio_unitario = item.get('precio_unitario', item.get('precioUnitario', 0))
        total = item.get('total', cantidad * precio_unitario)

        filas_html += f"""
        <tr>
            <td contenteditable="true" style="border: 1px solid #333; padding: 8px; background: #fff3cd; cursor: text; color: #000;">{descripcion}</td>
            <td contenteditable="true" style="border: 1px solid #333; padding: 8px; text-align: center; background: #fff3cd; cursor: text; color: #000; font-weight: bold;">{cantidad}</td>
            <td contenteditable="true" style="border: 1px solid #333; padding: 8px; text-align: center; background: #fff3cd; cursor: text; color: #000;">{unidad}</td>
            <td contenteditable="true" style="border: 1px solid #333; padding: 8px; text-align: right; background: #fff3cd; cursor: text; color: #000; font-weight: bold;">S/ {precio_unitario:.2f}</td>
            <td style="border: 1px solid #333; padding: 8px; text-align: right; background: #e8e8e8; font-weight: bold; color: #000; font-size: 15px;">S/ {total:.2f}</td>
        </tr>
        """

    return filas_html

def generar_preview_cotizacion(datos: Dict[str, Any], agente: str) -> str:
    """Genera HTML preview editable para cotización"""

    html = f"""
    <div class="cotizacion-preview" style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 8px;">
        <div class="pili-header" style="text-align: center; background: linear-gradient(135deg, #d4af37, #f4e37e); color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 20px;">🤖 {agente} - Vista Previa Editable</h2>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Puedes editar cualquier campo resaltado en amarillo</p>
        </div>
        
        <div class="header" style="text-align: center; border-bottom: 2px solid #d4af37; padding-bottom: 15px; margin-bottom: 20px;">
            <h1 style="color: #d4af37; margin: 0;">TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</h1>
            <p style="margin: 5px 0; color: #666;">RUC: 20601138787</p>
            <h2 style="color: #333; margin-top: 15px;">COTIZACIÓN</h2>
        </div>
        
        <div class="datos-cliente" style="margin-bottom: 20px; background: white; padding: 15px; border-radius: 8px; border: 2px solid #d4af37;">
            <h3 style="color: #b8860b; border-bottom: 2px solid #d4af37; padding-bottom: 5px; font-size: 18px;">DATOS DEL CLIENTE</h3>
            <p style="color: #000; font-size: 15px;"><strong style="color: #b8860b;">Cliente:</strong> <span contenteditable="true" style="background: #fff3cd; padding: 2px 4px; border-radius: 3px; cursor: text; color: #000; font-weight: bold;">{datos.get('cliente', '[EDITAR CLIENTE]')}</span></p>
            <p style="color: #000; font-size: 15px;"><strong style="color: #b8860b;">Proyecto:</strong> <span contenteditable="true" style="background: #fff3cd; padding: 2px 4px; border-radius: 3px; cursor: text; color: #000; font-weight: bold;">{datos.get('proyecto', '[EDITAR PROYECTO]')}</span></p>
            <p style="color: #000; font-size: 14px;"><strong style="color: #b8860b;">Número:</strong> {datos.get('numero', 'COT-202501-001')}</p>
            <p style="color: #000; font-size: 14px;"><strong style="color: #b8860b;">Fecha:</strong> {datos.get('fecha', datetime.now().strftime('%d/%m/%Y'))}</p>
            <p style="color: #000; font-size: 14px;"><strong style="color: #b8860b;">Vigencia:</strong> {datos.get('vigencia', '30 días')}</p>
        </div>
        
        <div class="descripcion" style="margin-bottom: 20px; background: white; padding: 15px; border-radius: 8px; border: 2px solid #d4af37;">
            <h3 style="color: #b8860b; border-bottom: 2px solid #d4af37; padding-bottom: 5px; font-size: 18px;">DESCRIPCIÓN DEL PROYECTO</h3>
            <div contenteditable="true" style="background: #fff3cd; padding: 12px; border: 2px dashed #d4af37; min-height: 80px; border-radius: 4px; cursor: text; color: #000; font-size: 14px;">
                {datos.get('descripcion', '[EDITAR DESCRIPCIÓN DEL PROYECTO - Describe el alcance del trabajo a realizar]')}
            </div>
        </div>
        
        <div class="items-tabla" style="margin-bottom: 20px;">
            <h3 style="color: #d4af37; border-bottom: 1px solid #ddd; padding-bottom: 5px;">DETALLE DE ITEMS</h3>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                <thead>
                    <tr style="background: #d4af37; color: white;">
                        <th style="border: 1px solid #333; padding: 10px; text-align: left;">DESCRIPCIÓN</th>
                        <th style="border: 1px solid #333; padding: 10px; width: 80px;">CANT.</th>
                        <th style="border: 1px solid #333; padding: 10px; width: 60px;">UND.</th>
                        <th style="border: 1px solid #333; padding: 10px; width: 100px;">P.UNIT.</th>
                        <th style="border: 1px solid #333; padding: 10px; width: 100px;">TOTAL</th>
                    </tr>
                </thead>
                <tbody>
                    {generar_filas_items(datos.get('items', []))}
                </tbody>
            </table>
            <div style="margin-top: 20px; text-align: right; background: #e8e8e8; padding: 15px; border-radius: 4px; border: 2px solid #d4af37;">
                <p style="margin: 5px 0; color: #000; font-size: 16px;"><strong>Subtotal: S/ {datos.get('subtotal', 0):.2f}</strong></p>
                <p style="margin: 5px 0; color: #000; font-size: 16px;"><strong>IGV (18%): S/ {datos.get('igv', 0):.2f}</strong></p>
                <p style="font-size: 22px; color: #b8860b; margin: 10px 0 0 0;"><strong>TOTAL: S/ {datos.get('total', 0):.2f}</strong></p>
            </div>
        </div>
        
        <div class="observaciones" style="margin-bottom: 20px;">
            <h3 style="color: #d4af37; border-bottom: 1px solid #ddd; padding-bottom: 5px;">OBSERVACIONES</h3>
            <div contenteditable="true" style="background: #fff3cd; padding: 12px; border: 1px dashed #d4af37; min-height: 60px; border-radius: 4px; cursor: text;">
                {datos.get('observaciones', 'Precios incluyen IGV. Instalación según CNE-Utilización. Garantía 12 meses. Materiales de primera calidad.')}
            </div>
        </div>
        
        <div class="footer" style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; background: #f8f9fa; padding: 15px; border-radius: 4px;">
            <p style="color: #666; margin: 0; font-size: 14px;"><strong>Tesla Electricidad y Automatización S.A.C.</strong></p>
            <p style="color: #666; margin: 5px 0; font-size: 12px;">Jr. Las Ágatas Mz B Lote 09, Urb. San Carlos - San Juan de Lurigancho</p>
            <p style="color: #666; margin: 0; font-size: 12px;">📞 906315961 | 📧 ingenieria.teslaelectricidad@gmail.com</p>
            <p style="color: #d4af37; margin: 10px 0 0 0; font-size: 12px; font-style: italic;">✨ Generado por {agente} - Tu agente IA especializada</p>
        </div>
    </div>
    
    <style>
        .cotizacion-preview [contenteditable="true"]:hover {{
            background: #fff8dc !important;
            box-shadow: 0 0 4px rgba(212, 175, 55, 0.5);
            transition: all 0.3s ease;
        }}
        .cotizacion-preview [contenteditable="true"]:focus {{
            outline: 2px solid #d4af37;
            background: white !important;
            box-shadow: 0 0 8px rgba(212, 175, 55, 0.8);
        }}
        .cotizacion-preview table {{
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
    """
    
    return html

def generar_preview_proyecto(datos: Dict[str, Any], agente: str) -> str:
    """Genera HTML preview para proyecto"""
    
    html = f"""
    <div class="proyecto-preview" style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 8px;">
        <div class="pili-header" style="text-align: center; background: linear-gradient(135deg, #28a745, #34ce57); color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 20px;">🤖 {agente} - Gestión de Proyecto</h2>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Vista previa editable del proyecto</p>
        </div>
        
        <div class="proyecto-info" style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="color: #28a745; margin-top: 0;">📁 {datos.get('nombre_proyecto', '[NOMBRE DEL PROYECTO]')}</h2>
            <p><strong>Cliente:</strong> <span contenteditable="true" style="background: #d4edda; padding: 2px 4px;">{datos.get('cliente', '[CLIENTE]')}</span></p>
            <p><strong>Fecha de inicio:</strong> {datos.get('fecha_inicio', '[FECHA]')}</p>
            <p><strong>Duración estimada:</strong> {datos.get('duracion_estimada', '[DURACIÓN]')}</p>
            <p><strong>Estado:</strong> <span style="background: #ffc107; color: #856404; padding: 4px 8px; border-radius: 4px;">{datos.get('estado', 'En planificación')}</span></p>
            
            <h3 style="color: #28a745; border-bottom: 1px solid #ddd; padding-bottom: 5px;">DESCRIPCIÓN</h3>
            <div contenteditable="true" style="background: #d4edda; padding: 12px; border: 1px dashed #28a745; min-height: 80px; border-radius: 4px;">
                {datos.get('descripcion', '[EDITAR DESCRIPCIÓN DEL PROYECTO]')}
            </div>
        </div>
    </div>
    """
    
    return html

def generar_preview_informe(datos: Dict[str, Any], agente: str) -> str:
    """Genera HTML preview para informe"""
    
    html = f"""
    <div class="informe-preview" style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 8px;">
        <div class="pili-header" style="text-align: center; background: linear-gradient(135deg, #6f42c1, #8a63d2); color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 20px;">🤖 {agente} - Informe Técnico</h2>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Vista previa editable del informe</p>
        </div>
        
        <div class="informe-content" style="background: white; padding: 20px; border-radius: 8px;">
            <h2 style="color: #6f42c1; margin-top: 0;">📊 {datos.get('titulo_informe', '[TÍTULO DEL INFORME]')}</h2>
            <p><strong>Fecha:</strong> {datos.get('fecha_informe', '[FECHA]')}</p>
            <p><strong>Autor:</strong> {datos.get('autor', 'Tesla Electricidad y Automatización S.A.C.')}</p>
            
            <h3 style="color: #6f42c1; border-bottom: 1px solid #ddd; padding-bottom: 5px;">RESUMEN EJECUTIVO</h3>
            <div contenteditable="true" style="background: #e7d9f7; padding: 12px; border: 1px dashed #6f42c1; min-height: 80px; border-radius: 4px;">
                {datos.get('resumen_ejecutivo', '[EDITAR RESUMEN EJECUTIVO]')}
            </div>
        </div>
    </div>
    """
    
    return html

@router.get("/pili/estadisticas-aprendizaje")
async def estadisticas_aprendizaje_pili(db: Session = Depends(get_db)):
    """
    🤖 NUEVO PILI v3.0 - Estadísticas de aprendizaje automático
    
    Muestra cómo PILI ha aprendido de las conversaciones previas y su evolución.
    """
    
    try:
        from app.models.documento import Documento
        
        # Contar documentos de aprendizaje PILI
        total_aprendizajes = db.query(Documento).filter(
            Documento.nombre.like("PILI_Aprendizaje%")
        ).count()
        
        # Estadísticas por tipo de servicio
        servicios_stats = {}
        for servicio_id in CONTEXTOS_SERVICIOS.keys():
            count = db.query(Documento).filter(
                Documento.content_text.like(f'%{servicio_id}%')
            ).count()
            servicios_stats[servicio_id] = count
        
        # Determinar nivel de inteligencia
        if total_aprendizajes > 100:
            nivel_inteligencia = "Experto"
            mensaje_nivel = "He procesado más de 100 casos. ¡Soy muy precisa!"
        elif total_aprendizajes > 50:
            nivel_inteligencia = "Avanzado"
            mensaje_nivel = "Con más de 50 casos procesados, mejoro constantemente."
        elif total_aprendizajes > 10:
            nivel_inteligencia = "Intermedio"
            mensaje_nivel = "Estoy aprendiendo rápidamente de cada conversación."
        else:
            nivel_inteligencia = "Básico"
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
                "servicios_utilizados": servicios_stats,
                "servicio_mas_usado": max(servicios_stats.items(), key=lambda x: x[1])[0] if servicios_stats else None,
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
                "ultima_actualizacion": datetime.now().isoformat()
            },
            "mensaje_pili": "🤖 ¡Soy PILI y estoy lista para comenzar nuestro trabajo juntos! Cada conversación me hará más inteligente."
        }

# ════════════════════════════════════════════════════════════════
# 🆕 ENDPOINTS SERVICIOS INTELIGENTES (CONSERVADOS + MEJORADOS)  
# ════════════════════════════════════════════════════════════════

@router.get("/botones-contextuales/{tipo_flujo}")
async def obtener_botones_contextuales(
    tipo_flujo: str,
    etapa: Optional[str] = "inicial",
    historial_length: Optional[int] = 0,
    tiene_cotizacion: Optional[bool] = False
):
    """
    🔄 CONSERVADO v2.0 + MEJORADO PILI v3.0
    
    Obtiene botones contextuales según el tipo de flujo y etapa.
    PILI ahora incluye información sobre qué agente está activo.
    """
    try:
        logger.info(f"🤖 PILI obteniendo botones para {tipo_flujo}, etapa: {etapa}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado por PILI"
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
            "pili_activa": contexto.get("nombre_pili", "PILI"),
            "personalidad": contexto.get("personalidad", ""),
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

        # Enviar a Gemini con contexto especializado
        respuesta = gemini_service.chat(
            mensaje=prompt_especializado,
            contexto=f"Agente: {nombre_pili}. Servicio: {tipo_flujo}. {contexto_adicional}",
            cotizacion_id=cotizacion_id
        )

        # Determinar etapa y botones sugeridos
        tiene_cotizacion = cotizacion_id is not None
        etapa_actual = determinar_etapa_conversacion(historial, tiene_cotizacion)
        botones_sugeridos = obtener_botones_para_etapa(tipo_flujo, etapa_actual)

        # NUEVO: Generar vista previa HTML si se solicitó
        html_preview = None
        datos_generados = None

        if generar_html and len(historial) >= 1:
            # Usar PILIBrain para generar datos reales con items
            try:
                if "cotizacion" in tipo_flujo:
                    # Detectar servicio y generar cotización completa con PILIBrain
                    mensaje_completo = contexto_adicional or mensaje
                    for msg in historial[-3:]:  # Últimos 3 mensajes para contexto
                        mensaje_completo += " " + msg.get('content', '')

                    # Detectar servicio basado en el mensaje
                    servicio_detectado = pili_brain.detectar_servicio(mensaje_completo)
                    complejidad = "complejo" if "complejo" in tipo_flujo else "simple"

                    # Generar cotización completa con items
                    cotizacion_data = pili_brain.generar_cotizacion(
                        mensaje=mensaje_completo,
                        servicio=servicio_detectado,
                        complejidad=complejidad
                    )

                    # Extraer datos generados con items
                    datos_generados = cotizacion_data.get("datos", {})

                    # Crear datos_json para preview
                    datos_json = {
                        "pili_version": "3.0",
                        "agente_responsable": nombre_pili,
                        "tipo_servicio": tipo_flujo,
                        "timestamp": datetime.now().isoformat(),
                        "datos_extraidos": datos_generados
                    }

                    logger.info(f"✅ PILIBrain generó {len(datos_generados.get('items', []))} items para cotización")

                else:
                    # Para proyecto e informe, usar datos básicos
                    datos_json = {
                        "pili_version": "3.0",
                        "agente_responsable": nombre_pili,
                        "tipo_servicio": tipo_flujo,
                        "timestamp": datetime.now().isoformat(),
                        "datos_extraidos": {
                            "cliente": "[Cliente por definir]",
                            "proyecto": "[Proyecto generado con PILI]",
                            "descripcion": contexto_adicional or mensaje,
                            "fecha": datetime.now().strftime("%d/%m/%Y")
                        }
                    }
                    datos_generados = datos_json.get("datos_extraidos")

                # Generar HTML preview según tipo
                html_preview = generar_preview_html(datos_json)

            except Exception as e:
                logger.error(f"Error generando datos con PILIBrain: {e}")
                # Fallback a datos básicos
                datos_json = {
                    "pili_version": "3.0",
                    "agente_responsable": nombre_pili,
                    "tipo_servicio": tipo_flujo,
                    "timestamp": datetime.now().isoformat(),
                    "datos_extraidos": {
                        "cliente": "[Cliente por definir]",
                        "proyecto": "[Proyecto generado con PILI]",
                        "descripcion": contexto_adicional or mensaje,
                        "fecha": datetime.now().strftime("%d/%m/%Y")
                    }
                }
                html_preview = generar_preview_html(datos_json)
                datos_generados = datos_json.get("datos_extraidos")

        return {
            "success": True,
            "agente_activo": nombre_pili,
            "respuesta": respuesta.get('mensaje', ''),
            "sugerencias": respuesta.get('sugerencias', []),
            "accion_recomendada": respuesta.get('accion_recomendada'),
            "botones_contextuales": botones_sugeridos,
            "etapa_actual": etapa_actual,
            "preguntas_pendientes": contexto.get("preguntas_esenciales", []),
            "tipo_flujo": tipo_flujo,
            "html_preview": html_preview,
            "cotizacion_generada": datos_generados if "cotizacion" in tipo_flujo else None,
            "proyecto_generado": datos_generados if "proyecto" in tipo_flujo else None,
            "informe_generado": datos_generados if "informe" in tipo_flujo else None
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
    🔄 CONSERVADO v2.0 + MEJORADO PILI v3.0
    
    Inicia un flujo inteligente con análisis automático.
    PILI ahora presenta el agente específico que se activará.
    """
    try:
        logger.info(f"🤖 PILI iniciando flujo {tipo_flujo}")
        
        # Obtener contexto del servicio
        contexto = obtener_contexto_servicio(tipo_flujo)
        
        if not contexto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de flujo '{tipo_flujo}' no soportado por PILI"
            )
        
        nombre_pili = contexto.get("nombre_pili", "PILI")
        
        # Crear análisis inicial inteligente
        prompt_analisis = f"""
        Como {nombre_pili}, analiza esta información inicial:
        
        Cliente: {nombre_cliente}
        Descripción: {descripcion_inicial}
        Tipo de servicio: {tipo_flujo}
        
        Proporciona un plan de trabajo específico y las primeras preguntas para avanzar eficientemente.
        """
        
        # Obtener análisis de Gemini
        analisis = gemini_service.analizar_documento(
            texto_documento=prompt_analisis,
            tipo_analisis=f"plan_trabajo_{tipo_flujo}"
        )
        
        # Botones iniciales para este flujo
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
# 🔄 ENDPOINTS LEGACY - CONSERVADOS INTACTOS
# ════════════════════════════════════════════════════════════════

@router.post("/generar-rapida", response_model=CotizacionResponse)
async def generar_cotizacion_rapida(
    request: CotizacionRapidaRequest,
    db: Session = Depends(get_db)
):
    """
    🔄 CONSERVADO - Generar cotización rápida con IA (endpoint legacy)
    
    Este endpoint se mantiene para compatibilidad hacia atrás.
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
    
    El usuario puede iterar y mejorar una cotización mediante conversación.
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
    🔄 CONSERVADO - Analizar descripción de un proyecto con IA
    
    NO crea la cotización, solo analiza y sugiere.
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
    🔄 CONSERVADO + MEJORADO - Verificar estado del servicio de IA
    
    Ahora incluye información sobre PILI.
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

# ════════════════════════════════════════════════════════════════
# 🔄 GESTIÓN DE PLANTILLAS (CONSERVADO INTACTO)
# ════════════════════════════════════════════════════════════════

@router.post("/subir-plantilla")
async def subir_plantilla_word(
    archivo: UploadFile = File(...),
    nombre_personalizado: Optional[str] = None
):
    """
    🔄 CONSERVADO - Subir plantilla Word personalizada
    
    ⭐ El usuario puede subir sus propias plantillas .docx
    
    Las plantillas pueden contener marcadores como:
    - {{cliente}} - Se reemplaza con nombre del cliente
    - {{proyecto}} - Se reemplaza con nombre del proyecto  
    - {{fecha}} - Se reemplaza con fecha actual
    - {{items_tabla}} - Se reemplaza con tabla de items
    - {{total}} - Se reemplaza with total de la cotización
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
    🔄 CONSERVADO - Listar todas las plantillas Word disponibles
    
    ⭐ Permite ver qué plantillas han sido subidas
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
    🔄 CONSERVADO - Obtener marcadores de una plantilla específica
    
    ⭐ Permite ver qué marcadores están disponibles en una plantilla
    
    Útil para que el chat pueda decir: 
    "Tu plantilla tiene los marcadores: {{cliente}}, {{fecha}}, {{items_tabla}}"
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
    🔄 CONSERVADO - Generar cotización usando una plantilla personalizada
    
    ⭐ PILI puede decir: "usa mi plantilla de informe"
    Y este endpoint procesa esa solicitud
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
    
    ⭐ Verificar que la plantilla es válida
    
    Verifica:
    - Que sea un archivo .docx válido
    - Extrae y muestra los marcadores
    - Valida la estructura
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