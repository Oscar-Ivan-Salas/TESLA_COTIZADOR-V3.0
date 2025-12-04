#!/usr/bin/env python3
"""
🔍 SISTEMA DE DIAGNÓSTICO COMPLETO - TESLA COTIZADOR V3.0
📁 RUTA: backend/test_diagnostico_completo.py

Este script prueba CADA componente del sistema y reporta errores específicos.

Pruebas:
1. ✅ PILIBrain - Lógica propia funciona?
2. ✅ ChromaDB - Se puede escribir y leer?
3. ✅ Word Generator - Convierte JSON a Word?
4. ✅ File Processor - Lee documentos?
5. ✅ RAG Service - Búsqueda semántica funciona?
6. ✅ Chat Endpoint - Responde correctamente?
7. ✅ Generación Directa - Crea Word sin BD?
8. ✅ Multi-IA - Fallback a PILIBrain funciona?
"""

import sys
import os
from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).parent))

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(test_name: str):
    print(f"\n{'='*70}")
    print(f"{Colors.BLUE}{Colors.BOLD}🧪 TEST: {test_name}{Colors.RESET}")
    print(f"{'='*70}")

def print_success(message: str):
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message: str):
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")


# ═══════════════════════════════════════════════════════════════
# TEST 1: PILIBrain - Lógica Propia
# ═══════════════════════════════════════════════════════════════

def test_pili_brain() -> bool:
    """Prueba que PILIBrain funcione correctamente"""
    print_test("PILIBrain - Lógica Propia Offline")

    try:
        from app.services.pili_brain import PILIBrain, SERVICIOS_PILI

        # Verificar que tenga 10 servicios
        print_info(f"Verificando servicios definidos...")
        assert len(SERVICIOS_PILI) == 10, f"Esperaba 10 servicios, encontré {len(SERVICIOS_PILI)}"
        print_success(f"10 servicios definidos correctamente")

        # Listar servicios
        for servicio_id, info in SERVICIOS_PILI.items():
            print(f"  • {servicio_id}: {info['nombre']}")

        # Inicializar PILIBrain
        print_info("Inicializando PILIBrain...")
        pili = PILIBrain()
        print_success("PILIBrain inicializado")

        # Probar detección de servicio
        print_info("Probando detección de servicio...")
        mensaje_test = "Necesito instalación eléctrica para una oficina de 100m2"
        servicio_detectado = pili.detectar_servicio(mensaje_test)
        print_success(f"Servicio detectado: {servicio_detectado}")

        # Probar generación de cotización
        print_info("Probando generación de cotización...")
        cotizacion = pili.generar_cotizacion(mensaje_test, servicio_detectado, "simple")

        assert "datos" in cotizacion, "Cotización no tiene campo 'datos'"
        assert "conversacion" in cotizacion, "Cotización no tiene campo 'conversacion'"

        datos = cotizacion["datos"]
        assert "numero" in datos, "Datos no tienen 'numero'"
        assert "items" in datos, "Datos no tienen 'items'"
        assert "total" in datos, "Datos no tienen 'total'"

        print_success(f"Cotización generada: {datos['numero']}")
        print_success(f"Total de items: {len(datos['items'])}")
        print_success(f"Total: S/ {datos['total']:.2f}")

        # Probar generación de proyecto
        print_info("Probando generación de proyecto...")
        proyecto = pili.generar_proyecto(mensaje_test, servicio_detectado, "simple")
        assert "datos" in proyecto, "Proyecto no tiene campo 'datos'"
        print_success(f"Proyecto generado correctamente")

        # Probar generación de informe
        print_info("Probando generación de informe...")
        informe = pili.generar_informe(mensaje_test, servicio_detectado, "simple")
        assert "datos" in informe, "Informe no tiene campo 'datos'"
        print_success(f"Informe generado correctamente")

        print_success("✅ TEST PILIBRAIN: APROBADO")
        return True

    except Exception as e:
        print_error(f"TEST PILIBRAIN: FALLIDO")
        print_error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════
