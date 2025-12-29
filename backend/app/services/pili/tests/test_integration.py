"""
🧪 TESTS DE INTEGRACIÓN - PILI
Tests para verificar integración completa
"""

import pytest
from app.services.pili.specialist import UniversalSpecialist
from app.services.pili.adapters.legacy_adapter import LocalSpecialistFactory, LegacySpecialistAdapter


class TestUniversalSpecialist:
    """Tests para UniversalSpecialist"""
    
    def test_init_itse(self):
        """Test inicialización con servicio ITSE"""
        specialist = UniversalSpecialist('itse', 'cotizacion-simple')
        assert specialist.service_name == 'itse'
        assert specialist.document_type == 'cotizacion-simple'
    
    def test_initial_message(self):
        """Test mensaje inicial muestra categorías"""
        specialist = UniversalSpecialist('itse', 'cotizacion-simple')
        response = specialist.process_message('', None)
        
        assert 'texto' in response
        assert 'botones' in response
        assert len(response['botones']) > 0
        # Verificar que muestra categorías ITSE
        botones_text = str(response['botones'])
        assert 'SALUD' in botones_text or 'Salud' in botones_text


class TestLegacyAdapter:
    """Tests para adapter de compatibilidad"""
    
    def test_adapter_init(self):
        """Test inicialización del adapter"""
        adapter = LegacySpecialistAdapter('itse')
        assert adapter.service_name == 'itse'
        assert adapter.specialist is not None
    
    def test_adapter_interface(self):
        """Test interfaz legacy del adapter"""
        adapter = LegacySpecialistAdapter('itse')
        response = adapter.process_message('', None)
        
        # Verificar formato legacy
        assert 'texto' in response
        assert 'botones' in response
        assert 'stage' in response
        assert 'conversation_state' in response
        assert 'datos_generados' in response
    
    def test_factory_create(self):
        """Test factory crea adapter correctamente"""
        specialist = LocalSpecialistFactory.create('itse')
        assert isinstance(specialist, LegacySpecialistAdapter)
        assert specialist.service_name == 'itse'


class TestFullConversationFlow:
    """Tests para flujo completo de conversación"""
    
    def test_itse_full_flow(self):
        """Test flujo completo ITSE"""
        specialist = UniversalSpecialist('itse', 'cotizacion-simple')
        
        # Paso 1: Mensaje inicial
        r1 = specialist.process_message('', None)
        assert r1.get('stage') in ['categoria', 'initial']
        assert len(r1.get('botones', [])) > 0
        
        # Paso 2: Seleccionar categoría SALUD
        r2 = specialist.process_message('SALUD', r1.get('state'))
        # El stage debería avanzar
        assert r2.get('stage') != r1.get('stage')
        
        # Verificar que guardó la selección
        state_data = r2.get('state', {}).get('data', {})
        assert 'categoria' in state_data or len(state_data) > 0
    
    def test_legacy_adapter_full_flow(self):
        """Test flujo completo con adapter legacy"""
        adapter = LegacySpecialistAdapter('itse')
        
        # Paso 1: Mensaje inicial
        r1 = adapter.process_message('', None)
        assert 'conversation_state' in r1
        assert 'datos_generados' in r1
        
        # Paso 2: Seleccionar categoría
        r2 = adapter.process_message('SALUD', r1['conversation_state'])
        assert r2['stage'] != r1['stage']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
