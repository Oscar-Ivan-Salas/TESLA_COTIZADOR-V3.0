#!/usr/bin/env python3
"""
TEST: Generación de Documentos Word desde Plantillas HTML
==========================================================

Este script prueba la conversión de las plantillas HTML profesionales
a documentos Word (.docx) usando el nuevo generador.

UBICACIÓN: test_html_to_word.py (raíz del proyecto)
"""

import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.services.html_to_word_generator import html_to_word_generator


def test_cotizacion_simple():
    """Probar generación de cotización simple"""
    print("\n" + "="*70)
    print("TEST 1: COTIZACIÓN SIMPLE")
    print("="*70)

    datos = {
        "numero": "COT-202512-0001",
        "cliente": "CONSTRUCTORA ABC S.A.C.",
        "proyecto": "Instalación Eléctrica Oficinas Corporativas",
        "area_m2": "150",
        "fecha": "13/12/2024",
        "vigencia": "30 días calendario",
        "servicio_nombre": "Instalaciones Eléctricas Comerciales",
        "descripcion": "Proyecto de instalación eléctrica completa para oficinas corporativas de 150m² ubicadas en San Isidro, Lima. Incluye tableros, circuitos, iluminación LED y sistema de puesta a tierra según CNE Suministro 2011.",
        "subtotal": 2715.00,
        "igv": 488.70,
        "total": 3203.70,
        "normativa": "CNE Suministro 2011"
    }

    try:
        ruta = html_to_word_generator.generar_cotizacion_simple(datos)
        print(f"✅ ÉXITO: Documento generado en {ruta}")
        print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cotizacion_compleja():
    """Probar generación de cotización compleja"""
    print("\n" + "="*70)
    print("TEST 2: COTIZACIÓN COMPLEJA")
    print("="*70)

    datos = {
        "numero": "COT-202512-0002-PRO",
        "cliente": "GRUPO INDUSTRIAL XYZ S.A.",
        "proyecto": "Sistema Eléctrico Industrial - Versión Profesional",
        "area_m2": "300",
        "servicio_nombre": "Instalaciones Eléctricas Industriales",
        "descripcion": "Proyecto profesional de instalación eléctrica industrial con ingeniería de detalle, suministro de materiales certificados, instalación por personal especializado, pruebas FAT/SAT y documentación técnica completa.",
        "subtotal": 5265.00,
        "igv": 947.70,
        "total": 6212.70,
        "dias_ingenieria": "10",
        "dias_adquisiciones": "10",
        "dias_instalacion": "20",
        "dias_pruebas": "5"
    }

    try:
        ruta = html_to_word_generator.generar_cotizacion_compleja(datos)
        print(f"✅ ÉXITO: Documento generado en {ruta}")
        print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_proyecto_simple():
    """Probar generación de proyecto simple"""
    print("\n" + "="*70)
    print("TEST 3: PROYECTO SIMPLE")
    print("="*70)

    datos = {
        "nombre": "Proyecto de Automatización Residencial",
        "codigo": "PROY-20241213-001",
        "cliente": "INMOBILIARIA MODERNA S.A.C.",
        "duracion_total": "35",
        "fecha_inicio": "15/01/2025",
        "fecha_fin": "19/02/2025",
        "presupuesto": 45000.00,
        "alcance": "El proyecto comprende el diseño, suministro, instalación y puesta en marcha de sistema de automatización residencial (domótica) para edificio multifamiliar de 10 departamentos.",
        "dias_ingenieria": "7",
        "dias_ejecucion": "20"
    }

    try:
        ruta = html_to_word_generator.generar_proyecto_simple(datos)
        print(f"✅ ÉXITO: Documento generado en {ruta}")
        print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_proyecto_complejo():
    """Probar generación de proyecto complejo PMI"""
    print("\n" + "="*70)
    print("TEST 4: PROYECTO COMPLEJO (PMI)")
    print("="*70)

    datos = {
        "nombre": "Sistema Contra Incendios - Hospital Central",
        "codigo": "PROY-20241213-002-PMI",
        "cliente": "CLÍNICA SAN RAFAEL S.A.",
        "duracion_total": "60",
        "fecha_inicio": "01/02/2025",
        "fecha_fin": "01/04/2025",
        "presupuesto": 150000.00,
        "alcance": "Proyecto PMI completo de sistema contra incendios para hospital de 5 pisos, incluyendo rociadores, detectores de humo, alarmas, extintores y sistema de presurización según NFPA 13, NFPA 72 y NFPA 20.",
        "spi": "1.0",
        "cpi": "1.0",
        "ev": 75000,
        "pv": 75000,
        "ac": 75000,
        "dias_ingenieria": "15",
        "dias_ejecucion": "35"
    }

    try:
        ruta = html_to_word_generator.generar_proyecto_complejo(datos)
        print(f"✅ ÉXITO: Documento generado en {ruta}")
        print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_informe_tecnico():
    """Probar generación de informe técnico"""
    print("\n" + "="*70)
    print("TEST 5: INFORME TÉCNICO")
    print("="*70)

    datos = {
        "titulo": "Sistema de Puesta a Tierra - Edificio Corporativo",
        "codigo": "INF-20241213-001",
        "cliente": "CORPORACIÓN EMPRESARIAL ABC",
        "resumen": "El presente informe técnico presenta el diseño del sistema de puesta a tierra para edificio corporativo de 8 pisos. El proyecto se ejecuta bajo la normativa CNE Suministro Sección 250 y cumple con todos los requisitos técnicos establecidos.",
        "servicio_nombre": "Sistema de Puesta a Tierra"
    }

    try:
        ruta = html_to_word_generator.generar_informe_tecnico(datos)
        print(f"✅ ÉXITO: Documento generado en {ruta}")
        print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_informe_ejecutivo():
    """Probar generación de informe ejecutivo APA"""
    print("\n" + "="*70)
    print("TEST 6: INFORME EJECUTIVO (APA)")
    print("="*70)

    datos = {
        "titulo": "Modernización del Sistema Eléctrico - Planta Industrial",
        "codigo": "INF-20241213-002-EXE",
        "cliente": "INDUSTRIAS METALMECÁNICAS S.A.",
        "resumen": "El presente informe ejecutivo analiza la viabilidad del proyecto de modernización del sistema eléctrico de planta industrial. La inversión total requerida es de USD 80,000 con un ROI estimado de 28%, período de retorno de 16 meses y TIR proyectada de 32%. El proyecto presenta alta viabilidad técnica y financiera, recomendándose su aprobación e implementación inmediata.",
        "presupuesto": 80000.00,
        "roi": "28",
        "payback": "16",
        "tir": "32",
        "ahorro_anual": 12000,
        "ahorro_energetico": 12000,
        "servicio_nombre": "Modernización de Sistemas Eléctricos Industriales"
    }

    try:
        ruta = html_to_word_generator.generar_informe_ejecutivo(datos)
        print(f"✅ ÉXITO: Documento generado en {ruta}")
        print(f"   Tamaño: {ruta.stat().st_size / 1024:.1f} KB")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("PRUEBA DE CONVERSIÓN HTML → WORD")
    print("Sistema de Generación de Documentos Profesionales")
    print("="*70)
    print("\nGenerando 6 documentos Word desde plantillas HTML...")

    resultados = []

    # Ejecutar tests
    resultados.append(("Cotización Simple", test_cotizacion_simple()))
    resultados.append(("Cotización Compleja", test_cotizacion_compleja()))
    resultados.append(("Proyecto Simple", test_proyecto_simple()))
    resultados.append(("Proyecto Complejo PMI", test_proyecto_complejo()))
    resultados.append(("Informe Técnico", test_informe_tecnico()))
    resultados.append(("Informe Ejecutivo APA", test_informe_ejecutivo()))

    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE RESULTADOS")
    print("="*70)

    exitos = sum(1 for _, ok in resultados if ok)
    total = len(resultados)

    for nombre, ok in resultados:
        estado = "✅ ÉXITO" if ok else "❌ FALLÓ"
        print(f"{estado}: {nombre}")

    print("\n" + "-"*70)
    print(f"TOTAL: {exitos}/{total} documentos generados correctamente")
    print("="*70)

    if exitos == total:
        print("\n🎉 ¡TODOS LOS DOCUMENTOS SE GENERARON CORRECTAMENTE!")
        print("\n📁 Ubicación: storage/generados/")
        return 0
    else:
        print(f"\n⚠️ {total - exitos} documento(s) fallaron")
        return 1


if __name__ == "__main__":
    exit(main())
