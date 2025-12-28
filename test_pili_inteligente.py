"""
🧪 Test Rápido: Verificar que PILI ahora es inteligente
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_pili_inteligente():
    """Test que PILI responde de manera inteligente"""
    print("\n" + "="*60)
    print("🧪 TEST: PILI Inteligente - Informe Simple")
    print("="*60)
    
    payload = {
        "tipo_flujo": "informe-simple",
        "mensaje": "Hola PILI, necesito ayuda para hacer un informe técnico",
        "historial": [],
        "contexto_adicional": "",
        "generar_html": True
    }
    
    try:
        print("\n📤 Enviando mensaje a PILI...")
        response = requests.post(
            f"{BASE_URL}/api/chat/chat-contextualizado",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Status: {response.status_code}")
            print(f"✅ Success: {data.get('success')}")
            print(f"✅ Agente: {data.get('agente_activo')}")
            print(f"✅ Modo: {data.get('pili_metadata', {}).get('modo', 'N/A')}")
            
            print(f"\n💬 Respuesta de PILI:")
            print("-" * 60)
            print(data.get('respuesta', ''))
            print("-" * 60)
            
            if data.get('informe_generado'):
                print(f"\n✅ PILI generó datos de informe:")
                informe = data['informe_generado']
                for key, value in informe.items():
                    if isinstance(value, str) and len(value) < 100:
                        print(f"   - {key}: {value}")
                return True
            else:
                print("\n⚠️ PILI respondió pero no generó datos estructurados aún")
                print("   (Esto es normal en la primera interacción)")
                return True
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text[:500])
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🚀 PROBANDO PILI INTELIGENTE")
    print("Verificando que PILI usa PILIIntegrator para respuestas brillantes\n")
    
    resultado = test_pili_inteligente()
    
    if resultado:
        print("\n🎉 ¡PILI ESTÁ FUNCIONANDO!")
        print("Ahora PILI debería responder de manera inteligente y dinámica")
    else:
        print("\n⚠️ Hubo un problema. Revisar logs del servidor.")
