import requests
import json

response = requests.post(
    "http://localhost:8000/api/chat/chat-contextualizado",
    json={
        "tipo_flujo": "cotizacion-simple",
        "mensaje": "Hola",
        "historial": [],
        "contexto_adicional": "Servicio: itse",
        "generar_html": True,
        "conversation_state": None
    }
)

data = response.json()

# Verificar si es ITSE o Electricidad
respuesta = data.get("respuesta", "")

print("STATUS:", "OK" if data.get("success") else "ERROR")
print("\nPRIMEROS 300 CARACTERES DE LA RESPUESTA:")
print(respuesta[:300])
print("\n" + "="*60)

if "ITSE" in respuesta or "Salud" in respuesta or "Educacion" in respuesta:
    print("RESULTADO: CORRECTO - Es respuesta de ITSE")
elif "Electr" in respuesta or "CNE" in respuesta:
    print("RESULTADO: INCORRECTO - Es respuesta de Electricidad")
else:
    print("RESULTADO: DESCONOCIDO")

print("\nBOTONES:", len(data.get("botones_sugeridos", [])))
