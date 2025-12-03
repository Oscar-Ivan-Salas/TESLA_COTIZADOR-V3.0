"""
═══════════════════════════════════════════════════════════════
TESLA COTIZADOR V3.0 - APLICACIÓN PRINCIPAL FASTAPI
═══════════════════════════════════════════════════════════════
Autor: Sistema de Arquitectura Profesional
Versión: 3.0.0

DESCRIPCIÓN:
Aplicación FastAPI principal con todos los routers, middleware y
configuraciones para producción.
═══════════════════════════════════════════════════════════════
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uvicorn
from typing import List, Optional
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Tesla Cotizador API v3.0",
    description="API profesional para sistema de cotización y gestión de proyectos",
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
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# RUTAS ESTÁTICAS
# ═══════════════════════════════════════════════════════════════
storage_path = Path("./backend/storage/generados")
storage_path.mkdir(parents=True, exist_ok=True)

app.mount("/storage", StaticFiles(directory=str(storage_path)), name="storage")

# ═══════════════════════════════════════════════════════════════
# ENDPOINT DE SALUD
# ═══════════════════════════════════════════════════════════════
@app.get("/")
async def root():
    """Endpoint raíz - verifica que la API está funcionando"""
    return {
        "message": "Tesla Cotizador API v3.0",
        "status": "online",
        "version": "3.0.0",
        "docs": "/docs",
        "health": "/health",
        "frontend_compatible": True
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": "Tesla Cotizador API",
        "version": "3.0.0"
    }

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS TEMPORALES (Hasta implementar routers completos)
# ═══════════════════════════════════════════════════════════════

# Modelos para el frontend dinámico
from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    tipo_flujo: str
    mensaje: str
    historial: List[dict] = []
    contexto_adicional: str = ""
    archivos_procesados: List[dict] = []
    generar_html: bool = True

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload temporal de archivos
    TODO: Mover a router de documentos
    """
    try:
        # Guardar archivo
        file_path = Path(f"./backend/storage/documentos/{file.filename}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "success": True,
            "filename": file.filename,
            "size": len(content),
            "path": str(file_path)
        }
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/chat-contextualizado")
async def chat_contextualizado(request: ChatRequest):
    """
    Chat principal para frontend dinámico
    Compatible con split-screen y vista previa HTML
    """
    try:
        logger.info(f"Chat dinámico: {request.tipo_flujo} - {request.mensaje[:50]}...")
        
        # Determinar tipo de respuesta
        es_primera = len(request.historial) == 0
        
        if 'cotizacion' in request.tipo_flujo:
            if es_primera:
                respuesta = """¡Hola! 👋 Soy Tesla IA especializada en cotizaciones eléctricas.

Para generar una cotización precisa, necesito conocer:

📋 **Información del proyecto:**
• ¿Qué tipo de instalación necesitas?
• ¿Residencial, comercial o industrial?
• ¿Metros cuadrados aproximados?

💡 **Ejemplo:** "Instalación eléctrica completa para casa de 120m² con 15 puntos de luz y 10 tomacorrientes"

¿Puedes contarme los detalles?"""
                
                return {
                    "success": True,
                    "respuesta": respuesta,
                    "html_preview": None,
                    "botones_contextuales": [
                        "🏠 Casa residencial 120m²",
                        "🏢 Oficina comercial 200m²", 
                        "🏭 Local industrial 500m²",
                        "💡 Solo puntos de luz",
                        "🔌 Instalación completa"
                    ]
                }
            else:
                # Generar cotización
                cotizacion_demo = {
                    "cliente": "Cliente Demo",
                    "proyecto": "Instalación Eléctrica",
                    "items": [
                        {
                            "descripcion": "Punto de luz empotrado LED 18W",
                            "cantidad": 15,
                            "precioUnitario": 25.0,
                            "capitulo": "ELECTRICIDAD"
                        },
                        {
                            "descripcion": "Tomacorriente doble con línea a tierra", 
                            "cantidad": 12,
                            "precioUnitario": 35.0,
                            "capitulo": "ELECTRICIDAD"
                        },
                        {
                            "descripcion": "Interruptor simple",
                            "cantidad": 8, 
                            "precioUnitario": 18.0,
                            "capitulo": "ELECTRICIDAD"
                        }
                    ]
                }
                
                # Generar HTML
                html_preview = generar_html_cotizacion(cotizacion_demo)
                
                return {
                    "success": True,
                    "respuesta": "¡Perfecto! He generado una cotización inicial basada en tu proyecto. Puedes editarla en tiempo real en la vista previa.",
                    "html_preview": html_preview,
                    "cotizacion_generada": cotizacion_demo,
                    "botones_contextuales": [
                        "📋 Agregar más items",
                        "💰 Ajustar precios", 
                        "📏 Cambiar cantidades",
                        "✅ Generar documento final"
                    ]
                }
        
        elif 'proyecto' in request.tipo_flujo:
            if es_primera:
                return {
                    "success": True,
                    "respuesta": """¡Excelente! 🚀 Te ayudo a planificar tu proyecto.

Para crear un plan detallado necesito:

🎯 **Objetivos:**
• ¿Cuál es el resultado esperado?
• ¿Hay fechas límite importantes?

📊 **Recursos:** 
• Presupuesto estimado
• Duración aproximada

¡Cuéntame más detalles!""",
                    "botones_contextuales": [
                        "🏗️ Proyecto de construcción",
                        "⚡ Instalación eléctrica",
                        "🤖 Sistema automatización",
                        "📅 Proyecto con plazo fijo",
                        "💰 Presupuesto limitado"
                    ]
                }
            else:
                proyecto_demo = {
                    "fases": ["Planificación", "Ejecución", "Entrega"],
                    "hitos": ["Inicio del proyecto", "50% de avance", "Finalización"],
                    "recursos": ["Personal técnico", "Materiales", "Equipos"]
                }
                
                html_preview = generar_html_proyecto(proyecto_demo)
                
                return {
                    "success": True,
                    "respuesta": "Perfecto. He estructurado tu proyecto con fases, hitos y recursos necesarios.",
                    "html_preview": html_preview,
                    "proyecto_generado": proyecto_demo
                }
        
        else:  # informes
            if es_primera:
                return {
                    "success": True,
                    "respuesta": """¡Perfecto! 📄 Te ayudo a crear un informe profesional.

Necesito saber:

📈 **Tipo de informe:**
• ¿Técnico, ejecutivo o de avance?
• ¿Qué información debe incluir?

🎯 **Audiencia:**
• ¿Para quién es el informe?
• ¿Qué formato prefieres?""",
                    "botones_contextuales": [
                        "📊 Informe ejecutivo",
                        "🔧 Informe técnico",
                        "📈 Reporte de avance",
                        "🏗️ Informe de proyecto",
                        "📋 Análisis de resultados"
                    ]
                }
            else:
                informe_demo = {
                    "secciones": ["Resumen Ejecutivo", "Desarrollo", "Conclusiones"],
                    "contenido": "Informe técnico profesional"
                }
                
                html_preview = generar_html_informe(informe_demo)
                
                return {
                    "success": True,
                    "respuesta": "Excelente. He creado la estructura de tu informe profesional.",
                    "html_preview": html_preview,
                    "informe_generado": informe_demo
                }
        
        # Respuesta por defecto
        return {
            "success": True,
            "respuesta": "¡Hola! ¿En qué puedo ayudarte hoy?",
            "botones_contextuales": ["💡 Cotización", "📁 Proyecto", "📄 Informe"]
        }
        
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        return {
            "success": False,
            "respuesta": f"Error: {str(e)}",
            "html_preview": None
        }

