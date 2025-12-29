#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de Estructura de Generadores Profesionales
Verifica que todos los archivos existan y tengan sintaxis correcta
"""

import ast
import sys
from pathlib import Path

def verificar_sintaxis(archivo_path):
    """Verifica que un archivo Python tenga sintaxis correcta"""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            codigo = f.read()
        ast.parse(codigo)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Error de sintaxis: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Verificación principal"""
    print("=" * 80)
    print("VERIFICACIÓN DE ESTRUCTURA - GENERADORES PROFESIONALES")
    print("=" * 80)
    print()

    base_path = Path("app/services/professional/generators")
    resultados = []

    # Archivos a verificar
    archivos = {
        "Root": [
            "__init__.py",
            "document_generator_pro.py",
            "pdf_converter.py"
        ],
        "Base": [
            "base/__init__.py",
            "base/base_generator.py"
        ],
        "Cotizaciones": [
            "cotizaciones/__init__.py",
            "cotizaciones/simple.py",
            "cotizaciones/compleja.py"
        ],
        "Proyectos": [
            "proyectos/__init__.py",
            "proyectos/simple.py",
            "proyectos/complejo_pmi.py"
        ],
        "Informes": [
            "informes/__init__.py",
            "informes/tecnico.py",
            "informes/ejecutivo_apa.py"
        ]
    }

    total_archivos = 0
    archivos_ok = 0

    for categoria, lista_archivos in archivos.items():
        print(f"\n📁 {categoria}:")
        for archivo in lista_archivos:
            total_archivos += 1
            archivo_path = base_path / archivo

            # Verificar existencia
            if not archivo_path.exists():
                print(f"   ❌ {archivo} - NO EXISTE")
                resultados.append(False)
                continue

            # Verificar sintaxis
            ok, mensaje = verificar_sintaxis(archivo_path)
            if ok:
                # Obtener tamaño
                tamaño = archivo_path.stat().st_size
                tamaño_kb = tamaño / 1024
                print(f"   ✅ {archivo} ({tamaño_kb:.1f} KB)")
                archivos_ok += 1
                resultados.append(True)
            else:
                print(f"   ❌ {archivo} - {mensaje}")
                resultados.append(False)

    # Resumen
    print("\n" + "=" * 80)
    print(f"RESULTADO: {archivos_ok}/{total_archivos} archivos correctos")

    # Calcular líneas totales
    total_lineas = 0
    for categoria, lista_archivos in archivos.items():
        for archivo in lista_archivos:
            archivo_path = base_path / archivo
            if archivo_path.exists():
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    lineas = len(f.readlines())
                    total_lineas += lineas

    print(f"📊 Total de líneas de código: {total_lineas:,}")

    if archivos_ok == total_archivos:
        print("✅ ¡Estructura completa y sintaxis correcta!")
        return 0
    else:
        print("⚠️  Algunos archivos tienen problemas")
        return 1

if __name__ == "__main__":
    sys.exit(main())
