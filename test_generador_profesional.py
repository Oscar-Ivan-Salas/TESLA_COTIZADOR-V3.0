"""
Test script para verificar generador profesional
"""
import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

from app.services.generators.cotizacion_simple_generator import generar_cotizacion_simple
from pathlib import Path

# Datos de prueba
datos_prueba = {
    'tipo_documento': 'cotizacion-simple',
    'numero': 'COT-TEST-001',
    'fecha': '21/12/2025',
    'vigencia': '30 días',
    'cliente': {
        'nombre': 'Rogelio Infantas Contreras',
        'ruc': '10204438189',
        'direccion': 'Concepción',
        'telefono': '906315971',
        'email': 'rogelio.infantas@gmail.com'
    },
    'proyecto': 'Instalación Eléctrica',
    'area_m2': 100,
    'servicio': 'Instalaciones Eléctricas',
    'items': [
        {
            'descripcion': 'Punto de luz LED 18W',
            'cantidad': 8,
            'unidad': 'pto',
            'precio_unitario': 30
        },
        {
            'descripcion': 'Tomacorriente doble',
            'cantidad': 6,
            'unidad': 'pto',
            'precio_unitario': 35
        },
        {
            'descripcion': 'Cable THW 2.5mm²',
            'cantidad': 50,
            'unidad': 'm',
            'precio_unitario': 4
        }
    ]
}

opciones = {
    'esquema_colores': 'azul-tesla',
    'fuente': 'Calibri',
    'tamaño_fuente': 11,
    'mostrar_logo': True
}

output_path = Path('e:/TESLA_COTIZADOR-V3.0/storage/generados/TEST_PROFESIONAL.docx')

try:
    print("🔍 Iniciando generación profesional...")
    resultado = generar_cotizacion_simple(datos_prueba, output_path, opciones)
    print(f"✅ Documento generado exitosamente: {resultado}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
