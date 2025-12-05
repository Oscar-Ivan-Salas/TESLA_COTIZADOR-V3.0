import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Configurar un logger simple para este script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables desde backend/.env
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
if not os.path.exists(env_path):
    logging.error(f"Error: No se encontró el archivo .env en la ruta: {env_path}")
    exit()

load_dotenv(dotenv_path=env_path)

# Obtener la clave de API
API_KEY = os.getenv("GEMINI_API_KEY")

async def test_api_key():
    """
    Script de prueba aislado para validar la clave de API de Gemini.
    """
    if not API_KEY or API_KEY == "tu_gemini_api_key_aqui":
        logging.error("La variable GEMINI_API_KEY no está configurada en el archivo backend/.env o sigue siendo el valor por defecto.")
        return

    logging.info(f"Clave de API encontrada. Últimos 4 caracteres: ...{API_KEY[-4:]}")
    
    try:
        logging.info("Configurando la librería de Google con la clave de API...")
        genai.configure(api_key=API_KEY)
        
        MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        logging.info(f"Creando el modelo generativo '{MODEL_NAME}'...")
        model = genai.GenerativeModel(MODEL_NAME)
        
        logging.info("Enviando una solicitud de prueba simple a la API de Gemini...")
        response = await model.generate_content_async("Hola, solo estoy haciendo una prueba. Responde 'OK' si me recibes.")
        
        logging.info("Respuesta recibida de la API.")
        
        print("\n" + "="*50)
        print("✅ ✅ ✅  ÉXITO  ✅ ✅ ✅")
        print("="*50)
        print("La clave de API es VÁLIDA y la conexión con Gemini funciona.")
        print(f"Respuesta de Gemini: {response.text.strip()}")
        print("="*50)

    except Exception as e:
        print("\n" + "="*50)
        print("❌ ❌ ❌  FALLO  ❌ ❌ ❌")
        print("="*50)
        print("Ocurrió un error al intentar comunicarse con la API de Gemini.")
        print("Esto confirma que la aplicación no puede usar la IA por esta razón.")
        print("\n--- DETALLES DEL ERROR ---")
        print(f"Tipo de Error: {type(e).__name__}")
        print(f"Mensaje: {e}")
        print("="*50)
        print("\n--- POSIBLES CAUSAS ---")
        print("1. La clave de API es incorrecta, ha sido revocada o ha expirado.")
        print("2. La API de 'generativelanguage' no está habilitada en tu proyecto de Google Cloud.")
        print("3. Hay un problema de red o un firewall que bloquea la conexión a los servidores de Google.")
        print("="*50)

if __name__ == "__main__":
    asyncio.run(test_api_key())
