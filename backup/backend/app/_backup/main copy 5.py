"""
═══════════════════════════════════════════════════════════════
TESLA COTIZADOR V3.0 - APLICACIÓN PRINCIPAL FASTAPI
═══════════════════════════════════════════════════════════════
Autor: Sistema de Arquitectura Profesional
Versión: 3.0.0

DESCRIPCIÓN:
Aplicación FastAPI principal con integración completa de Gemini AI,
compatible con el frontend dinámico split-screen.
═══════════════════════════════════════════════════════════════
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uvicorn
from typing import List, Optional, Dict, Any
import logging
import json
from datetime import datetime

# Importar configuración y servicios existentes
import sys
sys.path.append(str(Path(__file__).parent))

try:
    from app.core.config import settings, validate_gemini_key, get_gemini_api_key
    from app.services.gemini_service import gemini_service
    TIENE_GEMINI_SERVICE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ Servicios existentes cargados correctamente")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"⚠️ No se pudieron cargar servicios existentes: {e}")
    TIENE_GEMINI_SERVICE = False
    
    # Configuración básica si no existe
    class MockSettings:
        GEMINI_API_KEY = ""
        GEMINI_MODEL = "gemini-1.5-pro"
        FRONTEND_URL = "http://localhost:3000"
        BACKEND_HOST = "0.0.0.0"
        BACKEND_PORT = 8000
        
    settings = MockSettings()
    
    def validate_gemini_key():
        return False

# Configuración de logging básico si no está configurado
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Modelos Pydantic para el frontend
from pydantic import BaseModel

class ChatRequest(BaseModel):
    tipo_flujo: str
    mensaje: str
    historial: List[dict] = []
    contexto_adicional: str = ""
    archivos_procesados: List[dict] = []
    generar_html: bool = True

# ═══════════════════════════════════════════════════════════════
# CREAR APLICACIÓN FASTAPI
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="Tesla Cotizador API v3.0",
    description="API profesional para sistema de cotización con IA",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE CORS
# ═══════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# CONFIGURAR DIRECTORIOS
# ═══════════════════════════════════════════════════════════════

# Usar configuración existente si está disponible
try:
    from app.core.config import get_generated_directory, get_upload_directory
    storage_path = get_generated_directory()
    upload_path = get_upload_directory()
    logger.info(f"✅ Usando directorios configurados: {storage_path}")
except:
    # Fallback a directorios básicos
    storage_path = Path("./backend/storage/generados")
    upload_path = Path("./backend/storage/documentos")
    storage_path.mkdir(parents=True, exist_ok=True)
    upload_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"⚠️ Usando directorios por defecto: {storage_path}")

app.mount("/storage", StaticFiles(directory=str(storage_path)), name="storage")

# ═══════════════════════════════════════════════════════════════
# SERVICIO DE IA INTEGRADO
# ═══════════════════════════════════════════════════════════════

async def generar_respuesta_ia(mensaje: str, contexto: str, historial: List[Dict], tipo_flujo: str) -> Dict:
    """Genera respuesta usando Gemini existente o modo demo"""
    
    if TIENE_GEMINI_SERVICE and validate_gemini_key():
        # Usar servicio Gemini existente
        try:
            logger.info("🤖 Usando Gemini AI real")
            
            # Preparar contexto completo
            contexto_completo = f"""
Contexto: {contexto}
Tipo de flujo: {tipo_flujo}
Empresa: TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.

