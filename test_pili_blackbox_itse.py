"""
═══════════════════════════════════════════════════════════════════════════════
🧪 TEST PILI BLACKBOX - SERVICIO ITSE
═══════════════════════════════════════════════════════════════════════════════
Verifica que el servicio ITSE funciona correctamente con patrón caja negra

Test completo del flujo:
1. Mensaje inicial → Botones de categorías
2. Selección categoría → Botones de tipos
3. Selección tipo → Solicitud de área
4. Ingreso área → Solicitud de pisos
5. Ingreso pisos → Cotización completa

Fecha: 30 de Diciembre 2025
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.pili_blackbox.services.itse import ITSEChatPili


def test_flujo_completo_itse():
    """Test del flujo completo ITSE"""
    print("\n" + "="*80)
    print("🧪 TEST PILI BLACKBOX - SERVICIO ITSE")
    print("="*80 + "\n")

    # Inicializar servicio
    print("✅ Paso 1: Inicializar servicio ITSE...")
    pili_itse = ITSEChatPili()
    print("   Servicio inicializado correctamente.\n")

    # Historial de conversación
    historial = []

    # ═══════════════════════════════════════════════════════════════════════
    # ETAPA 1: Mensaje inicial
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("ETAPA 1: Mensaje Inicial")
    print("=" * 80)

    mensaje_1 = "Hola, necesito certificado ITSE"
    print(f"👤 Usuario: {mensaje_1}")

    resultado_1 = pili_itse.procesar(mensaje_1, historial)
    print(f"\n🤖 PILI: {resultado_1['respuesta']}")
    print(f"\n📊 Datos: {resultado_1.get('datos', {})}")
    print(f"🎯 Acción: {resultado_1['siguiente_accion']}")
    print(f"📈 Progreso: {resultado_1.get('progreso', 'N/A')}")
    print(f"🔘 Botones: {len(resultado_1.get('botones', []))} opciones")

    historial.append({'role': 'user', 'content': mensaje_1})
    historial.append({'role': 'assistant', 'content': resultado_1['respuesta'], 'datos': resultado_1['datos']})

    assert resultado_1['siguiente_accion'] == 'recopilar_datos'
    assert 'botones' in resultado_1
    print("\n✅ ETAPA 1: PASÓ\n")

    # ═══════════════════════════════════════════════════════════════════════
    # ETAPA 2: Selección de categoría
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("ETAPA 2: Selección de Categoría")
    print("=" * 80)

    mensaje_2 = "COMERCIO"
    print(f"👤 Usuario: {mensaje_2}")

    resultado_2 = pili_itse.procesar(mensaje_2, historial)
    print(f"\n🤖 PILI: {resultado_2['respuesta']}")
    print(f"\n📊 Datos: {resultado_2.get('datos', {})}")
    print(f"🎯 Acción: {resultado_2['siguiente_accion']}")
    print(f"📈 Progreso: {resultado_2.get('progreso', 'N/A')}")
    print(f"🔘 Botones: {len(resultado_2.get('botones', []))} opciones (tipos específicos)")

    historial.append({'role': 'user', 'content': mensaje_2})
    historial.append({'role': 'assistant', 'content': resultado_2['respuesta'], 'datos': resultado_2['datos']})

    assert resultado_2['datos']['categoria'] == 'COMERCIO'
    assert resultado_2.get('progreso') == '2/5'
    print("\n✅ ETAPA 2: PASÓ\n")

    # ═══════════════════════════════════════════════════════════════════════
    # ETAPA 3: Selección de tipo
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("ETAPA 3: Selección de Tipo Específico")
    print("=" * 80)

    mensaje_3 = "TIENDA"
    print(f"👤 Usuario: {mensaje_3}")

    resultado_3 = pili_itse.procesar(mensaje_3, historial)
    print(f"\n🤖 PILI: {resultado_3['respuesta']}")
    print(f"\n📊 Datos: {resultado_3.get('datos', {})}")
    print(f"🎯 Acción: {resultado_3['siguiente_accion']}")
    print(f"📈 Progreso: {resultado_3.get('progreso', 'N/A')}")

    historial.append({'role': 'user', 'content': mensaje_3})
    historial.append({'role': 'assistant', 'content': resultado_3['respuesta'], 'datos': resultado_3['datos']})

    assert resultado_3['datos']['tipo'] == 'TIENDA'
    assert resultado_3.get('progreso') == '3/5'
    print("\n✅ ETAPA 3: PASÓ\n")

    # ═══════════════════════════════════════════════════════════════════════
    # ETAPA 4: Ingreso de área
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("ETAPA 4: Ingreso de Área")
    print("=" * 80)

    mensaje_4 = "150"
    print(f"👤 Usuario: {mensaje_4} m²")

    resultado_4 = pili_itse.procesar(mensaje_4, historial)
    print(f"\n🤖 PILI: {resultado_4['respuesta']}")
    print(f"\n📊 Datos: {resultado_4.get('datos', {})}")
    print(f"🎯 Acción: {resultado_4['siguiente_accion']}")
    print(f"📈 Progreso: {resultado_4.get('progreso', 'N/A')}")

    historial.append({'role': 'user', 'content': mensaje_4})
    historial.append({'role': 'assistant', 'content': resultado_4['respuesta'], 'datos': resultado_4['datos']})

    assert resultado_4['datos']['area_m2'] == 150.0
    assert resultado_4.get('progreso') == '4/5'
    print("\n✅ ETAPA 4: PASÓ\n")

    # ═══════════════════════════════════════════════════════════════════════
    # ETAPA 5: Ingreso de pisos → COTIZACIÓN COMPLETA
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("ETAPA 5: Ingreso de Pisos → COTIZACIÓN")
    print("=" * 80)

    mensaje_5 = "1"
    print(f"👤 Usuario: {mensaje_5} piso")

    resultado_5 = pili_itse.procesar(mensaje_5, historial)
    print(f"\n🤖 PILI: {resultado_5['respuesta']}")
    print(f"\n📊 Datos extraídos:")
    print(f"   - Categoría: {resultado_5['datos'].get('categoria')}")
    print(f"   - Tipo: {resultado_5['datos'].get('tipo')}")
    print(f"   - Área: {resultado_5['datos'].get('area_m2')} m²")
    print(f"   - Pisos: {resultado_5['datos'].get('pisos')}")
    print(f"   - Nivel Riesgo: {resultado_5['datos'].get('nivel_riesgo')}")
    print(f"\n💰 Precios calculados:")
    precios = resultado_5['datos'].get('precios', {})
    print(f"   - TUPA: S/ {precios.get('tupa', 0):.2f}")
    print(f"   - Tesla (min-max): S/ {precios.get('tesla_min', 0):.2f} - S/ {precios.get('tesla_max', 0):.2f}")
    print(f"   - TOTAL (min-max): S/ {precios.get('total_min', 0):.2f} - S/ {precios.get('total_max', 0):.2f}")
    print(f"\n🎯 Acción: {resultado_5['siguiente_accion']}")
    print(f"📈 Progreso: {resultado_5.get('progreso', 'N/A')}")
    print(f"🔘 Botones: {len(resultado_5.get('botones', []))} opciones (Agendar, Info, Restart)")

    assert resultado_5['datos']['pisos'] == 1
    assert resultado_5.get('progreso') == '5/5'
    assert resultado_5['siguiente_accion'] == 'generar_documento'
    assert 'nivel_riesgo' in resultado_5['datos']
    assert 'precios' in resultado_5['datos']
    assert 'items' in resultado_5['datos']
    print("\n✅ ETAPA 5: PASÓ\n")

    # ═══════════════════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("✅ RESUMEN DE RESULTADOS")
    print("=" * 80)
    print(f"✅ Total etapas completadas: 5/5")
    print(f"✅ Flujo conversacional: FUNCIONANDO")
    print(f"✅ Cálculo de riesgo: FUNCIONANDO")
    print(f"✅ Cálculo de precios: FUNCIONANDO")
    print(f"✅ Generación de datos estructurados: FUNCIONANDO")
    print(f"✅ Patrón caja negra: VALIDADO")
    print("=" * 80)
    print("\n🎉 TEST COMPLETADO EXITOSAMENTE 🎉\n")


if __name__ == "__main__":
    try:
        test_flujo_completo_itse()
    except Exception as e:
        print(f"\n❌ ERROR EN EL TEST: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
