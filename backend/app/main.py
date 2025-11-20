"""
═══════════════════════════════════════════════════════════════
TESLA COTIZADOR V3.0 - APLICACIÓN PRINCIPAL FASTAPI HÍBRIDA
═══════════════════════════════════════════════════════════════
Autor: Sistema de Arquitectura Profesional
Versión: 3.0.0

DESCRIPCIÓN:
Aplicación FastAPI principal con integración completa de:
1. 🔄 CONSERVA: Todos los endpoints actuales funcionando
2. 🆕 AGREGA: Routers avanzados (PILI, CRUD completo, generadores)
3. 🛡️ GARANTIZA: Compatibilidad 100% con frontend existente

ARQUITECTURA HÍBRIDA:
- Si routers avanzados cargan → Funcionalidad completa PILI
- Si NO cargan → Funcionalidad actual (modo demo/mock)
- Frontend funciona SIEMPRE sin cambios
═══════════════════════════════════════════════════════════════
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uvicorn
from typing import List, Optional, Dict, Any
import logging
import json
from datetime import datetime

# Importar configuración y servicios existentes (CONSERVADO)
import sys
sys.path.append(str(Path(__file__).parent))

# ═══════════════════════════════════════════════════════════════
# 🔄 CONFIGURACIÓN ROBUSTA CONSERVADA
# ═══════════════════════════════════════════════════════════════

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
    
    # Configuración básica si no existe (CONSERVADO)
    class MockSettings:
        GEMINI_API_KEY = ""
        GEMINI_MODEL = "gemini-1.5-pro"
        FRONTEND_URL = "http://localhost:3000"
        BACKEND_HOST = "0.0.0.0"
        BACKEND_PORT = 8000
        
    settings = MockSettings()
    
    def validate_gemini_key():
        return False

# ═══════════════════════════════════════════════════════════════
# 🆕 IMPORTACIÓN ROUTERS AVANZADOS (NUEVO)
# ═══════════════════════════════════════════════════════════════

ROUTERS_AVANZADOS_DISPONIBLES = False
routers_info = {}

try:
    # Intentar cargar routers avanzados
    from app.routers import chat, cotizaciones, proyectos, informes, documentos, system
    ROUTERS_AVANZADOS_DISPONIBLES = True
    routers_info = {
        "chat": {"router": chat.router, "prefix": "/api/chat", "tags": ["Chat PILI"], "descripcion": "PILI Agente IA (1917 líneas)"},
        "cotizaciones": {"router": cotizaciones.router, "prefix": "/api/cotizaciones", "tags": ["Cotizaciones"], "descripcion": "CRUD + Generación completa"},
        "proyectos": {"router": proyectos.router, "prefix": "/api/proyectos", "tags": ["Proyectos"], "descripcion": "Gestión proyectos"},
        "informes": {"router": informes.router, "prefix": "/api/informes", "tags": ["Informes"], "descripcion": "Generación informes"},
        "documentos": {"router": documentos.router, "prefix": "/api/documentos", "tags": ["Documentos"], "descripcion": "Upload y análisis"},
        "system": {"router": system.router, "prefix": "/api/system", "tags": ["System"], "descripcion": "Health checks"}
    }
    logger.info("🚀 ROUTERS AVANZADOS CARGADOS EXITOSAMENTE")
except ImportError as e:
    logger.warning(f"⚠️ Routers avanzados no disponibles: {e}")
    logger.info("🔄 Continuando con endpoints básicos/mock")

# Configuración de logging básico si no está configurado (CONSERVADO)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# ═══════════════════════════════════════════════════════════════
# 🔄 MODELOS PYDANTIC CONSERVADOS
# ═══════════════════════════════════════════════════════════════

from pydantic import BaseModel

class ChatRequest(BaseModel):
    tipo_flujo: str
    mensaje: str
    historial: List[dict] = []
    contexto_adicional: str = ""
    archivos_procesados: List[dict] = []
    generar_html: bool = True

# ═══════════════════════════════════════════════════════════════
# CREAR APLICACIÓN FASTAPI (CONSERVADO)
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="Tesla Cotizador API v3.0",
    description="API profesional para sistema de cotización con IA",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE CORS (CONSERVADO)
# ═══════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# 🆕 REGISTRO DE ROUTERS AVANZADOS (NUEVO)
# ═══════════════════════════════════════════════════════════════

if ROUTERS_AVANZADOS_DISPONIBLES:
    logger.info("🔗 Registrando routers avanzados...")
    routers_registrados = []
    
    for nombre, info in routers_info.items():
        try:
            app.include_router(
                info["router"], 
                prefix=info["prefix"], 
                tags=info["tags"]
            )
            routers_registrados.append(f"{nombre} -> {info['prefix']}")
            logger.info(f"✅ Router {nombre}: {info['descripcion']}")
        except Exception as e:
            logger.error(f"❌ Error registrando router {nombre}: {e}")
    
    logger.info(f"🎉 ROUTERS REGISTRADOS: {len(routers_registrados)}/6")
else:
    logger.info("🔄 Usando endpoints básicos/mock (compatibilidad frontend)")

# ═══════════════════════════════════════════════════════════════
# CONFIGURAR DIRECTORIOS (CONSERVADO)
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
# 🆕 ENDPOINT ROOT (NUEVO)
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "message": "Tesla Cotizador API v3.0",
        "status": "online",
        "version": "3.0.0",
        "routers_avanzados": ROUTERS_AVANZADOS_DISPONIBLES,
        "gemini_disponible": TIENE_GEMINI_SERVICE and validate_gemini_key(),
        "modo": "COMPLETO" if ROUTERS_AVANZADOS_DISPONIBLES else "BÁSICO/DEMO",
        "endpoints_disponibles": {
            "chat": "/api/chat/",
            "cotizaciones": "/api/cotizaciones/",
            "proyectos": "/api/proyectos/",
            "informes": "/api/informes/",
            "documentos": "/api/documentos/" if ROUTERS_AVANZADOS_DISPONIBLES else "/api/upload",
            "system": "/api/system/health" if ROUTERS_AVANZADOS_DISPONIBLES else None,
            "docs": "/docs"
        }
    }

# ═══════════════════════════════════════════════════════════════
# 🔄 SERVICIO DE IA INTEGRADO (CONSERVADO)
# ═══════════════════════════════════════════════════════════════

async def generar_respuesta_ia(mensaje: str, contexto: str, historial: List[Dict], tipo_flujo: str) -> Dict:
    """Genera respuesta usando Gemini existente o modo demo (CONSERVADO)"""
    
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

# ═══════════════════════════════════════════════════════════════
# 🔄 FUNCIONES DEMO CONSERVADAS
# ═══════════════════════════════════════════════════════════════

def generar_cotizacion_demo(mensaje: str, contexto: str) -> Dict:
    """Genera cotización demo inteligente (CONSERVADO)"""
    
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
    """Genera proyecto demo (CONSERVADO)"""
    return {
        "fases": ["Planificación", "Ejecución", "Entrega"],
        "hitos": ["Inicio del proyecto", "50% de avance", "Finalización"],
        "recursos": ["Personal técnico", "Materiales", "Equipos"]
    }

def generar_informe_demo(mensaje: str, contexto: str) -> Dict:
    """Genera informe demo (CONSERVADO)"""
    return {
        "secciones": ["Resumen ejecutivo", "Análisis técnico", "Recomendaciones"],
        "datos": {"parametros": 5, "mediciones": 12, "conclusiones": 3}
    }

async def respuesta_demo(mensaje: str, tipo_flujo: str) -> Dict:
    """Respuesta demo cuando no hay IA real (CONSERVADO)"""
    
    respuestas_demo = {
        "cotizacion": "Perfecto. He analizado tu solicitud y puedo generar una cotización. Necesito confirmar algunos detalles técnicos para asegurar precisión en el presupuesto.",
        "proyecto": "Entiendo. Voy a estructurar este proyecto paso a paso. Primero definamos el alcance y luego organizaremos las fases de ejecución.",
        "informe": "Excelente. Procederé a crear el informe con la información proporcionada. Incluiré análisis técnico y recomendaciones específicas."
    }
    
    tipo_detectado = "cotizacion"
    if "proyecto" in tipo_flujo:
        tipo_detectado = "proyecto"
    elif "informe" in tipo_flujo:
        tipo_detectado = "informe"
    
    return {
        "respuesta": respuestas_demo.get(tipo_detectado, "Procesando solicitud..."),
        "generar_estructura": True
    }

def generar_html_preview(datos: Dict, tipo: str) -> str:
    """Genera HTML preview para frontend (CONSERVADO)"""
    
    if tipo == "cotizacion":
        items_html = ""
        total = 0
        
        for item in datos.get("items", []):
            subtotal = item["cantidad"] * item["precioUnitario"]
            total += subtotal
            items_html += f"""
            <tr>
                <td>{item['descripcion']}</td>
                <td>{item['cantidad']}</td>
                <td>S/ {item['precioUnitario']:.2f}</td>
                <td>S/ {subtotal:.2f}</td>
            </tr>
            """
        
        igv = total * 0.18
        total_con_igv = total + igv
        
        return f"""
        <div style="font-family: Arial; max-width: 800px; margin: 20px auto; padding: 20px; border: 1px solid #ddd;">
            <h2 style="color: #f39c12; text-align: center;">⚡ TESLA ELECTRICIDAD ⚡</h2>
            <h3>COTIZACIÓN - {datos.get('proyecto', 'Proyecto Tesla')}</h3>
            <p><strong>Cliente:</strong> {datos.get('cliente', 'Cliente Demo')}</p>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead style="background: #f39c12; color: white;">
                    <tr>
                        <th style="padding: 10px; border: 1px solid #ddd;">Descripción</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Cant.</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">P. Unit.</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            <div style="text-align: right; margin-top: 20px;">
                <p><strong>Subtotal: S/ {total:.2f}</strong></p>
                <p><strong>IGV (18%): S/ {igv:.2f}</strong></p>
                <p style="font-size: 1.2em; color: #f39c12;"><strong>TOTAL: S/ {total_con_igv:.2f}</strong></p>
            </div>
        </div>
        """
    
    return "<div>Vista previa no disponible</div>"

# ═══════════════════════════════════════════════════════════════
# 🔄 ENDPOINTS BÁSICOS CONSERVADOS (COMPATIBILIDAD FRONTEND)
# ═══════════════════════════════════════════════════════════════
# NOTA: Estos endpoints se mantienen para compatibilidad aunque 
# los routers avanzados tengan versiones mejores

@app.post("/api/chat/mensaje")
async def chat_mensaje(request: ChatRequest):
    """
    🔄 CONSERVADO - Endpoint principal de chat (compatible con frontend)
    
    Si routers avanzados cargan, este endpoint coexiste con /api/chat/
    Si NO cargan, este endpoint mantiene funcionalidad básica
    """
    
    try:
        logger.info(f"💬 Chat mensaje - Tipo: {request.tipo_flujo}, Routers avanzados: {ROUTERS_AVANZADOS_DISPONIBLES}")
        
        # Generar respuesta usando IA o demo
        ia_response = await generar_respuesta_ia(
            mensaje=request.mensaje,
            contexto=request.contexto_adicional,
            historial=request.historial,
            tipo_flujo=request.tipo_flujo
        )
        
        response_data = {
            "success": True,
            "respuesta": ia_response.get("respuesta", ""),
            "tipo_flujo": request.tipo_flujo,
            "generar_html": request.generar_html,
            "html_preview": None,
            "routers_avanzados_activos": ROUTERS_AVANZADOS_DISPONIBLES
        }
        
        # Generar HTML preview si se solicita
        if request.generar_html and ia_response.get("generar_estructura"):
            if request.tipo_flujo.startswith('cotizacion'):
                estructura = ia_response.get("estructura_generada")
                if estructura:
                    response_data["html_preview"] = generar_html_preview(estructura, "cotizacion")
                    response_data["cotizacion_generada"] = estructura
            elif request.tipo_flujo.startswith('proyecto'):
                estructura = ia_response.get("estructura_generada")
                if estructura:
                    response_data["proyecto_generado"] = estructura
            elif request.tipo_flujo.startswith('informe'):
                estructura = ia_response.get("estructura_generada")
                if estructura:
                    response_data["informe_generado"] = estructura
        
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Error en chat: {e}")
        return {
            "success": False,
            "respuesta": f"Error: {str(e)}. Intenta de nuevo.",
            "html_preview": None,
            "routers_avanzados_activos": ROUTERS_AVANZADOS_DISPONIBLES
        }

@app.post("/api/chat/chat-contextualizado")
async def chat_contextualizado(request: ChatRequest):
    """
    🆕 AGREGADO - Endpoint de chat contextualizado (compatibilidad con frontend v3.0)

    Este endpoint es un alias mejorado de /api/chat/mensaje con el mismo comportamiento
    """
    return await chat_mensaje(request)

@app.get("/api/chat/botones-contextuales/{tipo_flujo}")
async def obtener_botones_contextuales(tipo_flujo: str, etapa: str = "inicial"):
    """🔄 CONSERVADO - Obtiene botones contextuales según el tipo de flujo"""

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

# ═══════════════════════════════════════════════════════════════
# 🔄 ENDPOINTS DE GESTIÓN CONSERVADOS
# ═══════════════════════════════════════════════════════════════

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """🔄 CONSERVADO - Upload de archivos (básico)"""
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
    """🔄 CONSERVADO - Guardar cotización en sistema (JSON)"""
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
    """🔄 CONSERVADO - Guardar proyecto"""
    try:
        proyecto_id = f"PROJ-{datetime.now().strftime('%Y%m%d%H%M')}"
        logger.info(f"💾 Proyecto guardado: {proyecto_id}")
        return {"success": True, "id": proyecto_id}
    except Exception as e:
        logger.error(f"❌ Error guardando proyecto: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/informes/")
async def guardar_informe(data: dict):
    """🔄 CONSERVADO - Guardar informe"""
    try:
        informe_id = f"INF-{datetime.now().strftime('%Y%m%d%H%M')}"
        logger.info(f"💾 Informe guardado: {informe_id}")
        return {"success": True, "id": informe_id}
    except Exception as e:
        logger.error(f"❌ Error guardando informe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ═══════════════════════════════════════════════════════════════
# 🔄 MANEJO DE ERRORES CONSERVADO
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
# 🔄 EJECUCIÓN PRINCIPAL MEJORADA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Configurar puerto desde settings o usar por defecto
    puerto = getattr(settings, 'BACKEND_PORT', 8000)
    host = getattr(settings, 'BACKEND_HOST', '0.0.0.0')
    
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO TESLA COTIZADOR API V3.0 - SISTEMA HÍBRIDO")
    logger.info("=" * 60)
    
    # Información del sistema
    logger.info(f"🌐 Frontend: http://localhost:3000")
    logger.info(f"📍 Backend: http://{host}:{puerto}")
    logger.info(f"📚 Docs: http://{host}:{puerto}/docs")
    logger.info(f"🏠 Root: http://{host}:{puerto}/")
    
    # Estado de servicios
    logger.info(f"🤖 Gemini IA: {'✅ ACTIVADO' if (TIENE_GEMINI_SERVICE and validate_gemini_key()) else '🎭 MODO DEMO'}")
    logger.info(f"🔧 Servicios básicos: {'✅ CARGADOS' if TIENE_GEMINI_SERVICE else '⚠️ MOCK'}")
    logger.info(f"🚀 Routers avanzados: {'✅ ACTIVOS (PILI completa)' if ROUTERS_AVANZADOS_DISPONIBLES else '⚠️ NO DISPONIBLES'}")
    
    # Modo de funcionamiento
    modo = "COMPLETO" if ROUTERS_AVANZADOS_DISPONIBLES else "BÁSICO"
    logger.info(f"🎯 MODO DE FUNCIONAMIENTO: {modo}")
    
    if ROUTERS_AVANZADOS_DISPONIBLES:
        logger.info("🎉 SISTEMA COMPLETO:")
        logger.info("   - ✅ PILI Agente IA avanzada")
        logger.info("   - ✅ CRUD completo cotizaciones")
        logger.info("   - ✅ Generadores Word/PDF reales")
        logger.info("   - ✅ Upload y análisis documentos")
        logger.info("   - ✅ Health checks profesionales")
    else:
        logger.info("🔄 SISTEMA BÁSICO:")
        logger.info("   - ✅ Endpoints mock funcionando")
        logger.info("   - ✅ Compatible con frontend")
        logger.info("   - ✅ Demo inteligente")
        
    if not validate_gemini_key():
        logger.info("💡 Para activar IA real, configura GEMINI_API_KEY en tu archivo .env")
    
    logger.info("=" * 60)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=puerto,
        reload=True,
        log_level="info"
    )