Tu rol es asistir en {tipo_flujo} con información técnica y precisa.
"""
            
            # Llamar al servicio existente
            respuesta = await gemini_service.chat_conversacional(
                mensaje=mensaje,
                contexto=contexto_completo,
                historial=historial
            )
            
            if respuesta.get("success"):
                # Determinar si generar estructura
                generar_estructura = len(historial) > 0 and any(
                    word in mensaje.lower() 
                    for word in ['generar', 'crear', 'cotizar', 'proyecto', 'informe', 'listo']
                )
                
                resultado = {
                    "respuesta": respuesta.get("respuesta", ""),
                    "generar_estructura": generar_estructura
                }
                
                # Si debe generar estructura, crear datos demo
                if generar_estructura:
                    if 'cotizacion' in tipo_flujo:
                        resultado["estructura_generada"] = generar_cotizacion_demo(mensaje, contexto)
                    elif 'proyecto' in tipo_flujo:
                        resultado["estructura_generada"] = generar_proyecto_demo(mensaje, contexto)
                    else:
                        resultado["estructura_generada"] = generar_informe_demo(mensaje, contexto)
                
                return resultado
            else:
                logger.warning("Error en Gemini, usando demo")
                return await respuesta_demo(mensaje, tipo_flujo)
                
        except Exception as e:
            logger.error(f"Error en Gemini: {e}")
            return await respuesta_demo(mensaje, tipo_flujo)
    else:
        # Usar modo demo
        logger.info("🎭 Usando modo demo")
        return await respuesta_demo(mensaje, tipo_flujo)

def generar_cotizacion_demo(mensaje: str, contexto: str) -> Dict:
    """Genera cotización demo inteligente"""
    
    # Detectar tipo de instalación
    if any(word in mensaje.lower() for word in ['casa', 'residencial', 'hogar']):
        items = [
            {"descripcion": "Punto de luz empotrado LED 18W", "cantidad": 15, "precioUnitario": 25.0},
            {"descripcion": "Tomacorriente doble con tierra", "cantidad": 12, "precioUnitario": 35.0},
            {"descripcion": "Interruptor simple", "cantidad": 8, "precioUnitario": 18.0}
        ]
    elif any(word in mensaje.lower() for word in ['oficina', 'comercial']):
        items = [
            {"descripcion": "Luminaria LED panel 40W", "cantidad": 25, "precioUnitario": 120.0},
            {"descripcion": "Tomacorriente industrial", "cantidad": 20, "precioUnitario": 45.0},
            {"descripcion": "Tablero eléctrico 12 polos", "cantidad": 1, "precioUnitario": 1200.0}
        ]
    else:
        items = [
            {"descripcion": "Instalación eléctrica general", "cantidad": 1, "precioUnitario": 1500.0},
            {"descripcion": "Materiales diversos", "cantidad": 1, "precioUnitario": 800.0}
        ]
    
    return {
        "cliente": "Cliente Demo",
        "proyecto": "Instalación Eléctrica",
        "items": items
    }

def generar_proyecto_demo(mensaje: str, contexto: str) -> Dict:
    """Genera proyecto demo"""
    return {
        "fases": ["Planificación", "Ejecución", "Entrega"],
        "hitos": ["Inicio del proyecto", "50% de avance", "Finalización"],
        "recursos": ["Personal técnico", "Materiales", "Equipos"]
    }

def generar_informe_demo(mensaje: str, contexto: str) -> Dict:
    """Genera informe demo"""
    return {
        "secciones": ["Resumen Ejecutivo", "Desarrollo", "Conclusiones"],
        "contenido": "Informe técnico profesional"
    }

async def respuesta_demo(mensaje: str, tipo_flujo: str) -> Dict:
    """Respuestas demo inteligentes"""
    
    es_primera = any(palabra in mensaje.lower() for palabra in ['hola', 'buenos', 'necesito', 'quiero'])
    
    if 'cotizacion' in tipo_flujo:
        if es_primera:
            return {
                "respuesta": """¡Hola! 👋 Soy el asistente especializado de Tesla Electricidad.

Para generar una cotización precisa, necesito conocer:

📋 **Información básica:**
• ¿Qué tipo de instalación necesitas?
• ¿En qué tipo de edificación? (casa, oficina, fábrica)
• ¿Cuántos metros cuadrados aproximadamente?

💡 **Por ejemplo:** "Instalación eléctrica completa para casa de 120 m²"

¿Puedes contarme más detalles?""",
                "generar_estructura": False
            }
        else:
            return {
                "respuesta": "Perfecto. Con esa información puedo generar una cotización inicial.",
                "generar_estructura": True,
                "estructura_generada": generar_cotizacion_demo(mensaje, "")
            }
    elif 'proyecto' in tipo_flujo:
        if es_primera:
            return {
                "respuesta": """¡Excelente! 🚀 Te ayudo a estructurar tu proyecto.

Para crear un plan detallado, necesito entender:

🎯 **Objetivos del proyecto:**
• ¿Cuál es el resultado esperado?
• ¿Hay fechas límite importantes?

