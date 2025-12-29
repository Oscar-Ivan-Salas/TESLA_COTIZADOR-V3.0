#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificación de Imports de Generadores Profesionales
Verifica que todos los generadores se pueden importar correctamente
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Prueba importar todos los módulos de generadores"""
    resultados = []

    print("=" * 80)
    print("VERIFICACIÓN DE IMPORTS - GENERADORES PROFESIONALES")
    print("=" * 80)
    print()

    # Test 1: Importar base_generator
    print("1. Importando BaseDocumentGenerator...")
    try:
        from app.services.professional.generators.base import BaseDocumentGenerator
        print("   ✅ BaseDocumentGenerator importado correctamente")
        resultados.append(True)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append(False)

    # Test 2: Importar cotizaciones
    print("\n2. Importando generadores de cotizaciones...")
    try:
        from app.services.professional.generators.cotizaciones import (
            generar_cotizacion_simple,
            generar_cotizacion_compleja
        )
        print("   ✅ Generadores de cotizaciones importados correctamente")
        resultados.append(True)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append(False)

    # Test 3: Importar proyectos
    print("\n3. Importando generadores de proyectos...")
    try:
        from app.services.professional.generators.proyectos import (
            generar_proyecto_simple,
            generar_proyecto_complejo_pmi
        )
        print("   ✅ Generadores de proyectos importados correctamente")
        resultados.append(True)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append(False)

    # Test 4: Importar informes
    print("\n4. Importando generadores de informes...")
    try:
        from app.services.professional.generators.informes import (
            generar_informe_tecnico,
            generar_informe_ejecutivo_apa
        )
        print("   ✅ Generadores de informes importados correctamente")
        resultados.append(True)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append(False)

    # Test 5: Importar sistema de routing
    print("\n5. Importando sistema de routing...")
    try:
        from app.services.professional.generators import (
            generar_documento,
            tipos_disponibles,
            GENERADORES
        )
        print("   ✅ Sistema de routing importado correctamente")
        print(f"   📋 Tipos disponibles: {len(GENERADORES)} generadores")
        for tipo in sorted(GENERADORES.keys()):
            print(f"      - {tipo}")
        resultados.append(True)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append(False)

    # Test 6: Importar DocumentGeneratorPro
    print("\n6. Importando DocumentGeneratorPro...")
    try:
        from app.services.professional.generators import DocumentGeneratorPro
        print("   ✅ DocumentGeneratorPro importado correctamente")
        resultados.append(True)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append(False)

    # Resumen
    print("\n" + "=" * 80)
    exitosos = sum(resultados)
    total = len(resultados)
    porcentaje = (exitosos / total) * 100

    print(f"RESULTADO: {exitosos}/{total} imports exitosos ({porcentaje:.1f}%)")

    if exitosos == total:
        print("✅ ¡Todos los generadores están listos para usar!")
        return 0
    else:
        print("⚠️  Algunos generadores tienen problemas de importación")
        return 1

if __name__ == "__main__":
    sys.exit(test_imports())
