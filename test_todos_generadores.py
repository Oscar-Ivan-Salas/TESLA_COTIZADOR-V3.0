"""
Script de Testing Completo - 6 Generadores Profesionales
Genera documentos de prueba para todos los tipos
"""

import sys
sys.path.insert(0, 'e:/TESLA_COTIZADOR-V3.0/backend')

from app.services.generators import generar_documento
from pathlib import Path
from datetime import datetime

# Directorio de salida
output_dir = Path('e:/TESLA_COTIZADOR-V3.0/storage/generados')
output_dir.mkdir(parents=True, exist_ok=True)

# Opciones comunes
opciones = {
    'esquema_colores': 'azul-tesla',
    'fuente': 'Calibri',
    'tamano_fuente': 11,
    'mostrar_logo': True
}

print("=" * 80)
print("🧪 TESTING DE 6 GENERADORES PROFESIONALES")
print("=" * 80)
print()

# ============================================================================
# 1. COTIZACIÓN SIMPLE
# ============================================================================
print("1️⃣  Generando Cotización Simple...")
try:
    datos_cot_simple = {
        'tipo_documento': 'cotizacion-simple',
        'numero': 'COT-SIMPLE-TEST-001',
        'fecha': '22/12/2025',
        'vigencia': '30 días',
        'cliente': {
            'nombre': 'Empresa Constructora ABC S.A.C.',
            'ruc': '20123456789',
            'direccion': 'Av. Principal 123, Lima',
            'telefono': '987654321',
            'email': 'contacto@empresaabc.com'
        },
        'proyecto': 'Instalación Eléctrica Edificio Corporativo',
        'area_m2': 500,
        'servicio': 'Instalaciones Eléctricas Completas',
        'items': [
            {
                'descripcion': 'Punto de luz LED 18W empotrado',
                'cantidad': 50,
                'precio_unitario': 35.00,
                'unidad': 'pto'
            },
            {
                'descripcion': 'Tomacorriente doble con línea a tierra',
                'cantidad': 30,
                'precio_unitario': 42.00,
                'unidad': 'pto'
            },
            {
                'descripcion': 'Cable THW 2.5mm² (rollo 100m)',
                'cantidad': 10,
                'precio_unitario': 180.00,
                'unidad': 'rollo'
            },
            {
                'descripcion': 'Interruptor termomagnético 2x20A',
                'cantidad': 8,
                'precio_unitario': 65.00,
                'unidad': 'und'
            },
            {
                'descripcion': 'Tablero eléctrico 12 polos',
                'cantidad': 2,
                'precio_unitario': 450.00,
                'unidad': 'und'
            }
        ],
        'observaciones': 'Precios incluyen IGV. Validez de la oferta: 30 días. Tiempo de entrega: 15 días hábiles.'
    }
    
    ruta = output_dir / 'TEST_Cotizacion_Simple.docx'
    generar_documento('cotizacion-simple', datos_cot_simple, ruta, opciones)
    print(f"   ✅ Generado: {ruta.name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# 2. COTIZACIÓN COMPLEJA
# ============================================================================
print("\n2️⃣  Generando Cotización Compleja...")
try:
    datos_cot_compleja = {
        'tipo_documento': 'cotizacion-compleja',
        'numero': 'COT-COMPLEJA-TEST-001',
        'fecha': '22/12/2025',
        'vigencia': '45 días',
        'cliente': {
            'nombre': 'Inmobiliaria XYZ S.A.',
            'ruc': '20987654321'
        },
        'proyecto': 'Proyecto Residencial Los Pinos',
        'area_m2': 1200,
        'servicio': 'Instalaciones Eléctricas y Automatización',
        'capitulos': [
            {
                'nombre': 'INSTALACIONES ELÉCTRICAS',
                'items': [
                    {'descripcion': 'Punto de luz LED', 'cantidad': 80, 'precio_unitario': 35.00, 'unidad': 'pto'},
                    {'descripcion': 'Tomacorriente doble', 'cantidad': 60, 'precio_unitario': 42.00, 'unidad': 'pto'},
                    {'descripcion': 'Cable THW 2.5mm²', 'cantidad': 20, 'precio_unitario': 180.00, 'unidad': 'rollo'}
                ]
            },
            {
                'nombre': 'SISTEMA DE AUTOMATIZACIÓN',
                'items': [
                    {'descripcion': 'Control inteligente de iluminación', 'cantidad': 15, 'precio_unitario': 250.00, 'unidad': 'und'},
                    {'descripcion': 'Sensor de movimiento', 'cantidad': 10, 'precio_unitario': 120.00, 'unidad': 'und'},
                    {'descripcion': 'Panel de control central', 'cantidad': 1, 'precio_unitario': 1500.00, 'unidad': 'und'}
                ]
            },
            {
                'nombre': 'TABLEROS Y PROTECCIONES',
                'items': [
                    {'descripcion': 'Tablero general 24 polos', 'cantidad': 1, 'precio_unitario': 850.00, 'unidad': 'und'},
                    {'descripcion': 'Tablero de distribución 12 polos', 'cantidad': 3, 'precio_unitario': 450.00, 'unidad': 'und'},
                    {'descripcion': 'Interruptor diferencial 2x40A', 'cantidad': 4, 'precio_unitario': 180.00, 'unidad': 'und'}
                ]
            }
        ],
        'observaciones': 'Precios incluyen IGV. Incluye materiales y mano de obra. Garantía: 12 meses.'
    }
    
    ruta = output_dir / 'TEST_Cotizacion_Compleja.docx'
    generar_documento('cotizacion-compleja', datos_cot_compleja, ruta, opciones)
    print(f"   ✅ Generado: {ruta.name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# 3. PROYECTO SIMPLE
# ============================================================================
print("\n3️⃣  Generando Proyecto Simple...")
try:
    datos_proyecto_simple = {
        'tipo_documento': 'proyecto-simple',
        'nombre_proyecto': 'Modernización Sistema Eléctrico Planta Industrial',
        'resumen': 'Proyecto de modernización integral del sistema eléctrico de planta industrial, incluyendo actualización de tableros, cableado y sistema de iluminación LED. El proyecto busca mejorar la eficiencia energética y cumplir con normativas vigentes.',
        'fases': [
            {
                'descripcion': 'Diagnóstico y planificación inicial',
                'duracion': '1 semana',
                'responsable': 'Ing. Juan Pérez'
            },
            {
                'descripcion': 'Adquisición de materiales y equipos',
                'duracion': '2 semanas',
                'responsable': 'Área de Logística'
            },
            {
                'descripcion': 'Instalación de nuevos tableros eléctricos',
                'duracion': '3 semanas',
                'responsable': 'Equipo Técnico A'
            },
            {
                'descripcion': 'Renovación de cableado y puntos de luz',
                'duracion': '4 semanas',
                'responsable': 'Equipo Técnico B'
            },
            {
                'descripcion': 'Pruebas y puesta en marcha',
                'duracion': '1 semana',
                'responsable': 'Ing. María García'
            }
        ],
        'cronograma': {
            'fecha_inicio': '15/01/2025',
            'fecha_fin': '15/04/2025',
            'duracion_total': '3 meses'
        },
        'recursos': {
            'humanos': [
                'Ingeniero Eléctrico Senior (1)',
                'Técnicos Electricistas (4)',
                'Supervisor de Seguridad (1)',
                'Coordinador de Proyecto (1)'
            ],
            'materiales': [
                'Tableros eléctricos industriales',
                'Cable THW calibre 10 y 12',
                'Luminarias LED industriales',
                'Interruptores termomagnéticos',
                'Equipos de protección personal'
            ]
        }
    }
    
    ruta = output_dir / 'TEST_Proyecto_Simple.docx'
    generar_documento('proyecto-simple', datos_proyecto_simple, ruta, opciones)
    print(f"   ✅ Generado: {ruta.name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# 4. PROYECTO COMPLEJO (PMI)
# ============================================================================
print("\n4️⃣  Generando Proyecto Complejo (PMI)...")
try:
    datos_proyecto_pmi = {
        'tipo_documento': 'proyecto-complejo',
        'nombre_proyecto': 'Implementación Sistema SCADA Planta Eléctrica',
        'metricas_pmi': {
            'cpi': '1.05',
            'spi': '0.98',
            'eac': 'S/ 250,000.00',
            'etc': 'S/ 50,000.00',
            'vac': 'S/ 12,500.00'
        },
        'riesgos': [
            {
                'descripcion': 'Retraso en entrega de equipos importados',
                'probabilidad': 'Media',
                'impacto': 'Alto',
                'mitigacion': 'Compra anticipada con proveedores locales como backup'
            },
            {
                'descripcion': 'Incompatibilidad de software con sistemas legacy',
                'probabilidad': 'Baja',
                'impacto': 'Muy Alto',
                'mitigacion': 'Pruebas de integración en ambiente de desarrollo'
            },
            {
                'descripcion': 'Falta de personal capacitado',
                'probabilidad': 'Media',
                'impacto': 'Medio',
                'mitigacion': 'Programa de capacitación intensiva pre-proyecto'
            },
            {
                'descripcion': 'Cambios en normativa durante ejecución',
                'probabilidad': 'Baja',
                'impacto': 'Medio',
                'mitigacion': 'Monitoreo continuo de cambios regulatorios'
            }
        ],
        'plan_calidad': {
            'objetivos': [
                'Cumplimiento de norma ISO 9001:2015',
                'Disponibilidad del sistema ≥ 99.5%',
                'Tiempo de respuesta < 2 segundos',
                'Cero defectos críticos en producción'
            ],
            'metricas': [
                'Tasa de defectos < 1% en pruebas',
                'Cobertura de pruebas ≥ 95%',
                'Satisfacción del cliente ≥ 4.5/5',
                'Cumplimiento de cronograma ≥ 90%'
            ]
        }
    }
    
    ruta = output_dir / 'TEST_Proyecto_Complejo_PMI.docx'
    generar_documento('proyecto-complejo', datos_proyecto_pmi, ruta, opciones)
    print(f"   ✅ Generado: {ruta.name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# 5. INFORME TÉCNICO
# ============================================================================
print("\n5️⃣  Generando Informe Técnico...")
try:
    datos_informe_tecnico = {
        'tipo_documento': 'informe-tecnico',
        'titulo': 'Análisis de Eficiencia Energética - Edificio Corporativo',
        'resumen_ejecutivo': 'El presente informe técnico presenta los resultados del análisis de eficiencia energética realizado en el edificio corporativo ubicado en Av. Principal 456, Lima. Se identificaron oportunidades de ahorro energético del 35% mediante la implementación de tecnologías LED, sistemas de automatización y optimización de cargas eléctricas.',
        'introduccion': 'El consumo energético representa uno de los costos operativos más significativos en edificaciones corporativas. Este estudio fue realizado durante el período de noviembre-diciembre 2025, con el objetivo de identificar oportunidades de mejora en la eficiencia energética del edificio.',
        'analisis_tecnico': {
            'secciones': [
                {
                    'titulo': 'Análisis de Consumo Actual',
                    'contenido': 'El edificio presenta un consumo promedio mensual de 45,000 kWh, con picos de demanda de 180 kW. El sistema de iluminación representa el 40% del consumo total, seguido por climatización (35%) y equipos de oficina (25%).',
                    'hallazgos': [
                        'Sistema de iluminación obsoleto (fluorescentes T8)',
                        'Ausencia de control automático de iluminación',
                        'Factor de potencia bajo (0.75)',
                        'Equipos de climatización sin mantenimiento preventivo'
                    ]
                },
                {
                    'titulo': 'Oportunidades de Mejora',
                    'contenido': 'Se identificaron cuatro áreas principales de mejora que permitirían reducir el consumo energético significativamente.',
                    'hallazgos': [
                        'Reemplazo de luminarias por tecnología LED (ahorro 60%)',
                        'Implementación de sensores de presencia (ahorro 25%)',
                        'Corrección de factor de potencia (ahorro 8%)',
                        'Optimización de horarios de climatización (ahorro 15%)'
                    ]
                },
                {
                    'titulo': 'Análisis Económico',
                    'contenido': 'La inversión total estimada es de S/ 85,000 con un período de retorno de 2.3 años. El ahorro anual proyectado es de S/ 37,000.',
                    'hallazgos': [
                        'ROI: 43.5% anual',
                        'Período de retorno: 2.3 años',
                        'VAN (5 años): S/ 98,500',
                        'TIR: 38.2%'
                    ]
                }
            ]
        },
        'conclusiones': [
            'El edificio presenta un alto potencial de ahorro energético (35%)',
            'La inversión en tecnología LED es altamente rentable',
            'Se recomienda implementar el proyecto en fases',
            'El período de retorno es atractivo (2.3 años)'
        ],
        'recomendaciones': [
            'Iniciar con reemplazo de iluminación LED (Fase 1)',
            'Implementar sistema de control automático (Fase 2)',
            'Realizar corrección de factor de potencia (Fase 3)',
            'Establecer programa de mantenimiento preventivo',
            'Capacitar al personal en uso eficiente de energía'
        ],
        'anexos': [
            {
                'titulo': 'Mediciones de Consumo Eléctrico',
                'descripcion': 'Gráficos y tablas de mediciones realizadas durante 30 días'
            },
            {
                'titulo': 'Especificaciones Técnicas de Equipos',
                'descripcion': 'Fichas técnicas de luminarias LED y sensores propuestos'
            },
            {
                'titulo': 'Análisis Financiero Detallado',
                'descripcion': 'Flujo de caja proyectado a 5 años'
            }
        ]
    }
    
    ruta = output_dir / 'TEST_Informe_Tecnico.docx'
    generar_documento('informe-tecnico', datos_informe_tecnico, ruta, opciones)
    print(f"   ✅ Generado: {ruta.name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# 6. INFORME EJECUTIVO (APA)
# ============================================================================
print("\n6️⃣  Generando Informe Ejecutivo (APA)...")
try:
    datos_informe_apa = {
        'tipo_documento': 'informe-ejecutivo',
        'titulo': 'IMPACTO DE LA AUTOMATIZACIÓN EN LA EFICIENCIA OPERATIVA DE SISTEMAS ELÉCTRICOS INDUSTRIALES',
        'autor': 'Ing. Carlos Rodríguez Mendoza',
        'institucion': 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.',
        'fecha': 'Diciembre 2025',
        'resumen': 'Este estudio analiza el impacto de la implementación de sistemas de automatización en la eficiencia operativa de instalaciones eléctricas industriales. Se realizó un análisis comparativo de 15 plantas industriales durante un período de 12 meses, evaluando indicadores de eficiencia energética, tiempo de inactividad y costos operativos. Los resultados demuestran que la automatización genera mejoras significativas en todos los indicadores evaluados, con un incremento promedio de 28% en eficiencia energética y reducción de 45% en tiempos de inactividad no planificados.',
        'palabras_clave': ['automatización industrial', 'eficiencia energética', 'sistemas SCADA', 'mantenimiento predictivo', 'optimización de procesos'],
        'introduccion': 'La automatización de sistemas eléctricos industriales ha experimentado un crecimiento exponencial en la última década, impulsada por avances tecnológicos en sensores, comunicaciones y análisis de datos. Este estudio busca cuantificar el impacto real de estas tecnologías en la eficiencia operativa de plantas industriales del sector manufacturero.',
        'metodologia': 'Se seleccionaron 15 plantas industriales del sector manufacturero con capacidades instaladas entre 500 kW y 2 MW. El estudio se realizó mediante un diseño cuasi-experimental con mediciones pre y post implementación de sistemas de automatización. Se recopilaron datos de consumo energético, tiempos de inactividad, costos de mantenimiento y producción durante 6 meses antes y 6 meses después de la implementación.',
        'resultados': {
            'secciones': [
                {
                    'titulo': 'Eficiencia Energética',
                    'contenido': 'Se observó un incremento promedio de 28% en eficiencia energética (SD = 5.2%), con valores que oscilaron entre 18% y 35% dependiendo del sector industrial. Las plantas del sector alimentario mostraron las mayores mejoras (32% promedio).'
                },
                {
                    'titulo': 'Reducción de Tiempos de Inactividad',
                    'contenido': 'Los tiempos de inactividad no planificados se redujeron en promedio 45% (SD = 8.1%). El mantenimiento predictivo habilitado por la automatización permitió anticipar el 78% de las fallas potenciales.'
                },
                {
                    'titulo': 'Impacto Económico',
                    'contenido': 'El retorno de inversión promedio fue de 2.1 años (SD = 0.6 años). Los ahorros anuales promedio alcanzaron el 22% de los costos operativos eléctricos previos a la implementación.'
                }
            ]
        },
        'discusion': 'Los resultados confirman que la automatización de sistemas eléctricos industriales genera beneficios significativos y cuantificables. La variabilidad observada entre sectores sugiere que factores como el tipo de proceso productivo y la antigüedad de las instalaciones influyen en la magnitud de las mejoras. Es notable que el mantenimiento predictivo emerge como uno de los beneficios más valorados por los operadores, más allá de los ahorros energéticos directos.',
        'conclusiones': [
            'La automatización de sistemas eléctricos industriales genera mejoras significativas en eficiencia operativa',
            'El retorno de inversión promedio de 2.1 años es atractivo para la mayoría de industrias',
            'El mantenimiento predictivo representa un beneficio adicional importante',
            'Los resultados varían según el sector industrial y antigüedad de instalaciones',
            'Se recomienda un enfoque gradual de implementación para maximizar beneficios'
        ],
        'referencias': [
            'García, M., & López, J. (2024). Automatización industrial: Tendencias y aplicaciones. Editorial Técnica.',
            'Rodríguez, C. (2023). Eficiencia energética en sistemas industriales. Revista de Ingeniería Eléctrica, 15(2), 45-62.',
            'Smith, J., & Johnson, R. (2024). Industrial automation and energy efficiency: A comprehensive review. Journal of Industrial Engineering, 28(4), 112-135.',
            'Torres, A., Mendoza, L., & Vargas, P. (2023). SCADA systems implementation in manufacturing plants. International Conference on Industrial Automation, 234-248.',
            'World Energy Council. (2024). Energy efficiency in industrial sector: Global report. WEC Publications.'
        ]
    }
    
    ruta = output_dir / 'TEST_Informe_Ejecutivo_APA.docx'
    generar_documento('informe-ejecutivo', datos_informe_apa, ruta, opciones)
    print(f"   ✅ Generado: {ruta.name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 80)
print("✅ TESTING COMPLETADO")
print("=" * 80)
print(f"\n📁 Documentos generados en: {output_dir}")
print("\n📊 Resumen:")
print("   1. Cotización Simple")
print("   2. Cotización Compleja")
print("   3. Proyecto Simple")
print("   4. Proyecto Complejo (PMI)")
print("   5. Informe Técnico")
print("   6. Informe Ejecutivo (APA)")
print("\n🎯 Próximo paso: Convertir a PDF (requiere LibreOffice)")
print("=" * 80)
