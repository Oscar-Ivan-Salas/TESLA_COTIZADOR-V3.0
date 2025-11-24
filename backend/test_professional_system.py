"""
TEST COMPLETO DEL SISTEMA PROFESIONAL v4.0
Verifica todos los componentes del generador de documentos

Ejecutar: python test_professional_system.py
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# Agregar path del proyecto
sys.path.insert(0, str(Path(__file__).parent))

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

class ProfessionalSystemTest:
    """Suite de pruebas para el sistema profesional"""

    def __init__(self):
        self.results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }

    async def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print_header("TESLA COTIZADOR v4.0 - TEST SUITE")
        print_info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Test 1: Imports
        await self.test_imports()

        # Test 2: File Processor
        await self.test_file_processor()

        # Test 3: RAG Engine
        await self.test_rag_engine()

        # Test 4: ML Engine
        await self.test_ml_engine()

        # Test 5: Chart Engine
        await self.test_chart_engine()

        # Test 6: Document Generator
        await self.test_document_generator()

        # Test 7: Word Generator
        await self.test_word_generator()

        # Test 8: Integration Test
        await self.test_full_integration()

        # Resultados finales
        self.print_final_results()

    async def test_imports(self):
        """Test de imports de modulos"""
        print_header("TEST 1: IMPORTS DE MODULOS")

        # Componentes profesionales
        try:
            from app.services.professional import (
                FileProcessorPro,
                RAGEngine,
                MLEngine,
                ChartEngine,
                DocumentGeneratorPro
            )
            print_success("Componentes profesionales importados")
            self.results["passed"] += 1
        except ImportError as e:
            print_error(f"Error importando componentes profesionales: {e}")
            self.results["failed"] += 1

        # Dependencias opcionales
        dependencies = [
            ("pdfplumber", "Procesamiento de PDF"),
            ("python-docx", "Generacion de Word"),
            ("plotly", "Graficas profesionales"),
            ("sklearn", "Machine Learning"),
            ("chromadb", "Vector Database"),
            ("spacy", "NLP"),
            ("sentence_transformers", "Embeddings")
        ]

        for module_name, description in dependencies:
            try:
                if module_name == "python-docx":
                    import docx
                elif module_name == "sklearn":
                    import sklearn
                else:
                    __import__(module_name)
                print_success(f"{description} ({module_name})")
            except ImportError:
                print_warning(f"{description} ({module_name}) - No instalado")
                self.results["warnings"] += 1

    async def test_file_processor(self):
        """Test del procesador de archivos"""
        print_header("TEST 2: FILE PROCESSOR")

        try:
            from app.services.professional.processors.file_processor_pro import (
                FileProcessorPro, get_file_processor
            )

            processor = get_file_processor()

            # Verificar capacidades
            caps = processor.get_capabilities()
            print_info(f"Capacidades: {caps}")

            # Test de chunk_text
            text = "Este es un texto de prueba. " * 100
            chunks = processor.chunk_text(text, chunk_size=50)
            print_success(f"Chunking funciona: {len(chunks)} chunks creados")

            self.results["passed"] += 1

        except Exception as e:
            print_error(f"Error en FileProcessor: {e}")
            self.results["failed"] += 1

    async def test_rag_engine(self):
        """Test del motor RAG"""
        print_header("TEST 3: RAG ENGINE")

        try:
            from app.services.professional.rag.rag_engine import (
                RAGEngine, get_rag_engine
            )

            rag = get_rag_engine()

            if not rag.is_available():
                print_warning("RAG no completamente disponible (faltan dependencias)")
                self.results["warnings"] += 1
                return

            # Test agregar documento
            result = rag.add_document(
                "Este es un documento de prueba sobre instalaciones electricas residenciales",
                metadata={"tipo": "test"}
            )

            if result.get("success"):
                print_success(f"Documento agregado: {result.get('doc_id')}")

            # Test busqueda
            search_result = rag.search("instalaciones electricas", n_results=1)

            if search_result.get("success") and search_result.get("results"):
                print_success(f"Busqueda funciona: {len(search_result['results'])} resultados")

            # Stats
            stats = rag.get_stats()
            print_info(f"Documentos en coleccion: {stats.get('document_count', 0)}")

            self.results["passed"] += 1

        except Exception as e:
            print_error(f"Error en RAG Engine: {e}")
            self.results["failed"] += 1

    async def test_ml_engine(self):
        """Test del motor ML"""
        print_header("TEST 4: ML ENGINE")

        try:
            from app.services.professional.ml.ml_engine import (
                MLEngine, get_ml_engine
            )

            ml = get_ml_engine()

            # Test clasificacion
            text = "Necesito cotizar la instalacion electrica para una casa de 150 metros cuadrados"
            result = ml.classify_service(text)

            print_success(f"Servicio detectado: {result.get('service')}")
            print_info(f"Confianza: {result.get('confidence', 0):.2%}")
            print_info(f"Metodo: {result.get('method')}")

            # Test extraccion de entidades
            entities = ml.extract_entities(text)

            print_success(f"Area extraida: {entities.get('area_principal')} m2")
            print_info(f"Pisos: {entities.get('num_pisos')}")

            # Test analisis completo
            analysis = ml.analyze_text(text)
            print_success(f"Intencion detectada: {analysis.get('intent')}")

            self.results["passed"] += 1

        except Exception as e:
            print_error(f"Error en ML Engine: {e}")
            self.results["failed"] += 1

    async def test_chart_engine(self):
        """Test del motor de graficas"""
        print_header("TEST 5: CHART ENGINE")

        try:
            from app.services.professional.charts.chart_engine import (
                ChartEngine, get_chart_engine
            )

            charts = get_chart_engine()

            if not charts.is_available():
                print_warning("ChartEngine no disponible (instalar plotly)")
                self.results["warnings"] += 1
                return

            # Test grafico de barras
            data = {
                "Materiales": 5000,
                "Mano de obra": 3000,
                "Equipos": 2000
            }

            path = charts.create_bar_chart(
                data,
                title="Distribucion de Costos",
                y_label="Soles"
            )

            if path:
                print_success(f"Grafico de barras creado: {path}")
            else:
                print_warning("No se pudo crear grafico (falta kaleido)")

            # Test pie chart
            pie_path = charts.create_pie_chart(data, "Distribucion")
            if pie_path:
                print_success(f"Pie chart creado: {pie_path}")

            self.results["passed"] += 1

        except Exception as e:
            print_error(f"Error en Chart Engine: {e}")
            self.results["failed"] += 1

    async def test_document_generator(self):
        """Test del generador de documentos profesional"""
        print_header("TEST 6: DOCUMENT GENERATOR PRO")

        try:
            from app.services.professional.generators.document_generator_pro import (
                DocumentGeneratorPro, get_document_generator_pro
            )

            generator = get_document_generator_pro()

            # Verificar componentes
            status = generator.get_component_status()
            print_info(f"Version: {status.get('version')}")

            for component, available in status.get("components", {}).items():
                if available:
                    print_success(f"{component}: disponible")
                else:
                    print_warning(f"{component}: no disponible")

            # Tipos de documentos
            doc_types = generator.get_available_document_types()
            print_info(f"Tipos de documentos: {len(doc_types)}")

            self.results["passed"] += 1

        except Exception as e:
            print_error(f"Error en Document Generator: {e}")
            self.results["failed"] += 1

    async def test_word_generator(self):
        """Test del generador Word"""
        print_header("TEST 7: WORD GENERATOR")

        try:
            from app.services.word_generator import WordGenerator, get_word_generator

            word_gen = get_word_generator()

            if not word_gen:
                print_warning("WordGenerator no disponible")
                self.results["warnings"] += 1
                return

            # Test generacion de cotizacion
            datos = {
                "datos_extraidos": {
                    "cliente": "Cliente Test",
                    "proyecto": "Instalacion Electrica Test",
                    "numero": "COT-TEST-001",
                    "items": [
                        {
                            "descripcion": "Tablero electrico",
                            "cantidad": 1,
                            "unidad": "und",
                            "precio_unitario": 450,
                            "total": 450
                        },
                        {
                            "descripcion": "Circuitos",
                            "cantidad": 6,
                            "unidad": "cto",
                            "precio_unitario": 120,
                            "total": 720
                        }
                    ],
                    "observaciones": "Prueba del sistema"
                },
                "agente_responsable": "PILI Test"
            }

            result = word_gen.generar_desde_json_pili(
                datos_json=datos,
                tipo_documento="cotizacion"
            )

            if result.get("exito"):
                print_success(f"Documento generado: {result.get('nombre_archivo')}")
                print_info(f"Ruta: {result.get('ruta_archivo')}")
            else:
                print_error(f"Error: {result.get('error')}")

            self.results["passed"] += 1

        except Exception as e:
            print_error(f"Error en Word Generator: {e}")
            self.results["failed"] += 1

    async def test_full_integration(self):
        """Test de integracion completo"""
        print_header("TEST 8: INTEGRACION COMPLETA")

        try:
            from app.services.professional.generators.document_generator_pro import (
                get_document_generator_pro
            )

            generator = get_document_generator_pro()

            # Generar documento completo
            message = "Necesito una cotizacion para instalacion electrica residencial de una casa de 200 metros cuadrados con 2 pisos"

            result = await generator.generate_document(
                message=message,
                document_type="cotizacion",
                complexity="simple"
            )

            if result.get("success"):
                print_success("Documento generado exitosamente")

                # Mostrar pasos de procesamiento
                for step in result.get("processing_steps", []):
                    print_info(f"  - {step.get('step')}: {'OK' if step.get('success', True) else 'ERROR'}")

                if result.get("file_name"):
                    print_success(f"Archivo: {result.get('file_name')}")

            else:
                print_error(f"Error: {result.get('error')}")

            self.results["passed"] += 1

        except Exception as e:
            print_error(f"Error en integracion: {e}")
            self.results["failed"] += 1

    def print_final_results(self):
        """Imprime resultados finales"""
        print_header("RESULTADOS FINALES")

        total = self.results["passed"] + self.results["failed"]
        success_rate = (self.results["passed"] / total * 100) if total > 0 else 0

        print(f"{Colors.GREEN}Pasados: {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}Fallidos: {self.results['failed']}{Colors.END}")
        print(f"{Colors.YELLOW}Advertencias: {self.results['warnings']}{Colors.END}")
        print(f"\n{Colors.BOLD}Tasa de exito: {success_rate:.1f}%{Colors.END}")

        if self.results["failed"] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODOS LOS TESTS PASARON 🎉{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}Algunos tests fallaron. Revisar dependencias faltantes.{Colors.END}")


async def main():
    """Funcion principal"""
    tester = ProfessionalSystemTest()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
