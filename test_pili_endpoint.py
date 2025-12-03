import requests
import json

# Prueba del endpoint de PILI
url = "http://localhost:8000/api/chat/chat-contextualizado"

payload = {
    "tipo_flujo": "cotizacion-simple",
    "mensaje": "Necesito cotizar una instalación eléctrica para una casa de 120m2",
    "historial": [],
    "contexto_adicional": "",
    "archivos_procesados": []
}

print("=" * 80)
print("PRUEBA DE FUEGO - PILI CHAT CONTEXTUALIZADO")
print("=" * 80)
print()
print("📤 Enviando mensaje a PILI...")
print(f"Mensaje: {payload['mensaje']}")
print()

try:
    response = requests.post(url, json=payload, timeout=15)
    
    print(f"📊 Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        
        print("✅ RESPUESTA EXITOSA")
        print("=" * 80)
        print()
        
        if data.get('success'):
            print(f"🤖 Agente: {data.get('agente_activo', 'N/A')}")
            print()
            print("💬 Respuesta de PILI:")
            print("-" * 80)
            respuesta = data.get('respuesta', '')
            print(respuesta)
            print("-" * 80)
            print()
            print(f"📏 Longitud de respuesta: {len(respuesta)} caracteres")
            print()
            
            # Verificar si es una respuesta corta (correcto) o larga (incorrecto)
            if len(respuesta) < 200:
                print("✅ CORRECTO: Respuesta corta e inteligente (< 200 caracteres)")
            else:
                print("⚠️  ATENCIÓN: Respuesta larga (> 200 caracteres)")
            
            print()
            print("📋 Datos adicionales:")
            if data.get('botones_contextuales'):
                print(f"  - Botones: {data.get('botones_contextuales')}")
            if data.get('etapa_actual'):
                print(f"  - Etapa: {data.get('etapa_actual')}")
            if data.get('html_preview'):
                print(f"  - Vista HTML: Generada ({len(data.get('html_preview', ''))} caracteres)")
                
        else:
            print("❌ ERROR: success = False")
            print(f"Mensaje: {data.get('error', 'Sin mensaje de error')}")
    else:
        print(f"❌ ERROR HTTP {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("⏱️  TIMEOUT: El servidor tardó más de 15 segundos en responder")
except requests.exceptions.ConnectionError:
    print("🔌 ERROR DE CONEXIÓN: No se pudo conectar al servidor")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {str(e)}")

print()
print("=" * 80)
