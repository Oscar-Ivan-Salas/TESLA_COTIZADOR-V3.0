"""
🧪 TEST END-TO-END - Prueba del Sistema Completo
📁 RUTA: backend/test_pili_integration.py

Prueba la integración completa de PILI con el sistema de fallback.
"""

import asyncio
import sys
from pathlib import Path

# Agregar el path del backend al PYTHONPATH
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.pili_integrator import PILIIntegrator


async def test_pili_chat():
    """Prueba el chat de PILI con un servicio migrado."""
    print("\n" + "="*80)
    print("TEST END-TO-END: PILI CHAT INTEGRATION")
    print("="*80 + "\n")
    
    try:
        # Crear integrador
        print("Inicializando PILIIntegrator...")
        integrator = PILIIntegrator()
        print("[OK] PILIIntegrator inicializado\n")
        
        # Datos del cliente
        datos_cliente = {
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "999888777"
        }
        
        datos_empresa = {
            "nombre": "Tesla Electricidad",
            "ruc": "20601138787"
        }
        
        # Probar con servicio ITSE (migrado)
        print("Probando servicio: ITSE")
        print("Tipo de flujo: cotizacion-simple")
        print("Mensaje: Hola\n")
        
        resultado = await integrator.procesar_mensaje_chat(
            mensaje="Hola",
            tipo_flujo="cotizacion-simple",
            historial=[],
            servicio="itse",
            datos_cliente=datos_cliente,
            datos_empresa=datos_empresa
        )
        
        print("RESPUESTA RECIBIDA:")
        print("="*80)
        print(f"Agente: {resultado.get('agente', 'N/A')}")
        print(f"Stage: {resultado.get('stage', 'N/A')}")
        print(f"Progreso: {resultado.get('progreso', 'N/A')}")
        print(f"\nTexto:\n{resultado.get('texto', 'N/A')[:500]}...")
        
        if resultado.get('botones'):
            print(f"\nBotones disponibles: {len(resultado['botones'])}")
            for i, btn in enumerate(resultado['botones'][:5], 1):
                print(f"  {i}. {btn.get('text', 'N/A')}")
        
        print("\n" + "="*80)
        
        # Verificar que usó la nueva arquitectura
        if resultado.get('stage'):
            print("\n[OK] EXITO: Sistema respondio con nueva arquitectura modular")
            print(f"   - Stage detectado: {resultado['stage']}")
            print(f"   - Progreso: {resultado.get('progreso', 'N/A')}")
            return True
        else:
            print("\n[WARN] Sistema respondio pero sin stage (posible fallback)")
            return False
    
    except Exception as e:
        print(f"\n[ERROR] ERROR EN PRUEBA:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_services():
    """Prueba varios servicios migrados."""
    print("\n" + "="*80)
    print("TEST MULTIPLES SERVICIOS")
    print("="*80 + "\n")
    
    servicios_a_probar = [
        ("itse", "cotizacion-simple"),
        ("electricidad", "cotizacion-simple"),
        ("pozo-tierra", "cotizacion-simple"),
    ]
    
    integrator = PILIIntegrator()
    resultados = {}
    
    for servicio, tipo_flujo in servicios_a_probar:
        print(f"\nProbando: {servicio} ({tipo_flujo})")
        
        try:
            resultado = await integrator.procesar_mensaje_chat(
                mensaje="Hola",
                tipo_flujo=tipo_flujo,
                historial=[],
                servicio=servicio,
                datos_cliente={"nombre": "Test"},
                datos_empresa={"nombre": "Tesla"}
            )
            
            tiene_stage = bool(resultado.get('stage'))
            tiene_botones = bool(resultado.get('botones'))
            
            print(f"   [OK] Respondio - Stage: {tiene_stage}, Botones: {tiene_botones}")
            resultados[servicio] = True
        
        except Exception as e:
            print(f"   [ERROR] Error: {str(e)}")
            resultados[servicio] = False
    
    print("\n" + "="*80)
    print("RESUMEN:")
    exitosos = sum(1 for r in resultados.values() if r)
    print(f"   [OK] Exitosos: {exitosos}/{len(resultados)}")
    print(f"   [ERROR] Fallidos: {len(resultados) - exitosos}/{len(resultados)}")
    print("="*80 + "\n")
    
    return all(resultados.values())


async def main():
    """Función principal."""
    print("\nINICIANDO PRUEBAS DE INTEGRACION COMPLETA\n")
    
    # Prueba 1: Chat básico
    print("PRUEBA 1: Chat basico con ITSE")
    test1 = await test_pili_chat()
    
    # Prueba 2: Múltiples servicios
    print("\n\nPRUEBA 2: Multiples servicios")
    test2 = await test_multiple_services()
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN FINAL DE PRUEBAS")
    print("="*80)
    print(f"   Prueba 1 (Chat ITSE): {'[OK] PASO' if test1 else '[ERROR] FALLO'}")
    print(f"   Prueba 2 (Multiples servicios): {'[OK] PASO' if test2 else '[ERROR] FALLO'}")
    print("="*80)
    
    if test1 and test2:
        print("\n[OK] TODAS LAS PRUEBAS PASARON!")
        print("[OK] Sistema completamente funcional\n")
    else:
        print("\n[WARN] Algunas pruebas fallaron")
        print("[ERROR] Revisar errores arriba\n")


if __name__ == "__main__":
    asyncio.run(main())