def generar_html_cotizacion(datos: dict) -> str:
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

def generar_html_proyecto(datos: dict) -> str:
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
    </div>"""

def generar_html_informe(datos: dict) -> str:
    """Genera HTML para informe"""
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 100%; padding: 20px; background: white; color: #333;">
        <div style="border-bottom: 3px solid #16a34a; padding-bottom: 20px; margin-bottom: 20px;">
            <h1 style="color: #16a34a; margin: 0; font-size: 24px;">INFORME TÉCNICO</h1>
            <p style="color: #D4AF37; font-weight: bold; margin: 5px 0;">Tesla Electricidad y Automatización S.A.C.</p>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h2 style="color: #16a34a; margin-bottom: 15px;">Estructura del Informe</h2>
            <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #16a34a;">
                <h3 style="color: #16a34a; margin-top: 0;">Secciones</h3>
                <ol>
                    {' '.join([f"<li>{seccion}</li>" for seccion in datos.get('secciones', [])])}
                </ol>
            </div>
        </div>
    </div>"""

@app.get("/api/chat/botones-contextuales/{tipo_flujo}")
async def obtener_botones_contextuales(tipo_flujo: str, etapa: str = "inicial"):
    """Botones contextuales para el frontend"""
    botones_base = {
        "inicial": ["🏠 Residencial", "🏢 Comercial", "🏭 Industrial", "💡 LED", "🔌 Tomacorrientes"],
        "refinamiento": ["📋 Más items", "💰 Precios", "📏 Cantidades", "✅ Finalizar"]
    }
    
    return {
        "success": True,
        "tipo_flujo": tipo_flujo,
        "etapa": etapa,
        "botones": botones_base.get(etapa, botones_base["inicial"])
    }

