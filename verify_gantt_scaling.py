
import sys
import os
import io

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project root to path
sys.path.append(os.getcwd())

try:
    from Pili_ChatBot.pili_electricidad_proyecto_complejo_pmi_chatbot import PILIElectricidadProyectoComplejoPMIChatBot
except ImportError as e:
    print(f"Error importing Chatbot: {e}")
    sys.exit(1)

def verify_gantt_scaling():
    print("Iniciando Verificacion de Escalamiento Gantt (Acceso Directo)...")
    
    bot = PILIElectricidadProyectoComplejoPMIChatBot()
    
    # Caso de prueba: Usuario pide 120 dias, Complejidad 6
    target_duration = 120
    complexity = 6
    
    estado_simulado = {
        "etapa": "final", # Irrelevante si llamamos directo
        "complejidad": complexity,
        "duracion_dias": target_duration, # Prioridad 1
        "duracion_total": 999, # deberia ser ignorado
        "cliente_nombre": "Test Client",
        "nombre_proyecto": "Test Project",
        # NO INCLUIMOS cronograma_fases para forzar el fallback
    }
    
    print(f"Objetivo: Duracion Total = {target_duration} dias (Complejidad {complexity})")
    
    try:
        # Llamamos DIRECTAMENTE al metodo interno de generacion
        # Esto testea la logica que modificamos sin depender del flujo del chat
        resultado = bot._generar_proyecto(estado_simulado)
        
        datos = resultado.get('datos_generados', {})
        cronograma = datos.get('cronograma_fases', [])
        
        print(f"Fases generadas: {len(cronograma)}")
        
        total_dias_generados = 0
        for fase in cronograma:
            # fase['dias'] viene como "X días"
            dias_str = fase['dias'].split(' ')[0]
            dias = int(dias_str)
            total_dias_generados += dias
            print(f"  - {fase['label']}: {dias} dias ({fase['width']})")
            
        print(f"\nTotal Dias Generados: {total_dias_generados}")
        print(f"Total Dias Objetivo: {target_duration}")
        
        if total_dias_generados == target_duration:
            print("EXITO: El cronograma coincide EXACTAMENTE con la duracion del usuario.")
        elif abs(total_dias_generados - target_duration) <= 1:
            print("EXITO PARCIAL: Diferencia de 1 dia por redondeo (Aceptable).")
        else:
            print(f"FALLO: Diferencia significativa ({total_dias_generados - target_duration} dias).")
            
    except Exception as e:
        print(f"Error ejecutando prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_gantt_scaling()
