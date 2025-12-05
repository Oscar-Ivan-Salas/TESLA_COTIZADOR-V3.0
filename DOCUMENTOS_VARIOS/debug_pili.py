import sys
import os

# Agregar path para importar app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.services.pili_brain import PILIBrain

def test_pili():
    brain = PILIBrain()
    mensaje = "Hola, quiero una cotización" # Mensaje sin números
    
    print(f"Probando mensaje: '{mensaje}'")
    
    try:
        servicio = brain.detectar_servicio(mensaje)
        print(f"Servicio detectado: {servicio}")
        
        cotizacion = brain.generar_cotizacion(mensaje, servicio, "simple")
        print("Cotización generada exitosamente")
        print(cotizacion)
        
    except Exception as e:
        print(f"❌ ERROR CAPTURADO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pili()
