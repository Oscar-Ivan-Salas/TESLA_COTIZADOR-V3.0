#!/usr/bin/env python3
"""
Script para generar 30 documentos de prueba (5 de cada tipo)
usando datos reales de la BD
"""

import sys
import os
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from pathlib import Path

OUTPUT_DIR = Path("backend/documentos_prueba")
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    print("🚀 Iniciando generación de 30 documentos de prueba...\n")

    # Conectar BD con sqlite3
    conn = sqlite3.connect('database/tesla_cotizador.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, ruc FROM clientes LIMIT 5")
    clientes = cursor.fetchall()
    conn.close()

    if not clientes:
        print("❌ No hay clientes en la BD")
        return

    print(f"✅ Encontrados {len(clientes)} clientes\n")

    # Importar aquí para evitar conflictos
    from backend.app.services.word_generator import WordGenerator
    from backend.app.templates.documentos.plantillas_modelo import (
        plantilla_cotizacion_simple,
        plantilla_cotizacion_compleja,
        plantilla_proyecto_simple,
        plantilla_proyecto_complejo,
        plantilla_informe_tecnico,
        plantilla_informe_ejecutivo
    )

    word_gen = WordGenerator()
    documentos_generados = []

    # Generar 5 de cada tipo (30 total)
    for i, (nombre, ruc) in enumerate(clientes, 1):
        print(f"📄 Generando documentos para: {nombre}")

        # 1. Cotización Simple
        try:
            datos = plantilla_cotizacion_simple(
                servicio="electrico-residencial",
                cliente=nombre,
                area_m2=100.0
            )
            archivo = OUTPUT_DIR / f"{i}_Cotizacion_Simple_{ruc}.docx"
            word_gen.generar_desde_json_pili(datos, str(archivo))
            documentos_generados.append(str(archivo))
            print(f"  ✅ Cotización Simple")
        except Exception as e:
            print(f"  ❌ Error: {e}")

        # 2. Cotización Compleja
        try:
            datos = plantilla_cotizacion_compleja(
                servicio="electrico-industrial",
                cliente=nombre,
                area_m2=500.0
            )
            archivo = OUTPUT_DIR / f"{i}_Cotizacion_Compleja_{ruc}.docx"
            word_gen.generar_desde_json_pili(datos, str(archivo))
            documentos_generados.append(str(archivo))
            print(f"  ✅ Cotización Compleja")
        except Exception as e:
            print(f"  ❌ Error: {e}")

        # 3. Proyecto Simple
        try:
            datos = plantilla_proyecto_simple(
                servicio="domotica",
                cliente=nombre,
                area_m2=150.0
            )
            archivo = OUTPUT_DIR / f"{i}_Proyecto_Simple_{ruc}.docx"
            word_gen.generar_desde_json_pili(datos, str(archivo))
            documentos_generados.append(str(archivo))
            print(f"  ✅ Proyecto Simple")
        except Exception as e:
            print(f"  ❌ Error: {e}")

        # 4. Proyecto Complejo
        try:
            datos = plantilla_proyecto_complejo(
                servicio="contraincendios",
                cliente=nombre,
                area_m2=300.0
            )
            archivo = OUTPUT_DIR / f"{i}_Proyecto_Complejo_{ruc}.docx"
            word_gen.generar_desde_json_pili(datos, str(archivo))
            documentos_generados.append(str(archivo))
            print(f"  ✅ Proyecto Complejo")
        except Exception as e:
            print(f"  ❌ Error: {e}")

        # 5. Informe Técnico
        try:
            datos = plantilla_informe_tecnico(
                servicio="itse",
                cliente=nombre
            )
            archivo = OUTPUT_DIR / f"{i}_Informe_Tecnico_{ruc}.docx"
            word_gen.generar_desde_json_pili(datos, str(archivo))
            documentos_generados.append(str(archivo))
            print(f"  ✅ Informe Técnico")
        except Exception as e:
            print(f"  ❌ Error: {e}")

        # 6. Informe Ejecutivo
        try:
            datos = plantilla_informe_ejecutivo(
                servicio="saneamiento",
                cliente=nombre
            )
            archivo = OUTPUT_DIR / f"{i}_Informe_Ejecutivo_{ruc}.docx"
            word_gen.generar_desde_json_pili(datos, str(archivo))
            documentos_generados.append(str(archivo))
            print(f"  ✅ Informe Ejecutivo\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")

    print(f"\n{'='*60}")
    print(f"✅ COMPLETADO: {len(documentos_generados)} documentos generados")
    print(f"📁 Ubicación: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