# TEST 2: ChromaDB - Base de Datos Vectorial
# ═══════════════════════════════════════════════════════════════

def test_chromadb() -> bool:
    """Prueba que ChromaDB funcione correctamente"""
    print_test("ChromaDB - Base de Datos Vectorial")

    try:
        from app.services.rag_service import RAGService

        print_info("Inicializando RAGService...")
        rag = RAGService()

        if not rag.is_available():
            print_error("ChromaDB no está disponible")
            return False

        print_success("ChromaDB disponible")

        # Probar agregar documento
        print_info("Probando agregar documento...")
        doc_id = f"test_doc_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        texto_test = "Este es un documento de prueba sobre instalaciones eléctricas residenciales"
        metadata_test = {
            "tipo": "cotizacion",
            "cliente": "Cliente Test",
            "fecha": datetime.now().isoformat()
        }

        resultado = rag.agregar_documento(doc_id, texto_test, metadata_test)

        if resultado:
            print_success(f"Documento agregado: {doc_id}")
        else:
            print_error("No se pudo agregar el documento")
            return False

        # Probar búsqueda
        print_info("Probando búsqueda semántica...")
        query = "instalación eléctrica"
        resultados = rag.buscar_similar(query, n_results=3)

        if resultados:
            print_success(f"Búsqueda exitosa: {len(resultados)} resultados")
            for i, resultado in enumerate(resultados, 1):
                print(f"  {i}. Distancia: {resultado.get('distance', 'N/A')}")
        else:
            print_warning("Búsqueda no retornó resultados (puede ser normal si la BD está vacía)")

        print_success("✅ TEST CHROMADB: APROBADO")
        return True

    except Exception as e:
        print_error(f"TEST CHROMADB: FALLIDO")
        print_error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════
# TEST 3: Word Generator - Conversión JSON a Word
# ═══════════════════════════════════════════════════════════════

def test_word_generator() -> bool:
    """Prueba que el generador de Word funcione"""
    print_test("Word Generator - Conversión JSON a Word")

    try:
        from app.services.word_generator import WordGenerator
        from app.services.pili_brain import PILIBrain

        print_info("Inicializando WordGenerator...")
        word_gen = WordGenerator()
        print_success("WordGenerator inicializado")

        # Generar datos de prueba con PILIBrain
        print_info("Generando datos de prueba...")
        pili = PILIBrain()
        mensaje_test = "Instalación eléctrica para oficina de 100m2"
        servicio = pili.detectar_servicio(mensaje_test)
        cotizacion_data = pili.generar_cotizacion(mensaje_test, servicio, "simple")

        # Preparar datos en formato PILI
        datos_pili = {
            "tipo_documento": "cotizacion",
            "datos_extraidos": cotizacion_data["datos"],
            "agente_responsable": "PILI-Cotizadora",
            "servicio_detectado": servicio,
            "timestamp": datetime.now().isoformat()
        }

        # Crear directorio de pruebas si no existe
        test_dir = Path("storage/test_diagnostico")
        test_dir.mkdir(parents=True, exist_ok=True)

        output_path = test_dir / f"test_cotizacion_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"

        print_info(f"Generando Word en: {output_path}")
        resultado = word_gen.generar_cotizacion(
            datos=datos_pili,
            ruta_salida=output_path
        )

        if resultado and output_path.exists():
            tamano = output_path.stat().st_size
            print_success(f"Word generado: {output_path.name}")
            print_success(f"Tamaño: {tamano:,} bytes")

            if tamano < 10000:  # Menos de 10KB es sospechoso
                print_warning(f"Archivo muy pequeño ({tamano} bytes), puede estar vacío")

        else:
            print_error("No se pudo generar el archivo Word")
            return False

        print_success("✅ TEST WORD GENERATOR: APROBADO")
        return True

    except Exception as e:
        print_error(f"TEST WORD GENERATOR: FALLIDO")
        print_error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════
# TEST 4: File Processor - Lectura de Documentos
# ═══════════════════════════════════════════════════════════════

