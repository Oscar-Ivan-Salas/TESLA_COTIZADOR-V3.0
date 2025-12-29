"""
Script de prueba para verificar integración de PILI modular
Prueba el endpoint del backend directamente
"""

import requests
import json

# URL del backend
BASE_URL = "http://localhost:8000"

def test_pili_chat_itse():
    """Prueba el chat de PILI con servicio ITSE"""
    print("\n" + "="*80)
    print("PRUEBA: Chat PILI con servicio ITSE")
    print("="*80 + "\n")
    
    # Datos de prueba
    payload = {
        "mensaje": "Hola",
        "tipo_flujo": "cotizacion-simple",
        "servicio": "itse",
        "historial": [],
        "datos_cliente": {
            "nombre": "Juan Perez",
            "email": "juan@test.com",
            "telefono": "999888777"
        },
        "datos_empresa": {
            "nombre": "Tesla Electricidad",
            "ruc": "20601138787"
        }
    }
    
    try:
        print(f"Enviando peticion a: {BASE_URL}/api/pili/chat")
        print(f"Servicio: {payload['servicio']}")
        print(f"Mensaje: {payload['mensaje']}\n")
        
        response = requests.post(
            f"{BASE_URL}/api/pili/chat",
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n[OK] Respuesta recibida:")
            print(f"  - Agente: {data.get('agente', 'N/A')}")
            print(f"  - Stage: {data.get('stage', 'N/A')}")
            print(f"  - Progreso: {data.get('progreso', 'N/A')}")
            print(f"  - Texto: {data.get('texto', '')[:200]}...")
            
            if data.get('botones'):
                print(f"\n  - Botones: {len(data['botones'])} opciones")
                for i, btn in enumerate(data['botones'][:3], 1):
                    print(f"      {i}. {btn.get('text', 'N/A')}")
            
            # Verificar si usó la nueva arquitectura
            if data.get('stage'):
                print("\n[OK] Sistema uso NUEVA ARQUITECTURA MODULAR")
                return True
            else:
                print("\n[WARN] Sistema respondio sin stage (posible fallback)")
                return False
        else:
            print(f"\n[ERROR] Error en respuesta: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] No se pudo conectar al backend")
        print("Verifica que el servidor este corriendo en http://localhost:8000")
        return False
    
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {str(e)}")
        return False


def test_pili_chat_electricidad():
    """Prueba el chat de PILI con servicio Electricidad"""
    print("\n" + "="*80)
    print("PRUEBA: Chat PILI con servicio Electricidad")
    print("="*80 + "\n")
    
    payload = {
        "mensaje": "Hola",
        "tipo_flujo": "cotizacion-simple",
        "servicio": "electricidad",
        "historial": []
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/pili/chat",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("[OK] Electricidad respondio correctamente")
            print(f"  - Stage: {data.get('stage', 'N/A')}")
            return True
        else:
            print(f"[ERROR] Error: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False


def main():
    """Funcion principal"""
    print("\n" + "="*80)
    print("VERIFICACION DE INTEGRACION PILI MODULAR")
    print("="*80)
    
    # Prueba 1: ITSE
    test1 = test_pili_chat_itse()
    
    # Prueba 2: Electricidad
    test2 = test_pili_chat_electricidad()
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE PRUEBAS")
    print("="*80)
    print(f"  ITSE: {'[OK] PASO' if test1 else '[ERROR] FALLO'}")
    print(f"  Electricidad: {'[OK] PASO' if test2 else '[ERROR] FALLO'}")
    print("="*80 + "\n")
    
    if test1 and test2:
        print("[OK] INTEGRACION EXITOSA - Sistema funcionando correctamente\n")
    else:
        print("[WARN] Algunas pruebas fallaron - Revisar configuracion\n")


if __name__ == "__main__":
    main()
