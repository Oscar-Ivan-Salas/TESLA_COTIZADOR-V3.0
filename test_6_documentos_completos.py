#!/usr/bin/env python3
"""
Script de prueba completa del sistema Tesla Cotizador V3.0
Genera los 6 tipos de documentos Word profesionales

Prueba:
1. Cotización Simple
2. Cotización Compleja
3. Proyecto Simple
4. Proyecto Complejo (PMI)
5. Informe Técnico
6. Informe Ejecutivo (APA)
"""
import sys
import os
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.services.html_to_word_generator import html_to_word_generator
from datetime import datetime

# Directorio de salida
OUTPUT_DIR = Path(__file__).parent / "storage" / "generados"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("🚀 PRUEBA COMPLETA - SISTEMA TESLA COTIZADOR V3.0")
print("=" * 80)
print(f"📁 Directorio salida: {OUTPUT_DIR}")
print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("=" * 80)
print()

resultados = []

# ═══════════════════════════════════════════════════════════════════
# 1. COTIZACIÓN SIMPLE
# ═══════════════════════════════════════════════════════════════════
print("📄 1/6: Generando Cotización Simple...")
try:
    datos_cot_simple = {
        "numero": "COT-202512-0001",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "cliente": "CORPORACIÓN INDUSTRIAL ABC S.A.C.",
        "proyecto": "Instalación Eléctrica Oficinas Administrativas",
        "atencion": "Ing. Carlos Mendoza",
        "items": [
            {
                "descripcion": "Tablero eléctrico general 3F 100A",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 1200.00
            },
            {
                "descripcion": "Cable THW 10mm² - Color Rojo/Negro/Azul",
                "cantidad": 50,
                "unidad": "m",
                "precio_unitario": 3.80
            },
            {
                "descripcion": "Luminaria LED panel 60x60 48W",
                "cantidad": 20,
                "unidad": "und",
                "precio_unitario": 85.00
            },
            {
                "descripcion": "Tomacorriente doble con línea a tierra",
                "cantidad": 30,
                "unidad": "und",
                "precio_unitario": 12.50
            },
            {
                "descripcion": "Interruptor termomagnético 2x32A",
                "cantidad": 8,
                "unidad": "und",
                "precio_unitario": 45.00
            }
        ],
        "observaciones": "Precios en Soles peruanos incluyen IGV. Instalación según CNE-Utilización 2011.",
        "vigencia": "30 días calendario"
    }

    ruta = OUTPUT_DIR / "COTIZACION_SIMPLE_PROFESIONAL.docx"
    html_to_word_generator.generar_cotizacion_simple(datos_cot_simple, ruta)
    print(f"   ✅ Generado: {ruta.name} ({ruta.stat().st_size / 1024:.1f} KB)")
    resultados.append(("Cotización Simple", True, ruta))
except Exception as e:
    print(f"   ❌ Error: {e}")
    resultados.append(("Cotización Simple", False, None))

# ═══════════════════════════════════════════════════════════════════
# 2. COTIZACIÓN COMPLEJA
# ═══════════════════════════════════════════════════════════════════
print("📄 2/6: Generando Cotización Compleja...")
try:
    datos_cot_compleja = {
        "numero": "COT-202512-0002-PRO",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "cliente": "CONSTRUCTORA MEGAPROYECTOS S.A.",
        "proyecto": "Sistema Eléctrico Edificio Corporativo Torre Azul",
        "atencion": "Arq. Patricia Rojas - Gerente de Proyectos",
        "items": [
            {
                "descripcion": "Subestación eléctrica 630 kVA",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 45000.00
            },
            {
                "descripcion": "Tablero de distribución general 3F 800A",
                "cantidad": 2,
                "unidad": "und",
                "precio_unitario": 8500.00
            },
            {
                "descripcion": "Sistema de puesta a tierra (pozo completo)",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 3500.00
            },
            {
                "descripcion": "Cable NYY 3x70mm² + 35mm² (tierra)",
                "cantidad": 250,
                "unidad": "m",
                "precio_unitario": 28.50
            },
            {
                "descripcion": "Luminarias LED industriales 150W",
                "cantidad": 80,
                "unidad": "und",
                "precio_unitario": 180.00
            },
            {
                "descripcion": "Sistema detección y alarma contra incendios",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 12000.00
            }
        ],
        "condiciones": "Instalación certificada CNE. Incluye pruebas y puesta en marcha.",
        "terminos_pago": "40% adelanto, 40% avance 50%, 20% entrega final",
        "garantia_meses": "24 meses",
        "vigencia": "45 días calendario"
    }

    ruta = OUTPUT_DIR / "COTIZACION_COMPLEJA_PROFESIONAL.docx"
    html_to_word_generator.generar_cotizacion_compleja(datos_cot_compleja, ruta)
    print(f"   ✅ Generado: {ruta.name} ({ruta.stat().st_size / 1024:.1f} KB)")
    resultados.append(("Cotización Compleja", True, ruta))
