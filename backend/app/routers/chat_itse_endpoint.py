

# ═══════════════════════════════════════════════════════════════
# 🤖 PILI ITSE CHATBOT - Endpoint usando CAJA NEGRA
# ═══════════════════════════════════════════════════════════════

# Importar caja negra
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot

# Crear instancia global
pili_itse_bot = PILIITSEChatBot()

@router.post("/pili-itse")
async def chat_pili_itse(request: ChatRequest):
    """
    Endpoint para PILI ITSE usando CAJA NEGRA
    
    La lógica está en: Pili_ChatBot/pili_itse_chatbot.py
    """
    try:
        mensaje = request.mensaje
        estado = request.conversation_state if hasattr(request, 'conversation_state') else None
        
        logger.info(f"🤖 PILI ITSE - Mensaje: {mensaje[:50] if mensaje else 'INICIO'}...")
        logger.info(f"📊 Estado recibido: {estado}")
        
        # Llamar a la caja negra
        resultado = pili_itse_bot.procesar(mensaje, estado)
        
        logger.info(f"✅ Resultado: success={resultado['success']}, etapa={resultado['estado'].get('etapa')}")
        
        # Formatear respuesta
        response = {
            "success": resultado['success'],
            "respuesta": resultado['respuesta'],
            "botones_sugeridos": resultado.get('botones'),
            "botones": resultado.get('botones'),
            "state": resultado['estado'],
            "conversation_state": resultado['estado'],
            "datos_generados": resultado.get('cotizacion'),
            "cotizacion_generada": resultado.get('cotizacion') is not None,
            "agente_pili": "PILI ITSE"
        }
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en PILI ITSE: {e}", exc_info=True)
        return {
            "success": False,
            "respuesta": "Lo siento, hubo un error. Por favor intenta de nuevo.",
            "botones_sugeridos": None,
            "botones": None,
            "state": estado or {},
            "conversation_state": estado or {},
            "datos_generados": None,
            "cotizacion_generada": False,
            "agente_pili": "PILI ITSE"
        }
