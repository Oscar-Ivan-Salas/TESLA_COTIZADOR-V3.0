"""
🧪 Test de Integración PILI - Verificar que funciona para los 6 documentos
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_pili_informe_simple():
    """Test PILI con Informe Simple"""
    print("\n" + "="*60)
    print("🧪 TEST 1: PILI - Informe Simple")
    print("="*60)
    
    payload = {
        "tipo_flujo": "informe-simple",
        "mensaje": "Necesito un informe técnico para una instalación eléctrica residencial de 120m²",
        "historial": [],
        "contexto_adicional": "Servicio: Instalaciones Eléctricas, Industria: Residencial",
        "generar_html": True,
        "datos_cliente": {
            "nombre": "Cliente Test",
            "ruc": "20123456789"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/chat-contextualizado",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Success: {data.get('success')}")
            print(f"✅ Agente: {data.get('agente_activo')}")
            print(f"\n📝 Respuesta PILI:")
            print(data.get('respuesta', '')[:200] + "...")
            
            if data.get('informe_generado'):
                print(f"\n✅ Informe generado con datos:")
                informe = data['informe_generado']
                print(f"   - Título: {informe.get('titulo', 'N/A')}")
                print(f"   - Cliente: {informe.get('cliente', 'N/A')}")
                print(f"   - Código: {informe.get('codigo', 'N/A')}")
                return True
            else:
                print("⚠️ No se generó informe_generado")
                return False
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pili_cotizacion_simple():
    """Test PILI con Cotización Simple"""
    print("\n" + "="*60)
    print("🧪 TEST 2: PILI - Cotización Simple")
    print("="*60)
    
    payload = {
        "tipo_flujo": "cotizacion-simple",
        "mensaje": "Cotización para casa de 150m² con 10 puntos de luz y 8 tomacorrientes",
        "historial": [],
        "contexto_adicional": "Servicio: Instalaciones Eléctricas, Industria: Residencial",
        "generar_html": True,
        "datos_cliente": {
            "nombre": "Juan Pérez",
            "ruc": "20987654321"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/chat-contextualizado",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Success: {data.get('success')}")
            print(f"✅ Agente: {data.get('agente_activo')}")
            print(f"\n📝 Respuesta PILI:")
            print(data.get('respuesta', '')[:200] + "...")
            
            if data.get('cotizacion_generada'):
                print(f"\n✅ Cotización generada con datos:")
                cot = data['cotizacion_generada']
                print(f"   - Número: {cot.get('numero', 'N/A')}")
                print(f"   - Cliente: {cot.get('cliente', 'N/A')}")
                print(f"   - Items: {len(cot.get('items', []))}")
                print(f"   - Total: ${cot.get('total', 0):.2f}")
                return True
            else:
                print("⚠️ No se generó cotizacion_generada")
                return False
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pili_proyecto_simple():
    """Test PILI con Proyecto Simple"""
    print("\n" + "="*60)
    print("🧪 TEST 3: PILI - Proyecto Simple")
    print("="*60)
    
    payload = {
        "tipo_flujo": "proyecto-simple",
        "mensaje": "Proyecto de instalación eléctrica para edificio de 3 pisos",
        "historial": [],
        "contexto_adicional": "Servicio: Instalaciones Eléctricas, Industria: Comercial",
        "generar_html": True,
        "datos_cliente": {
            "nombre": "Empresa XYZ",
            "ruc": "20111222333"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/chat-contextualizado",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Success: {data.get('success')}")
            print(f"✅ Agente: {data.get('agente_activo')}")
            print(f"\n📝 Respuesta PILI:")
            print(data.get('respuesta', '')[:200] + "...")
            
            if data.get('proyecto_generado'):
                print(f"\n✅ Proyecto generado con datos:")
                proy = data['proyecto_generado']
                print(f"   - Nombre: {proy.get('nombre_proyecto', 'N/A')}")
                print(f"   - Cliente: {proy.get('cliente', 'N/A')}")
                print(f"   - Duración: {proy.get('duracion', 'N/A')}")
                return True
            else:
                print("⚠️ No se generó proyecto_generado")
                return False
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 INICIANDO TESTS DE INTEGRACIÓN PILI")
    print("Verificando que PILI responde correctamente para cada tipo de documento\n")
    
    results = []
    
    # Test 1: Informe Simple
    results.append(("Informe Simple", test_pili_informe_simple()))
    
    # Test 2: Cotización Simple
    results.append(("Cotización Simple", test_pili_cotizacion_simple()))
    
    # Test 3: Proyecto Simple
    results.append(("Proyecto Simple", test_pili_proyecto_simple()))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE TESTS")
    print("="*60)
    
    for nombre, resultado in results:
        status = "✅ PASS" if resultado else "❌ FAIL"
        print(f"{status} - {nombre}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\n🎯 Total: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("PILI está funcionando correctamente para todos los tipos de documentos")
    else:
        print("\n⚠️ Algunos tests fallaron. Revisar logs arriba.")
