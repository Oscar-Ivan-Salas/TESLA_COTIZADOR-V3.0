"""
🧪 TEST RÁPIDO - MODO OFFLINE DE PILI
Valida que PILI nunca se paralice sin IAs
"""

import sys
import os

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.pili_multi_ia import PILIMultiIA

def test_modo_offline():
    """Test que PILI funciona sin API keys (modo offline)"""

    print("🧪 TESTEANDO MODO OFFLINE DE PILI")
    print("=" * 50)

    # Asegurar que NO hay API keys (simular fallo total)
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GROQ_API_KEY", None)
    os.environ.pop("TOGETHER_API_KEY", None)
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("ANTHROPIC_API_KEY", None)

    # Inicializar PILI
    multi = PILIMultiIA()

    print("\n✅ PILI inicializada sin API keys")
    print(f"   Modelos disponibles: {multi.get_available_models()}")

    # Test 1: Saludo
    print("\n📝 Test 1: Saludo")
    resultado = multi.chat("Hola PILI")
    print(f"   Modo usado: {resultado.get('modelo_usado')}")
    print(f"   Respuesta: {resultado['respuesta'][:100]}...")
    assert resultado["exito"] is True
    assert resultado["modelo_usado"] == "PILI_OFFLINE"
    print("   ✅ PASÓ")

    # Test 2: Cotización
    print("\n📝 Test 2: Cotización")
    resultado = multi.chat("Necesito una cotización")
    print(f"   Modo usado: {resultado.get('modelo_usado')}")
    print(f"   Respuesta: {resultado['respuesta'][:100]}...")
    assert resultado["exito"] is True
    assert resultado["modelo_usado"] == "PILI_OFFLINE"
    assert "MODO OFFLINE" in resultado["respuesta"]
    print("   ✅ PASÓ")

    # Test 3: Proyecto
    print("\n📝 Test 3: Proyecto")
    resultado = multi.chat("Quiero crear un proyecto")
    print(f"   Modo usado: {resultado.get('modelo_usado')}")
    print(f"   Respuesta: {resultado['respuesta'][:100]}...")
    assert resultado["exito"] is True
    assert resultado["modelo_usado"] == "PILI_OFFLINE"
    print("   ✅ PASÓ")

    # Test 4: Informe
    print("\n📝 Test 4: Informe")
    resultado = multi.chat("Necesito un informe técnico")
    print(f"   Modo usado: {resultado.get('modelo_usado')}")
    print(f"   Respuesta: {resultado['respuesta'][:100]}...")
    assert resultado["exito"] is True
    assert resultado["modelo_usado"] == "PILI_OFFLINE"
    print("   ✅ PASÓ")

    # Test 5: Mensaje genérico
    print("\n📝 Test 5: Mensaje genérico")
    resultado = multi.chat("No sé qué hacer")
    print(f"   Modo usado: {resultado.get('modelo_usado')}")
    print(f"   Respuesta: {resultado['respuesta'][:100]}...")
    assert resultado["exito"] is True
    assert resultado["modelo_usado"] == "PILI_OFFLINE"
    print("   ✅ PASÓ")

    print("\n" + "=" * 50)
    print("✅ TODOS LOS TESTS PASARON")
    print("\n🎉 PILI NUNCA SE PARALIZA - Modo Offline funciona perfectamente")
    print("   Sin API keys, sin internet, sin IAs → PILI sigue funcionando")


if __name__ == "__main__":
    test_modo_offline()
