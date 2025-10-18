import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
from app.core.config import settings

# Configurar Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
    async def generar_cotizacion(
        self,
        descripcion_proyecto: str,
        contexto_documentos: Optional[List[str]] = None,
        historial_chat: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Genera una cotización completa usando Gemini AI
        """
        
        # Construir el prompt
        prompt = self._construir_prompt_cotizacion(
            descripcion_proyecto,
            contexto_documentos,
            historial_chat
        )
        
        try:
            response = self.model.generate_content(prompt)
            
            # Parsear la respuesta
            cotizacion_data = self._parsear_respuesta_cotizacion(response.text)
            
            return {
                "exito": True,
                "cotizacion": cotizacion_data,
                "respuesta_ia": response.text
            }
            
        except Exception as e:
            return {
                "exito": False,
                "error": str(e),
                "respuesta_ia": None
            }
    
    async def chat_conversacional(
        self,
        mensaje: str,
        historial: List[Dict[str, str]],
        contexto: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Chat conversacional para refinar cotizaciones
        """
        
        prompt = self._construir_prompt_chat(mensaje, historial, contexto)
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "exito": True,
                "respuesta": response.text,
                "cotizacion_actualizada": self._extraer_cotizacion_si_existe(response.text)
            }
            
        except Exception as e:
            return {
                "exito": False,
                "error": str(e)
            }
    
    async def analizar_documento(self, contenido: str, tipo: str) -> Dict[str, Any]:
        """
        Analiza un documento y extrae información relevante para cotización
        """
        
        prompt = f"""
Eres un asistente experto en análisis de documentos para cotizaciones.

TIPO DE DOCUMENTO: {tipo}

CONTENIDO DEL DOCUMENTO:
{contenido[:5000]}  # Limitar a 5000 caracteres

TAREA:
Extrae la siguiente información del documento (si existe):
1. Cliente/Empresa mencionada
2. Servicios o productos mencionados
3. Cantidades mencionadas
4. Precios mencionados
5. Fechas relevantes
6. Requisitos específicos del proyecto
7. Cualquier otra información relevante para una cotización

RESPONDE EN FORMATO JSON:
{{
    "cliente": "nombre del cliente si se menciona",
    "servicios": ["servicio1", "servicio2"],
    "cantidades": {{"servicio": cantidad}},
    "precios": {{"servicio": precio}},
    "fechas": ["fecha1", "fecha2"],
    "requisitos": ["req1", "req2"],
    "resumen": "resumen breve del documento",
    "datos_relevantes": {{"clave": "valor"}}
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Intentar parsear JSON
            texto = response.text.strip()
            # Limpiar markdown si existe
            if "```json" in texto:
                texto = texto.split("```json")[1].split("```")[0].strip()
            elif "```" in texto:
                texto = texto.split("```")[1].split("```")[0].strip()
            
            datos = json.loads(texto)
            
            return {
                "exito": True,
                "datos_extraidos": datos
            }
            
        except Exception as e:
            return {
                "exito": False,
                "error": str(e),
                "respuesta_raw": response.text if 'response' in locals() else None
            }
    
    def _construir_prompt_cotizacion(
        self,
        descripcion: str,
        contexto_docs: Optional[List[str]],
        historial: Optional[List[Dict[str, str]]]
    ) -> str:
        """
        Construye el prompt para generar cotización
        """
        
        prompt = f"""
Eres un asistente experto en crear cotizaciones profesionales para proyectos en Perú.

DESCRIPCIÓN DEL PROYECTO:
{descripcion}
"""
        
        if contexto_docs and len(contexto_docs) > 0:
            prompt += f"""

INFORMACIÓN DE DOCUMENTOS ANALIZADOS:
{chr(10).join(contexto_docs[:3])}  # Máximo 3 documentos
"""
        
        if historial and len(historial) > 0:
            prompt += "\n\nHISTORIAL DE CONVERSACIÓN:\n"
            for msg in historial[-5:]:  # Últimos 5 mensajes
                role = "Usuario" if msg["role"] == "user" else "Asistente"
                prompt += f"{role}: {msg['content']}\n"
        
        prompt += """