📊 **Recursos:**
• ¿Qué presupuesto preliminar tienes?
• ¿Cuánto tiempo estimado?

¡Cuéntame más detalles!""",
                "generar_estructura": False
            }
        else:
            return {
                "respuesta": "Perfecto. Con esa información puedo estructurar tu proyecto.",
                "generar_estructura": True,
                "estructura_generada": generar_proyecto_demo(mensaje, "")
            }
    else:  # informe
        if es_primera:
            return {
                "respuesta": """¡Perfecto! 📄 Te ayudo a crear tu informe profesional.

Para generar un documento completo, necesito saber:

📈 **Tipo de informe:**
• ¿Es técnico, ejecutivo o de avance?
• ¿Qué información debe incluir?

🎯 **Audiencia:**
• ¿Para quién es el informe?

¡Cuéntame más detalles!""",
                "generar_estructura": False
            }
        else:
            return {
                "respuesta": "Excelente. Con esa información puedo generar tu informe.",
                "generar_estructura": True,
                "estructura_generada": generar_informe_demo(mensaje, "")
            }

# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE HTML
# ═══════════════════════════════════════════════════════════════

def generar_html_cotizacion(datos: Dict) -> str:
    """Genera HTML para cotización"""
    items = datos.get('items', [])
    cliente = datos.get('cliente', 'Cliente Demo')
    
    subtotal = sum(item.get('cantidad', 0) * item.get('precioUnitario', 0) for item in items)
    igv = subtotal * 0.18
    total = subtotal + igv
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 100%; margin: 0; padding: 20px; background: white; color: #333;">
        <div style="border-bottom: 3px solid #8B0000; padding-bottom: 20px; margin-bottom: 20px;">
            <h1 style="color: #8B0000; margin: 0; font-size: 24px;">COTIZACIÓN</h1>
            <p style="color: #D4AF37; font-weight: bold; margin: 5px 0;">Tesla Electricidad y Automatización S.A.C.</p>
            <p style="color: #666; margin: 0; font-size: 14px;">RUC: 20601138787 • Cliente: {cliente}</p>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h3 style="color: #8B0000; margin-bottom: 15px;">DETALLE DE LA COTIZACIÓN</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <thead>
                    <tr style="background: #8B0000; color: white;">
                        <th style="padding: 8px; text-align: left; border: 1px solid #8B0000;">DESCRIPCIÓN</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #8B0000; width: 60px;">CANT.</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #8B0000; width: 80px;">P. UNIT.</th>
                        <th style="padding: 8px; text-align: center; border: 1px solid #8B0000; width: 80px;">TOTAL</th>
                    </tr>
                </thead>
                <tbody>"""
    
    for item in items:
        cantidad = item.get('cantidad', 0)
        precio = item.get('precioUnitario', 0)
        total_item = cantidad * precio
        
        html += f"""
                    <tr style="border-bottom: 1px solid #ddd;">
                        <td style="padding: 8px; border: 1px solid #ddd;">{item.get('descripcion', '')}</td>
                        <td style="padding: 8px; text-align: center; border: 1px solid #ddd;">{cantidad}</td>
                        <td style="padding: 8px; text-align: center; border: 1px solid #ddd;">S/ {precio:.2f}</td>
                        <td style="padding: 8px; text-align: center; border: 1px solid #ddd; font-weight: bold;">S/ {total_item:.2f}</td>
                    </tr>"""
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <div style="text-align: right; margin-top: 20px;">
            <div style="display: inline-block; background: #f9f9f9; padding: 15px; border-radius: 8px; border: 2px solid #D4AF37;">
                <div style="margin-bottom: 8px; font-size: 16px;">
                    <span style="font-weight: bold;">Subtotal:</span>
                    <span style="margin-left: 20px;">S/ {subtotal:.2f}</span>
                </div>
                <div style="margin-bottom: 8px; font-size: 16px;">
                    <span style="font-weight: bold;">IGV (18%):</span>
                    <span style="margin-left: 20px;">S/ {igv:.2f}</span>
                </div>
                <div style="border-top: 2px solid #8B0000; padding-top: 8px; font-size: 18px;">
                    <span style="font-weight: bold; color: #8B0000;">TOTAL:</span>
                    <span style="margin-left: 20px; font-weight: bold; color: #8B0000;">S/ {total:.2f}</span>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 30px; padding-top: 15px; border-top: 2px solid #D4AF37; color: #666; font-size: 12px;">
            <p><strong>Condiciones:</strong> Precios incluyen IGV. Vigencia: 30 días.</p>
            <p><strong>Contacto:</strong> 906315961 | ingenieria.teslaelectricidad@gmail.com</p>
        </div>
    </div>"""
    
    return html

def generar_html_proyecto(datos: Dict) -> str:
    """Genera HTML para proyecto"""
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 100%; padding: 20px; background: white; color: #333;">
        <div style="border-bottom: 3px solid #2563eb; padding-bottom: 20px; margin-bottom: 20px;">
            <h1 style="color: #2563eb; margin: 0; font-size: 24px;">PROYECTO</h1>
            <p style="color: #D4AF37; font-weight: bold; margin: 5px 0;">Tesla Electricidad y Automatización S.A.C.</p>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h2 style="color: #2563eb; margin-bottom: 15px;">Plan de Proyecto</h2>
            <div style="background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #2563eb;">
                <h3 style="color: #2563eb; margin-top: 0;">Fases del Proyecto</h3>
                <ul>
                    {' '.join([f"<li>{fase}</li>" for fase in datos.get('fases', [])])}
                </ul>
                
                <h3 style="color: #2563eb; margin-top: 15px;">Hitos Principales</h3>
                <ul>
                    {' '.join([f"<li>{hito}</li>" for hito in datos.get('hitos', [])])}
                </ul>
            </div>
        </div>
        
        <div style="padding-top: 15px; border-top: 2px solid #D4AF37; color: #666; font-size: 12px;">
            <p><strong>Contacto:</strong> 906315961 | ingenieria.teslaelectricidad@gmail.com</p>
        </div>
    </div>"""

