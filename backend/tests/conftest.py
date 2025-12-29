"""
Fixtures para tests de Tesla Cotizador V3.0
"""
import pytest
from pathlib import Path
import tempfile
import shutil
from datetime import datetime


@pytest.fixture
def temp_output_dir():
    """Crea directorio temporal para archivos generados"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def datos_cotizacion_simple():
    """Datos de prueba para cotización simple"""
    return {
        "numero": "COT-TEST-001",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "cliente": "Cliente de Prueba S.A.C.",
        "proyecto": "Instalación Eléctrica Oficinas",
        "descripcion": "Proyecto de instalación eléctrica para oficinas administrativas",
        "items": [
            {
                "descripcion": "Tablero eléctrico trifásico 24 polos",
                "cantidad": 2,
                "unidad": "und",
                "precio_unitario": 1500.00
            },
            {
                "descripcion": "Cable NYY 3x10mm² (metro lineal)",
                "cantidad": 150,
                "unidad": "ml",
                "precio_unitario": 12.50
            },
            {
                "descripcion": "Interruptor termomagnético 3x63A",
                "cantidad": 4,
                "unidad": "und",
                "precio_unitario": 350.00
            },
            {
                "descripcion": "Tomacorriente doble 20A",
                "cantidad": 24,
                "unidad": "und",
                "precio_unitario": 45.00
            },
            {
                "descripcion": "Luminaria LED panel 60x60 48W",
                "cantidad": 36,
                "unidad": "und",
                "precio_unitario": 185.00
            }
        ],
        "subtotal": 12347.50,
        "igv": 2222.55,
        "total": 14570.05,
        "vigencia": "30 días",
        "observaciones": "Precios incluyen IGV. Válido por 30 días desde la fecha de emisión."
    }


@pytest.fixture
def datos_cotizacion_compleja():
    """Datos de prueba para cotización compleja"""
    datos = {
        "numero": "COT-TEST-002",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "cliente": "Industria Manufacturera S.A.",
        "proyecto": "Sistema Eléctrico Industrial Planta Norte",
        "descripcion": "Implementación de sistema eléctrico industrial completo",
        "items": [
            {
                "descripcion": "Subestación eléctrica 1000 KVA",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 85000.00
            },
            {
                "descripcion": "Tablero de distribución industrial",
                "cantidad": 3,
                "unidad": "und",
                "precio_unitario": 12500.00
            },
            {
                "descripcion": "Sistema de puesta a tierra (kit completo)",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 15000.00
            }
        ],
        "subtotal": 137500.00,
        "igv": 24750.00,
        "total": 162250.00,
        "vigencia": "45 días",
        "observaciones": "Proyecto de gran envergadura con garantía extendida",
        "analisis_riesgos": [
            "Riesgo climático: Temporada de lluvias puede retrasar instalación exterior",
            "Riesgo de suministro: Equipos especializados requieren importación (45 días)",
            "Riesgo operativo: Coordinación con operaciones de planta en funcionamiento"
        ],
        "cronograma_estimado": [
            {"fase": "Ingeniería de detalle", "duracion": "2 semanas"},
            {"fase": "Adquisición de equipos", "duracion": "6 semanas"},
            {"fase": "Instalación y montaje", "duracion": "4 semanas"},
            {"fase": "Pruebas y puesta en marcha", "duracion": "1 semana"}
        ]
    }
    return datos


@pytest.fixture
def datos_proyecto_simple():
    """Datos de prueba para proyecto simple"""
    return {
        "numero": "PROY-TEST-001",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "nombre": "Proyecto Domótica Residencial",
        "cliente": "Familia García Rodríguez",
        "descripcion": "Implementación de sistema domótico para vivienda unifamiliar",
        "objetivos": [
            "Automatizar control de iluminación en todas las áreas",
            "Integrar sistema de seguridad con cámaras IP",
            "Implementar control de climatización inteligente"
        ],
        "entregables": [
            "Sistema domótico instalado y configurado",
            "Manual de usuario en español",
            "Capacitación de 2 horas para los propietarios",
            "Garantía de 12 meses"
        ],
        "presupuesto": 18500.00
    }


@pytest.fixture
def datos_proyecto_complejo_pmi():
    """Datos de prueba para proyecto complejo PMI"""
    return {
        "numero": "PROY-TEST-002",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "nombre": "Proyecto Sistema Eléctrico Edificio Corporativo",
        "cliente": "Corporación Empresarial del Perú S.A.",
        "descripcion": "Diseño e implementación integral de sistema eléctrico para edificio corporativo de 15 pisos",
        "objetivos": [
            "Diseñar sistema eléctrico eficiente para edificio de 15 pisos",
            "Implementar subestación eléctrica de 2500 KVA",
            "Instalar sistema de respaldo con grupo electrógeno",
            "Certificar instalaciones con ITSE"
        ],
        "entregables": [
            "Ingeniería de detalle aprobada",
            "Sistema eléctrico completo instalado",
            "Certificado ITSE obtenido",
            "Manuales de operación y mantenimiento",
            "Personal capacitado"
        ],
        "presupuesto": 450000.00,
        "stakeholders": [
            {"nombre": "Gerente General", "rol": "Sponsor", "poder": "Alto", "interes": "Alto"},
            {"nombre": "Jefe de Mantenimiento", "rol": "Usuario Clave", "poder": "Medio", "interes": "Alto"},
            {"nombre": "Jefe de Compras", "rol": "Aprobador", "poder": "Alto", "interes": "Medio"}
        ],
        "kpis": {
            "SPI": 1.05,  # Schedule Performance Index
            "CPI": 0.98,  # Cost Performance Index
            "horas_hombre": 3200,
            "avance_fisico": 65.5
        },
        "matriz_raci": [
            {"actividad": "Diseño", "pm": "A", "ing": "R", "tec": "C", "cliente": "I"},
            {"actividad": "Adquisiciones", "pm": "R", "ing": "C", "tec": "I", "cliente": "A"},
            {"actividad": "Instalación", "pm": "A", "ing": "C", "tec": "R", "cliente": "I"},
            {"actividad": "Pruebas", "pm": "R", "ing": "R", "tec": "C", "cliente": "A"}
        ],
        "plan_comunicaciones": {
            "reportes_semanales": "Todos los lunes 10:00 AM",
            "reuniones_comite": "Quincenal - Viernes 3:00 PM",
            "canal_emergencias": "WhatsApp 24/7"
        }
    }


@pytest.fixture
def datos_informe_tecnico():
    """Datos de prueba para informe técnico"""
    return {
        "numero": "INF-TEST-001",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "titulo": "Informe Técnico de Puesta a Tierra",
        "autor": "Ing. Carlos Mendoza - Tesla Electricidad",
        "cliente": "Industrial Textil del Norte S.A.C.",
        "resumen": "Informe de medición de sistema de puesta a tierra en planta industrial",
        "introduccion": "El presente informe documenta las mediciones realizadas al sistema de puesta a tierra de la planta industrial, conforme a la normativa vigente CNE.",
        "metodologia": "Se utilizó el método de caída de potencial con telurómetro digital FLUKE 1625-2, realizando mediciones en 12 puntos críticos de la instalación.",
        "resultados": [
            "Resistencia promedio del sistema: 4.8 Ω (dentro de rango aceptable < 5Ω)",
            "Punto crítico 1 (Subestación): 3.2 Ω - CONFORME",
            "Punto crítico 2 (Tablero Principal): 4.5 Ω - CONFORME",
            "Punto crítico 3 (Área de Máquinas): 5.8 Ω - NO CONFORME"
        ],
        "conclusiones": [
            "El sistema de puesta a tierra se encuentra en condiciones operativas aceptables",
            "Se requiere mejora en el área de máquinas (Punto 3) para cumplir normativa",
            "Se recomienda instalación de 2 electrodos adicionales en zona deficiente"
        ],
        "recomendaciones": [
            "Instalar 2 varillas de cobre de 2.4m en paralelo en área de máquinas",
            "Realizar nueva medición de verificación en 30 días",
            "Programar mantenimiento preventivo semestral del sistema de puesta a tierra"
        ]
    }


@pytest.fixture
def datos_informe_ejecutivo_apa():
    """Datos de prueba para informe ejecutivo APA"""
    return {
        "numero": "INF-TEST-002",
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "titulo": "Análisis de Viabilidad: Implementación de Sistema Solar Fotovoltaico",
        "autor": "Tesla Electricidad y Automatización S.A.C.",
        "cliente": "Grupo Hotelero Costa Verde",
        "formato": "APA 7ma edición",
        "abstract": "Este informe ejecutivo evalúa la viabilidad técnica y económica de implementar un sistema solar fotovoltaico de 100 kWp en el complejo hotelero. El análisis demuestra un retorno de inversión favorable con un payback de 4.2 años.",
        "resumen": "Análisis completo de viabilidad técnica, económica y ambiental para implementación de energía solar",
        "introduccion": "El sector hotelero enfrenta costos energéticos crecientes. La energía solar fotovoltaica representa una oportunidad de reducción de costos operativos y mejora de imagen corporativa sustentable.",
        "metodologia": "Análisis mediante software PVsyst 7.2, revisión de facturación eléctrica de 12 meses, visita técnica in situ, evaluación financiera con VAN y TIR.",
        "resultados": [
            "Consumo promedio actual: 18,500 kWh/mes",
            "Generación estimada sistema 100kWp: 13,200 kWh/mes (71% del consumo)",
            "Inversión total: S/ 285,000",
            "Ahorro mensual estimado: S/ 5,850"
        ],
        "conclusiones": [
            "El proyecto es técnicamente viable con área de techo suficiente (850 m²)",
            "Económicamente atractivo con TIR de 24% y VAN positivo",
            "Reducción de emisiones CO2: 95 toneladas/año"
        ],
        "recomendaciones": [
            "Proceder con ingeniería de detalle para optimización del diseño",
            "Evaluar financiamiento con entidades bancarias especializadas",
            "Iniciar trámites de conexión a red con distribuidora eléctrica"
        ],
        "referencias": [
            "Código Nacional de Electricidad - Suministro 2011",
            "Norma Técnica DGE (2006). Procedimientos para la conexión de sistemas fotovoltaicos a la red",
            "MINEM (2023). Atlas Solar del Perú"
        ],
        "metricas_clave": {
            "roi_estimado": 25.8,
            "payback_meses": 50,
            "tir_proyectada": 24.3,
            "reduccion_costos_operativos": 71.2
        }
    }


@pytest.fixture
def opciones_generacion_defecto():
    """Opciones por defecto para generación de documentos"""
    return {
        "mostrarPreciosUnitarios": True,
        "mostrarPreciosTotales": True,
        "mostrarIGV": True,
        "incluirLogo": False,  # Sin logo para tests
        "esquema_colores": "tesla_azul"
    }