def test_file_processor() -> bool:
    """Prueba que el procesador de archivos funcione"""
    print_test("File Processor - Lectura de Documentos")

    try:
        from app.services.file_processor import FileProcessor

        print_info("Inicializando FileProcessor...")
        processor = FileProcessor()
        print_success("FileProcessor inicializado")

        # Verificar formatos soportados
        print_info("Formatos soportados:")
        for formato, mimetypes in processor.SUPPORTED_FORMATS.items():
            print(f"  • {formato}: {', '.join(mimetypes)}")

        print_success("✅ TEST FILE PROCESSOR: APROBADO")
        return True

    except Exception as e:
        print_error(f"TEST FILE PROCESSOR: FALLIDO")
        print_error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════
# TEST 5: Multi-IA Service
# ═══════════════════════════════════════════════════════════════

def test_multi_ia() -> bool:
    """Prueba el servicio Multi-IA"""
    print_test("Multi-IA Service - Proveedores de IA")

    try:
        from app.services.multi_ia_service import MultiIAProvider

        print_info("Inicializando Multi-IA...")
        multi_ia = MultiIAProvider()
        print_success("Multi-IA inicializado")

        print_info(f"Proveedores disponibles: {len(multi_ia.providers)}")
        for provider in multi_ia.providers:
            print(f"  • {provider['nombre']} (prioridad: {provider['prioridad']})")

        if len(multi_ia.providers) == 0:
            print_warning("No hay proveedores de IA configurados")
            print_info("Sistema usará PILIBrain (offline) por defecto")

        print_success("✅ TEST MULTI-IA: APROBADO")
        return True

    except Exception as e:
        print_error(f"TEST MULTI-IA: FALLIDO")
        print_error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════
# TEST 6: Endpoint Chat Contextualizado
# ═══════════════════════════════════════════════════════════════

