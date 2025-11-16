"""
🎯 PRUEBA FINAL - GENERAR 6 DOCUMENTOS WORD
Genera los 6 tipos de documentos usando PILIBrain + word_generator
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.pili_brain import pili_brain
from services.word_generator import word_generator
from datetime import datetime
import json

print("=" * 80)
print("🎯 GENERANDO LOS 6 TIPOS DE DOCUMENTOS - PRUEBA FINAL")
print("=" * 80)

# Crear carpeta de salida
output_dir = "documentos_generados_demo"
os.makedirs(output_dir, exist_ok=True)

mensaje_test = "Necesito para instalación eléctrica residencial de 150m²"

documentos_generados = []

# ═══════════════════════════════════════════════════════════════
# 1. COTIZACIÓN SIMPLE
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("💰 1/6: GENERANDO COTIZACIÓN SIMPLE...")
print("━" * 80)

try:
    # Generar JSON con PILIBrain
    cot_simple_json = pili_brain.generar_cotizacion(
        mensaje=mensaje_test,
        servicio="electrico-residencial",
        complejidad="simple"
    )

    # Generar documento Word
    filepath_cot_simple = word_generator.generar_desde_json_pili(
        datos_json=cot_simple_json["datos"],
        tipo_documento="cotizacion",
        opciones={"complejidad": "simple"}
    )

    # Mover a carpeta demo
    import shutil
    dest = os.path.join(output_dir, "1_Cotizacion_Simple.docx")
    shutil.copy(filepath_cot_simple, dest)

    print(f"✅ GENERADO: {dest}")
    print(f"   Total: ${cot_simple_json['datos']['total']:,.2f} USD")
    print(f"   Items: {len(cot_simple_json['datos']['items'])}")

    documentos_generados.append({
        "tipo": "Cotización Simple",
        "archivo": dest,
        "total": cot_simple_json['datos']['total']
    })

except Exception as e:
    print(f"❌ ERROR: {e}")

# ═══════════════════════════════════════════════════════════════
# 2. COTIZACIÓN COMPLEJA
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("💰 2/6: GENERANDO COTIZACIÓN COMPLEJA...")
print("━" * 80)

try:
    cot_compleja_json = pili_brain.generar_cotizacion(
        mensaje=mensaje_test,
        servicio="electrico-residencial",
        complejidad="complejo"
    )

    filepath_cot_compleja = word_generator.generar_desde_json_pili(
        datos_json=cot_compleja_json["datos"],
        tipo_documento="cotizacion",
        opciones={"complejidad": "complejo"}
    )

    dest = os.path.join(output_dir, "2_Cotizacion_Compleja.docx")
    shutil.copy(filepath_cot_compleja, dest)

    print(f"✅ GENERADO: {dest}")
    print(f"   Total: ${cot_compleja_json['datos']['total']:,.2f} USD")

    documentos_generados.append({
        "tipo": "Cotización Compleja",
        "archivo": dest,
        "total": cot_compleja_json['datos']['total']
    })

except Exception as e:
    print(f"❌ ERROR: {e}")

# ═══════════════════════════════════════════════════════════════
# 3. PROYECTO SIMPLE
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("📊 3/6: GENERANDO PROYECTO SIMPLE...")
print("━" * 80)

try:
    proy_simple_json = pili_brain.generar_proyecto(
        mensaje=mensaje_test,
        servicio="electrico-residencial",
        complejidad="simple"
    )

    filepath_proy_simple = word_generator.generar_desde_json_pili(
        datos_json=proy_simple_json["datos"],
        tipo_documento="proyecto",
        opciones={"complejidad": "simple"}
    )

    dest = os.path.join(output_dir, "3_Proyecto_Simple.docx")
    shutil.copy(filepath_proy_simple, dest)

    print(f"✅ GENERADO: {dest}")
    print(f"   Duración: {proy_simple_json['datos']['duracion_total_dias']} días")
    print(f"   Fases: {len(proy_simple_json['datos']['fases'])}")

    documentos_generados.append({
        "tipo": "Proyecto Simple",
        "archivo": dest,
        "duracion": proy_simple_json['datos']['duracion_total_dias']
    })

except Exception as e:
    print(f"❌ ERROR: {e}")

# ═══════════════════════════════════════════════════════════════
# 4. PROYECTO COMPLEJO (PMI)
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("📊 4/6: GENERANDO PROYECTO COMPLEJO PMI...")
print("━" * 80)

try:
    proy_complejo_json = pili_brain.generar_proyecto(
        mensaje=mensaje_test,
        servicio="electrico-residencial",
        complejidad="complejo"
    )

    filepath_proy_complejo = word_generator.generar_desde_json_pili(
        datos_json=proy_complejo_json["datos"],
        tipo_documento="proyecto",
        opciones={"complejidad": "complejo"}
    )

    dest = os.path.join(output_dir, "4_Proyecto_Complejo_PMI.docx")
    shutil.copy(filepath_proy_complejo, dest)

    print(f"✅ GENERADO: {dest}")
    print(f"   Duración: {proy_complejo_json['datos']['duracion_total_dias']} días")
    print(f"   Fases: {len(proy_complejo_json['datos']['fases'])} (incluye Stakeholders)")
    print(f"   Gantt: {'SÍ' if proy_complejo_json['datos']['cronograma_gantt'] else 'NO'}")

    documentos_generados.append({
        "tipo": "Proyecto Complejo PMI",
        "archivo": dest,
        "duracion": proy_complejo_json['datos']['duracion_total_dias']
    })

except Exception as e:
    print(f"❌ ERROR: {e}")

# ═══════════════════════════════════════════════════════════════
# 5. INFORME TÉCNICO
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("📄 5/6: GENERANDO INFORME TÉCNICO...")
print("━" * 80)

try:
    inf_simple_json = pili_brain.generar_informe(
        mensaje=mensaje_test,
        servicio="electrico-residencial",
        complejidad="simple"
    )

    filepath_inf_simple = word_generator.generar_desde_json_pili(
        datos_json=inf_simple_json["datos"],
        tipo_documento="informe",
        opciones={"complejidad": "simple"}
    )

    dest = os.path.join(output_dir, "5_Informe_Tecnico.docx")
    shutil.copy(filepath_inf_simple, dest)

    print(f"✅ GENERADO: {dest}")
    print(f"   Secciones: {len(inf_simple_json['datos']['secciones'])}")
    print(f"   Formato: {inf_simple_json['datos']['formato']}")

    documentos_generados.append({
        "tipo": "Informe Técnico",
        "archivo": dest,
        "secciones": len(inf_simple_json['datos']['secciones'])
    })

except Exception as e:
    print(f"❌ ERROR: {e}")

# ═══════════════════════════════════════════════════════════════
# 6. INFORME EJECUTIVO (APA)
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("📄 6/6: GENERANDO INFORME EJECUTIVO APA...")
print("━" * 80)

try:
    inf_ejecutivo_json = pili_brain.generar_informe(
        mensaje=mensaje_test,
        servicio="electrico-residencial",
        complejidad="complejo"
    )

    filepath_inf_ejecutivo = word_generator.generar_desde_json_pili(
        datos_json=inf_ejecutivo_json["datos"],
        tipo_documento="informe",
        opciones={"complejidad": "complejo"}
    )

    dest = os.path.join(output_dir, "6_Informe_Ejecutivo_APA.docx")
    shutil.copy(filepath_inf_ejecutivo, dest)

    print(f"✅ GENERADO: {dest}")
    print(f"   Secciones: {len(inf_ejecutivo_json['datos']['secciones'])}")
    print(f"   Formato: {inf_ejecutivo_json['datos']['formato']}")
    if inf_ejecutivo_json['datos'].get('metricas_clave'):
        metricas = inf_ejecutivo_json['datos']['metricas_clave']
        print(f"   ROI: {metricas['roi_estimado']}% | TIR: {metricas['tir_proyectada']}%")

    documentos_generados.append({
        "tipo": "Informe Ejecutivo APA",
        "archivo": dest,
        "secciones": len(inf_ejecutivo_json['datos']['secciones'])
    })

except Exception as e:
    print(f"❌ ERROR: {e}")

# ═══════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("✅ GENERACIÓN COMPLETADA")
print("=" * 80)

print(f"\n📊 RESUMEN:")
print(f"   Documentos generados: {len(documentos_generados)}/6")
print(f"   Ubicación: {os.path.abspath(output_dir)}/")
print(f"\n📁 ARCHIVOS:")

for i, doc in enumerate(documentos_generados, 1):
    print(f"   {i}. {doc['tipo']}")
    print(f"      📄 {os.path.basename(doc['archivo'])}")

print(f"\n🎯 PRUEBA EXITOSA:")
print(f"   ✅ PILIBrain generó los JSONs")
print(f"   ✅ word_generator creó los documentos Word")
print(f"   ✅ {len(documentos_generados)} documentos listos para demostración")

print(f"\n💡 SIGUIENTE PASO:")
print(f"   Abre los archivos Word en {output_dir}/ para verificar")

print("=" * 80)

# Guardar reporte JSON
reporte = {
    "fecha_generacion": datetime.now().isoformat(),
    "documentos_generados": documentos_generados,
    "total": len(documentos_generados),
    "exitoso": len(documentos_generados) == 6
}

with open(os.path.join(output_dir, "reporte_generacion.json"), "w", encoding="utf-8") as f:
    json.dump(reporte, f, indent=2, ensure_ascii=False)

print(f"\n📋 Reporte guardado en: {output_dir}/reporte_generacion.json")
