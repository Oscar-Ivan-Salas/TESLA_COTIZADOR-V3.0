"""
Script de prueba para verificar que el formulario se envía correctamente
desde el chatbot PMI hasta el frontend
"""
import requests
import json

# URL del endpoint
url = "http://localhost:8000/api/chat/pili-electricidad-proyecto-complejo-pmi"

# Simular el estado que llevaría al formulario de profesionales
# Según el código del bot, después de completar los 5 riesgos, debe mostrar el formulario
estado_test = {
    "etapa": "riesgo5_mit",  # Última etapa antes del formulario
    "cliente_nombre": "Test Cliente",
    "proyecto_nombre": "Proyecto Test",
    "presupuesto": 100000,
    "moneda": "USD",
    "duracion_meses": 6,
    "ubicacion": "Lima",
    "area_m2": 5000,
    "descripcion": "Proyecto de prueba",
    "normativa": "CNE Suministro 2011",
    "fecha_inicio": "01/02/2026",
    "spi": 1.0,
    "cpi": 1.0,
    "ev_k": 70,
    "pv_k": 75,
    "ac_k": 65,
    "alcance": "Alcance de prueba",
    "dias_ingenieria": 25,
    "dias_ejecucion": 50,
    "duracion_total": 99,
    "riesgos": [
        {
            "id": "R01",
            "descripcion": "Riesgo 1",
            "probabilidad": "Media",
            "impacto": "Alto",
            "severidad": "Alta",
            "mitigacion": "Plan 1"
        },
        {
            "id": "R02",
            "descripcion": "Riesgo 2",
            "probabilidad": "Baja",
            "impacto": "Medio",
            "severidad": "Baja",
            "mitigacion": "Plan 2"
        },
        {
            "id": "R03",
            "descripcion": "Riesgo 3",
            "probabilidad": "Alta",
            "impacto": "Alto",
            "severidad": "Alta",
            "mitigacion": "Plan 3"
        },
        {
            "id": "R04",
            "descripcion": "Riesgo 4",
            "probabilidad": "Media",
            "impacto": "Medio",
            "severidad": "Media",
            "mitigacion": "Plan 4"
        }
    ],
    "riesgo_temp": {
        "descripcion": "Riesgo 5",
        "probabilidad": "Baja",
        "impacto": "Bajo",
        "severidad": "Baja"
    }
}

# Mensaje que completaría el último riesgo
mensaje = "Plan de mitigación para riesgo 5"

print("=" * 80)
print("🧪 TEST: Verificando envío de formulario en Chat PMI")
print("=" * 80)

try:
    # Hacer la petición
    response = requests.post(
        url,
        json={
            "mensaje": mensaje,
            "conversation_state": estado_test
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n📦 RESPUESTA DEL BACKEND:")
        print("-" * 80)
        print(f"Success: {data.get('success')}")
        print(f"Agente: {data.get('agente_pili')}")
        print(f"\nRespuesta (primeros 200 chars):")
        print(data.get('respuesta', '')[:200] + "...")
        
        print(f"\n🔍 VERIFICACIÓN DE CLAVES:")
        print("-" * 80)
        claves_esperadas = ['success', 'respuesta', 'botones', 'formulario', 'conversation_state', 'datos_generados']
        for clave in claves_esperadas:
            presente = clave in data
            valor = data.get(clave)
            tipo = type(valor).__name__ if valor is not None else "None"
            print(f"  {clave:20s}: {'✅' if presente else '❌'} (tipo: {tipo})")
        
        # VERIFICACIÓN CRÍTICA: ¿Tiene formulario?
        print("\n" + "=" * 80)
        if 'formulario' in data and data['formulario'] is not None:
            print("✅ ¡FORMULARIO ENCONTRADO!")
            print("=" * 80)
            formulario = data['formulario']
            print(f"Tipo de formulario: {formulario.get('tipo')}")
            print(f"Tipo de proyecto: {formulario.get('tipoProyecto')}")
            print(f"Presupuesto: {formulario.get('presupuesto')}")
            print(f"Área: {formulario.get('area')}")
            print("\n✅ El backend está enviando el formulario correctamente")
        else:
            print("❌ FORMULARIO NO ENCONTRADO EN LA RESPUESTA")
            print("=" * 80)
            print("\n🔍 Contenido completo de la respuesta:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print("\n❌ El backend NO está enviando el formulario")
        
        print("\n" + "=" * 80)
        print("📊 ESTADO DE CONVERSACIÓN ACTUALIZADO:")
        print("-" * 80)
        nuevo_estado = data.get('conversation_state', {})
        print(f"Etapa actual: {nuevo_estado.get('etapa')}")
        print(f"Riesgos registrados: {len(nuevo_estado.get('riesgos', []))}")
        
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ ERROR DE CONEXIÓN: {e}")
    print("\n⚠️  Verifica que el backend esté corriendo en http://localhost:8000")

print("\n" + "=" * 80)
print("FIN DEL TEST")
print("=" * 80)
