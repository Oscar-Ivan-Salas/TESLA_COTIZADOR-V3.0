#!/usr/bin/env python
"""
Script de prueba automática: Crear 30 documentos reales
Simula usuario real usando las plantillas predefinidas
"""

import requests
import json
import time
from pathlib import Path

# Configuración
BACKEND_URL = "http://localhost:8000"
TEST_DATA_FILE = "test_data_30_ejemplos.json"
OUTPUT_DIR = Path("test_results_30_docs")
OUTPUT_DIR.mkdir(exist_ok=True)

class ColorText:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(msg, color=ColorText.BLUE):
    print(f"{color}{msg}{ColorText.END}")

def test_backend_health():
    """Verificar que backend esté corriendo"""
    log("🔍 Verificando backend...")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            log(f"✅ Backend corriendo - Modo: {data.get('modo', 'DESCONOCIDO')}", ColorText.GREEN)
            log(f"   Routers cargados: {len(data.get('routers_cargados', []))}")
            return True
        else:
            log(f"❌ Backend responde con código {response.status_code}", ColorText.RED)
            return False
    except Exception as e:
        log(f"❌ Backend NO accesible: {e}", ColorText.RED)
        return False

def load_test_data():
    """Cargar datos de prueba"""
    log("📂 Cargando datos de prueba...")
    try:
        with open(TEST_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        log(f"✅ Datos cargados correctamente", ColorText.GREEN)
        return data
    except Exception as e:
        log(f"❌ Error cargando datos: {e}", ColorText.RED)
        return None

def test_cotizacion_simple(cotizacion, index):
    """Probar generación de cotización simple"""
    log(f"\n{'='*60}")
    log(f"📝 COTIZACIÓN SIMPLE #{index + 1}: {cotizacion['proyecto']}", ColorText.YELLOW)
    log(f"   Cliente: {cotizacion['cliente']}")

    result = {
        "tipo": "cotizacion_simple",
        "id": cotizacion['id'],
        "cliente": cotizacion['cliente'],
        "proyecto": cotizacion['proyecto'],
        "tests": {}
    }

    # Test 1: Generar con IA (endpoint chat)
    log("  🤖 Test 1: Generación con PILI...")
    try:
        chat_request = {
            "mensaje": cotizacion['descripcion'],
            "tipo_flujo": "cotizacion-rapida",
            "contexto": f"Servicio: {cotizacion['servicio']}, Cliente: {cotizacion['cliente']}",
            "historial": []
        }
        response = requests.post(
            f"{BACKEND_URL}/api/chat/generar-cotizacion-rapida",
            json=chat_request,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            log(f"     ✅ Cotización generada con IA", ColorText.GREEN)
            result["tests"]["chat_ia"] = "PASS"
            result["cotizacion_data"] = data.get("cotizacion", {})
        else:
            log(f"     ❌ Error {response.status_code}: {response.text[:200]}", ColorText.RED)
            result["tests"]["chat_ia"] = f"FAIL - {response.status_code}"

    except Exception as e:
        log(f"     ❌ Excepción: {str(e)[:200]}", ColorText.RED)
        result["tests"]["chat_ia"] = f"EXCEPTION - {str(e)[:100]}"

    # Test 2: Generar documento directo Word
    log("  📄 Test 2: Generación documento Word directo...")
    try:
        doc_request = {
            "tipo_documento": "cotizacion",
            "numero": f"COT-TEST-{cotizacion['id']}",
            "cliente": cotizacion['cliente'],
            "proyecto": cotizacion['proyecto'],
            "descripcion": cotizacion['descripcion'],
            "items": [
                {"descripcion": "Item de prueba", "cantidad": 1, "unidad": "und", "precio_unitario": 100}
            ],
            "subtotal": 100,
            "igv": 18,
            "total": 118,
            "fecha": "2025-12-06",
            "vigencia": "30 días"
        }

        response = requests.post(
            f"{BACKEND_URL}/api/generar-documento-directo?formato=word",
            json=doc_request,
            timeout=30
        )

        if response.status_code == 200:
            # Guardar archivo
            filename = OUTPUT_DIR / f"cotizacion_simple_{cotizacion['id']}.docx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            log(f"     ✅ Word generado: {filename}", ColorText.GREEN)
            result["tests"]["word_directo"] = "PASS"
            result["word_file"] = str(filename)
        else:
            log(f"     ❌ Error {response.status_code}: {response.text[:200]}", ColorText.RED)
            result["tests"]["word_directo"] = f"FAIL - {response.status_code}"

    except Exception as e:
        log(f"     ❌ Excepción: {str(e)[:200]}", ColorText.RED)
        result["tests"]["word_directo"] = f"EXCEPTION - {str(e)[:100]}"

    # Test 3: Generar documento directo PDF
    log("  📄 Test 3: Generación documento PDF directo...")
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/generar-documento-directo?formato=pdf",
            json=doc_request,
            timeout=30
        )

        if response.status_code == 200:
            # Guardar archivo
            filename = OUTPUT_DIR / f"cotizacion_simple_{cotizacion['id']}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            log(f"     ✅ PDF generado: {filename}", ColorText.GREEN)
            result["tests"]["pdf_directo"] = "PASS"
            result["pdf_file"] = str(filename)
        else:
            log(f"     ❌ Error {response.status_code}: {response.text[:200]}", ColorText.RED)
            result["tests"]["pdf_directo"] = f"FAIL - {response.status_code}"

    except Exception as e:
        log(f"     ❌ Excepción: {str(e)[:200]}", ColorText.RED)
        result["tests"]["pdf_directo"] = f"EXCEPTION - {str(e)[:100]}"

    return result

def generar_resumen(resultados):
    """Generar resumen de resultados"""
    log(f"\n{'='*80}")
    log(f"📊 RESUMEN FINAL DE PRUEBAS", ColorText.YELLOW)
    log(f"{'='*80}")

    total_tests = len(resultados)
    total_pass = sum(1 for r in resultados if all(v == "PASS" for v in r["tests"].values() if v))
    total_fail = total_tests - total_pass

    log(f"\n📈 ESTADÍSTICAS GLOBALES:")
    log(f"   Total documentos probados: {total_tests}")
    log(f"   ✅ Exitosos: {total_pass}", ColorText.GREEN)
    log(f"   ❌ Fallidos: {total_fail}", ColorText.RED if total_fail > 0 else ColorText.GREEN)

    # Detalles por tipo de test
    log(f"\n📋 DETALLE POR TIPO DE TEST:")
    test_names = ["chat_ia", "word_directo", "pdf_directo"]
    for test_name in test_names:
        passed = sum(1 for r in resultados if r["tests"].get(test_name) == "PASS")
        failed = total_tests - passed
        log(f"   {test_name:20} - PASS: {passed:3} | FAIL: {failed:3}")

    # Guardar resultados completos
    output_file = OUTPUT_DIR / "resultados_completos.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    log(f"\n💾 Resultados guardados en: {output_file}", ColorText.BLUE)

    return total_pass, total_fail

def main():
    """Función principal"""
    log("="*80)
    log("🚀 TEST AUTOMÁTICO: 30 DOCUMENTOS REALES", ColorText.YELLOW)
    log("="*80)

    # 1. Verificar backend
    if not test_backend_health():
        log("\n⚠️  Backend no disponible. Verifica que esté corriendo.", ColorText.YELLOW)
        return

    # 2. Cargar datos de prueba
    test_data = load_test_data()
    if not test_data:
        log("\n⚠️  No se pudieron cargar los datos de prueba.", ColorText.YELLOW)
        return

    # 3. Ejecutar pruebas
    resultados = []

    # Cotizaciones simples
    log(f"\n{'#'*80}")
    log(f"🔷 BLOQUE 1: COTIZACIONES SIMPLES (6 documentos)", ColorText.BLUE)
    log(f"{'#'*80}")
    for idx, cot in enumerate(test_data.get("cotizaciones_simples", [])):
        result = test_cotizacion_simple(cot, idx)
        resultados.append(result)
        time.sleep(0.5)  # Pequeña pausa entre requests

    # TODO: Agregar otros bloques (cotizaciones complejas, proyectos, informes)
    # Por ahora solo pruebo cotizaciones simples

    # 4. Generar resumen
    passed, failed = generar_resumen(resultados)

    log(f"\n{'='*80}")
    if failed == 0:
        log(f"✨ ¡TODAS LAS PRUEBAS PASARON! ✨", ColorText.GREEN)
    else:
        log(f"⚠️  HAY {failed} PRUEBAS FALLIDAS - Revisar logs", ColorText.YELLOW)
    log(f"{'='*80}\n")

if __name__ == "__main__":
    main()
