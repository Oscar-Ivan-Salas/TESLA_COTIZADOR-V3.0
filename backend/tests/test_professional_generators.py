"""
Tests Funcionales para Generadores Profesionales
FASE 3: Testing - Tarea 9

Prueba todos los generadores modulares individualmente y el sistema de routing.
"""
import pytest
from pathlib import Path
import sys

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestGeneradoresIndividuales:
    """Tests para cada generador individual"""

    def test_cotizacion_simple_genera_archivo(
        self,
        datos_cotizacion_simple,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generador de cotización simple crea archivo válido"""
        try:
            from app.services.professional.generators.cotizaciones import generar_cotizacion_simple
        except ImportError:
            pytest.skip("Generadores modulares no disponibles (faltan dependencias)")

        # Preparar ruta de salida
        output_path = temp_output_dir / "cotizacion_simple_test.docx"

        # Generar documento
        result_path = generar_cotizacion_simple(
            datos=datos_cotizacion_simple,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        # Validaciones
        assert result_path is not None, "Generador debe retornar ruta"
        result_file = Path(result_path)
        assert result_file.exists(), "Archivo debe existir"
        assert result_file.suffix == ".docx", "Debe ser archivo .docx"
        assert result_file.stat().st_size > 0, "Archivo no debe estar vacío"
        assert result_file.stat().st_size > 10000, "Archivo debe tener contenido significativo (>10KB)"

    def test_cotizacion_compleja_genera_archivo(
        self,
        datos_cotizacion_compleja,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generador de cotización compleja crea archivo válido"""
        try:
            from app.services.professional.generators.cotizaciones import generar_cotizacion_compleja
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "cotizacion_compleja_test.docx"

        result_path = generar_cotizacion_compleja(
            datos=datos_cotizacion_compleja,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        # Validaciones
        assert Path(result_path).exists()
        assert Path(result_path).suffix == ".docx"
        assert Path(result_path).stat().st_size > 15000  # Más grande que simple

    def test_proyecto_simple_genera_archivo(
        self,
        datos_proyecto_simple,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generador de proyecto simple crea archivo válido"""
        try:
            from app.services.professional.generators.proyectos import generar_proyecto_simple
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "proyecto_simple_test.docx"

        result_path = generar_proyecto_simple(
            datos=datos_proyecto_simple,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        # Validaciones
        assert Path(result_path).exists()
        assert Path(result_path).suffix == ".docx"
        assert Path(result_path).stat().st_size > 10000

    def test_proyecto_complejo_pmi_genera_archivo(
        self,
        datos_proyecto_complejo_pmi,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generador de proyecto PMI crea archivo válido"""
        try:
            from app.services.professional.generators.proyectos import generar_proyecto_complejo_pmi
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "proyecto_pmi_test.docx"

        result_path = generar_proyecto_complejo_pmi(
            datos=datos_proyecto_complejo_pmi,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        # Validaciones
        assert Path(result_path).exists()
        assert Path(result_path).suffix == ".docx"
        assert Path(result_path).stat().st_size > 20000  # Más grande que simple

    def test_informe_tecnico_genera_archivo(
        self,
        datos_informe_tecnico,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generador de informe técnico crea archivo válido"""
        try:
            from app.services.professional.generators.informes import generar_informe_tecnico
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "informe_tecnico_test.docx"

        result_path = generar_informe_tecnico(
            datos=datos_informe_tecnico,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        # Validaciones
        assert Path(result_path).exists()
        assert Path(result_path).suffix == ".docx"
        assert Path(result_path).stat().st_size > 10000

    def test_informe_ejecutivo_apa_genera_archivo(
        self,
        datos_informe_ejecutivo_apa,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generador de informe ejecutivo APA crea archivo válido"""
        try:
            from app.services.professional.generators.informes import generar_informe_ejecutivo_apa
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "informe_apa_test.docx"

        result_path = generar_informe_ejecutivo_apa(
            datos=datos_informe_ejecutivo_apa,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        # Validaciones
        assert Path(result_path).exists()
        assert Path(result_path).suffix == ".docx"
        assert Path(result_path).stat().st_size > 15000


class TestSistemaRouting:
    """Tests para el sistema de routing de generadores"""

    def test_routing_importa_correctamente(self):
        """Test: Sistema de routing se puede importar"""
        try:
            from app.services.professional.generators import (
                generar_documento,
                tipos_disponibles,
                GENERADORES
            )
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        assert generar_documento is not None
        assert tipos_disponibles is not None
        assert GENERADORES is not None

    def test_routing_tiene_todos_los_generadores(self):
        """Test: Diccionario GENERADORES contiene todos los tipos"""
        try:
            from app.services.professional.generators import GENERADORES
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        # Tipos principales
        tipos_esperados = [
            'cotizacion-simple',
            'cotizacion-compleja',
            'proyecto-simple',
            'proyecto-pmi',
            'informe-tecnico',
            'informe-apa'
        ]

        for tipo in tipos_esperados:
            assert tipo in GENERADORES, f"Tipo {tipo} debe estar en GENERADORES"
            assert callable(GENERADORES[tipo]), f"Generador {tipo} debe ser callable"

    def test_routing_aliases_funcionan(self):
        """Test: Aliases en routing apuntan a generadores correctos"""
        try:
            from app.services.professional.generators import GENERADORES
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        # Verificar aliases
        assert GENERADORES['cotizacion'] == GENERADORES['cotizacion-simple']
        assert GENERADORES['proyecto-complejo'] == GENERADORES['proyecto-pmi']
        assert GENERADORES['informe-ejecutivo'] == GENERADORES['informe-apa']

    def test_routing_generar_documento_cotizacion_simple(
        self,
        datos_cotizacion_simple,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: generar_documento() funciona con cotizacion-simple"""
        try:
            from app.services.professional.generators import generar_documento
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "routing_cotizacion.docx"

        result_path = generar_documento(
            tipo_documento="cotizacion-simple",
            datos=datos_cotizacion_simple,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        assert Path(result_path).exists()

    def test_routing_generar_documento_con_alias(
        self,
        datos_cotizacion_simple,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: generar_documento() funciona con alias 'cotizacion'"""
        try:
            from app.services.professional.generators import generar_documento
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "routing_alias.docx"

        result_path = generar_documento(
            tipo_documento="cotizacion",  # Usando alias
            datos=datos_cotizacion_simple,
            ruta_salida=str(output_path),
            opciones=opciones_generacion_defecto
        )

        assert Path(result_path).exists()

    def test_routing_tipo_invalido_lanza_excepcion(
        self,
        datos_cotizacion_simple,
        temp_output_dir
    ):
        """Test: generar_documento() lanza ValueError con tipo inválido"""
        try:
            from app.services.professional.generators import generar_documento
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        output_path = temp_output_dir / "invalid.docx"

        with pytest.raises(ValueError, match="no soportado"):
            generar_documento(
                tipo_documento="tipo-inexistente",
                datos=datos_cotizacion_simple,
                ruta_salida=str(output_path)
            )

    def test_tipos_disponibles_retorna_lista(self):
        """Test: tipos_disponibles() retorna lista completa"""
        try:
            from app.services.professional.generators import tipos_disponibles
        except ImportError:
            pytest.skip("Generadores modulares no disponibles")

        tipos = tipos_disponibles()

        assert isinstance(tipos, list)
        assert len(tipos) >= 6  # Al menos 6 tipos principales
        assert 'cotizacion-simple' in tipos
        assert 'proyecto-pmi' in tipos


class TestDocumentGeneratorPro:
    """Tests para la integración con DocumentGeneratorPro"""

    def test_document_generator_pro_se_puede_importar(self):
        """Test: DocumentGeneratorPro se puede importar"""
        try:
            from app.services.professional.generators import DocumentGeneratorPro
        except ImportError:
            pytest.skip("DocumentGeneratorPro no disponible")

        assert DocumentGeneratorPro is not None

    def test_document_generator_pro_inicializa(self):
        """Test: DocumentGeneratorPro inicializa correctamente"""
        try:
            from app.services.professional.generators import DocumentGeneratorPro
        except ImportError:
            pytest.skip("DocumentGeneratorPro no disponible")

        generator = DocumentGeneratorPro()

        assert generator is not None
        assert hasattr(generator, 'component_status')
        assert hasattr(generator, 'generadores_modulares')

    def test_document_generator_pro_tiene_generadores_modulares(self):
        """Test: DocumentGeneratorPro detecta generadores modulares"""
        try:
            from app.services.professional.generators import DocumentGeneratorPro
        except ImportError:
            pytest.skip("DocumentGeneratorPro no disponible")

        generator = DocumentGeneratorPro()

        # Si las dependencias están instaladas, debe detectar generadores modulares
        if 'docx' in sys.modules or 'python-docx' in sys.modules:
            assert generator.generadores_modulares == True
            assert generator.component_status['generadores_modulares'] == True

    def test_document_generator_pro_metodo_map_to_generator_type(self):
        """Test: Método _map_to_generator_type() mapea correctamente"""
        try:
            from app.services.professional.generators import DocumentGeneratorPro
        except ImportError:
            pytest.skip("DocumentGeneratorPro no disponible")

        generator = DocumentGeneratorPro()

        # Tests de mapeo
        assert generator._map_to_generator_type("cotizacion", "simple") == "cotizacion-simple"
        assert generator._map_to_generator_type("cotizacion", "complejo") == "cotizacion-compleja"
        assert generator._map_to_generator_type("proyecto", "simple") == "proyecto-simple"
        assert generator._map_to_generator_type("proyecto", "complejo") == "proyecto-pmi"
        assert generator._map_to_generator_type("informe", "simple") == "informe-tecnico"
        assert generator._map_to_generator_type("informe", "complejo") == "informe-apa"

    def test_document_generator_pro_metodo_prepare_data_cotizacion(self):
        """Test: _prepare_data_for_generator() prepara datos de cotización"""
        try:
            from app.services.professional.generators import DocumentGeneratorPro
        except ImportError:
            pytest.skip("DocumentGeneratorPro no disponible")

        generator = DocumentGeneratorPro()

        structured_data = {
            "numero": "COT-TEST-123",
            "fecha": "29/12/2025",
            "cliente": "Cliente Test",
            "servicio": "Eléctrico",
            "items": [
                {"descripcion": "Item 1", "cantidad": 1, "precio_unitario": 100.0}
            ]
        }

        datos_preparados = generator._prepare_data_for_generator(
            structured_data=structured_data,
            document_type="cotizacion",
            complexity="simple",
            charts={}
        )

        # Verificar estructura de cotización
        assert "numero" in datos_preparados
        assert "fecha" in datos_preparados
        assert "cliente" in datos_preparados
        assert "items" in datos_preparados
        assert "subtotal" in datos_preparados
        assert "igv" in datos_preparados
        assert "total" in datos_preparados

        # Verificar cálculos
        assert datos_preparados["subtotal"] == 100.0
        assert datos_preparados["igv"] == 18.0
        assert datos_preparados["total"] == 118.0


class TestValidacionEstructuras:
    """Tests para validar estructuras de datos"""

    def test_estructura_cotizacion_simple_valida(self, datos_cotizacion_simple):
        """Test: Fixture de cotización simple tiene estructura válida"""
        # Campos obligatorios
        assert "numero" in datos_cotizacion_simple
        assert "fecha" in datos_cotizacion_simple
        assert "cliente" in datos_cotizacion_simple
        assert "proyecto" in datos_cotizacion_simple
        assert "items" in datos_cotizacion_simple
        assert "subtotal" in datos_cotizacion_simple
        assert "igv" in datos_cotizacion_simple
        assert "total" in datos_cotizacion_simple

        # Validar items
        assert len(datos_cotizacion_simple["items"]) > 0
        for item in datos_cotizacion_simple["items"]:
            assert "descripcion" in item
            assert "cantidad" in item
            assert "precio_unitario" in item

        # Validar cálculos
        subtotal_calculado = sum(
            item["cantidad"] * item["precio_unitario"]
            for item in datos_cotizacion_simple["items"]
        )
        assert abs(datos_cotizacion_simple["subtotal"] - subtotal_calculado) < 0.01

    def test_estructura_proyecto_pmi_valida(self, datos_proyecto_complejo_pmi):
        """Test: Fixture de proyecto PMI tiene estructura válida"""
        # Campos PMI específicos
        assert "stakeholders" in datos_proyecto_complejo_pmi
        assert "kpis" in datos_proyecto_complejo_pmi
        assert "matriz_raci" in datos_proyecto_complejo_pmi
        assert "plan_comunicaciones" in datos_proyecto_complejo_pmi

        # Validar stakeholders
        assert len(datos_proyecto_complejo_pmi["stakeholders"]) > 0
        for stakeholder in datos_proyecto_complejo_pmi["stakeholders"]:
            assert "nombre" in stakeholder
            assert "rol" in stakeholder

        # Validar KPIs
        assert "SPI" in datos_proyecto_complejo_pmi["kpis"]
        assert "CPI" in datos_proyecto_complejo_pmi["kpis"]

        # Validar matriz RACI
        assert len(datos_proyecto_complejo_pmi["matriz_raci"]) > 0


# Marcar tests que requieren dependencias pesadas
pytestmark = pytest.mark.skipif(
    'docx' not in sys.modules,
    reason="Requiere python-docx instalado (pip install python-docx)"
)
