import requests
import json

# Test simple y directo
url = "http://localhost:8000/api/chat/pili-electricidad-proyecto-complejo-pmi"

# Estado que debería activar el formulario
estado = {
    "etapa": "riesgo5_mit",
    "presupuesto": 100000,
    "area_m2": 5000,
    "riesgos": [
        {"id": "R01", "descripcion": "R1", "probabilidad": "Media", "impacto": "Alto", "severidad": "Alta", "mitigacion": "P1"},
        {"id": "R02", "descripcion": "R2", "probabilidad": "Baja", "impacto": "Medio", "severidad": "Baja", "mitigacion": "P2"},
        {"id": "R03", "descripcion": "R3", "probabilidad": "Alta", "impacto": "Alto", "severidad": "Alta", "mitigacion": "P3"},
        {"id": "R04", "descripcion": "R4", "probabilidad": "Media", "impacto": "Medio", "severidad": "Media", "mitigacion": "P4"}
    ],
    "riesgo_temp": {
        "descripcion": "R5",
        "probabilidad": "Baja",
        "impacto": "Bajo",
        "severidad": "Baja"
    }
}

print("=" * 80)
print("TEST DIRECTO: Verificando formulario en respuesta")
print("=" * 80)

response = requests.post(url, json={"mensaje": "Plan de mitigación 5", "conversation_state": estado})
data = response.json()

print(f"\nStatus: {response.status_code}")
print(f"Success: {data.get('success')}")

# Verificar formulario
formulario = data.get('formulario')
print(f"\n{'✅' if formulario else '❌'} FORMULARIO: {formulario}")

if formulario:
    print(f"\n  Tipo: {formulario.get('tipo')}")
    print(f"  Tipo Proyecto: {formulario.get('tipoProyecto')}")
    print(f"  Presupuesto: {formulario.get('presupuesto')}")
    print(f"  Área: {formulario.get('area')}")
    print("\n✅ EL BACKEND ESTÁ FUNCIONANDO CORRECTAMENTE")
    print("\n⚠️  Si no ves el formulario en el navegador:")
    print("   1. Presiona Ctrl+Shift+R para recargar sin caché")
    print("   2. Abre la consola del navegador (F12)")
    print("   3. Ve a la pestaña Network")
    print("   4. Envía un mensaje en el chat")
    print("   5. Busca la petición a 'pili-electricidad-proyecto-complejo-pmi'")
    print("   6. Verifica que en la respuesta aparezca 'formulario'")
else:
    print("\n❌ EL BACKEND NO ESTÁ ENVIANDO EL FORMULARIO")
    print("\nRespuesta completa:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

print("\n" + "=" * 80)