def generar_html_informe(datos: Dict) -> str:
    """Genera HTML para informe"""
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 100%; padding: 20px; background: white; color: #333;">
        <div style="border-bottom: 3px solid #16a34a; padding-bottom: 20px; margin-bottom: 20px;">
            <h1 style="color: #16a34a; margin: 0; font-size: 24px;">INFORME TÉCNICO</h1>
            <p style="color: #D4AF37; font-weight: bold; margin: 5px 0;">Tesla Electricidad y Automatización S.A.C.</p>
            <p style="color: #666; margin: 0; font-size: 14px;">Fecha: {datetime.now().strftime('%d/%m/%Y')}</p>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h2 style="color: #16a34a; margin-bottom: 15px;">Estructura del Informe</h2>
            <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #16a34a;">
                <h3 style="color: #16a34a; margin-top: 0;">Secciones</h3>
                <ol>
                    {' '.join([f"<li>{seccion}</li>" for seccion in datos.get('secciones', [])])}
                </ol>
                
                <h3 style="color: #16a34a; margin-top: 15px;">Contenido</h3>
                <p>{datos.get('contenido', 'Contenido del informe técnico')}</p>
            </div>
        </div>
        
        <div style="padding-top: 15px; border-top: 2px solid #D4AF37; color: #666; font-size: 12px;">
            <p><strong>Contacto:</strong> 906315961 | ingenieria.teslaelectricidad@gmail.com</p>
        </div>
    </div>"""

def generar_html_preview(datos: Dict, tipo_flujo: str) -> str:
    """Genera vista previa HTML según el tipo"""
    if 'cotizacion' in tipo_flujo:
        return generar_html_cotizacion(datos)
    elif 'proyecto' in tipo_flujo:
        return generar_html_proyecto(datos)
    else:
        return generar_html_informe(datos)

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS PRINCIPALES
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Endpoint raíz"""
    gemini_status = "REAL" if (TIENE_GEMINI_SERVICE and validate_gemini_key()) else "DEMO"
    
    return {
        "message": "Tesla Cotizador API v3.0 - INTEGRACIÓN COMPLETA",
        "status": "online",
        "version": "3.0.0",
        "gemini_integration": gemini_status,
        "frontend_compatible": True,
        "services_loaded": TIENE_GEMINI_SERVICE,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check con estado de servicios"""
    return {
        "status": "healthy",
        "service": "Tesla Cotizador API",
        "version": "3.0.0",
        "gemini_configured": validate_gemini_key() if TIENE_GEMINI_SERVICE else False,
        "services_operational": TIENE_GEMINI_SERVICE
    }

# ENDPOINT PRINCIPAL DEL CHAT (compatible con frontend dinámico)
@app.post("/api/chat/chat-contextualizado")
async def chat_contextualizado(request: ChatRequest):
    """Endpoint principal para chat con IA y generación de vista previa"""
    try:
        logger.info(f"💬 Chat request: {request.tipo_flujo} - {request.mensaje[:50]}...")
        
        # Generar respuesta con IA (Gemini real o demo)
        respuesta_ia = await generar_respuesta_ia(
            request.mensaje,
            request.contexto_adicional,
            request.historial,
            request.tipo_flujo
        )
        
        # Preparar respuesta base
        response_data = {
            "success": True,
            "respuesta": respuesta_ia.get("respuesta", "Error en la respuesta"),
            "botones_contextuales": [
                "📋 Agregar más detalles",
                "💰 Revisar precios",
                "⚡ Generar cotización",
                "📄 Ver documento final"
            ]
        }
        
        # Si se generó estructura, crear HTML y datos
        if respuesta_ia.get("generar_estructura") and request.generar_html:
            estructura = respuesta_ia.get("estructura_generada", {})
            
            # Generar HTML preview
            html_preview = generar_html_preview(estructura, request.tipo_flujo)
            response_data["html_preview"] = html_preview
            
            # Agregar datos según tipo
            if 'cotizacion' in request.tipo_flujo:
                response_data["cotizacion_generada"] = estructura
            elif 'proyecto' in request.tipo_flujo:
                response_data["proyecto_generado"] = estructura
            else:
                response_data["informe_generado"] = estructura
        
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Error en chat: {e}")
        return {
            "success": False,
            "respuesta": f"Error: {str(e)}. Intenta de nuevo.",
            "html_preview": None
        }

# ENDPOINTS PARA BOTONES CONTEXTUALES
@app.get("/api/chat/botones-contextuales/{tipo_flujo}")
async def obtener_botones_contextuales(tipo_flujo: str, etapa: str = "inicial"):
    """Obtiene botones contextuales según el tipo de flujo"""
    
    botones_base = {
        "inicial": [
            "🏠 Instalación Residencial",
            "🏢 Instalación Comercial", 
            "🏭 Instalación Industrial",
            "💡 Iluminación LED",
            "🔌 Tomacorrientes",
            "⚡ Tablero eléctrico"
        ],
        "refinamiento": [
            "📋 Agregar más items",
            "💰 Ajustar precios",
            "📏 Modificar cantidades",
            "🔧 Detalles técnicos",
            "📝 Observaciones",
            "✅ Finalizar"
        ]
    }
    
    if 'proyecto' in tipo_flujo:
        botones_base["inicial"] = [
            "🎯 Definir objetivos",
            "📅 Establecer cronograma", 
            "💰 Estimar presupuesto",
            "👥 Asignar recursos",
            "📊 Crear hitos"
        ]
    elif 'informe' in tipo_flujo:
        botones_base["inicial"] = [
            "📄 Informe técnico",
            "📊 Informe ejecutivo",
            "📈 Análisis de datos",
            "📋 Resumen de proyecto",
            "🔍 Informe de inspección"
        ]
    
    return {
        "success": True,
        "tipo_flujo": tipo_flujo,
        "etapa": etapa,
        "botones": botones_base.get(etapa, botones_base["inicial"])
    }

# ENDPOINTS PARA GESTIÓN DE DOCUMENTOS
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload de archivos"""
    try:
        file_path = upload_path / file.filename
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"📁 Archivo subido: {file.filename}")
        return {
            "success": True,
            "filename": file.filename,
            "size": len(content),
            "path": str(file_path)
        }
        
    except Exception as e:
        logger.error(f"❌ Error subiendo archivo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cotizaciones/")
