# test_gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import sys

# Cargar variables de entorno
env_path = '.env'
print(f"📄 Intentando cargar variables de entorno desde: {os.path.abspath(env_path)}")
if not os.path.exists(env_path):
    print("\n❌ ERROR: No se encontró el archivo .env.")
    sys.exit(1)
    
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("\n❌ ERROR: La variable GEMINI_API_KEY no está configurada en el archivo .env")
    sys.exit(1)
    
print(f"🔑 API Key encontrada. Últimos 4 caracteres: ...{api_key[-4:]}")

# Configurar la API de Google
print("   Configurando cliente de Google Gemini...")
genai.configure(api_key=api_key)

try:
    # Listar modelos disponibles
    print("   Obteniendo modelos disponibles...")
    for m in genai.list_models():
        print(f"   - {m.name}")

    # Usar el modelo
    print("\n   Probando generación de contenido...")
    try:
        # Primero intentamos con gemini-2.0-flash
        model_name = 'gemini-2.0-flash'
        print(f"   Intentando con el modelo: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hola, ¿puedes decirme 'OK' si todo funciona bien?")
    except Exception as e:
        print(f"   Error con {model_name}: {str(e)}")
        # Si falla, intentamos con gemini-2.5-flash
        try:
            model_name = 'gemini-2.5-flash'
            print(f"   Intentando con el modelo: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hola, ¿puedes decirme 'OK' si todo funciona bien?")
        except Exception as e2:
            print(f"   Error con {model_name}: {str(e2)}")
            # Si ambos fallan, probamos con el modelo más reciente
            model_name = 'gemini-2.5-flash-latest'
            print(f"   Intentando con el modelo: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hola, ¿puedes decirme 'OK' si todo funciona bien?")
    
    print("\n" + "="*50)
    print("✅ ¡ÉXITO! La conexión con la API de Google Gemini funciona correctamente.")
    print(f"   Respuesta: {response.text}")
    print("="*50)
    
except Exception as e:
    print("\n" + "="*50)
    print("❌ ¡ERROR! No se pudo conectar con la API de Google Gemini.")
    print(f"   Detalles del error: {str(e)}")
    print("="*50)