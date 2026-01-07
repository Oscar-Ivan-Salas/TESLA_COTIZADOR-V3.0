import requests
import json

url = "http://localhost:8000/api/generar-documento-v2?formato=word&guardar_bd=false"

payload = {
  "tipo_documento": "proyecto-complejo",
  "numero": "PROY-TEST-001",
  "codigo_proyecto": "PROY-PMI-001",
  "nombre_proyecto": "SISTEMA DE INSTALACIÓN ELÉCTRICA INDUSTRIAL",
  "cliente": {
     "nombre": "Test Cliente",
     "ruc": "20601138787",
     "direccion": "Av. Test 123"
  },
  "duracion_total": 60,
  "fecha_inicio": "06/01/2026",
  "presupuesto": "75,000",
  "moneda": "PEN",
  "personalizacion": {
     "esquema_colores": "azul-tesla",
     "fuente": "Calibri",
     "tamano_fuente": 11,
     "mostrar_logo": True,
     "logo_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKwAEQAAAABJRU5ErkJggg=="
  },
  # Arrays que podrían estar causando el problema si están vacíos o mal formados
  "entregables": [],
  "cronograma_fases": [],
  "raci_actividades": [],
  "stakeholders": [],
  "riesgos": []
}

try:
    print(f"Enviando request a {url}...")
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Éxito! Archivo generado.")
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"Excepción: {e}")
