"""
🧪 TEST SIMPLE - Nueva Arquitectura PILI
Test rápido para verificar que la nueva arquitectura funciona
"""

import sys
sys.path.append('e:/TESLA_COTIZADOR-V3.0/backend')

def test_config_loader():
    """Test 1: ConfigLoader carga servicios"""
    print("🧪 Test 1: ConfigLoader...")
    try:
        from app.services.pili.core import get_config_loader
        
        loader = get_config_loader()
        config = loader.load_service('itse')
        
        assert config is not None, "Config no debe ser None"
        assert 'service' in config, "Config debe tener 'service'"
        print("✅ Test 1 PASÓ: ConfigLoader funciona")
        return True
    except Exception as e:
        print(f"❌ Test 1 FALLÓ: {e}")
        return False


def test_universal_specialist():
    """Test 2: UniversalSpecialist se inicializa"""
    print("\n🧪 Test 2: UniversalSpecialist...")
    try:
        from app.services.pili.specialists import UniversalSpecialist
        
        specialist = UniversalSpecialist('itse', 'cotizacion-simple')
        
        assert specialist is not None, "Specialist no debe ser None"
        assert specialist.service_name == 'itse', "Service name debe ser 'itse'"
        print("✅ Test 2 PASÓ: UniversalSpecialist se inicializa")
        return True
    except Exception as e:
        print(f"❌ Test 2 FALLÓ: {e}")
        return False


def test_legacy_adapter():
    """Test 3: LegacyAdapter mantiene compatibilidad"""
    print("\n🧪 Test 3: LegacyAdapter...")
    try:
        from app.services.pili.adapters import LocalSpecialistFactory
        
        specialist = LocalSpecialistFactory.create('itse')
        response = specialist.process_message('', None)
        
        assert 'texto' in response, "Response debe tener 'texto'"
        assert 'botones' in response, "Response debe tener 'botones'"
        assert 'conversation_state' in response, "Response debe tener 'conversation_state'"
        print("✅ Test 3 PASÓ: LegacyAdapter mantiene compatibilidad")
        return True
    except Exception as e:
        print(f"❌ Test 3 FALLÓ: {e}")
        return False


def test_validators():
    """Test 4: Validators funcionan"""
    print("\n🧪 Test 4: Validators...")
    try:
        from app.services.pili.utils import validate_area, validate_pisos
        
        is_valid, msg = validate_area(150)
        assert is_valid == True, "Área 150 debe ser válida"
        
        is_valid, msg = validate_pisos(2)
        assert is_valid == True, "2 pisos debe ser válido"
        
        print("✅ Test 4 PASÓ: Validators funcionan")
        return True
    except Exception as e:
        print(f"❌ Test 4 FALLÓ: {e}")
        return False


def test_calculators():
    """Test 5: Calculators funcionan"""
    print("\n🧪 Test 5: Calculators...")
    try:
        from app.services.pili.utils import calculate_simple_quote
        
        data = {"area_m2": 100, "servicio": "electrico-residencial"}
        result = calculate_simple_quote(data)
        
        assert 'subtotal' in result, "Result debe tener 'subtotal'"
        assert 'igv' in result, "Result debe tener 'igv'"
        assert 'total' in result, "Result debe tener 'total'"
        assert result['subtotal'] == 5000, "Subtotal debe ser 5000 (100m² * 50)"
        
        print("✅ Test 5 PASÓ: Calculators funcionan")
        return True
    except Exception as e:
        print(f"❌ Test 5 FALLÓ: {e}")
        return False


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("🚀 INICIANDO TESTS DE NUEVA ARQUITECTURA PILI")
    print("=" * 60)
    
    results = []
    results.append(test_config_loader())
    results.append(test_universal_specialist())
    results.append(test_legacy_adapter())
    results.append(test_validators())
    results.append(test_calculators())
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n✅ Tests pasados: {passed}/{total}")
    print(f"❌ Tests fallidos: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TODOS LOS TESTS PASARON")
        print("✅ Nueva arquitectura PILI funciona correctamente")
        print("✅ Listo para migración")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("❌ Revisar errores antes de migración")
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
