"""
Script de Diagnóstico - Endpoint Correcto de PILI
"""

import requests
import json

print("\n" + "="*70)
print("DIAGNOSTICO - ENDPOINT CORRECTO DE PILI")
print("="*70 + "\n")

# Endpoint correcto que usa pili_integrator
endpoint = "http://localhost:8000/api/chat/chat-contextualizado"

print(f"Probando endpoint: {endpoint}\n")

# Payload de prueba
payload = {
    "tipo_flujo": "cotizacion-simple",
    "mensaje": "Hola PILI, necesito una cotizacion ITSE",
    "historial": [],
    "contexto_adicional": "",
    "generar_html": False
}

try:
    print("Enviando peticion...")
    response = requests.post(endpoint, json=payload, timeout=10)
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        print("[OK] RESPUESTA RECIBIDA:")
        print("="*70)
        print(f"Mensaje: {data.get('mensaje', data.get('respuesta', 'N/A'))[:200]}...")
        print(f"\nModo: {data.get('modo', 'N/A')}")
        print(f"Agente: {data.get('agente_pili', data.get('agente', 'N/A'))}")
        print(f"Stage: {data.get('stage', 'N/A')}")
        print(f"Progreso: {data.get('progreso', 'N/A')}")
        
        if data.get('botones_sugeridos') or data.get('botones'):
            botones = data.get('botones_sugeridos') or data.get('botones')
            print(f"\nBotones: {len(botones)} opciones")
            for i, btn in enumerate(botones[:5], 1):
                if isinstance(btn, dict):
                    print(f"  {i}. {btn.get('text', btn.get('label', 'N/A'))}")
                else:
                    print(f"  {i}. {btn}")
        
        print("\n" + "="*70)
        print("DIAGNOSTICO:")
        print("="*70)
        
        # Verificar si usa nueva arquitectura
        if data.get('stage'):
            print("\n[OK] Backend esta usando NUEVA ARQUITECTURA MODULAR")
            print("     - Sistema UniversalSpecialist activo")
            print("     - Conversacion por etapas funcionando")
        elif data.get('agente_pili'):
            print("\n[OK] Backend esta usando PILIIntegrator")
            print("     - Sistema de fallback activo")
        else:
            print("\n[WARN] Backend respondio pero sin indicadores de arquitectura")
        
        print("\n[OK] SISTEMA FUNCIONANDO CORRECTAMENTE")
        print("\nSi el frontend aun muestra modo demo:")
        print("1. Verificar que frontend llame a /api/chat/chat-contextualizado")
        print("2. Limpiar cache del navegador (Ctrl+Shift+Delete)")
        print("3. Revisar consola del navegador (F12) para ver errores")
        
    else:
        print(f"[ERROR] Status {response.status_code}")
        print(f"Respuesta: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("[ERROR] No se puede conectar al backend")
    print("Verifica que el servidor este corriendo en http://localhost:8000")
    
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "="*70 + "\n")
