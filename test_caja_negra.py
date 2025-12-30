import sys
sys.path.insert(0, 'e:\\TESLA_COTIZADOR-V3.0')

from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot

bot = PILIITSEChatBot()

# Test 1: Estado inicial
print("=== TEST 1: Estado inicial ===")
resultado = bot.procesar("", None)
print(f"Etapa: {resultado['estado']['etapa']}")
print(f"Success: {resultado['success']}")
print()

# Test 2: Enviar SALUD con etapa categoria
print("=== TEST 2: Enviar SALUD con etapa categoria ===")
resultado = bot.procesar("SALUD", {'etapa': 'categoria', 'categoria': None, 'tipo': None, 'area': None, 'pisos': None, 'riesgo': None})
print(f"Etapa resultado: {resultado['estado']['etapa']}")
print(f"Categoria: {resultado['estado']['categoria']}")
print(f"Success: {resultado['success']}")
print(f"Respuesta: {resultado['respuesta'][:100]}...")