# Endpoints para guardar documentos (cotizaciones, proyectos, informes)
@app.post("/api/cotizaciones/")
async def guardar_cotizacion(data: dict):
    """Guardar cotización en sistema"""
    try:
        from datetime import datetime
        import json
        
        cotizacion_id = f"COT-{datetime.now().strftime('%Y%m%d%H%M')}"
        
        # Guardar en archivo JSON temporal (en producción usar BD)
        storage_path = Path("./backend/storage/generados")
        storage_path.mkdir(parents=True, exist_ok=True)
        
        datos_cotizacion = data.copy()
        datos_cotizacion["id"] = cotizacion_id
        datos_cotizacion["created_at"] = datetime.now().isoformat()
        
        archivo_json = storage_path / f"{cotizacion_id}.json"
        with open(archivo_json, "w", encoding="utf-8") as f:
            json.dump(datos_cotizacion, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Cotización guardada: {cotizacion_id}")
        return {"success": True, "id": cotizacion_id}
        
    except Exception as e:
        logger.error(f"Error guardando cotización: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/proyectos/")
async def guardar_proyecto(data: dict):
    """Guardar proyecto"""
    try:
        from datetime import datetime
        proyecto_id = f"PROJ-{datetime.now().strftime('%Y%m%d%H%M')}"
        logger.info(f"Proyecto guardado: {proyecto_id}")
        return {"success": True, "id": proyecto_id}
    except Exception as e:
        logger.error(f"Error guardando proyecto: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/informes/")
async def guardar_informe(data: dict):
    """Guardar informe"""
    try:
        from datetime import datetime
        informe_id = f"INF-{datetime.now().strftime('%Y%m%d%H%M')}"
        logger.info(f"Informe guardado: {informe_id}")
        return {"success": True, "id": informe_id}
    except Exception as e:
        logger.error(f"Error guardando informe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para generar documentos
@app.post("/api/cotizaciones/{cotizacion_id}/generar-pdf")
async def generar_cotizacion_pdf(cotizacion_id: str):
    """Generar PDF de cotización"""
    try:
        logger.info(f"Generando PDF para cotización: {cotizacion_id}")
        # Simulación - en producción generar PDF real
        return JSONResponse(
            content={"message": f"PDF generado para {cotizacion_id}", "tipo": "cotizacion"},
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cotizaciones/{cotizacion_id}/generar-word")
async def generar_cotizacion_word(cotizacion_id: str):
    """Generar Word de cotización"""
    try:
        logger.info(f"Generando Word para cotización: {cotizacion_id}")
        # Simulación - en producción generar Word real con logo
        return JSONResponse(
            content={"message": f"Word generado para {cotizacion_id}", "logo_incluido": True},
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        logger.error(f"Error generando Word: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints similares para proyectos e informes
@app.post("/api/proyectos/{proyecto_id}/generar-{formato}")
async def generar_proyecto_doc(proyecto_id: str, formato: str):
    """Generar documento de proyecto"""
    try:
        return {"message": f"{formato.upper()} de proyecto generado", "id": proyecto_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/informes/{informe_id}/generar-{formato}")
async def generar_informe_doc(informe_id: str, formato: str):
    """Generar documento de informe"""
    try:
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
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# ═══════════════════════════════════════════════════════════════
# EJECUCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    logger.info("🚀 Iniciando Tesla Cotizador API v3.0...")
    logger.info("📍 Backend: http://localhost:8000")
    logger.info("📚 Docs: http://localhost:8000/docs")
    logger.info("🌐 Frontend compatible: Sí")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )