#!/usr/bin/env python
"""
Script para generar 30 documentos reales usando el endpoint directo
"""

import requests
import json
from pathlib import Path
import time

BACKEND_URL = "http://localhost:8000"
TEST_DATA_FILE = "test_data_30_ejemplos.json"
OUTPUT_DIR = Path("documentos_generados_30")
OUTPUT_DIR.mkdir(exist_ok=True)

def log(msg, color="blue"):
    colors = {
        "green": '\033[92m',
        "yellow": '\033[93m',
        "red": '\033[91m',
        "blue": '\033[94m',
        "end": '\033[0m'
    }
    print(f"{colors.get(color, colors['blue'])}{msg}{colors['end']}")

def generar_documento(datos, formato="word"):
    """Generar documento usando endpoint directo"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/generar-documento-directo?formato={formato}",
            json=datos,
            timeout=30
        )

        if response.status_code == 200:
            return response.content
        else:
            log(f"❌ Error {response.status_code}: {response.text[:200]}", "red")
            return None
    except Exception as e:
        log(f"❌ Exception: {str(e)}", "red")
        return None

def main():
    log("="*80)
    log("🚀 GENERACIÓN DE 30 DOCUMENTOS REALES", "yellow")
    log("="*80)

    # Cargar datos de prueba
    log("📂 Cargando datos de prueba...")
    with open(TEST_DATA_FILE, 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    log(f"✅ {len(test_data)} categorías cargadas", "green")

    total_docs = 0
    success_count = 0
    fail_count = 0

    # Generar cotizaciones simples (6 docs)
    log("\n" + "="*80)
    log("📝 COTIZACIONES SIMPLES (6 documentos)", "blue")
    log("="*80)

    for idx, cot in enumerate(test_data.get("cotizaciones_simples", []), 1):
        log(f"\n[{idx}/6] {cot['cliente']}")

        datos_doc = {
            "numero": f"COT-SIMPLE-{cot['id']:03d}",
            "cliente": cot['cliente'],
            "proyecto": cot['proyecto'],
            "descripcion": cot['descripcion'],
            "fecha": "2025-12-06",
            "vigencia": "30 días",
            "items": [
                {
                    "descripcion": f"{cot['servicio']} - Área: {cot.get('area_m2', 100)}m²",
                    "cantidad": 1,
                    "unidad": "servicio",
                    "precio_unitario": 2500
                },
                {
                    "descripcion": "Materiales eléctricos",
                    "cantidad": 1,
                    "unidad": "glb",
                    "precio_unitario": 1500
                }
            ],
            "subtotal": 4000,
            "igv": 720,
            "total": 4720
        }

        # Generar Word
        content = generar_documento(datos_doc, "word")
        if content:
            filename = OUTPUT_DIR / f"cotizacion_simple_{cot['id']:03d}.docx"
            with open(filename, 'wb') as f:
                f.write(content)
            log(f"  ✅ Word generado: {filename}", "green")
            success_count += 1
        else:
            fail_count += 1

        total_docs += 1
        time.sleep(0.3)

    # Generar cotizaciones complejas (6 docs)
    log("\n" + "="*80)
    log("📝 COTIZACIONES COMPLEJAS (6 documentos)", "blue")
    log("="*80)

    for idx, cot in enumerate(test_data.get("cotizaciones_complejas", []), 1):
        log(f"\n[{idx}/6] {cot['cliente']}")

        datos_doc = {
            "numero": f"COT-COMPLEJA-{cot['id']:03d}",
            "cliente": cot['cliente'],
            "proyecto": cot['proyecto'],
            "descripcion": cot['descripcion'],
            "fecha": "2025-12-06",
            "vigencia": "45 días",
            "items": [
                {
                    "descripcion": f"{cot['servicio']} - Capacidad: {cot.get('capacidad_kw', 500)}kW",
                    "cantidad": 1,
                    "unidad": "servicio",
                    "precio_unitario": 15000
                },
                {
                    "descripcion": "Ingeniería y diseño",
                    "cantidad": 1,
                    "unidad": "glb",
                    "precio_unitario": 8000
                },
                {
                    "descripcion": "Materiales y equipos",
                    "cantidad": 1,
                    "unidad": "glb",
                    "precio_unitario": 12000
                }
            ],
            "subtotal": 35000,
            "igv": 6300,
            "total": 41300
        }

        content = generar_documento(datos_doc, "word")
        if content:
            filename = OUTPUT_DIR / f"cotizacion_compleja_{cot['id']:03d}.docx"
            with open(filename, 'wb') as f:
                f.write(content)
            log(f"  ✅ Word generado: {filename}", "green")
            success_count += 1
        else:
            fail_count += 1

        total_docs += 1
        time.sleep(0.3)

    # Generar proyectos simples (6 docs)
    log("\n" + "="*80)
    log("🏗️ PROYECTOS SIMPLES (6 documentos)", "blue")
    log("="*80)

    for idx, proj in enumerate(test_data.get("proyectos_simples", []), 1):
        log(f"\n[{idx}/6] {proj['nombre']}")

        datos_doc = {
            "numero": f"PROJ-SIMPLE-{proj['id']:03d}",
            "cliente": proj['cliente'],
            "proyecto": proj['nombre'],
            "descripcion": proj['descripcion'],
            "fecha": "2025-12-06",
            "duracion": f"{proj.get('duracion_meses', 2)} meses",
            "items": [
                {
                    "descripcion": f"Fase 1: Planificación y diseño",
                    "cantidad": 1,
                    "unidad": "fase",
                    "precio_unitario": 1500
                },
                {
                    "descripcion": f"Fase 2: Ejecución de obra",
                    "cantidad": 1,
                    "unidad": "fase",
                    "precio_unitario": 3500
                }
            ],
            "subtotal": 5000,
            "igv": 900,
            "total": 5900,
            "fases": [
                {"nombre": "Planificación", "duracion": "1 semana"},
                {"nombre": "Ejecución", "duracion": "2 semanas"}
            ]
        }

        content = generar_documento(datos_doc, "word")
        if content:
            filename = OUTPUT_DIR / f"proyecto_simple_{proj['id']:03d}.docx"
            with open(filename, 'wb') as f:
                f.write(content)
            log(f"  ✅ Word generado: {filename}", "green")
            success_count += 1
        else:
            fail_count += 1

        total_docs += 1
        time.sleep(0.3)

    # Generar proyectos complejos (6 docs)
    log("\n" + "="*80)
    log("🏗️ PROYECTOS COMPLEJOS (6 documentos)", "blue")
    log("="*80)

    for idx, proj in enumerate(test_data.get("proyectos_complejos", []), 1):
        log(f"\n[{idx}/6] {proj['nombre']}")

        datos_doc = {
            "numero": f"PROJ-COMPLEJO-{proj['id']:03d}",
            "cliente": proj['cliente'],
            "proyecto": proj['nombre'],
            "descripcion": proj['descripcion'],
            "fecha": "2025-12-06",
            "duracion": f"{proj.get('duracion_meses', 2)} meses",
            "items": [
                {
                    "descripcion": "Fase 1: Estudio de factibilidad",
                    "cantidad": 1,
                    "unidad": "fase",
                    "precio_unitario": 25000
                },
                {
                    "descripcion": "Fase 2: Diseño e ingeniería",
                    "cantidad": 1,
                    "unidad": "fase",
                    "precio_unitario": 45000
                },
                {
                    "descripcion": "Fase 3: Implementación",
                    "cantidad": 1,
                    "unidad": "fase",
                    "precio_unitario": 150000
                }
            ],
            "subtotal": 220000,
            "igv": 39600,
            "total": 259600,
            "fases": [
                {"nombre": "Estudio", "duracion": "2 meses"},
                {"nombre": "Diseño", "duracion": "3 meses"},
                {"nombre": "Implementación", "duracion": "7 meses"}
            ],
            "cronograma": "12 meses"
        }

        content = generar_documento(datos_doc, "word")
        if content:
            filename = OUTPUT_DIR / f"proyecto_complejo_{proj['id']:03d}.docx"
            with open(filename, 'wb') as f:
                f.write(content)
            log(f"  ✅ Word generado: {filename}", "green")
            success_count += 1
        else:
            fail_count += 1

        total_docs += 1
        time.sleep(0.3)

    # Generar informes simples (6 docs)
    log("\n" + "="*80)
    log("📊 INFORMES SIMPLES (6 documentos)", "blue")
    log("="*80)

    for idx, inf in enumerate(test_data.get("informes_simples", []), 1):
        log(f"\n[{idx}/6] {inf['titulo']}")

        datos_doc = {
            "numero": f"INF-SIMPLE-{inf['id']:03d}",
            "cliente": inf['cliente'],
            "proyecto": inf['titulo'],
            "descripcion": inf['descripcion'],
            "fecha": "2025-12-06",
            "items": [
                {
                    "descripcion": "Servicio de inspección técnica",
                    "cantidad": 1,
                    "unidad": "servicio",
                    "precio_unitario": 800
                }
            ],
            "subtotal": 800,
            "igv": 144,
            "total": 944,
            "secciones": ["Introducción", "Metodología", "Resultados", "Conclusiones"]
        }

        content = generar_documento(datos_doc, "word")
        if content:
            filename = OUTPUT_DIR / f"informe_simple_{inf['id']:03d}.docx"
            with open(filename, 'wb') as f:
                f.write(content)
            log(f"  ✅ Word generado: {filename}", "green")
            success_count += 1
        else:
            fail_count += 1

        total_docs += 1
        time.sleep(0.3)

    # Resultados finales
    log("\n" + "="*80)
    log("📊 RESUMEN FINAL", "yellow")
    log("="*80)
    log(f"Total documentos procesados: {total_docs}")
    log(f"✅ Exitosos: {success_count}", "green")
    log(f"❌ Fallidos: {fail_count}", "red" if fail_count > 0 else "green")
    log(f"📁 Directorio: {OUTPUT_DIR.absolute()}")
    log("="*80)

    if success_count == total_docs:
        log("\n🎉 ¡TODOS LOS DOCUMENTOS GENERADOS EXITOSAMENTE! 🎉", "green")
    else:
        log(f"\n⚠️  Se generaron {success_count}/{total_docs} documentos", "yellow")

if __name__ == "__main__":
    main()