TAREA:
Genera una cotización completa y profesional. Debes proporcionar:

1. Un resumen ejecutivo del proyecto
2. Lista detallada de servicios/productos con:
   - Descripción clara
   - Cantidad estimada
   - Precio unitario realista (en soles peruanos)
   - Total por item
3. Cálculo correcto de:
   - Subtotal
   - IGV (18%)
   - Total

RESPONDE EN FORMATO JSON ESTRICTO:
{
    "resumen": "Resumen ejecutivo del proyecto",
    "cliente": "Nombre sugerido del cliente",
    "proyecto": "Nombre del proyecto",
    "items": [
        {
            "id": 1,
            "descripcion": "Descripción detallada del servicio",
            "cantidad": 1.0,
            "precioUnitario": 1000.00,
            "total": 1000.00
        }
    ],
    "observaciones": "Observaciones adicionales o condiciones",
    "vigencia": "30 días"
}

IMPORTANTE:
- Precios realistas para el mercado peruano
- Descripciones profesionales y claras
- Cantidades lógicas
- NO incluyas texto adicional fuera del JSON
- SOLO responde con el JSON válido
"""
        
        return prompt
    
    def _construir_prompt_chat(
        self,
        mensaje: str,
        historial: List[Dict[str, str]],
        contexto: Optional[Dict[str, Any]]
    ) -> str:
        """
        Construye prompt para chat conversacional
        """
        
        prompt = """
Eres un asistente de cotización inteligente y conversacional.

El usuario está refinando una cotización. Responde de manera natural y profesional.

HISTORIAL:
"""
        
        for msg in historial[-10:]:
            role = "Usuario" if msg["role"] == "user" else "Asistente"
            prompt += f"{role}: {msg['content']}\n"
        
        if contexto:
            prompt += f"\n\nCONTEXTO ACTUAL DE LA COTIZACIÓN:\n{json.dumps(contexto, indent=2, ensure_ascii=False)}\n"
        
        prompt += f"\n\nNUEVO MENSAJE DEL USUARIO:\n{mensaje}\n"
        prompt += """

RESPONDE:
1. De manera conversacional y útil
2. Si el usuario pide cambios en la cotización, proporciona el JSON actualizado
3. Si solo hace preguntas, responde claramente
"""
        
        return prompt
    
    def _parsear_respuesta_cotizacion(self, texto: str) -> Dict[str, Any]:
        """
        Parsea la respuesta de Gemini y extrae el JSON de cotización
        """
        
        try:
            # Limpiar markdown
            if "```json" in texto:
                texto = texto.split("```json")[1].split("```")[0].strip()
            elif "```" in texto:
                texto = texto.split("```")[1].split("```")[0].strip()
            
            # Parsear JSON
            data = json.loads(texto)
            
            # Calcular totales si no existen
            items = data.get("items", [])
            subtotal = sum(item.get("total", 0) for item in items)
            igv = subtotal * 0.18
            total = subtotal + igv
            
            return {
                "cliente": data.get("cliente", "Cliente"),
                "proyecto": data.get("proyecto", "Proyecto"),
                "descripcion": data.get("resumen", ""),
                "items": items,
                "subtotal": round(subtotal, 2),
                "igv": round(igv, 2),
                "total": round(total, 2),
                "observaciones": data.get("observaciones", ""),
                "vigencia": data.get("vigencia", "30 días")
            }
            
        except Exception as e:
            # Si falla el parseo, devolver estructura básica
            return {
                "cliente": "Cliente",
                "proyecto": "Proyecto",
                "items": [],
                "subtotal": 0.0,
                "igv": 0.0,
                "total": 0.0,
                "error_parseo": str(e),
                "respuesta_raw": texto
            }
    
    def _extraer_cotizacion_si_existe(self, texto: str) -> Optional[Dict[str, Any]]:
        """
        Intenta extraer una cotización actualizada del texto de respuesta
        """
        
        if "```json" in texto or "{" in texto:
            try:
                return self._parsear_respuesta_cotizacion(texto)
            except:
                return None
        
        return None

# Instancia global
gemini_service = GeminiService()
