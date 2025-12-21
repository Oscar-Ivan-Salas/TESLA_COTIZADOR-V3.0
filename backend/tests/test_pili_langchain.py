"""
🧪 TESTS PARA PILI LANGCHAIN
Tests exhaustivos para los 3 agentes especializados
"""

import pytest
import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar agentes
from app.services.pili_cotizadora_langchain import PILICotizadoraLangChain
from app.services.pili_proyectos_langchain import PILIProyectosLangChain
from app.services.pili_informes_langchain import PILIInformesLangChain
from app.services.pili_multi_ia import PILIMultiIA


# ========================================
# FIXTURES
# ========================================

@pytest.fixture
def gemini_api_key():
    """API key de Gemini desde .env"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY no configurada en .env")
    return api_key


@pytest.fixture
def cotizadora(gemini_api_key):
    """Fixture de PILICotizadora"""
    return PILICotizadoraLangChain(gemini_api_key)


@pytest.fixture
def proyectos(gemini_api_key):
    """Fixture de PILIProyectos"""
    return PILIProyectosLangChain(gemini_api_key)


@pytest.fixture
def informes(gemini_api_key):
    """Fixture de PILIInformes"""
    return PILIInformesLangChain(gemini_api_key)


@pytest.fixture
def multi_ia():
    """Fixture de PILIMultiIA"""
    return PILIMultiIA()


# ========================================
# TESTS - PILI MULTI-IA
# ========================================

class TestPILIMultiIA:
    """Tests para el router multi-IA"""

    def test_inicializacion(self, multi_ia):
        """Test que se inicialice correctamente"""
        assert multi_ia is not None
        assert multi_ia.primary_model is not None
        print(f"✅ Modelo primario: {multi_ia.primary_model}")

    def test_chat_basico(self, multi_ia):
        """Test chat básico"""
        response = multi_ia.chat(
            mensaje="Hola, ¿cómo estás?",
            temperature=0.3
        )

        assert response["exito"] is True
        assert "respuesta" in response
        assert response["modelo_usado"] is not None

        print(f"✅ Chat exitoso con: {response['modelo_usado']}")
        print(f"   Respuesta: {response['respuesta'][:100]}...")

    def test_modelos_disponibles(self, multi_ia):
        """Test que retorne modelos disponibles"""
        modelos = multi_ia.get_available_models()

        assert isinstance(modelos, list)
        assert len(modelos) > 0

        print(f"✅ Modelos disponibles: {len(modelos)}")
        for modelo in modelos:
            print(f"   - {modelo}")


# ========================================
# TESTS - PILI COTIZADORA
# ========================================

class TestPILICotizadora:
    """Tests para PILICotizadora LangChain"""

    def test_inicializacion(self, cotizadora):
        """Test que se inicialice correctamente"""
        assert cotizadora is not None
        assert cotizadora.llm is not None
        assert len(cotizadora.tools) == 6
        print("✅ PILICotizadora inicializada correctamente")

    def test_calcular_carga_electrica(self, cotizadora):
        """Test cálculo de carga eléctrica"""
        input_data = json.dumps({
            "area_m2": 100,
            "tipo": "residencial"
        })

        resultado_str = cotizadora._calcular_carga_electrica(input_data)
        resultado = json.loads(resultado_str)

        assert "carga_va" in resultado
        assert resultado["carga_va"] == 2000  # 100m2 * 20 VA/m2
        assert "conductor_recomendado" in resultado
        assert "normativa" in resultado

        print(f"✅ Carga calculada: {resultado['carga_va']} VA")
        print(f"   Conductor: {resultado['conductor_recomendado']}")

    def test_generar_items_instalacion(self, cotizadora):
        """Test generación de items de instalación"""
        input_data = json.dumps({
            "area_m2": 80,
            "puntos_luz": 12,
            "tomacorrientes": 8
        })

        resultado_str = cotizadora._generar_items_instalacion(input_data)
        items = json.loads(resultado_str)

        assert isinstance(items, list)
        assert len(items) > 0
        assert "descripcion" in items[0]
        assert "cantidad" in items[0]
        assert "precio_unitario" in items[0]

        print(f"✅ Items generados: {len(items)}")
        for item in items[:3]:
            print(f"   - {item['descripcion']}: {item['cantidad']} {item['unidad']}")

    def test_generar_items_itse(self, cotizadora):
        """Test generación de items ITSE"""
        input_data = json.dumps({
            "tipo_local": "comercio",
            "area_m2": 120
        })

        resultado_str = cotizadora._generar_items_itse(input_data)
        items = json.loads(resultado_str)

        assert isinstance(items, list)
        assert len(items) >= 3

        print(f"✅ Items ITSE generados: {len(items)}")

    def test_validar_completitud(self, cotizadora):
        """Test validación de completitud"""
        # Datos incompletos
        input_data_incompleto = json.dumps({
            "cliente": None,
            "items": [],
            "servicio": ""
        })

        resultado_str = cotizadora._validar_completitud(input_data_incompleto)
        resultado = json.loads(resultado_str)

        assert resultado["completo"] is False
        assert len(resultado["faltantes"]) > 0

        print(f"✅ Validación detecta faltantes: {resultado['faltantes']}")

        # Datos completos
        input_data_completo = json.dumps({
            "cliente": {"nombre": "Test"},
            "items": [{"desc": "item1"}],
            "servicio": "instalacion"
        })

        resultado_str = cotizadora._validar_completitud(input_data_completo)
        resultado = json.loads(resultado_str)

        assert resultado["completo"] is True

        print("✅ Validación aprueba datos completos")

    def test_formatear_cotizacion(self, cotizadora):
        """Test formateo de cotización"""
        input_data = json.dumps({
            "cliente": {"nombre": "Cliente Test", "ruc": "12345678901"},
            "proyecto": "Instalación Eléctrica Test",
            "servicio": "instalacion-electrica",
            "items": [
                {
                    "descripcion": "Tablero eléctrico",
                    "cantidad": 1,
                    "unidad": "und",
                    "precio_unitario": 450.00
                },
                {
                    "descripcion": "Punto de luz",
                    "cantidad": 10,
                    "unidad": "pto",
                    "precio_unitario": 35.00
                }
            ]
        })

        resultado_str = cotizadora._formatear_cotizacion(input_data)
        cotizacion = json.loads(resultado_str)

        assert cotizacion["tipo_documento"] == "cotizacion"
        assert cotizacion["puede_generar"] is True
        assert "datos_extraidos" in cotizacion
        assert cotizacion["datos_extraidos"]["subtotal"] == 800.0  # 450 + 350
        assert cotizacion["datos_extraidos"]["igv"] == 144.0  # 800 * 0.18
        assert cotizacion["datos_extraidos"]["total"] == 944.0

        print("✅ Cotización formateada correctamente")
        print(f"   Subtotal: S/ {cotizacion['datos_extraidos']['subtotal']}")
        print(f"   IGV (18%): S/ {cotizacion['datos_extraidos']['igv']}")
        print(f"   Total: S/ {cotizacion['datos_extraidos']['total']}")


# ========================================
# TESTS - PILI PROYECTOS
# ========================================

class TestPILIProyectos:
    """Tests para PILIProyectos LangChain"""

    def test_inicializacion(self, proyectos):
        """Test que se inicialice correctamente"""
        assert proyectos is not None
        assert proyectos.llm is not None
        assert len(proyectos.tools) == 6
        print("✅ PILIProyectos inicializada correctamente")

    def test_generar_gantt(self, proyectos):
        """Test generación de Gantt"""
        input_data = json.dumps({
            "fases": [
                {"nombre": "Planificación", "duracion_semanas": 2},
                {"nombre": "Ejecución", "duracion_semanas": 6},
                {"nombre": "Cierre", "duracion_semanas": 1}
            ]
        })

        resultado_str = proyectos._generar_gantt(input_data)
        resultado = json.loads(resultado_str)

        assert "gantt" in resultado
        assert len(resultado["gantt"]) == 3
        assert resultado["duracion_total_semanas"] == 9

        print("✅ Gantt generado correctamente")
        for fase in resultado["gantt"]:
            print(f"   {fase['nombre']}: {fase['fecha_inicio']} - {fase['fecha_fin']}")

    def test_calcular_roi(self, proyectos):
        """Test cálculo de ROI"""
        input_data = json.dumps({
            "inversion": 50000,
            "beneficio_anual": 20000,
            "años": 3
        })

        resultado_str = proyectos._calcular_roi(input_data)
        resultado = json.loads(resultado_str)

        assert "roi_porcentaje" in resultado
        assert "payback_años" in resultado
        assert resultado["roi_porcentaje"] == 20.0  # (60k - 50k) / 50k * 100
        assert resultado["payback_años"] == 2.5  # 50k / 20k

        print("✅ ROI calculado correctamente")
        print(f"   ROI: {resultado['roi_porcentaje']}%")
        print(f"   Payback: {resultado['payback_años']} años")

    def test_analizar_riesgos(self, proyectos):
        """Test análisis de riesgos"""
        input_data = json.dumps({
            "descripcion_proyecto": "Instalación eléctrica comercial",
            "presupuesto": 60000
        })

        resultado_str = proyectos._analizar_riesgos(input_data)
        riesgos = json.loads(resultado_str)

        assert isinstance(riesgos, list)
        assert len(riesgos) >= 3

        for riesgo in riesgos:
            assert "riesgo" in riesgo
            assert "probabilidad" in riesgo
            assert "impacto" in riesgo
            assert "mitigacion" in riesgo

        print(f"✅ Riesgos analizados: {len(riesgos)}")
        for r in riesgos[:2]:
            print(f"   - {r['riesgo']} (Sev: {r['severidad']})")

    def test_calcular_presupuesto(self, proyectos):
        """Test cálculo de presupuesto"""
        input_data = json.dumps({
            "tipo": "electrico",
            "duracion_meses": 3
        })

        resultado_str = proyectos._calcular_presupuesto(input_data)
        resultado = json.loads(resultado_str)

        assert "presupuesto_estimado" in resultado
        assert "desglose" in resultado
        assert resultado["presupuesto_estimado"] == 24000.0  # 8000 * 3

        print("✅ Presupuesto calculado correctamente")
        print(f"   Total: S/ {resultado['presupuesto_estimado']}")
        print(f"   Materiales: S/ {resultado['desglose']['materiales']}")

    def test_generar_kpis(self, proyectos):
        """Test generación de KPIs"""
        input_data = json.dumps({
            "tipo_proyecto": "electrico",
            "presupuesto": 50000,
            "duracion_meses": 4
        })

        resultado_str = proyectos._generar_kpis(input_data)
        kpis = json.loads(resultado_str)

        assert isinstance(kpis, list)
        assert len(kpis) >= 3

        for kpi in kpis:
            assert "kpi" in kpi
            assert "meta" in kpi

        print(f"✅ KPIs generados: {len(kpis)}")
        for kpi in kpis[:3]:
            print(f"   - {kpi['kpi']}: {kpi['meta']}")


# ========================================
# TESTS - PILI INFORMES
# ========================================

class TestPILIInformes:
    """Tests para PILIInformes LangChain"""

    def test_inicializacion(self, informes):
        """Test que se inicialice correctamente"""
        assert informes is not None
        assert informes.llm is not None
        assert len(informes.tools) == 7
        print("✅ PILIInformes inicializada correctamente")

    def test_generar_resumen_ejecutivo(self, informes):
        """Test generación de resumen ejecutivo"""
        input_data = json.dumps({
            "tema": "Modernización Eléctrica Industrial",
            "objetivos": ["Mejorar eficiencia", "Reducir costos", "Cumplir normativas"],
            "conclusiones_clave": ["Viable técnicamente", "ROI positivo"]
        })

        resultado_str = informes._generar_resumen_ejecutivo(input_data)
        resumen = json.loads(resultado_str)

        assert "titulo" in resumen
        assert "parrafos" in resumen
        assert len(resumen["parrafos"]) >= 3

        print("✅ Resumen ejecutivo generado")
        print(f"   Párrafos: {len(resumen['parrafos'])}")

    def test_generar_analisis_tecnico(self, informes):
        """Test generación de análisis técnico"""
        input_data = json.dumps({
            "tipo_proyecto": "electrico",
            "datos": {"area": 200}
        })

        resultado_str = informes._generar_analisis_tecnico(input_data)
        analisis = json.loads(resultado_str)

        assert "titulo" in analisis
        assert "subsecciones" in analisis
        assert len(analisis["subsecciones"]) >= 3

        print("✅ Análisis técnico generado")
        print(f"   Subsecciones: {len(analisis['subsecciones'])}")

    def test_generar_conclusiones(self, informes):
        """Test generación de conclusiones y recomendaciones"""
        input_data = json.dumps({
            "hallazgos": ["Sistema obsoleto", "Necesita upgrade"],
            "objetivos": ["Modernizar", "Optimizar"]
        })

        resultado_str = informes._generar_conclusiones(input_data)
        resultado = json.loads(resultado_str)

        assert "conclusiones" in resultado
        assert "recomendaciones" in resultado
        assert len(resultado["conclusiones"]) >= 4
        assert len(resultado["recomendaciones"]) >= 4

        print("✅ Conclusiones y recomendaciones generadas")
        print(f"   Conclusiones: {len(resultado['conclusiones'])}")
        print(f"   Recomendaciones: {len(resultado['recomendaciones'])}")

    def test_generar_bibliografia_apa(self, informes):
        """Test generación de bibliografía APA"""
        input_data = json.dumps({
            "tipo_fuentes": ["normas_electricas", "pmi"]
        })

        resultado_str = informes._generar_bibliografia_apa(input_data)
        bibliografia = json.loads(resultado_str)

        assert "titulo" in bibliografia
        assert "formato" in bibliografia
        assert bibliografia["formato"] == "APA 7ma Edición"
        assert "referencias" in bibliografia
        assert len(bibliografia["referencias"]) >= 2

        print("✅ Bibliografía APA generada")
        print(f"   Referencias: {len(bibliografia['referencias'])}")
        for ref in bibliografia["referencias"][:2]:
            print(f"   - {ref['referencia'][:80]}...")

    def test_estructurar_informe_tecnico(self, informes):
        """Test estructura de informe técnico"""
        input_data = json.dumps({
            "titulo": "Informe Técnico Test",
            "cliente": {"nombre": "Cliente Test"}
        })

        resultado_str = informes._estructurar_informe_tecnico(input_data)
        estructura = json.loads(resultado_str)

        assert estructura["tipo"] == "informe_tecnico"
        assert "portada" in estructura
        assert "secciones" in estructura
        assert len(estructura["secciones"]) >= 5

        print("✅ Estructura de informe técnico generada")
        print(f"   Secciones: {len(estructura['secciones'])}")

    def test_estructurar_informe_apa(self, informes):
        """Test estructura de informe APA"""
        input_data = json.dumps({
            "titulo": "Informe Ejecutivo APA Test"
        })

        resultado_str = informes._estructurar_informe_apa(input_data)
        estructura = json.loads(resultado_str)

        assert estructura["tipo"] == "informe_ejecutivo_apa"
        assert "portada_apa" in estructura
        assert "contenido_preliminar" in estructura
        assert "cuerpo_principal" in estructura
        assert "contenido_final" in estructura
        assert "formato" in estructura

        print("✅ Estructura APA generada")
        print(f"   Capítulos: {len(estructura['cuerpo_principal'])}")


# ========================================
# TESTS INTEGRACIÓN E2E
# ========================================

class TestIntegracionE2E:
    """Tests de integración end-to-end"""

    @pytest.mark.slow
    def test_flujo_cotizacion_completo(self, cotizadora):
        """Test flujo completo de generación de cotización"""
        mensaje = """
        Necesito cotización para instalación eléctrica en oficina de 100m2.
        Cliente: Empresa Test S.A.C.
        RUC: 20123456789
        Incluir 15 puntos de luz y 10 tomacorrientes.
        """

        resultado = cotizadora.procesar(mensaje)

        assert "respuesta" in resultado
        print("✅ Flujo completo de cotización")
        print(f"   Respuesta: {resultado['respuesta'][:150]}...")

    @pytest.mark.slow
    def test_flujo_proyecto_completo(self, proyectos):
        """Test flujo completo de generación de proyecto"""
        mensaje = """
        Crear proyecto PMI para modernización eléctrica industrial.
        Presupuesto: S/ 80,000
        Duración: 4 meses
        Incluir Gantt, análisis de riesgos y KPIs.
        """

        resultado = proyectos.procesar(mensaje)

        assert "respuesta" in resultado
        print("✅ Flujo completo de proyecto")
        print(f"   Respuesta: {resultado['respuesta'][:150]}...")

    @pytest.mark.slow
    def test_flujo_informe_completo(self, informes):
        """Test flujo completo de generación de informe"""
        mensaje = """
        Generar informe técnico sobre instalación eléctrica comercial.
        Cliente: Comercial ABC
        Tipo: Informe técnico con análisis y conclusiones.
        """

        resultado = informes.procesar(mensaje)

        assert "respuesta" in resultado
        print("✅ Flujo completo de informe")
        print(f"   Respuesta: {resultado['respuesta'][:150]}...")


# ========================================
# CONFIGURACIÓN PYTEST
# ========================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
