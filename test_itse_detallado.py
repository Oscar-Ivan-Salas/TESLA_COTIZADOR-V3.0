import requests
import json

print("="*80)
print("TEST DETALLADO - ENDPOINT ITSE")
print("="*80)

url = "http://localhost:8000/api/chat/chat-contextualizado"

payload = {
    "tipo_flujo": "itse",
    "mensaje": "Hola",
    "historial": [],
    "contexto_adicional": "Servicio: itse",
    "generar_html": True,
    "conversation_state": None
}

print("\n📤 PAYLOAD ENVIADO:")
print(json.dumps(payload, indent=2))

try:
    response = requests.post(url, json=payload, timeout=10)
    
    print(f"\n📥 STATUS CODE: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n✅ RESPUESTA EXITOSA")
        print("="*80)
        
        # Mostrar campos clave
        print(f"\n🔑 success: {data.get('success')}")
        print(f"🔑 agente_pili: {data.get('agente_pili', 'NO PRESENTE')}")
        
        respuesta = data.get("respuesta", "")
        print(f"\n📝 RESPUESTA (primeros 200 caracteres):")
        print(respuesta[:200])
        
        # Verificar contenido
        print("\n🔍 ANÁLISIS:")
        if "ITSE" in respuesta or "certificado" in respuesta.lower():
            print("✅ CORRECTO: Respuesta contiene contenido de ITSE")
        elif "Eléctric" in respuesta or "CNE" in respuesta:
            print("❌ INCORRECTO: Respuesta contiene contenido de ELECTRICIDAD")
        else:
            print("⚠️ DESCONOCIDO: No se puede determinar el tipo")
        
        # Botones
        botones = data.get("botones_sugeridos", data.get("botones", []))
        print(f"\n🔘 BOTONES: {len(botones)}")
        if botones:
            print("Primeros 3 botones:")
            for btn in botones[:3]:
                print(f"  - {btn}")
        
        # Datos generados
        if data.get("datos_generados"):
            print(f"\n📊 datos_generados presente: SÍ")
            print(f"   Servicio: {data['datos_generados'].get('servicio', 'NO PRESENTE')}")
        else:
            print(f"\n📊 datos_generados presente: NO")
        
        # HTML Preview
        if data.get("html_preview"):
            print(f"\n🌐 html_preview presente: SÍ ({len(data['html_preview'])} caracteres)")
        else:
            print(f"\n🌐 html_preview presente: NO")
            
    else:
        print(f"\n❌ ERROR HTTP {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"\n❌ EXCEPCIÓN: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
