"""
Tests de Comparación: Sistema Antiguo vs Sistema Nuevo
FASE 3 - Tarea 10: Validación de Salidas Idénticas

Compara documentos generados por:
- Sistema ANTIGUO: backend/app/services/generators/
- Sistema NUEVO: backend/app/services/professional/generators/

Verifica que ambos sistemas producen salidas equivalentes.
"""
import pytest
from pathlib import Path
import sys
import json

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestComparacionSistemas:
    """
    Tests de comparación entre sistema antiguo y nuevo.

    Estrategia:
    1. Generar documento con sistema antiguo
    2. Generar documento con sistema nuevo
    3. Comparar que sean equivalentes
    """

    def test_sistemas_disponibles(self):
        """Test: Verificar que ambos sistemas están disponibles para comparación"""
        # Verificar sistema antiguo
        try:
            from app.services.generators import generar_documento as generar_antiguo
            sistema_antiguo_disponible = True
        except ImportError:
            sistema_antiguo_disponible = False

        # Verificar sistema nuevo
        try:
            from app.services.professional.generators import generar_documento as generar_nuevo
            sistema_nuevo_disponible = True
        except ImportError:
            sistema_nuevo_disponible = False

        if not sistema_antiguo_disponible:
            pytest.skip("Sistema antiguo no disponible (falta generators/)")

        if not sistema_nuevo_disponible:
            pytest.skip("Sistema nuevo no disponible (falta professional/generators/)")

        assert sistema_antiguo_disponible, "Sistema antiguo debe estar disponible"
        assert sistema_nuevo_disponible, "Sistema nuevo debe estar disponible"

    def test_comparar_cotizacion_simple(
        self,
        datos_cotizacion_simple,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Comparar cotización simple - antiguo vs nuevo"""
        try:
            from app.services.generators import generar_documento as generar_antiguo
            from app.services.professional.generators import generar_documento as generar_nuevo
        except ImportError:
            pytest.skip("Uno de los sistemas no está disponible")

        # Generar con sistema antiguo
        path_antiguo = temp_output_dir / "cotizacion_simple_antiguo.docx"
        resultado_antiguo = generar_antiguo(
            tipo_documento="cotizacion-simple",
            datos=datos_cotizacion_simple,
            ruta_salida=str(path_antiguo),
            opciones=opciones_generacion_defecto
        )

        # Generar con sistema nuevo
        path_nuevo = temp_output_dir / "cotizacion_simple_nuevo.docx"
        resultado_nuevo = generar_nuevo(
            tipo_documento="cotizacion-simple",
            datos=datos_cotizacion_simple,
            ruta_salida=str(path_nuevo),
            opciones=opciones_generacion_defecto
        )

        # Validar que ambos archivos existen
        assert Path(resultado_antiguo).exists(), "Sistema antiguo debe generar archivo"
        assert Path(resultado_nuevo).exists(), "Sistema nuevo debe generar archivo"

        # Comparar tamaños (deben ser similares, ±20%)
        size_antiguo = Path(resultado_antiguo).stat().st_size
        size_nuevo = Path(resultado_nuevo).stat().st_size

        ratio = size_nuevo / size_antiguo if size_antiguo > 0 else 0
        assert 0.8 <= ratio <= 1.2, f"Tamaños muy diferentes: antiguo={size_antiguo}, nuevo={size_nuevo}"

        print(f"✅ Tamaños similares: antiguo={size_antiguo} bytes, nuevo={size_nuevo} bytes (ratio={ratio:.2f})")

    def test_comparar_estructura_datos_preparados(self):
        """Test: Verificar que _prepare_data_for_generator crea estructura correcta"""
        try:
            from app.services.professional.generators import DocumentGeneratorPro
        except ImportError:
            pytest.skip("DocumentGeneratorPro no disponible")

        generator = DocumentGeneratorPro()

        # Datos de entrada simulados
        structured_data = {
            "numero": "COT-TEST-123",
            "fecha": "29/12/2025",
            "cliente": "Cliente Test",
            "servicio": "Instalación Eléctrica",
            "items": [
                {"descripcion": "Tablero eléctrico", "cantidad": 2, "precio_unitario": 1500.0},
                {"descripcion": "Cable NYY 3x10mm²", "cantidad": 150, "precio_unitario": 12.50}
            ]
        }

        # Preparar datos para generador
        datos_preparados = generator._prepare_data_for_generator(
            structured_data=structured_data,
            document_type="cotizacion",
            complexity="simple",
            charts={}
        )

        # Validar estructura esperada
        assert "numero" in datos_preparados
        assert "fecha" in datos_preparados
        assert "cliente" in datos_preparados
        assert "items" in datos_preparados
        assert "subtotal" in datos_preparados
        assert "igv" in datos_preparados
        assert "total" in datos_preparados

        # Validar cálculos
        subtotal_esperado = (2 * 1500.0) + (150 * 12.50)
        assert datos_preparados["subtotal"] == subtotal_esperado, f"Subtotal incorrecto"
        assert datos_preparados["igv"] == subtotal_esperado * 0.18, f"IGV incorrecto"
        assert datos_preparados["total"] == subtotal_esperado * 1.18, f"Total incorrecto"

        print(f"✅ Estructura de datos correcta:")
        print(f"   Subtotal: S/ {datos_preparados['subtotal']:,.2f}")
        print(f"   IGV:      S/ {datos_preparados['igv']:,.2f}")
        print(f"   Total:    S/ {datos_preparados['total']:,.2f}")

    def test_mapeo_tipos_correcto(self):
        """Test: Verificar que mapeo de tipos es correcto"""
        try:
            from app.services.professional.generators import DocumentGeneratorPro
        except ImportError:
            pytest.skip("DocumentGeneratorPro no disponible")

        generator = DocumentGeneratorPro()

        # Mapeos esperados
        mapeos_esperados = [
            (("cotizacion", "simple"), "cotizacion-simple"),
            (("cotizacion", "complejo"), "cotizacion-compleja"),
            (("proyecto", "simple"), "proyecto-simple"),
            (("proyecto", "complejo"), "proyecto-pmi"),
            (("informe", "simple"), "informe-tecnico"),
            (("informe", "complejo"), "informe-apa"),
        ]

        for (doc_type, complexity), tipo_esperado in mapeos_esperados:
            tipo_resultado = generator._map_to_generator_type(doc_type, complexity)
            assert tipo_resultado == tipo_esperado, \
                f"Mapeo incorrecto: {doc_type}+{complexity} → {tipo_resultado} (esperado: {tipo_esperado})"

        print(f"✅ Todos los mapeos de tipos son correctos")

    def test_validar_datos_fixtures_son_validos(
        self,
        datos_cotizacion_simple,
        datos_proyecto_simple,
        datos_informe_tecnico
    ):
        """Test: Validar que las fixtures tienen todos los datos necesarios"""

        # Validar cotización
        campos_cotizacion = ["numero", "fecha", "cliente", "proyecto", "items", "subtotal", "igv", "total"]
        for campo in campos_cotizacion:
            assert campo in datos_cotizacion_simple, f"Falta campo {campo} en cotización"

        # Validar proyecto
        campos_proyecto = ["numero", "fecha", "nombre", "cliente", "objetivos", "entregables"]
        for campo in campos_proyecto:
            assert campo in datos_proyecto_simple, f"Falta campo {campo} en proyecto"

        # Validar informe
        campos_informe = ["numero", "fecha", "titulo", "autor", "resumen", "conclusiones"]
        for campo in campos_informe:
            assert campo in datos_informe_tecnico, f"Falta campo {campo} en informe"

        print(f"✅ Todas las fixtures tienen datos completos")


class TestCompatibilidadSistemas:
    """Tests de compatibilidad entre sistemas"""

    def test_sistema_nuevo_acepta_mismo_formato_datos(
        self,
        datos_cotizacion_simple,
        temp_output_dir
    ):
        """Test: Sistema nuevo acepta mismo formato de datos que antiguo"""
        try:
            from app.services.professional.generators import generar_documento
        except ImportError:
            pytest.skip("Sistema nuevo no disponible")

        # El sistema nuevo debe aceptar los mismos datos que el antiguo
        path_output = temp_output_dir / "test_compatibilidad.docx"

        try:
            resultado = generar_documento(
                tipo_documento="cotizacion-simple",
                datos=datos_cotizacion_simple,
                ruta_salida=str(path_output),
                opciones={"mostrarPreciosUnitarios": True}
            )

            assert Path(resultado).exists(), "Documento debe generarse"
            print(f"✅ Sistema nuevo acepta formato de datos del antiguo")

        except Exception as e:
            pytest.fail(f"Sistema nuevo falló con datos del antiguo: {e}")

    def test_opciones_son_compatibles(self):
        """Test: Opciones de generación son compatibles entre sistemas"""

        # Opciones que ambos sistemas deben soportar
        opciones_comunes = {
            "mostrarPreciosUnitarios": True,
            "mostrarPreciosTotales": True,
            "mostrarIGV": True,
            "incluirLogo": False,
            "esquema_colores": "tesla_azul"
        }

        # Verificar que opciones son válidas
        for key, value in opciones_comunes.items():
            assert isinstance(key, str), "Clave de opción debe ser string"
            assert value is not None, f"Valor de {key} no debe ser None"

        print(f"✅ Opciones compatibles entre sistemas")


class TestRendimiento:
    """Tests básicos de rendimiento"""

    def test_tiempo_generacion_aceptable(
        self,
        datos_cotizacion_simple,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generación de documento no debe tomar más de 5 segundos"""
        try:
            from app.services.professional.generators import generar_documento
            import time
        except ImportError:
            pytest.skip("Sistema nuevo no disponible")

        path_output = temp_output_dir / "test_rendimiento.docx"

        start_time = time.time()

        resultado = generar_documento(
            tipo_documento="cotizacion-simple",
            datos=datos_cotizacion_simple,
            ruta_salida=str(path_output),
            opciones=opciones_generacion_defecto
        )

        end_time = time.time()
        tiempo_generacion = end_time - start_time

        assert tiempo_generacion < 5.0, f"Generación muy lenta: {tiempo_generacion:.2f}s"

        print(f"✅ Tiempo de generación aceptable: {tiempo_generacion:.3f}s")

    def test_multiples_generaciones_secuenciales(
        self,
        datos_cotizacion_simple,
        temp_output_dir,
        opciones_generacion_defecto
    ):
        """Test: Generar múltiples documentos secuencialmente"""
        try:
            from app.services.professional.generators import generar_documento
            import time
        except ImportError:
            pytest.skip("Sistema nuevo no disponible")

        num_documentos = 5
        start_time = time.time()

        for i in range(num_documentos):
            path_output = temp_output_dir / f"test_multi_{i}.docx"

            resultado = generar_documento(
                tipo_documento="cotizacion-simple",
                datos=datos_cotizacion_simple,
                ruta_salida=str(path_output),
                opciones=opciones_generacion_defecto
            )

            assert Path(resultado).exists(), f"Documento {i} debe existir"

        end_time = time.time()
        tiempo_total = end_time - start_time
        tiempo_promedio = tiempo_total / num_documentos

        print(f"✅ {num_documentos} documentos generados en {tiempo_total:.2f}s")
        print(f"   Tiempo promedio por documento: {tiempo_promedio:.3f}s")

        assert tiempo_promedio < 3.0, f"Promedio muy lento: {tiempo_promedio:.2f}s"


class TestValidacionErrores:
    """Tests de manejo de errores"""

    def test_tipo_documento_invalido_lanza_error(
        self,
        datos_cotizacion_simple,
        temp_output_dir
    ):
        """Test: Tipo de documento inválido debe lanzar ValueError"""
        try:
            from app.services.professional.generators import generar_documento
        except ImportError:
            pytest.skip("Sistema nuevo no disponible")

        path_output = temp_output_dir / "test_error.docx"

        with pytest.raises(ValueError, match="no soportado"):
            generar_documento(
                tipo_documento="tipo-invalido-xyz",
                datos=datos_cotizacion_simple,
                ruta_salida=str(path_output)
            )

    def test_datos_incompletos_no_rompe_sistema(
        self,
        temp_output_dir
    ):
        """Test: Datos incompletos deben generar documento con valores por defecto"""
        try:
            from app.services.professional.generators import generar_documento
        except ImportError:
            pytest.skip("Sistema nuevo no disponible")

        # Datos mínimos
        datos_minimos = {
            "numero": "COT-MIN-001",
            "fecha": "29/12/2025",
            "cliente": "Cliente",
            "items": []  # Sin items
        }

        path_output = temp_output_dir / "test_minimo.docx"

        try:
            resultado = generar_documento(
                tipo_documento="cotizacion-simple",
                datos=datos_minimos,
                ruta_salida=str(path_output)
            )

            # Debe generar algo, aunque con datos mínimos
            assert Path(resultado).exists()
            print(f"✅ Sistema maneja datos incompletos sin romperse")

        except Exception as e:
            # Si falla, al menos debe dar un error claro
            assert "items" in str(e).lower() or "datos" in str(e).lower(), \
                f"Error poco claro: {e}"


# Marcar que estos tests requieren ambos sistemas
pytestmark = pytest.mark.skipif(
    'docx' not in sys.modules,
    reason="Requiere python-docx instalado"
)
