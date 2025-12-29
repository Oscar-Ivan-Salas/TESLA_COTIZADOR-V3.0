"""
Script de Diagnóstico Completo - PILI
Verifica todo el flujo desde frontend hasta backend
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime una sección"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_1_backend_health():
    """Prueba 1: Verificar que el backend esté corriendo"""
    print_section("PRUEBA 1: Verificar Backend")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("[OK] Backend esta corriendo")
            print(f"     Status: {response.status_code}")
            return True
        else:
            print(f"[ERROR] Backend respondio con status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] No se puede conectar al backend")
        print("        Verifica que el servidor este corriendo en puerto 8000")
        return False
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        return False

def test_2_pili_integrator_status():
    """Prueba 2: Verificar estado de PILI Integrator"""
    print_section("PRUEBA 2: Estado de PILI Integrator")
    
    try:
        # Intentar endpoint de estado si existe
        response = requests.get(f"{BASE_URL}/api/pili/estado", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("[OK] PILI Integrator respondio")
            print(f"     Datos: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"[WARN] Endpoint /api/pili/estado no disponible (status {response.status_code})")
            print("       Esto es normal si el endpoint no existe")
            return True
    except Exception as e:
        print(f"[WARN] No se pudo verificar estado: {e}")
        print("       Continuando con otras pruebas...")
        return True

def test_3_chat_endpoint():
    """Prueba 3: Probar endpoint de chat"""
    print_section("PRUEBA 3: Endpoint de Chat")
    
    # Buscar el endpoint correcto
    endpoints_to_try = [
        "/api/chat",
        "/chat",
        "/api/pili/chat",
        "/pili/chat"
    ]
    
    for endpoint in endpoints_to_try:
        try:
            print(f"\nProbando: {BASE_URL}{endpoint}")
            
            payload = {
                "mensaje": "Hola PILI, necesito una cotizacion ITSE",
                "tipo_flujo": "cotizacion-simple",
                "historial": []
            }
            
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"[OK] Endpoint encontrado: {endpoint}")
                data = response.json()
                
                # Mostrar respuesta
                print("\nRespuesta del servidor:")
                print(f"  - Texto: {data.get('respuesta', data.get('texto', 'N/A'))[:200]}...")
                print(f"  - Agente: {data.get('agente_pili', data.get('agente', 'N/A'))}")
                print(f"  - Modo: {data.get('modo', 'N/A')}")
                print(f"  - Stage: {data.get('stage', 'N/A')}")
                
                # Verificar si tiene botones
                if data.get('botones'):
                    print(f"  - Botones: {len(data['botones'])} opciones")
                
                return endpoint, data
            elif response.status_code == 404:
                print(f"[INFO] Endpoint no encontrado")
            else:
                print(f"[WARN] Status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Error: {e}")
    
    print("\n[ERROR] No se encontro ningun endpoint de chat funcional")
    return None, None

def test_4_verify_pili_mode():
    """Prueba 4: Verificar modo de PILI"""
    print_section("PRUEBA 4: Verificar Modo de PILI")
    
    endpoint, response_data = test_3_chat_endpoint()
    
    if not endpoint or not response_data:
        print("[ERROR] No se pudo obtener respuesta de PILI")
        return False
    
    # Verificar modo
    modo = response_data.get('modo', 'desconocido')
    print(f"\nModo actual de PILI: {modo}")
    
    if modo == "demo" or modo == "basico":
        print("[WARN] PILI esta en modo DEMO/BASICO")
        print("       Esto significa que no esta usando el backend real")
        return False
    elif modo == "PILIIntegrator" or modo == "produccion":
        print("[OK] PILI esta usando PILIIntegrator")
        return True
    else:
        print(f"[WARN] Modo desconocido: {modo}")
        return False

def test_5_check_frontend_config():
    """Prueba 5: Verificar configuración del frontend"""
    print_section("PRUEBA 5: Configuración del Frontend")
    
    print("Verificando archivos del frontend...")
    
    # Buscar App.jsx
    try:
        with open("e:/TESLA_COTIZADOR-V3.0/frontend/src/App.jsx", "r", encoding="utf-8") as f:
            content = f.read()
            
            # Buscar URL del backend
            if "localhost:8000" in content or "http://localhost:8000" in content:
                print("[OK] Frontend configurado para usar localhost:8000")
            else:
                print("[WARN] No se encontro referencia a localhost:8000")
            
            # Buscar modo demo
            if "modo: 'demo'" in content or 'modo: "demo"' in content:
                print("[WARN] Frontend tiene modo demo hardcodeado")
                print("       Esto podria estar causando el problema")
                return False
            else:
                print("[OK] No se encontro modo demo hardcodeado")
                return True
                
    except FileNotFoundError:
        print("[ERROR] No se encontro App.jsx")
        return False
    except Exception as e:
        print(f"[ERROR] Error leyendo App.jsx: {e}")
        return False

def test_6_full_conversation_flow():
    """Prueba 6: Flujo completo de conversación"""
    print_section("PRUEBA 6: Flujo Completo de Conversación")
    
    endpoint, _ = test_3_chat_endpoint()
    
    if not endpoint:
        print("[ERROR] No se puede probar flujo sin endpoint")
        return False
    
    print("Simulando conversación completa...")
    
    # Mensaje 1: Inicio
    print("\n1. Usuario: Hola PILI, necesito cotizacion ITSE")
    payload1 = {
        "mensaje": "Hola PILI, necesito cotizacion ITSE",
        "tipo_flujo": "cotizacion-simple",
        "historial": []
    }
    
    try:
        response1 = requests.post(f"{BASE_URL}{endpoint}", json=payload1, timeout=10)
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"   PILI: {data1.get('respuesta', data1.get('texto', 'N/A'))[:100]}...")
            print(f"   Modo: {data1.get('modo', 'N/A')}")
            print(f"   Stage: {data1.get('stage', 'N/A')}")
            
            if data1.get('botones'):
                print(f"   Botones: {[b.get('text', 'N/A') for b in data1['botones'][:3]]}")
                return True
            else:
                print("   [WARN] No hay botones en la respuesta")
                return False
        else:
            print(f"   [ERROR] Status {response1.status_code}")
            return False
    except Exception as e:
        print(f"   [ERROR] {e}")
        return False

def main():
    """Función principal"""
    print("\n" + "="*80)
    print("  DIAGNOSTICO COMPLETO - SISTEMA PILI")
    print("="*80)
    
    resultados = {}
    
    # Ejecutar pruebas
    resultados['backend_health'] = test_1_backend_health()
    resultados['pili_status'] = test_2_pili_integrator_status()
    resultados['chat_endpoint'] = test_3_chat_endpoint()[0] is not None
    resultados['pili_mode'] = test_4_verify_pili_mode()
    resultados['frontend_config'] = test_5_check_frontend_config()
    resultados['conversation_flow'] = test_6_full_conversation_flow()
    
    # Resumen
    print_section("RESUMEN DE DIAGNOSTICO")
    
    for test, result in resultados.items():
        status = "[OK]" if result else "[ERROR]"
        print(f"{status} {test}")
    
    # Diagnóstico
    print("\n" + "="*80)
    print("  DIAGNOSTICO")
    print("="*80 + "\n")
    
    if not resultados['backend_health']:
        print("PROBLEMA: Backend no esta corriendo")
        print("SOLUCION: Iniciar el backend con 'python -m uvicorn app.main:app --reload'")
    
    elif not resultados['chat_endpoint']:
        print("PROBLEMA: No se encontro endpoint de chat")
        print("SOLUCION: Verificar rutas en el backend")
    
    elif not resultados['pili_mode']:
        print("PROBLEMA: PILI esta en modo DEMO")
        print("SOLUCION: Verificar que el frontend este llamando al backend correcto")
    
    elif not resultados['frontend_config']:
        print("PROBLEMA: Frontend tiene configuracion incorrecta")
        print("SOLUCION: Revisar App.jsx y eliminar modo demo hardcodeado")
    
    elif not resultados['conversation_flow']:
        print("PROBLEMA: Flujo de conversacion no funciona correctamente")
        print("SOLUCION: Verificar que pili_integrator este retornando botones")
    
    else:
        print("SISTEMA FUNCIONANDO CORRECTAMENTE")
        print("Si aun ves modo demo, limpia el cache del navegador (Ctrl+Shift+Delete)")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
