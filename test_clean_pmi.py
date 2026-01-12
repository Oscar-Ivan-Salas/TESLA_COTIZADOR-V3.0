
import sys
import os
import json
# Aseguramos que podemos importar modulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Pili_ChatBot.pili_electricidad_proyecto_complejo_pmi_chatbot import PILIElectricidadProyectoComplejoPMIChatBot

def run_test():
    print("🚀 INICIANDO TEST LIMPIO: CHATBOT PMI COMPLEJO")
    
    bot = PILIElectricidadProyectoComplejoPMIChatBot()
    estado = {}
    
    # 1. Simular Estado Inicial (Pasado desde Frontend)
    print("\n--- PASO 1: ESTADO INICIAL ---")
    estado = {
        "etapa": "inicial",
        "nombre_proyecto": "Test Clean PMI",
        "presupuesto": 100000,
        "complejidad": 7
    }
    
    res = bot.procesar("", estado)
    print(f"Respuesta 1 (Bienvenida/Ubicacion): Success={res['success']}, Etapa={res['estado'].get('etapa')}")
    estado = res['estado']

    # 2. Ubicacion
    print("\n--- PASO 2: UBICACION ---")
    res = bot.procesar("Lima, Peru", estado.copy())
    estado = res['estado']
    print(f"Respuesta 2: Etapa={estado.get('etapa')}")

    # 3. Area (si aplica)
    if estado.get('etapa') == 'area':
        print("\n--- PASO 3: AREA ---")
        res = bot.procesar("5000", estado.copy())
        estado = res['estado']
        print(f"Respuesta 3: Etapa={estado.get('etapa')}")

    # 4. Descripción
    if estado.get('etapa') == 'descripcion':
        print("\n--- PASO 4: DESCRIPCION ---")
        res = bot.procesar("Instalación eléctrica industrial completa.", estado.copy())
        estado = res['estado']
        print(f"Respuesta 4: Etapa={estado.get('etapa')}")

    # 5. Descripción Adicional
    if estado.get('etapa') == 'descripcion_adicional':
         print("\n--- PASO 5: DESC ADICIONAL ---")
         res = bot.procesar("NO_AGREGAR", estado.copy())
         estado = res['estado']
         print(f"Respuesta 5: Etapa={estado.get('etapa')}")
    
    # 6. Normativa
    if estado.get('etapa') == 'normativa':
        print("\n--- PASO 6: NORMATIVA ---")
        res = bot.procesar("CNE Suministro 2011", estado.copy())
        estado = res['estado']
        print(f"Respuesta 6: Etapa={estado.get('etapa')}")

    # 7. Fecha Inicio
    if estado.get('etapa') == 'fecha_inicio':
        print("\n--- PASO 7: FECHA INICIO ---")
        res = bot.procesar("01/02/2026", estado.copy())
        estado = res['estado']
        print(f"Respuesta 7: Etapa={estado.get('etapa')}")

    # 8. KPIs (SPI)
    if estado.get('etapa') == 'kpi_spi':
        print("\n--- PASO 8: KPI SPI ---")
        res = bot.procesar("1.0", estado.copy())
        estado = res['estado']
        print(f"Respuesta 8: Etapa={estado.get('etapa')}")

    # 9. KPIs (CPI)
    if estado.get('etapa') == 'kpi_cpi':
        print("\n--- PASO 9: KPI CPI ---")
        res = bot.procesar("1.0", estado.copy())
        estado = res['estado']
        print(f"Respuesta 9: Etapa={estado.get('etapa')}")

    # 10. KPIs (EV)
    if estado.get('etapa') == 'kpi_ev':
        print("\n--- PASO 10: KPI EV ---")
        res = bot.procesar("70", estado.copy())
        estado = res['estado']
        print(f"Respuesta 10: Etapa={estado.get('etapa')}")

    # 11. KPIs (PV)
    if estado.get('etapa') == 'kpi_pv':
        print("\n--- PASO 11: KPI PV ---")
        res = bot.procesar("75", estado.copy())
        estado = res['estado']
        print(f"Respuesta 11: Etapa={estado.get('etapa')}")

    # 12. KPIs (AC) -> AQUÍ ESTÁ EL PUNTO CRÍTICO
    if estado.get('etapa') == 'kpi_ac':
        print("\n--- PASO 12: KPI AC (PUNTO CRÍTICO) ---")
        res = bot.procesar("65", estado.copy())
        estado = res['estado']
        print(f"Respuesta 12: Etapa={estado.get('etapa')}")
        print(f"Formulario recibido: {res.get('formulario')}")
        if res.get('formulario', {}).get('tipo') == 'gantt_dias':
            print("✅ TEST EXITOSO: El backend respondió correctamente con el formulario Gantt.")
        else:
            print("❌ ERROR: No se recibió el formulario Gantt esperado.")

    # 13. Procesar Gantt (Simulación de envío de formulario)
    if estado.get('etapa') == 'procesar_gantt':
        print("\n--- PASO 13: PROCESAR GANTT ---")
        json_gantt = {
            "fases": [{"nombre": "Inicio", "duracion": 10}],
            "total": 100,
            "configuracionCalendario": {"diasLaborables": {"lun": True}, "horasPorDia": 8}
        }
        mensaje_gantt = f"GANTT_DATA_JSON:{json.dumps(json_gantt)}"
        res = bot.procesar(mensaje_gantt, estado.copy())
        estado = res['estado']
        print(f"Respuesta 13: Etapa={estado.get('etapa')}")
        if estado.get('etapa') == 'riesgo1_desc':
            print("✅ TEST COMPLETADO: Transición a Riesgos exitosa.")
        else:
            print("❌ ERROR: Fallo en transición post-Gantt.")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN DETECTADA: {e}")
        import traceback
        traceback.print_exc()
