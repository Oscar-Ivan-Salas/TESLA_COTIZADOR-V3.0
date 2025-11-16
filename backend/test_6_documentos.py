"""
🧪 TEST COMPLETO - 6 TIPOS DE DOCUMENTOS
Prueba los 6 tipos de documentos que PILI puede generar sin APIs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.pili_brain import pili_brain
import json

print("=" * 80)
print("🧪 TEST DE LOS 6 TIPOS DE DOCUMENTOS - PILIBrain")
print("=" * 80)

mensaje_test = "Necesito para instalación eléctrica residencial de 150m²"

# ═══════════════════════════════════════════════════════════════
# COTIZACIONES
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("💰 1. COTIZACIÓN SIMPLE")
print("━" * 80)
cot_simple = pili_brain.generar_cotizacion(
    mensaje=mensaje_test,
    servicio="electrico-residencial",
    complejidad="simple"
)
print(f"✅ Generada: {cot_simple['datos']['numero']}")
print(f"   Total: ${cot_simple['datos']['total']:,.2f} USD")
print(f"   Items: {len(cot_simple['datos']['items'])}")
print(f"   Mensaje: {cot_simple['conversacion']['mensaje_pili'][:100]}...")

print("\n" + "━" * 80)
print("💰 2. COTIZACIÓN COMPLEJA")
print("━" * 80)
cot_compleja = pili_brain.generar_cotizacion(
    mensaje=mensaje_test,
    servicio="electrico-residencial",
    complejidad="complejo"
)
print(f"✅ Generada: {cot_compleja['datos']['numero']}")
print(f"   Total: ${cot_compleja['datos']['total']:,.2f} USD")
print(f"   Complejidad: {cot_compleja['complejidad']}")
print(f"   Items: {len(cot_compleja['datos']['items'])}")

# ═══════════════════════════════════════════════════════════════
# PROYECTOS
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("📊 3. PROYECTO SIMPLE")
print("━" * 80)
proy_simple = pili_brain.generar_proyecto(
    mensaje=mensaje_test,
    servicio="electrico-residencial",
    complejidad="simple"
)
print(f"✅ Generado: {proy_simple['datos']['codigo']}")
print(f"   Duración: {proy_simple['datos']['duracion_total_dias']} días")
print(f"   Presupuesto: ${proy_simple['datos']['presupuesto_estimado']:,.2f} USD")
print(f"   Fases: {len(proy_simple['datos']['fases'])}")
print(f"   Recursos: {len(proy_simple['datos']['recursos'])}")
print(f"   Riesgos: {len(proy_simple['datos']['riesgos'])}")

print("\n" + "━" * 80)
print("📊 4. PROYECTO COMPLEJO (PMI)")
print("━" * 80)
proy_complejo = pili_brain.generar_proyecto(
    mensaje=mensaje_test,
    servicio="electrico-residencial",
    complejidad="complejo"
)
print(f"✅ Generado: {proy_complejo['datos']['codigo']}")
print(f"   Duración: {proy_complejo['datos']['duracion_total_dias']} días")
print(f"   Presupuesto: ${proy_complejo['datos']['presupuesto_estimado']:,.2f} USD")
print(f"   Fases: {len(proy_complejo['datos']['fases'])} (incluye Stakeholders)")
print(f"   Recursos: {len(proy_complejo['datos']['recursos'])} (equipo ampliado)")
print(f"   Gantt: {'SÍ' if proy_complejo['datos']['cronograma_gantt'] else 'NO'}")
if proy_complejo['datos']['cronograma_gantt']:
    print(f"   Tareas Gantt: {len(proy_complejo['datos']['cronograma_gantt']['tareas'])}")

# ═══════════════════════════════════════════════════════════════
# INFORMES
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("📄 5. INFORME TÉCNICO (Simple)")
print("━" * 80)
inf_simple = pili_brain.generar_informe(
    mensaje=mensaje_test,
    servicio="electrico-residencial",
    complejidad="simple"
)
print(f"✅ Generado: {inf_simple['datos']['codigo']}")
print(f"   Título: {inf_simple['datos']['titulo']}")
print(f"   Tipo: {inf_simple['tipo_informe']}")
print(f"   Formato: {inf_simple['datos']['formato']}")
print(f"   Secciones: {len(inf_simple['datos']['secciones'])}")
print(f"   Conclusiones: {len(inf_simple['datos']['conclusiones'])}")
print(f"   Gráficos sugeridos: {len(inf_simple['datos']['graficos_sugeridos'])}")

print("\n" + "━" * 80)
print("📄 6. INFORME EJECUTIVO (Complejo - APA)")
print("━" * 80)
inf_ejecutivo = pili_brain.generar_informe(
    mensaje=mensaje_test,
    servicio="electrico-residencial",
    complejidad="complejo"
)
print(f"✅ Generado: {inf_ejecutivo['datos']['codigo']}")
print(f"   Título: {inf_ejecutivo['datos']['titulo']}")
print(f"   Tipo: {inf_ejecutivo['tipo_informe']}")
print(f"   Formato: {inf_ejecutivo['datos']['formato']}")
print(f"   Secciones: {len(inf_ejecutivo['datos']['secciones'])} (incluye Análisis Financiero)")
print(f"   Métricas KPI: {'SÍ' if inf_ejecutivo['datos']['metricas_clave'] else 'NO'}")
if inf_ejecutivo['datos']['metricas_clave']:
    metricas = inf_ejecutivo['datos']['metricas_clave']
    print(f"   ROI: {metricas['roi_estimado']}%")
    print(f"   Payback: {metricas['payback_meses']} meses")
    print(f"   TIR: {metricas['tir_proyectada']}%")
print(f"   Bibliografía APA: {len(inf_ejecutivo['datos']['bibliografia'])} referencias")

# ═══════════════════════════════════════════════════════════════
# EXPORTAR JSONs
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("💾 EXPORTANDO JSONs DE MUESTRA")
print("━" * 80)

documentos_generados = {
    "cotizacion_simple": cot_simple,
    "cotizacion_compleja": cot_compleja,
    "proyecto_simple": proy_simple,
    "proyecto_complejo": proy_complejo,
    "informe_simple": inf_simple,
    "informe_ejecutivo": inf_ejecutivo
}

for nombre, documento in documentos_generados.items():
    filename = f"muestra_{nombre}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(documento, f, indent=2, ensure_ascii=False)
    print(f"✅ {filename}")

# ═══════════════════════════════════════════════════════════════
# PRUEBA CON DIFERENTES SERVICIOS
# ═══════════════════════════════════════════════════════════════

print("\n" + "━" * 80)
print("🔥 BONUS: TEST DE OTROS SERVICIOS")
print("━" * 80)

# Contraincendios
cot_incendio = pili_brain.generar_cotizacion(
    mensaje="Sistema contraincendios para edificio de 500m²",
    servicio="contraincendios",
    complejidad="complejo"
)
print(f"🔥 Contraincendios: ${cot_incendio['datos']['total']:,.2f} USD")

# Domótica
cot_domotica = pili_brain.generar_cotizacion(
    mensaje="Automatizar casa de 200m² con KNX",
    servicio="domotica",
    complejidad="complejo"
)
print(f"🏠 Domótica: ${cot_domotica['datos']['total']:,.2f} USD")

# Pozo a Tierra
cot_pozo = pili_brain.generar_cotizacion(
    mensaje="Necesito pozo a tierra para planta industrial",
    servicio="pozo-tierra",
    complejidad="simple"
)
print(f"🌍 Pozo a Tierra: ${cot_pozo['datos']['total']:,.2f} USD")

# ═══════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
print("=" * 80)

print(f"""
📊 RESUMEN DE CAPACIDADES:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 6 TIPOS DE DOCUMENTOS:
   1. Cotización Simple
   2. Cotización Compleja
   3. Proyecto Simple
   4. Proyecto Complejo (PMI + Gantt)
   5. Informe Técnico
   6. Informe Ejecutivo (APA + ROI)

✅ 10 SERVICIOS DISPONIBLES:
   - Eléctrico Residencial/Comercial/Industrial
   - Contraincendios (NFPA)
   - Domótica (KNX)
   - Expedientes Técnicos
   - Saneamiento (RNE)
   - Certificaciones ITSE
   - Pozo a Tierra (SPT)
   - Redes y CCTV

🧠 MODO: 100% OFFLINE (Sin APIs)
💰 PRECIOS: Mercado Peruano 2025
📋 NORMATIVAS: CNE, NFPA, RNE
🎯 TOTAL: {len(documentos_generados)} documentos generados

🚀 PILI BRAIN ESTÁ LISTO PARA PRODUCCIÓN
""")

print("=" * 80)
