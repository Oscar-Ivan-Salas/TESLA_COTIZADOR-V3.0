"""
Test para verificar que el título dinámico del documento PMI
muestra correctamente SERVICIO - INDUSTRIA
"""

import requests
import json

# URL del backend
BASE_URL = "http://localhost:8000"

print("🧪 TEST: Título Dinámico PMI - SERVICIO - INDUSTRIA")
print("=" * 60)

# Datos de prueba simulando lo que envía el chatbot
datos_prueba = {
    "nombre_proyecto": "PRUEBA TITULO DINAMICO",
    "codigo_proyecto": "PROY-TEST-001",
    "servicio": "electricidad",  # ✅ CRÍTICO: Debe aparecer en el título
    "industria": "construccion",  # ✅ CRÍTICO: Debe aparecer en el título
    "cliente": {
        "nombre": "Cliente Test",
        "ruc": "20123456789"
    },
    "duracion_total": 60,
    "fecha_inicio": "10/01/2026",
    "fecha_fin": "10/03/2026",
    "presupuesto": "100000",
    "alcance_proyecto": "Instalación eléctrica industrial",
    "cronograma_fases": [
        {"label": "1. Inicio", "width": "15%", "dias": "10 días"},
        {"label": "2. Planificación", "width": "20%", "dias": "15 días"},
        {"label": "3. Ejecución", "width": "40%", "dias": "25 días"},
        {"label": "4. Cierre", "width": "10%", "dias": "5 días"}
    ]
}

print("\n📤 Enviando datos al endpoint /generar-directo...")
print(f"   Servicio: {datos_prueba['servicio']}")
print(f"   Industria: {datos_prueba['industria']}")

try:
    # Endpoint de generación directa
    response = requests.post(
        f"{BASE_URL}/generar-directo",
        json={
            "tipo_documento": "proyecto-complejo",
            "datos": datos_prueba,
            "formato": "docx"
        },
        timeout=30
    )
    
    if response.status_code == 200:
        print("\n✅ Documento generado exitosamente")
        
        # Guardar documento para inspección manual
        output_file = "test_titulo_dinamico.docx"
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print(f"\n📄 Documento guardado en: {output_file}")
        print("\n🔍 VERIFICACIÓN MANUAL REQUERIDA:")
        print("   1. Abre el archivo test_titulo_dinamico.docx")
        print("   2. Verifica que el título del Project Charter sea:")
        print("      'ELECTRICIDAD - CONSTRUCCIÓN'")
        print("   3. Si dice 'ELECTRICIDAD - CONSTRUCCIÓN' → ✅ ÉXITO")
        print("   4. Si dice otra cosa → ❌ FALLO")
        
    else:
        print(f"\n❌ Error al generar documento: {response.status_code}")
        print(f"   Respuesta: {response.text}")

except Exception as e:
    print(f"\n❌ Error en la prueba: {str(e)}")

print("\n" + "=" * 60)