except Exception as e:
    print(f"   ❌ Error: {e}")
    resultados.append(("Cotización Compleja", False, None))

# ═══════════════════════════════════════════════════════════════════
# 3. PROYECTO SIMPLE
# ═══════════════════════════════════════════════════════════════════
print("📄 3/6: Generando Proyecto Simple...")
try:
    datos_proyecto_simple = {
        "nombre": "Modernización Sistema Eléctrico Planta Industrial",
        "codigo": "PROY-202512-001",
        "cliente": "INDUSTRIAS METALMECÁNICAS DEL SUR S.A.C.",
        "fecha_inicio": "15/01/2025",
        "fecha_fin": "15/03/2025",
        "duracion_total": "60 días",
        "presupuesto": 85000.00,
        "alcance": "Modernización completa del sistema eléctrico de planta industrial incluyendo subestación, tableros de distribución, sistema de iluminación LED y puesta a tierra.",
        "normativa": "CNE Suministro 2011, Código Nacional de Electricidad - Utilización"
    }

    ruta = OUTPUT_DIR / "PROYECTO_SIMPLE_PROFESIONAL.docx"
    html_to_word_generator.generar_proyecto_simple(datos_proyecto_simple, ruta)
    print(f"   ✅ Generado: {ruta.name} ({ruta.stat().st_size / 1024:.1f} KB)")
    resultados.append(("Proyecto Simple", True, ruta))
except Exception as e:
    print(f"   ❌ Error: {e}")
    resultados.append(("Proyecto Simple", False, None))

# ═══════════════════════════════════════════════════════════════════
# 4. PROYECTO COMPLEJO (PMI)
# ═══════════════════════════════════════════════════════════════════
print("📄 4/6: Generando Proyecto Complejo PMI...")
try:
    datos_proyecto_pmi = {
        "nombre": "Implementación Sistema Automatización Industrial Avanzada",
        "codigo": "PROY-202512-002-PMI",
        "cliente": "CORPORACIÓN MINERA ATLAS S.A.C.",
        "fecha_inicio": "01/02/2025",
        "fecha_fin": "01/08/2025",
        "duracion_total": "180 días",
        "presupuesto": 350000.00,
        "alcance": "Project Charter PMI para implementación de sistema SCADA, automatización de procesos productivos, sistema eléctrico de respaldo y monitoreo remoto 24/7.",
        "normativa": "PMBoK 7th Edition, CNE Suministro 2011, IEC 61508",
        "spi": "1.05",
        "cpi": "0.98",
        "ev": 175000,
        "pv": 166667,
        "ac": 178571,
        "dias_ingenieria": "45",
        "dias_ejecucion": "120"
    }

    ruta = OUTPUT_DIR / "PROYECTO_PMI_COMPLEJO_PROFESIONAL.docx"
    html_to_word_generator.generar_proyecto_complejo(datos_proyecto_pmi, ruta)
    print(f"   ✅ Generado: {ruta.name} ({ruta.stat().st_size / 1024:.1f} KB)")
    resultados.append(("Proyecto PMI", True, ruta))
