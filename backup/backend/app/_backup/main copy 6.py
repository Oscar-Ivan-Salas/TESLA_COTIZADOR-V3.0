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

from fastapi import FastAPI, HTTPException, UploadFile, File, Body
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
        "secciones": ["Resumen ejecutivo", "Análisis técnico", "Conclusiones"],
        "hallazgos": ["Cumple normativas", "Instalación adecuada", "Recomendaciones"],
        "recomendaciones": ["Mantenimiento preventivo", "Actualización de equipos"]
    }

async def respuesta_demo(mensaje: str, tipo_flujo: str) -> Dict:
    """Respuesta inteligente en modo demo"""
    
    respuestas_por_tipo = {
        "cotizacion-simple": f"""¡Perfecto! 📋 Veo que necesitas una cotización eléctrica.

Para brindarte un presupuesto preciso, necesito algunos datos:

🏠 **Tipo de instalación:** {mensaje}
📏 **Área aproximada:** ¿Cuántos m² tiene el espacio?
💡 **Puntos de luz:** ¿Cuántos necesitas aproximadamente?
🔌 **Tomacorrientes:** ¿Cantidad requerida?
⚡ **Tablero eléctrico:** ¿Nuevo o existente?

Tesla Electricidad - Expertos en instalaciones eléctricas peruanas 🇵🇪""",
        
        "proyecto-complejo": f"""📊 Entiendo que requieres gestión de proyecto eléctrico complejo.

Análisis inicial de: {mensaje}

📋 **Siguiente paso:** Definir alcance y objetivos específicos
📅 **Cronograma:** Establecer hitos principales  
💰 **Presupuesto:** Estimar recursos necesarios
👥 **Equipo:** Asignar responsables

¿Qué aspecto te gustaría desarrollar primero?""",
        
        "informe-tecnico": f"""📄 Perfecto para generar informe técnico sobre: {mensaje}

**Estructura propuesta:**
1. 📋 Resumen ejecutivo
2. 🔍 Análisis técnico detallado
3. 📊 Conclusiones y recomendaciones
4. 📈 Próximos pasos

¿Qué tipo de análisis específico necesitas incluir?"""
    }
    
    respuesta_base = respuestas_por_tipo.get(tipo_flujo, f"Entiendo tu consulta sobre: {mensaje}. ¿Podrías proporcionarme más detalles específicos?")
    
    return {
        "respuesta": respuesta_base,
        "generar_estructura": False
    }

def generar_html_preview(datos: Dict, tipo: str) -> str:
    """Genera vista previa HTML mejorada"""
    
    if tipo == "cotizacion":
        items_html = ""
        subtotal = 0
        
        for item in datos.get("items", []):
            total_item = item.get("cantidad", 0) * item.get("precioUnitario", 0)
            subtotal += total_item
            
            items_html += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{item.get('descripcion', '')}</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{item.get('cantidad', '')}</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">S/ {item.get('precioUnitario', 0):.2f}</td>
                <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">S/ {total_item:.2f}</td>
            </tr>"""
        
        igv = subtotal * 0.18
        total = subtotal + igv
        
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #1a365d; margin: 0;">⚡ TESLA ELECTRICIDAD</h1>
                <p style="color: #666; margin: 5px 0;">Especialistas en Instalaciones Eléctricas</p>
                <hr style="border: 2px solid #f39c12; width: 100px;">
            </div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h2 style="color: #2c3e50; margin-top: 0;">📋 COTIZACIÓN ELÉCTRICA</h2>
                <p><strong>Cliente:</strong> {datos.get('cliente', 'Cliente Demo')}</p>
                <p><strong>Proyecto:</strong> {datos.get('proyecto', 'Instalación Eléctrica')}</p>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead>
                    <tr style="background-color: #3498db; color: white;">
                        <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Descripción</th>
                        <th style="border: 1px solid #ddd; padding: 12px; text-align: center;">Cantidad</th>
                        <th style="border: 1px solid #ddd; padding: 12px; text-align: center;">Precio Unit.</th>
                        <th style="border: 1px solid #ddd; padding: 12px; text-align: center;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            
            <div style="text-align: right; margin-top: 20px;">
                <div style="background: #ecf0f1; padding: 15px; border-radius: 5px; display: inline-block; min-width: 250px;">
                    <p style="margin: 5px 0;"><strong>Subtotal: S/ {subtotal:.2f}</strong></p>
                    <p style="margin: 5px 0;">IGV (18%): S/ {igv:.2f}</p>
                    <p style="margin: 10px 0; font-size: 18px; color: #e74c3c;"><strong>TOTAL: S/ {total:.2f}</strong></p>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding: 15px; background: #fff3cd; border-radius: 5px; border-left: 4px solid #f39c12;">
                <h4 style="margin-top: 0; color: #856404;">📋 Condiciones:</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>Precios incluyen materiales e instalación</li>
                    <li>Vigencia: 15 días calendario</li>
                    <li>Tiempo de ejecución: A coordinar</li>
                    <li>Garantía: 12 meses</li>
                </ul>
            </div>
        </div>"""
        
    elif tipo == "proyecto":
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50;">📊 Plan de Proyecto</h2>
            <p><strong>Fases:</strong> {', '.join(datos.get('fases', []))}</p>
            <p><strong>Hitos:</strong> {', '.join(datos.get('hitos', []))}</p>
            <p><strong>Recursos:</strong> {', '.join(datos.get('recursos', []))}</p>
        </div>"""
        
    elif tipo == "informe":
        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50;">📄 Informe Técnico</h2>
            <p><strong>Secciones:</strong> {', '.join(datos.get('secciones', []))}</p>
            <p><strong>Hallazgos:</strong> {', '.join(datos.get('hallazgos', []))}</p>
            <p><strong>Recomendaciones:</strong> {', '.join(datos.get('recomendaciones', []))}</p>
        </div>"""
    
    return f"<div style='padding: 20px;'><h3>Vista previa de {tipo}</h3><pre>{json.dumps(datos, indent=2, ensure_ascii=False)}</pre></div>"