def test_chat_endpoint() -> bool:
    """Prueba el endpoint de chat"""
    print_test("Chat Endpoint - /chat-contextualizado")

    try:
        import requests

        print_info("Probando endpoint...")

        url = "http://localhost:8000/api/chat/chat-contextualizado"
        payload = {
            "tipo_flujo": "cotizacion-simple",
            "mensaje": "Necesito instalación eléctrica para oficina de 100m2",
            "historial": [],
            "contexto_adicional": "",
            "generar_html": True
        }

        print_info(f"POST {url}")
        print_info(f"Payload: {json.dumps(payload, indent=2)}")

        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            print_success(f"Respuesta exitosa: {response.status_code}")

            # Verificar campos críticos
            if "cotizacion_generada" in data and data["cotizacion_generada"]:
                print_success("✅ Campo 'cotizacion_generada' presente")
                cot = data["cotizacion_generada"]
                print_info(f"  • Número: {cot.get('numero', 'N/A')}")
                print_info(f"  • Cliente: {cot.get('cliente', 'N/A')}")
                print_info(f"  • Items: {len(cot.get('items', []))}")
                print_info(f"  • Total: S/ {cot.get('total', 0):.2f}")
            else:
                print_error("❌ Campo 'cotizacion_generada' NO presente o vacío")
                return False

            if "html_preview" in data and data["html_preview"]:
                print_success("✅ Campo 'html_preview' presente")
                html_len = len(data["html_preview"])
                print_info(f"  • Tamaño HTML: {html_len} caracteres")
            else:
                print_warning("⚠️  Campo 'html_preview' NO presente")

            print_success("✅ TEST CHAT ENDPOINT: APROBADO")
            return True
        else:
            print_error(f"Respuesta con error: {response.status_code}")
            print_error(f"Detalle: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        print_info("Asegúrate de que el backend esté corriendo: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print_error(f"TEST CHAT ENDPOINT: FALLIDO")
        print_error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════
# TEST 7: Generación Directa (Sin BD)
# ═══════════════════════════════════════════════════════════════

def test_generacion_directa() -> bool:
    """Prueba la generación directa de documentos"""
    print_test("Generación Directa - Sin Base de Datos")

    try:
        import requests

        print_info("Probando endpoint de generación directa...")

        url = "http://localhost:8000/api/generar-documento-directo"
        params = {"formato": "word"}

        payload = {
            "tipo_documento": "cotizacion",
            "numero": "COT-TEST-001",
            "cliente": "Cliente de Prueba",
            "proyecto": "Instalación Eléctrica Test",
            "items": [
                {
                    "descripcion": "Punto de luz LED 18W",
                    "cantidad": 10,
                    "unidad": "pto",
                    "precio_unitario": 30.00,
                    "total": 300.00
                },
                {
                    "descripcion": "Tomacorriente doble",
                    "cantidad": 8,
                    "unidad": "pto",
                    "precio_unitario": 35.00,
                    "total": 280.00
                }
            ],
            "subtotal": 580.00,
            "igv": 104.40,
            "total": 684.40
        }

        print_info(f"POST {url}")

        response = requests.post(url, params=params, json=payload, timeout=30)

        if response.status_code == 200:
            print_success(f"Documento generado exitosamente")

            # Verificar que el contenido sea un archivo Word
            content_type = response.headers.get('Content-Type', '')
            if 'application/vnd.openxmlformats-officedocument' in content_type:
                print_success(f"Content-Type correcto: {content_type}")
            else:
                print_warning(f"Content-Type inesperado: {content_type}")

            tamano = len(response.content)
            print_info(f"  • Tamaño del archivo: {tamano:,} bytes")

            if tamano < 10000:
                print_warning(f"Archivo muy pequeño ({tamano} bytes), puede estar vacío")

            # Guardar archivo de prueba
            test_dir = Path("storage/test_diagnostico")
            test_dir.mkdir(parents=True, exist_ok=True)
            test_file = test_dir / f"test_directo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"

            with open(test_file, 'wb') as f:
                f.write(response.content)

            print_success(f"Archivo guardado: {test_file}")

            print_success("✅ TEST GENERACIÓN DIRECTA: APROBADO")
            return True
        else:
            print_error(f"Error en generación: {response.status_code}")
            print_error(f"Detalle: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        return False
    except Exception as e:
        print_error(f"TEST GENERACIÓN DIRECTA: FALLIDO")
        print_error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ═══════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def main():
    """Ejecuta todos los tests"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}🔍 SISTEMA DE DIAGNÓSTICO COMPLETO - TESLA COTIZADOR V3.0{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

    resultados = {}

    # Tests que NO requieren servidor
    print(f"\n{Colors.BOLD}📦 FASE 1: Tests de Componentes (No requieren servidor){Colors.RESET}\n")

    resultados["PILIBrain"] = test_pili_brain()
    resultados["ChromaDB"] = test_chromadb()
    resultados["WordGenerator"] = test_word_generator()
    resultados["FileProcessor"] = test_file_processor()
    resultados["MultiIA"] = test_multi_ia()

    # Tests que SÍ requieren servidor
    print(f"\n{Colors.BOLD}🌐 FASE 2: Tests de API (Requieren servidor corriendo){Colors.RESET}\n")
    print_info("Asegúrate de que el backend esté corriendo:")
    print_info("  cd backend && uvicorn app.main:app --reload\n")

    resultados["ChatEndpoint"] = test_chat_endpoint()
    resultados["GeneracionDirecta"] = test_generacion_directa()

    # Resumen final
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}📊 RESUMEN DE RESULTADOS{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

    total_tests = len(resultados)
    tests_aprobados = sum(1 for resultado in resultados.values() if resultado)
    tests_fallidos = total_tests - tests_aprobados

    for test_name, resultado in resultados.items():
        if resultado:
            print(f"{Colors.GREEN}✅ {test_name}: APROBADO{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ {test_name}: FALLIDO{Colors.RESET}")

    print(f"\n{Colors.BOLD}Total: {tests_aprobados}/{total_tests} tests aprobados{Colors.RESET}")

    if tests_fallidos == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODOS LOS TESTS APROBADOS 🎉{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  {tests_fallidos} tests fallidos{Colors.RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