except Exception as e:
    print(f"   ❌ Error: {e}")
    resultados.append(("Proyecto PMI", False, None))

# ═══════════════════════════════════════════════════════════════════
# 5. INFORME TÉCNICO
# ═══════════════════════════════════════════════════════════════════
print("📄 5/6: Generando Informe Técnico...")
try:
    datos_informe_tecnico = {
        "titulo": "Sistema de Puesta a Tierra - Edificio Corporativo",
        "codigo": "INF-TEC-202512-001",
        "cliente": "BANCO CONTINENTAL DEL PERÚ",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "servicio_nombre": "Implementación Sistema de Puesta a Tierra",
        "resumen": "El presente informe técnico describe el diseño, instalación y pruebas del sistema de puesta a tierra implementado en el Edificio Corporativo del Banco Continental, cumpliendo con normativa peruana vigente.",
        "normativa": "CNE Suministro 2011, NTP-IEC 60364"
    }

    ruta = OUTPUT_DIR / "INFORME_TECNICO_PROFESIONAL.docx"
    html_to_word_generator.generar_informe_tecnico(datos_informe_tecnico, ruta)
    print(f"   ✅ Generado: {ruta.name} ({ruta.stat().st_size / 1024:.1f} KB)")
    resultados.append(("Informe Técnico", True, ruta))
except Exception as e:
    print(f"   ❌ Error: {e}")
    resultados.append(("Informe Técnico", False, None))

# ═══════════════════════════════════════════════════════════════════
# 6. INFORME EJECUTIVO (APA)
# ═══════════════════════════════════════════════════════════════════
print("📄 6/6: Generando Informe Ejecutivo APA...")
try:
    datos_informe_ejecutivo = {
        "titulo": "Viabilidad Económica: Modernización Energética Industrial",
        "codigo": "INF-EXE-202512-002-APA",
        "cliente": "TEXTILES PERUANOS PREMIUM S.A.C.",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "servicio_nombre": "Estudio de Viabilidad para Modernización Sistema Eléctrico",
        "resumen": "El presente informe ejecutivo analiza la viabilidad técnica y económica del proyecto de modernización del sistema eléctrico de Textiles Peruanos Premium, con proyecciones financieras a 5 años y análisis de retorno de inversión.",
        "presupuesto": 180000.00,
        "roi": "28",
        "payback": "16",
        "tir": "32",
        "ahorro_anual": 42000,
        "ahorro_energetico": 85000,
        "normativa": "CNE Suministro 2011, NTP-IEC 60364, ISO 50001"
    }

    ruta = OUTPUT_DIR / "INFORME_EJECUTIVO_APA_PROFESIONAL.docx"
    html_to_word_generator.generar_informe_ejecutivo(datos_informe_ejecutivo, ruta)
    print(f"   ✅ Generado: {ruta.name} ({ruta.stat().st_size / 1024:.1f} KB)")
    resultados.append(("Informe Ejecutivo APA", True, ruta))
except Exception as e:
    print(f"   ❌ Error: {e}")
    resultados.append(("Informe Ejecutivo APA", False, None))

# ═══════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═══════════════════════════════════════════════════════════════════
print()
print("=" * 80)
print("📊 RESUMEN DE RESULTADOS")
print("=" * 80)

exitosos = sum(1 for _, exito, _ in resultados if exito)
total = len(resultados)

for nombre, exito, ruta in resultados:
    status = "✅" if exito else "❌"
    if exito:
        print(f"{status} {nombre:30} → {ruta.name} ({ruta.stat().st_size / 1024:.1f} KB)")
    else:
        print(f"{status} {nombre:30} → ERROR")

print("=" * 80)
print(f"🎯 TOTAL: {exitosos}/{total} documentos generados correctamente")
print(f"📁 Ubicación: {OUTPUT_DIR}")
print("=" * 80)

if exitosos == total:
    print("🎉 ¡ÉXITO TOTAL! Todos los documentos se generaron correctamente")
    sys.exit(0)
else:
    print("⚠️  ATENCIÓN: Algunos documentos no se generaron")
    sys.exit(1)