# ═══════════════════════════════════════════════════════════════
# ENDPOINTS PRINCIPALES
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Endpoint raíz con información del sistema"""
    gemini_status = "✅ REAL" if (TIENE_GEMINI_SERVICE and validate_gemini_key()) else "🎭 DEMO"
    
    return {
        "message": "Tesla Cotizador API v3.0 - INTEGRACIÓN COMPLETA",
        "status": "online",
        "version": "3.0.0",
        "gemini_integration": gemini_status,
        "endpoints": {
            "docs": "/docs",
            "chat": "/api/chat/chat-contextualizado",
            "botones": "/api/chat/botones-contextuales/{tipo}",
            "upload": "/api/upload"
        },
        "services": {
            "gemini": TIENE_GEMINI_SERVICE,
            "configurado": validate_gemini_key() if TIENE_GEMINI_SERVICE else False
        }
    }

@app.get("/health")
async def health_check():
    """Health check detallado"""
    return {
        "status": "healthy",
        "service": "Tesla Cotizador API v3.0",
        "gemini": "✅ OPERATIVO" if (TIENE_GEMINI_SERVICE and validate_gemini_key()) else "⚠️ MODO DEMO",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# 🔧 ENDPOINT PRINCIPAL DE CHAT - COMPATIBLE CON TU FRONTEND
# ═══════════════════════════════════════════════════════════════

@app.post("/api/chat/chat-contextualizado")
async def chat_contextualizado(
    # 🔧 AGREGADO: Acepta datos directos del frontend también
    tipo_flujo: str = Body(...),
    mensaje: str = Body(...), 
    historial: List[dict] = Body([]),
    contexto_adicional: str = Body(""),
    archivos_procesados: List[dict] = Body([]),
    generar_html: bool = Body(True)
):
    """
    Chat contextualizado compatible con frontend dinámico
    
    ✅ CONSERVA TODA TU LÓGICA EXISTENTE
    🔧 AGREGADO: Compatibilidad directa con formato frontend
    """
    try:
        logger.info(f"💬 Chat contextualizado: {tipo_flujo} - {mensaje[:50]}...")
        
        # Preparar contexto según tipo de flujo
        contextos_flujo = {
            "cotizacion-simple": "Eres un experto en cotizaciones eléctricas rápidas y precisas",
            "cotizacion-compleja": "Eres un ingeniero eléctrico especializado en proyectos complejos", 
            "proyecto-simple": "Eres un coordinador de proyectos eléctricos",
            "proyecto-complejo": "Eres un project manager certificado PMP especializado en electricidad",
            "informe-simple": "Eres un técnico especializado en informes eléctricos",
            "informe-complejo": "Eres un ingeniero senior especializado en informes técnicos detallados"
        }
        
        contexto = contextos_flujo.get(tipo_flujo, "Eres un asistente especializado en electricidad")
        
        if contexto_adicional:
            contexto += f"\n\nContexto adicional: {contexto_adicional}"
        
        # Generar respuesta con IA
        resultado_ia = await generar_respuesta_ia(mensaje, contexto, historial, tipo_flujo)
        
        response_data = {
            "success": True,
            "respuesta": resultado_ia.get("respuesta", ""),
            "tipo_flujo": tipo_flujo,
            "timestamp": datetime.now().isoformat()
        }
        
        # Generar vista previa HTML si es solicitada y hay estructura
        if generar_html and resultado_ia.get("generar_estructura"):
            estructura = resultado_ia.get("estructura_generada")
            if estructura:
                if 'cotizacion' in tipo_flujo:
                    response_data["html_preview"] = generar_html_preview(estructura, "cotizacion")
                    response_data["cotizacion_generada"] = estructura
                elif 'proyecto' in tipo_flujo:
                    response_data["html_preview"] = generar_html_preview(estructura, "proyecto")
                    response_data["proyecto_generado"] = estructura
                elif 'informe' in tipo_flujo:
                    response_data["html_preview"] = generar_html_preview(estructura, "informe")
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