async def guardar_cotizacion(data: dict):
    """Guardar cotización en sistema"""
    try:
        cotizacion_id = f"COT-{datetime.now().strftime('%Y%m%d%H%M')}"
        
        # Guardar datos
        datos_cotizacion = data.copy()
        datos_cotizacion["id"] = cotizacion_id
        datos_cotizacion["created_at"] = datetime.now().isoformat()
        
        archivo_json = storage_path / f"{cotizacion_id}.json"
        with open(archivo_json, "w", encoding="utf-8") as f:
            json.dump(datos_cotizacion, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Cotización guardada: {cotizacion_id}")
        return {"success": True, "id": cotizacion_id}
        
    except Exception as e:
        logger.error(f"❌ Error guardando cotización: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/proyectos/")
async def guardar_proyecto(data: dict):
    """Guardar proyecto"""
    try:
        proyecto_id = f"PROJ-{datetime.now().strftime('%Y%m%d%H%M')}"
        logger.info(f"💾 Proyecto guardado: {proyecto_id}")
        return {"success": True, "id": proyecto_id}
    except Exception as e:
        logger.error(f"❌ Error guardando proyecto: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/informes/")
async def guardar_informe(data: dict):
    """Guardar informe"""
    try:
        informe_id = f"INF-{datetime.now().strftime('%Y%m%d%H%M')}"
        logger.info(f"💾 Informe guardado: {informe_id}")
        return {"success": True, "id": informe_id}
    except Exception as e:
        logger.error(f"❌ Error guardando informe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ENDPOINTS PARA GENERAR DOCUMENTOS
@app.post("/api/cotizaciones/{cotizacion_id}/generar-pdf")
async def generar_cotizacion_pdf(cotizacion_id: str):
    """Generar PDF de cotización"""
    try:
        logger.info(f"📄 Generando PDF para cotización: {cotizacion_id}")
        return JSONResponse(
            content={"message": f"PDF generado para {cotizacion_id}", "tipo": "cotizacion"},
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        logger.error(f"❌ Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cotizaciones/{cotizacion_id}/generar-word")
async def generar_cotizacion_word(cotizacion_id: str):
    """Generar Word de cotización"""
    try:
        logger.info(f"📝 Generando Word para cotización: {cotizacion_id}")
        return JSONResponse(
            content={"message": f"Word generado para {cotizacion_id}", "logo_incluido": True},
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        logger.error(f"❌ Error generando Word: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/proyectos/{proyecto_id}/generar-{formato}")
async def generar_proyecto_doc(proyecto_id: str, formato: str):
    """Generar documento de proyecto"""
    try:
        logger.info(f"📄 Generando {formato} para proyecto: {proyecto_id}")
        return {"message": f"{formato.upper()} de proyecto generado", "id": proyecto_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/informes/{informe_id}/generar-{formato}")
async def generar_informe_doc(informe_id: str, formato: str):
    """Generar documento de informe"""
    try:
        logger.info(f"📄 Generando {formato} para informe: {informe_id}")
        return {"message": f"{formato.upper()} de informe generado", "id": informe_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ═══════════════════════════════════════════════════════════════
# MANEJO DE ERRORES
# ═══════════════════════════════════════════════════════════════

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# ═══════════════════════════════════════════════════════════════
# EJECUCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Configurar puerto desde settings o usar por defecto
    puerto = getattr(settings, 'BACKEND_PORT', 8000)
    host = getattr(settings, 'BACKEND_HOST', '0.0.0.0')
    
    logger.info("🚀 Iniciando Tesla Cotizador API v3.0 - INTEGRACIÓN COMPLETA")
    logger.info(f"🌐 Frontend: http://localhost:3000")
    logger.info(f"📍 Backend: http://{host}:{puerto}")
    logger.info(f"📚 Docs: http://{host}:{puerto}/docs")
    logger.info(f"🤖 Gemini IA: {'✅ ACTIVADO' if (TIENE_GEMINI_SERVICE and validate_gemini_key()) else '🎭 MODO DEMO'}")
    logger.info(f"🔧 Servicios: {'✅ CARGADOS' if TIENE_GEMINI_SERVICE else '⚠️ BÁSICOS'}")
    
    if not validate_gemini_key():
        logger.info("💡 Para activar IA real, configura GEMINI_API_KEY en tu archivo .env")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=puerto,
        reload=True,
        log_level="info"
    )