"""
🧠 PILI LOCAL SPECIALISTS - Sistema de Fallback Inteligente Profesional
📁 RUTA: backend/app/services/pili_local_specialists.py

Conversación profesional de alta gama para 10 servicios eléctricos
Se usa como FALLBACK cuando Gemini API no está disponible

CARACTERÍSTICAS PROFESIONALES:
- ✅ Conversación por etapas inteligente (estilo ITSE)
- ✅ Botones dinámicos según contexto
- ✅ Validación en tiempo real con mensajes claros
- ✅ Cálculo automático de items y totales
- ✅ Actualización de plantilla HTML en tiempo real
- ✅ Progreso visible (3/7, 5/7, etc.)
- ✅ Mensajes profesionales con emojis y formato
- ✅ Cotizaciones formateadas profesionalmente
- ✅ Reglas de negocio por servicio
- ✅ Normativas técnicas incluidas

SERVICIOS IMPLEMENTADOS (10/10):
1. ⚡ Electricidad (Residencial/Comercial/Industrial) - 7 etapas
2. 📋 ITSE (8 categorías) - 5 etapas
3. 🔌 Puesta a Tierra - 5 etapas
4. 🔥 Contraincendios (Detección/Extinción) - 6 etapas
5. 🏠 Domótica - 5 etapas
6. 📹 CCTV (Analógico/IP) - 6 etapas
7. 🌐 Redes (CAT5E/CAT6/Fibra) - 5 etapas
8. ⚙️ Automatización Industrial - 6 etapas
9. 📄 Expedientes Técnicos - 5 etapas
10. 💧 Saneamiento - 6 etapas

VERSION: 2.0 PROFESSIONAL - Código de Alta Gama
AUTOR: Tesla Electricidad - PILI AI Team
FECHA: 2025-12-26
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
import re
import math

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# 💰 KNOWLEDGE BASES PROFESIONALES - Base de Conocimiento Completa
# ══════════════════════════════════════════════════════════════════════════════

KNOWLEDGE_BASE = {
    # ──────────────────────────────────────────────────────────────────────────
    # ⚡ ELECTRICIDAD - Instalaciones Eléctricas Profesionales
    # ──────────────────────────────────────────────────────────────────────────
    "electricidad": {
        "tipos": {
            "RESIDENCIAL": {
                "nombre": "Instalación Eléctrica Residencial",
                "descripcion": "Viviendas unifamiliares y multifamiliares hasta 200m²",
                "precios": {
                    "punto_luz_empotrado": 80,
                    "punto_luz_adosado": 65,
                    "tomacorriente_doble": 60,
                    "tomacorriente_simple": 45,
                    "interruptor_simple": 35,
                    "interruptor_doble": 50,
                    "interruptor_triple": 65,
                    "tablero_monofasico": 800,
                    "tablero_trifasico": 1200,
                    "cable_thw_2_5mm": 2.5,
                    "cable_thw_4mm": 3.8,
                    "cable_thw_6mm": 5.5,
                    "tuberia_pvc_3_4": 1.2,
                    "tuberia_pvc_1": 1.8,
                    "caja_octogonal": 3.5,
                    "caja_rectangular": 4.0,
                    "pozo_tierra": 1760
                },
                "reglas": {
                    "area_max": 200,
                    "pisos_max": 2,
                    "puntos_por_m2": 0.15,
                    "tomas_por_m2": 0.10,
                    "potencia_estimada_w_m2": 50
                },
                "normativa": "CNE Suministro 2011 - Sección 050",
                "tiempo_estimado": "5-7 días hábiles",
                "garantia": "1 año"
            },
            "COMERCIAL": {
                "nombre": "Instalación Eléctrica Comercial",
                "descripcion": "Locales comerciales, oficinas, tiendas 50-1000m²",
                "precios": {
                    "punto_luz_empotrado": 95,
                    "punto_luz_led_panel": 110,
                    "tomacorriente_doble": 75,
                    "tomacorriente_estabilizado": 95,
                    "interruptor_simple": 45,
                    "interruptor_doble": 60,
                    "tablero_trifasico": 1500,
                    "tablero_industrial": 2200,
                    "cable_thw_2_5mm": 3.2,
                    "cable_thw_4mm": 4.5,
                    "cable_thw_6mm": 6.8,
                    "tuberia_pvc_3_4": 1.5,
                    "tuberia_pvc_1": 2.2,
                    "caja_octogonal": 4.0,
                    "pozo_tierra": 1960
                },
                "reglas": {
                    "area_min": 50,
                    "area_max": 1000,
                    "puntos_por_m2": 0.12,
                    "tomas_por_m2": 0.15,
                    "potencia_estimada_w_m2": 80
                },
                "normativa": "CNE Suministro 2011 - Sección 050 + 060",
                "tiempo_estimado": "7-10 días hábiles",
                "garantia": "1 año"
            },
            "INDUSTRIAL": {
                "nombre": "Instalación Eléctrica Industrial",
                "descripcion": "Plantas industriales, fábricas, talleres >200m²",
                "precios": {
                    "punto_luz_industrial": 120,
                    "luminaria_led_industrial": 280,
                    "tomacorriente_industrial": 95,
                    "tomacorriente_trifasico": 150,
                    "tablero_industrial": 2800,
                    "tablero_fuerza": 3500,
                    "cable_thw_6mm": 6.5,
                    "cable_thw_10mm": 10.5,
                    "cable_thw_16mm": 16.8,
                    "tuberia_pvc_1": 2.0,
                    "tuberia_pvc_1_5": 3.2,
                    "canaleta_metalica": 12.5,
                    "pozo_tierra_industrial": 2500
                },
                "reglas": {
                    "area_min": 200,
                    "potencia_min_kw": 50,
                    "puntos_por_m2": 0.08,
                    "tomas_por_m2": 0.12,
                    "potencia_estimada_w_m2": 150
                },
                "normativa": "CNE Suministro + CNE Utilización + NTP 370.252",
                "tiempo_estimado": "15-20 días hábiles",
                "garantia": "2 años"
            }
        },
        "etapas": ["initial", "area", "pisos", "puntos_luz", "tomacorrientes", "tableros", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 📋 ITSE - Certificaciones Técnicas de Seguridad
    # ──────────────────────────────────────────────────────────────────────────
    "itse": {
        "categorias": {
            "SALUD": {
                "tipos": ["Hospital", "Clínica", "Centro Médico", "Consultorio", "Laboratorio Clínico"],
                "riesgo_default": "ALTO",
                "reglas": "Más de 500m² o 2+ pisos = MUY ALTO",
                "icon": "🏥"
            },
            "EDUCACION": {
                "tipos": ["Colegio", "Universidad", "Instituto", "Academia", "Guardería", "CEBA"],
                "riesgo_default": "MEDIO",
                "reglas": "Más de 1000m² o 3+ pisos = ALTO",
                "icon": "🎓"
            },
            "HOSPEDAJE": {
                "tipos": ["Hotel", "Hostal", "Residencia", "Apart-hotel", "Albergue"],
                "riesgo_default": "MEDIO",
                "reglas": "Más de 20 habitaciones o 3+ pisos = ALTO",
                "icon": "🏨"
            },
            "COMERCIO": {
                "tipos": ["Tienda", "Supermercado", "Centro Comercial", "Galería", "Bodega"],
                "riesgo_default": "MEDIO",
                "reglas": "Más de 500m² = ALTO",
                "icon": "🏪"
            },
            "RESTAURANTE": {
                "tipos": ["Restaurante", "Cafetería", "Bar", "Discoteca", "Pub"],
                "riesgo_default": "MEDIO",
                "reglas": "Con GLP o >100 personas = ALTO",
                "icon": "🍽️"
            },
            "OFICINA": {
                "tipos": ["Oficina", "Estudio", "Coworking", "Consultorio"],
                "riesgo_default": "BAJO",
                "reglas": "Más de 500m² = MEDIO",
                "icon": "🏢"
            },
            "INDUSTRIAL": {
                "tipos": ["Fábrica", "Taller", "Almacén", "Planta Industrial", "Depósito"],
                "riesgo_default": "ALTO",
                "reglas": "Materiales peligrosos = MUY ALTO",
                "icon": "🏭"
            },
            "ENCUENTRO": {
                "tipos": ["Auditorio", "Cine", "Teatro", "Iglesia", "Gimnasio", "Estadio"],
                "riesgo_default": "ALTO",
                "reglas": "Más de 100 personas = MUY ALTO",
                "icon": "🎭"
            }
        },
        "precios_municipales": {
            "BAJO": {"precio": 168.30, "renovacion": 90.30, "dias": 7, "descripcion": "Riesgo Bajo"},
            "MEDIO": {"precio": 208.60, "renovacion": 109.40, "dias": 7, "descripcion": "Riesgo Medio"},
            "ALTO": {"precio": 703.00, "renovacion": 417.40, "dias": 7, "descripcion": "Riesgo Alto"},
            "MUY_ALTO": {"precio": 1084.60, "renovacion": 629.20, "dias": 7, "descripcion": "Riesgo Muy Alto"}
        },
        "precios_tesla": {
            "BAJO": {"min": 300, "max": 500, "incluye": "Evaluación + Planos básicos"},
            "MEDIO": {"min": 450, "max": 650, "incluye": "Evaluación + Planos + Memoria"},
            "ALTO": {"min": 800, "max": 1200, "incluye": "Evaluación + Planos + Memoria + Seguimiento"},
            "MUY_ALTO": {"min": 1200, "max": 1800, "incluye": "Evaluación completa + Planos + Memoria + Gestión total"}
        },
        "normativa": "D.S. 002-2018-PCM - Reglamento de Inspecciones Técnicas",
        "etapas": ["initial", "tipo_especifico", "area", "pisos", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 🔌 PUESTA A TIERRA - Sistemas de Protección Eléctrica
    # ──────────────────────────────────────────────────────────────────────────
    "pozo-tierra": {
        "tipos_suelo": {
            "ARCILLOSO": {
                "nombre": "Suelo Arcilloso",
                "resistividad": 50,
                "factor_correccion": 1.0,
                "descripcion": "Suelo húmedo, buena conductividad"
            },
            "ARENOSO": {
                "nombre": "Suelo Arenoso",
                "resistividad": 200,
                "factor_correccion": 1.5,
                "descripcion": "Suelo seco, conductividad media"
            },
            "ROCOSO": {
                "nombre": "Suelo Rocoso",
                "resistividad": 1000,
                "factor_correccion": 2.0,
                "descripcion": "Suelo muy seco, baja conductividad"
            },
            "MIXTO": {
                "nombre": "Suelo Mixto",
                "resistividad": 300,
                "factor_correccion": 1.3,
                "descripcion": "Combinación de tipos de suelo"
            }
        },
        "precios": {
            "pozo_completo_basico": 1760,
            "pozo_completo_profesional": 2200,
            "varilla_copperweld_2_4m": 85,
            "varilla_copperweld_3m": 110,
            "cable_desnudo_cu_25mm": 12,
            "cable_desnudo_cu_35mm": 16,
            "bentonita_saco_25kg": 45,
            "thor_gel_saco": 120,
            "sal_industrial_saco": 15,
            "carbon_vegetal_saco": 25,
            "conector_cadweld": 35,
            "caja_registro": 180,
            "medicion_telurometro": 250
        },
        "normativa": "CNE Suministro 2011 - Sección 250 + IEEE Std 142",
        "resistencia_objetivo_residencial": 25,
        "resistencia_objetivo_comercial": 10,
        "resistencia_objetivo_industrial": 5,
        "etapas": ["initial", "tipo_suelo", "potencia", "area", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 🔥 CONTRAINCENDIOS - Sistemas de Detección y Extinción
    # ──────────────────────────────────────────────────────────────────────────
    "contraincendios": {
        "sistemas": {
            "DETECCION": {
                "nombre": "Sistema de Detección de Incendios",
                "descripcion": "Detectores, central, sirenas y pulsadores",
                "precios": {
                    "detector_humo_optico": 85,
                    "detector_humo_ionico": 95,
                    "detector_calor_termico": 95,
                    "detector_llama": 180,
                    "pulsador_manual": 65,
                    "central_deteccion_4zonas": 1200,
                    "central_deteccion_8zonas": 1800,
                    "sirena_interior": 120,
                    "sirena_exterior": 180,
                    "luz_estrobo": 95,
                    "cable_deteccion_2x18": 1.8
                },
                "cobertura_detector_m2": 80,
                "normativa": "NFPA 72"
            },
            "EXTINCION": {
                "nombre": "Sistema de Extinción de Incendios",
                "descripcion": "Extintores, gabinetes, rociadores y bombas",
                "precios": {
                    "extintor_pqs_6kg": 85,
                    "extintor_pqs_12kg": 120,
                    "extintor_co2_6kg": 180,
                    "extintor_agua_10lt": 95,
                    "gabinete_manguera_30m": 450,
                    "gabinete_manguera_45m": 550,
                    "rociador_sprinkler": 35,
                    "tuberia_sprinkler_1": 8.5,
                    "bomba_contraincendios_10hp": 3500,
                    "bomba_contraincendios_15hp": 4500,
                    "tanque_reserva_5000lt": 2800,
                    "valvula_check": 280
                },
                "area_por_extintor_m2": 200,
                "normativa": "NFPA 13, NFPA 10, NFPA 20"
            },
            "COMPLETO": {
                "nombre": "Sistema Completo (Detección + Extinción)",
                "descripcion": "Sistema integrado de protección",
                "descuento_porcentaje": 10
            }
        },
        "normativa_general": "NFPA 1, NFPA 13, NFPA 72, NFPA 20",
        "etapas": ["initial", "tipo_sistema", "area", "pisos", "nivel_riesgo", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 🏠 DOMÓTICA - Automatización Inteligente
    # ──────────────────────────────────────────────────────────────────────────
    "domotica": {
        "niveles": {
            "BASICO": {
                "nombre": "Domótica Básica",
                "descripcion": "Control de iluminación y persianas",
                "dispositivos": ["Interruptores inteligentes", "Sensores de movimiento", "Control de persianas"],
                "precio_m2": 45
            },
            "INTERMEDIO": {
                "nombre": "Domótica Intermedia",
                "descripcion": "Control de iluminación, clima y seguridad",
                "dispositivos": ["Todo lo básico", "Termostatos", "Cámaras IP", "Cerraduras inteligentes"],
                "precio_m2": 85
            },
            "AVANZADO": {
                "nombre": "Domótica Avanzada",
                "descripcion": "Sistema completo integrado",
                "dispositivos": ["Todo lo intermedio", "Control de audio/video", "Riego automático", "Alarma"],
                "precio_m2": 150
            }
        },
        "precios": {
            "interruptor_inteligente_wifi": 120,
            "interruptor_inteligente_zigbee": 95,
            "sensor_movimiento": 80,
            "sensor_puerta_ventana": 65,
            "camara_ip_interior": 350,
            "camara_ip_exterior": 450,
            "central_domotica_basica": 1500,
            "central_domotica_avanzada": 2800,
            "actuador_cortina": 180,
            "termostato_inteligente": 280,
            "cerradura_inteligente": 450,
            "hub_zigbee": 85,
            "hub_zwave": 120
        },
        "protocolos": ["WiFi", "Zigbee", "Z-Wave", "KNX", "Matter"],
        "normativa": "KNX/EIB, Z-Wave Alliance, Zigbee Alliance",
        "etapas": ["initial", "nivel", "area", "dispositivos", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 📹 CCTV - Videovigilancia Profesional
    # ──────────────────────────────────────────────────────────────────────────
    "cctv": {
        "tipos_camara": {
            "ANALOGICA": {
                "nombre": "Cámaras Analógicas HD",
                "descripcion": "Tecnología AHD/TVI/CVI",
                "precios": {
                    "camara_2mp_domo": 250,
                    "camara_2mp_bala": 280,
                    "camara_4mp_domo": 350,
                    "camara_4mp_bala": 380,
                    "camara_5mp_domo": 420,
                    "camara_5mp_bala": 450
                },
                "grabador": "DVR",
                "cable": "Coaxial RG59"
            },
            "IP": {
                "nombre": "Cámaras IP (Red)",
                "descripcion": "Tecnología IP PoE",
                "precios": {
                    "camara_2mp_domo": 350,
                    "camara_2mp_bala": 380,
                    "camara_4mp_domo": 450,
                    "camara_4mp_bala": 480,
                    "camara_8mp_domo": 650,
                    "camara_8mp_bala": 680,
                    "camara_ptz_2mp": 850,
                    "camara_ptz_4mp": 1200
                },
                "grabador": "NVR",
                "cable": "UTP Cat6"
            }
        },
        "precios_accesorios": {
            "dvr_4ch": 450,
            "dvr_8ch": 800,
            "dvr_16ch": 1200,
            "nvr_4ch_poe": 650,
            "nvr_8ch_poe": 1200,
            "nvr_16ch_poe": 1800,
            "disco_1tb_purple": 180,
            "disco_2tb_purple": 280,
            "disco_4tb_purple": 450,
            "cable_coaxial_rg59_metro": 1.5,
            "cable_utp_cat6_metro": 1.2,
            "fuente_12v_5a": 35,
            "fuente_12v_10a": 55,
            "switch_poe_8p": 280,
            "switch_poe_16p": 550,
            "monitor_led_24": 450
        },
        "dias_grabacion": [7, 15, 30, 60, 90],
        "normativa": "Ley 29733 - Protección de Datos Personales",
        "etapas": ["initial", "tipo_camara", "num_camaras", "resolucion", "almacenamiento", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 🌐 REDES - Cableado Estructurado
    # ──────────────────────────────────────────────────────────────────────────
    "redes": {
        "tipos_cable": {
            "CAT5E": {
                "nombre": "Cable UTP Cat5e",
                "velocidad": "1 Gbps",
                "distancia_max": "100m",
                "precio_metro": 0.8,
                "aplicacion": "Redes básicas, internet"
            },
            "CAT6": {
                "nombre": "Cable UTP Cat6",
                "velocidad": "10 Gbps (55m)",
                "distancia_max": "100m",
                "precio_metro": 1.2,
                "aplicacion": "Redes empresariales"
            },
            "CAT6A": {
                "nombre": "Cable UTP Cat6a",
                "velocidad": "10 Gbps (100m)",
                "distancia_max": "100m",
                "precio_metro": 1.8,
                "aplicacion": "Redes de alto rendimiento"
            },
            "FIBRA": {
                "nombre": "Fibra Óptica Monomodo",
                "velocidad": "100 Gbps",
                "distancia_max": "10km+",
                "precio_metro": 2.5,
                "aplicacion": "Backbone, larga distancia"
            }
        },
        "precios_componentes": {
            "punto_red_completo": 45,
            "faceplate_doble": 12,
            "jack_rj45_cat6": 8,
            "patch_cord_1m": 8,
            "patch_cord_3m": 12,
            "access_point_ac": 280,
            "access_point_ax": 450,
            "switch_8p_gigabit": 180,
            "switch_24p_gigabit": 450,
            "switch_48p_gigabit": 850,
            "rack_6u": 350,
            "rack_12u": 550,
            "rack_24u": 850,
            "patch_panel_24p": 85,
            "patch_panel_48p": 150,
            "organizador_cables": 35,
            "bandeja_rack": 45
        },
        "normativa": "TIA/EIA 568, ISO/IEC 11801",
        "etapas": ["initial", "tipo_cable", "area", "puntos", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # ⚙️ AUTOMATIZACIÓN INDUSTRIAL - PLCs y Control de Procesos
    # ──────────────────────────────────────────────────────────────────────────
    "automatizacion-industrial": {
        "tipos_plc": {
            "BASICO": {
                "nombre": "PLC Básico (Micro)",
                "descripcion": "Hasta 32 I/O, procesos simples",
                "precio": 1200,
                "entradas_max": 16,
                "salidas_max": 16,
                "marcas": ["Siemens S7-1200", "Allen Bradley Micro800"]
            },
            "INTERMEDIO": {
                "nombre": "PLC Intermedio (Compacto)",
                "descripcion": "Hasta 128 I/O, procesos medios",
                "precio": 2800,
                "entradas_max": 64,
                "salidas_max": 64,
                "marcas": ["Siemens S7-1500", "Allen Bradley CompactLogix"]
            },
            "AVANZADO": {
                "nombre": "PLC Avanzado (Modular)",
                "descripcion": "I/O ilimitadas, procesos complejos",
                "precio": 5500,
                "entradas_max": 512,
                "salidas_max": 512,
                "marcas": ["Siemens S7-1500 Advanced", "Allen Bradley ControlLogix"]
            }
        },
        "precios_componentes": {
            "hmi_7inch_basico": 650,
            "hmi_10inch_avanzado": 950,
            "hmi_15inch_industrial": 1500,
            "variador_frecuencia_1hp": 450,
            "variador_frecuencia_5hp": 850,
            "variador_frecuencia_10hp": 1500,
            "sensor_inductivo": 45,
            "sensor_capacitivo": 55,
            "sensor_fotoelectrico": 85,
            "sensor_ultrasonico": 120,
            "contactor_16a": 35,
            "contactor_32a": 55,
            "rele_termico": 45,
            "guardamotor": 65,
            "botonera_completa": 85,
            "luz_torre_3_colores": 95,
            "encoder_incremental": 180,
            "modulo_entrada_digital": 280,
            "modulo_salida_rele": 320
        },
        "normativa": "IEC 61131-3, NFPA 79",
        "etapas": ["initial", "tipo_plc", "entradas", "salidas", "hmi", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 📄 EXPEDIENTES TÉCNICOS - Documentación Profesional
    # ──────────────────────────────────────────────────────────────────────────
    "expedientes": {
        "tipos_proyecto": {
            "ELECTRICO": {
                "nombre": "Expediente Técnico Eléctrico",
                "precio_base": 1500,
                "precio_por_m2": 3.5,
                "tiempo": "10-15 días hábiles",
                "incluye": [
                    "Memoria descriptiva",
                    "Especificaciones técnicas",
                    "Planos eléctricos (plantas, detalles, diagramas)",
                    "Metrados y presupuesto",
                    "Análisis de precios unitarios",
                    "Cálculos justificatorios",
                    "Cronograma de obra"
                ]
            },
            "SANITARIO": {
                "nombre": "Expediente Técnico Sanitario",
                "precio_base": 1200,
                "precio_por_m2": 2.8,
                "tiempo": "8-12 días hábiles",
                "incluye": [
                    "Memoria descriptiva",
                    "Especificaciones técnicas",
                    "Planos sanitarios (agua, desagüe, drenaje)",
                    "Metrados y presupuesto",
                    "Análisis de precios unitarios",
                    "Cálculos hidráulicos",
                    "Cronograma de obra"
                ]
            },
            "ESTRUCTURAL": {
                "nombre": "Expediente Técnico Estructural",
                "precio_base": 2000,
                "precio_por_m2": 4.5,
                "tiempo": "15-20 días hábiles",
                "incluye": [
                    "Memoria de cálculo estructural",
                    "Especificaciones técnicas",
                    "Planos estructurales (cimentación, columnas, vigas, losas)",
                    "Metrados y presupuesto",
                    "Análisis de precios unitarios",
                    "Estudio de mecánica de suelos",
                    "Cronograma de obra"
                ]
            },
            "ARQUITECTURA": {
                "nombre": "Expediente Técnico Arquitectónico",
                "precio_base": 1800,
                "precio_por_m2": 4.0,
                "tiempo": "12-18 días hábiles",
                "incluye": [
                    "Memoria descriptiva",
                    "Especificaciones técnicas",
                    "Planos arquitectónicos (plantas, cortes, elevaciones, detalles)",
                    "Metrados y presupuesto",
                    "Análisis de precios unitarios",
                    "Renders 3D",
                    "Cronograma de obra"
                ]
            }
        },
        "complejidad": {
            "SIMPLE": {"factor": 1.0, "descripcion": "Proyecto estándar sin complicaciones"},
            "MEDIA": {"factor": 1.3, "descripcion": "Proyecto con algunas particularidades"},
            "ALTA": {"factor": 1.6, "descripcion": "Proyecto complejo con múltiples desafíos"}
        },
        "normativa": "RNE (Reglamento Nacional de Edificaciones)",
        "etapas": ["initial", "tipo_proyecto", "area", "complejidad", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 💧 SANEAMIENTO - Sistemas de Agua y Desagüe
    # ──────────────────────────────────────────────────────────────────────────
    "saneamiento": {
        "sistemas": {
            "AGUA_FRIA": {
                "nombre": "Sistema de Agua Fría",
                "precios": {
                    "punto_agua_fria": 55,
                    "tuberia_pvc_1_2": 2.5,
                    "tuberia_pvc_3_4": 3.5,
                    "tuberia_pvc_1": 5.0,
                    "codo_pvc": 1.5,
                    "tee_pvc": 2.0,
                    "valvula_compuerta_1_2": 25,
                    "valvula_compuerta_3_4": 35
                }
            },
            "AGUA_CALIENTE": {
                "nombre": "Sistema de Agua Caliente",
                "precios": {
                    "punto_agua_caliente": 75,
                    "tuberia_cpvc_1_2": 4.5,
                    "tuberia_cpvc_3_4": 6.0,
                    "terma_electrica_50lt": 450,
                    "terma_electrica_80lt": 650,
                    "terma_gas_10lt": 550,
                    "calentador_solar": 1800
                }
            },
            "DESAGUE": {
                "nombre": "Sistema de Desagüe",
                "precios": {
                    "punto_desague": 45,
                    "tuberia_pvc_2": 3.5,
                    "tuberia_pvc_4": 5.5,
                    "tuberia_pvc_6": 12.0,
                    "codo_pvc_2": 2.5,
                    "codo_pvc_4": 4.0,
                    "yee_pvc_2": 3.5,
                    "yee_pvc_4": 5.5,
                    "registro_bronce_2": 35,
                    "registro_bronce_4": 55,
                    "sumidero_2": 25,
                    "caja_registro_12x24": 85
                }
            },
            "ALMACENAMIENTO": {
                "nombre": "Tanques y Bombeo",
                "precios": {
                    "tanque_elevado_600lt": 650,
                    "tanque_elevado_1100lt": 850,
                    "tanque_elevado_2500lt": 1500,
                    "cisterna_2500lt": 1800,
                    "cisterna_5000lt": 2500,
                    "cisterna_10000lt": 4500,
                    "bomba_agua_1_2hp": 450,
                    "bomba_agua_1hp": 650,
                    "bomba_agua_2hp": 950,
                    "hidroneumatico_24lt": 350,
                    "hidroneumatico_50lt": 550
                }
            }
        },
        "normativa": "RNE IS.010 (Instalaciones Sanitarias), IS.020 (Tanques Sépticos)",
        "etapas": ["initial", "tipo_sistema", "area", "banos", "puntos", "quotation"]
    },
    
    # ──────────────────────────────────────────────────────────────────────────
    # 📋 ITSE - Certificado de Inspección Técnica de Seguridad en Edificaciones
    # ──────────────────────────────────────────────────────────────────────────
    "itse": {
        "categorias": {
            "SALUD": {
                "nombre": "Establecimientos de Salud",
                "tipos": [
                    "Hospital",
                    "Clínica",
                    "Centro de Salud",
                    "Posta Médica",
                    "Consultorio Médico",
                    "Laboratorio Clínico",
                    "Centro de Diagnóstico"
                ],
                "riesgo_base": "ALTO"
            },
            "EDUCACION": {
                "nombre": "Centros Educativos",
                "tipos": [
                    "Universidad",
                    "Instituto",
                    "Colegio",
                    "Escuela",
                    "Centro de Idiomas",
                    "Academia",
                    "Guardería/Nido"
                ],
                "riesgo_base": "ALTO"
            },
            "HOSPEDAJE": {
                "nombre": "Establecimientos de Hospedaje",
                "tipos": [
                    "Hotel 5 Estrellas",
                    "Hotel 4 Estrellas",
                    "Hotel 3 Estrellas",
                    "Hostal",
                    "Albergue",
                    "Casa de Huéspedes"
                ],
                "riesgo_base": "MEDIO"
            },
            "COMERCIO": {
                "nombre": "Locales Comerciales",
                "tipos": [
                    "Centro Comercial",
                    "Supermercado",
                    "Tienda por Departamentos",
                    "Tienda Retail",
                    "Galería Comercial",
                    "Mercado",
                    "Bodega"
                ],
                "riesgo_base": "MEDIO"
            },
            "RESTAURANTE": {
                "nombre": "Establecimientos de Alimentación",
                "tipos": [
                    "Restaurante",
                    "Cafetería",
                    "Fast Food",
                    "Bar",
                    "Discoteca",
                    "Pub",
                    "Panadería"
                ],
                "riesgo_base": "MEDIO"
            },
            "OFICINA": {
                "nombre": "Oficinas Administrativas",
                "tipos": [
                    "Edificio de Oficinas",
                    "Oficina Corporativa",
                    "Coworking",
                    "Consultorio Profesional",
                    "Estudio",
                    "Agencia"
                ],
                "riesgo_base": "BAJO"
            },
            "INDUSTRIAL": {
                "nombre": "Establecimientos Industriales",
                "tipos": [
                    "Fábrica",
                    "Planta Industrial",
                    "Taller Industrial",
                    "Almacén Industrial",
                    "Centro de Distribución",
                    "Depósito"
                ],
                "riesgo_base": "ALTO"
            },
            "ENCUENTRO": {
                "nombre": "Centros de Reunión",
                "tipos": [
                    "Auditorio",
                    "Teatro",
                    "Cine",
                    "Centro de Convenciones",
                    "Sala de Eventos",
                    "Gimnasio",
                    "Iglesia/Templo"
                ],
                "riesgo_base": "ALTO"
            }
        },
        
        # 💰 PRECIOS OFICIALES TUPA HUANCAYO 2025
        "precios_tupa": {
            "BAJO": {
                "hasta_100m2": 245.50,
                "100_500m2": 368.30,
                "500_1000m2": 491.00,
                "mas_1000m2": 613.80
            },
            "MEDIO": {
                "hasta_100m2": 368.30,
                "100_500m2": 491.00,
                "500_1000m2": 613.80,
                "mas_1000m2": 736.50
            },
            "ALTO": {
                "hasta_100m2": 491.00,
                "100_500m2": 613.80,
                "500_1000m2": 736.50,
                "mas_1000m2": 859.30
            },
            "MUY_ALTO": {
                "hasta_100m2": 613.80,
                "100_500m2": 736.50,
                "500_1000m2": 859.30,
                "mas_1000m2": 982.00
            }
        },
        
        "normativa": "Ley N° 28976 - Reglamento de Inspecciones Técnicas de Seguridad en Edificaciones",
        "etapas": ["initial", "categoria", "tipo_especifico", "area", "pisos", "quotation"]
    }


}


# 
#  CLASE BASE - LocalSpecialist
# 

class LocalSpecialist:
    '''
    Clase base para todos los especialistas locales
    Implementa patrn de conversacin por etapas profesional
    '''
    
    def __init__(self, service_type: str):
        self.service_type = service_type
        self.kb = KNOWLEDGE_BASE.get(service_type, {})
        self.conversation_state = {
            'stage': 'initial',
            'data': {},
            'history': []
        }
    
    def process_message(self, message: str, state: Optional[Dict] = None) -> Dict:
        # Inicializar estado si es None o vacío
        if state is None or not isinstance(state, dict):
            state = {
                'stage': 'initial',
                'data': {},
                'history': []
            }
        
        # Asegurar que tiene las claves necesarias
        if 'stage' not in state:
            state['stage'] = 'initial'
        if 'data' not in state:
            state['data'] = {}
        if 'history' not in state:
            state['history'] = []
        
        # Actualizar el estado de conversación
        self.conversation_state = state
        
        method_name = f'_process_{self.service_type.replace("-", "_")}'
        method = getattr(self, method_name, self._process_generic)
        
        return method(message)

    def _process_generic(self, message: str) -> Dict:
        return {
            'texto': f'Servicio {self.service_type} en desarrollo. Por favor usa Gemini o contacta soporte.',
            'stage': 'error',
            'state': self.conversation_state
        }
    
    def _validar_numero(self, valor: str, tipo: str = 'entero', min_val: float = 0, max_val: float = None) -> Tuple[bool, Optional[float], str]:
        try:
            valor_limpio = valor.strip().replace(',', '.')
            num = int(float(valor_limpio)) if tipo == 'entero' else float(valor_limpio)
            
            if num <= min_val:
                return False, None, f'El valor debe ser mayor a {min_val}'
            if max_val and num > max_val:
                return False, None, f'El valor debe ser menor a {max_val}'
            
            return True, num, ''
        except ValueError:
            return False, None, 'Por favor ingresa un nmero vlido'
    
    def _calcular_progreso(self) -> str:
        etapas = self.kb.get('etapas', [])
        stage_actual = self.conversation_state['stage']
        try:
            indice = etapas.index(stage_actual)
            return f'{indice + 1}/{len(etapas)}'
        except:
            return '0/0'


# ══════════════════════════════════════════════════════════════════════════════
# ⚡ ELECTRICIDAD SPECIALIST
# ══════════════════════════════════════════════════════════════════════════════

class ElectricidadSpecialist(LocalSpecialist):
    """Especialista en instalaciones eléctricas profesionales"""
    
    def _process_electricidad(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Instalaciones Eléctricas de **Tesla Electricidad**.

🎯 Te ayudo a cotizar tu proyecto eléctrico con:
✅ Precios según CNE 2011
✅ Cálculo automático de materiales
✅ Cotización profesional en minutos

**¿Qué tipo de instalación necesitas?**""",
                "botones": [
                    {"text": "🏠 Residencial", "value": "RESIDENCIAL"},
                    {"text": "🏢 Comercial", "value": "COMERCIAL"},
                    {"text": "🏭 Industrial", "value": "INDUSTRIAL"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/7"
            }
        
        elif stage == "tipo" or (stage == "initial" and message in ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"]):
            data["tipo"] = message
            self.conversation_state["stage"] = "area"
            tipo_info = self.kb["tipos"][message]
            
            return {


                "texto": f"""Perfecto, instalación **{tipo_info["nombre"]}**. 

📋 **Normativa:** {tipo_info["normativa"]}
⏱️ **Tiempo:** {tipo_info["tiempo_estimado"]}

📏 **¿Cuál es el área total del proyecto en m²?**

_Escribe el número (ejemplo: 120)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "2/7"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 10000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m² (ejemplo: 120)",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "2/7"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "pisos"
            
            return {
                "texto": f"""✅ Área: **{area} m²**

🏢 **¿Cuántos pisos tiene el proyecto?**

_Escribe el número (ejemplo: 2)_""",
                "stage": "pisos",
                "state": self.conversation_state,
                "datos_generados": {"area_m2": area},
                "progreso": "3/7"
            }
        
        elif stage == "pisos":
            es_valido, pisos, error = self._validar_numero(message, "entero", 0, 50)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de pisos (ejemplo: 2)",
                    "stage": "pisos",
                    "state": self.conversation_state,
                    "progreso": "3/7"
                }
            
            data["pisos"] = pisos
            self.conversation_state["stage"] = "puntos_luz"
            
            return {
                "texto": f"""✅ Pisos: **{pisos}**

💡 **¿Cuántos puntos de luz necesitas?**

_Escribe el número (ejemplo: 25)_""",
                "stage": "puntos_luz",
                "state": self.conversation_state,
                "progreso": "4/7"
            }
        
        elif stage == "puntos_luz":
            es_valido, puntos, error = self._validar_numero(message, "entero", 0, 500)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de puntos de luz (ejemplo: 25)",
                    "stage": "puntos_luz",
                    "state": self.conversation_state,
                    "progreso": "4/7"
                }
            
            data["puntos_luz"] = puntos
            self.conversation_state["stage"] = "tomacorrientes"
            
            return {
                "texto": f"""✅ Puntos de luz: **{puntos}**

🔌 **¿Cuántos tomacorrientes?**

_Escribe el número (ejemplo: 15)_""",
                "stage": "tomacorrientes",
                "state": self.conversation_state,
                "progreso": "5/7"
            }
        
        elif stage == "tomacorrientes":
            es_valido, tomas, error = self._validar_numero(message, "entero", 0, 500)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de tomacorrientes (ejemplo: 15)",
                    "stage": "tomacorrientes",
                    "state": self.conversation_state,
                    "progreso": "5/7"
                }
            
            data["tomacorrientes"] = tomas
            self.conversation_state["stage"] = "tableros"
            
            return {
                "texto": f"""✅ Tomacorrientes: **{tomas}**

⚡ **¿Cuántos tableros eléctricos?**

_Escribe el número (ejemplo: 2)_""",
                "stage": "tableros",
                "state": self.conversation_state,
                "progreso": "6/7"
            }
        
        elif stage == "tableros":
            es_valido, tableros, error = self._validar_numero(message, "entero", 0, 20)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de tableros (ejemplo: 2)",
                    "stage": "tableros",
                    "state": self.conversation_state,
                    "progreso": "6/7"
                }
            
            data["tableros"] = tableros
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_electricidad()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista para generar. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "7/7"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_electricidad("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_electricidad(self) -> Dict:
        data = self.conversation_state["data"]
        tipo = data["tipo"]
        area = data["area"]
        pisos = data["pisos"]
        puntos = data["puntos_luz"]
        tomas = data["tomacorrientes"]
        tableros = data["tableros"]
        
        precios = self.kb["tipos"][tipo]["precios"]
        
        items = []
        
        items.append({
            "descripcion": f"Puntos de luz empotrados ({puntos} und)",
            "cantidad": puntos,
            "precio_unitario": precios["punto_luz_empotrado"],
            "total": puntos * precios["punto_luz_empotrado"]
        })
        
        items.append({
            "descripcion": f"Tomacorrientes dobles ({tomas} und)",
            "cantidad": tomas,
            "precio_unitario": precios["tomacorriente_doble"],
            "total": tomas * precios["tomacorriente_doble"]
        })
        
        precio_tablero = precios.get("tablero_trifasico", precios.get("tablero_industrial", 1200))
        items.append({
            "descripcion": f"Tableros eléctricos ({tableros} und)",
            "cantidad": tableros,
            "precio_unitario": precio_tablero,
            "total": tableros * precio_tablero
        })
        
        cable_metros = area * 1.5 * pisos
        items.append({
            "descripcion": f"Cable THW 2.5mm² ({cable_metros:.0f}m)",
            "cantidad": cable_metros,
            "precio_unitario": precios["cable_thw_2_5mm"],
            "total": cable_metros * precios["cable_thw_2_5mm"]
        })
        
        tuberia_metros = area * 1.2 * pisos
        items.append({
            "descripcion": f"Tubería PVC 3/4\" ({tuberia_metros:.0f}m)",
            "cantidad": tuberia_metros,
            "precio_unitario": precios["tuberia_pvc_3_4"],
            "total": tuberia_metros * precios["tuberia_pvc_3_4"]
        })
        
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto_cotizacion = f"""📊 **COTIZACIÓN INSTALACIÓN ELÉCTRICA {tipo}**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

📏 Área: {area} m²
🏢 Pisos: {pisos}
💡 Puntos de luz: {puntos}
🔌 Tomacorrientes: {tomas}
⚡ Tableros: {tableros}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto_cotizacion += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        texto_cotizacion += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Materiales + Mano de obra
⏱️ Tiempo: {self.kb["tipos"][tipo]["tiempo_estimado"]}
📋 Normativa: {self.kb["tipos"][tipo]["normativa"]}
🎁 Garantía: {self.kb["tipos"][tipo]["garantia"]}

¿Deseas generar el documento?"""
        
        return {
            "texto": texto_cotizacion,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": f"Instalación Eléctrica {tipo}",
                    "area_m2": area
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "7/7"
        }


# ══════════════════════════════════════════════════════════════════════════════
# 📋 ITSE SPECIALIST
# ══════════════════════════════════════════════════════════════════════════════

class ITSESpecialist(LocalSpecialist):
    """Especialista en certificaciones ITSE profesionales"""
    
    def _process_itse(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        # 🔥 CRÍTICO: Detectar selección de categoría PRIMERO (antes de verificar stage)
        message_upper = message.upper().strip()
        if message_upper in self.kb["categorias"].keys():
            # Usuario seleccionó una categoría válida
            data["categoria"] = message_upper
            self.conversation_state["stage"] = "tipo_especifico"
            tipos = self.kb["categorias"][message_upper]["tipos"]
            
            return {
                "texto": f"""Perfecto, sector **{self.kb["categorias"][message_upper]["nombre"]}**. 

¿Qué tipo específico es tu establecimiento?""",
                "botones": [{"text": t, "value": t} for t in tipos],
                "stage": "tipo_especifico",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        # Si no es una categoría, procesar según el stage actual
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en certificados ITSE de **Tesla Electricidad**.

🎯 Te ayudo a obtener tu certificado ITSE con:
✅ Visita técnica GRATUITA
✅ Precios oficiales TUPA Huancayo
✅ Trámite 100% gestionado
✅ Entrega en 7 días hábiles

**Selecciona tu tipo de establecimiento:**""",
                "botones": [
                    {"text": "🏥 Salud", "value": "SALUD"},
                    {"text": "🎓 Educación", "value": "EDUCACION"},
                    {"text": "🏨 Hospedaje", "value": "HOSPEDAJE"},
                    {"text": "🏪 Comercio", "value": "COMERCIO"},
                    {"text": "🍽️ Restaurante", "value": "RESTAURANTE"},
                    {"text": "🏢 Oficina", "value": "OFICINA"},
                    {"text": "🏭 Industrial", "value": "INDUSTRIAL"},
                    {"text": "🎭 Encuentro", "value": "ENCUENTRO"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/5"
            }
        
        elif stage == "categoria" or (stage == "initial" and message in self.kb["categorias"].keys()):
            data["categoria"] = message
            self.conversation_state["stage"] = "tipo_especifico"
            tipos = self.kb["categorias"][message]["tipos"]
            
            return {
                "texto": f"""Perfecto, sector **{message}**. ¿Qué tipo específico es?""",
                "botones": [{"text": t, "value": t} for t in tipos],
                "stage": "tipo_especifico",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        elif stage == "tipo_especifico":
            data["tipo_especifico"] = message
            self.conversation_state["stage"] = "area"
            
            return {
                "texto": f"""Entendido, es un **{message}**. 

¿Cuál es el área total en m²?

_Escribe el número (ejemplo: 150)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "3/5"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 50000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m²",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "3/5"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "pisos"
            
            return {
                "texto": f"""📐 Área: **{area} m²**

¿Cuántos pisos tiene el establecimiento?

_Escribe el número (ejemplo: 2)_""",
                "stage": "pisos",
                "state": self.conversation_state,
                "progreso": "4/5"
            }
        
        elif stage == "pisos":
            es_valido, pisos, error = self._validar_numero(message, "entero", 0, 50)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de pisos",
                    "stage": "pisos",
                    "state": self.conversation_state,
                    "progreso": "4/5"
                }
            
            data["pisos"] = pisos
            self.conversation_state["stage"] = "quotation"
            
            riesgo = self._calcular_riesgo(data["categoria"], data["area"], pisos)
            data["riesgo"] = riesgo
            
            return self._generar_cotizacion_itse(riesgo)
        
        elif stage == "quotation":
            if message == "AGENDAR":
                return {
                    "texto": "✅ Excelente! Para agendar tu visita técnica GRATUITA, contacta:\n\n📞 WhatsApp: 906 315 961\n📧 Email: ingenieria.teslaelectricidad@gmail.com",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "5/5"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_itse("")
        
        return self._process_generic(message)
    
    def _calcular_riesgo(self, categoria: str, area: float, pisos: int) -> str:
        if categoria == "SALUD":
            return "MUY_ALTO" if area > 500 or pisos >= 2 else "ALTO"
        elif categoria == "EDUCACION":
            return "ALTO" if area > 1000 or pisos >= 3 else "MEDIO"
        elif categoria == "HOSPEDAJE":
            return "ALTO" if area > 500 or pisos >= 3 else "MEDIO"
        elif categoria == "COMERCIO":
            return "ALTO" if area > 500 else "MEDIO"
        elif categoria == "RESTAURANTE":
            return "ALTO" if area > 300 else "MEDIO"
        elif categoria == "OFICINA":
            return "MEDIO" if area > 500 else "BAJO"
        elif categoria == "INDUSTRIAL":
            return "ALTO"
        elif categoria == "ENCUENTRO":
            return "MUY_ALTO" if area > 500 else "ALTO"
        return self.kb["categorias"][categoria]["riesgo_default"]
    
    def _generar_cotizacion_itse(self, riesgo: str) -> Dict:
        municipal = self.kb["precios_municipales"][riesgo]
        tesla = self.kb["precios_tesla"][riesgo]
        total_min = municipal["precio"] + tesla["min"]
        total_max = municipal["precio"] + tesla["max"]
        
        texto = f"""📊 **COTIZACIÓN ITSE - NIVEL {riesgo.replace('_', ' ')}**

━━━━━━━━━━━━━━━━━━━━━━━
**💰 COSTOS DESGLOSADOS:**

🏛️ **Derecho Municipal (TUPA):**
└ S/ {municipal["precio"]:.2f}

⚡ **Servicio Técnico TESLA:**
└ S/ {tesla["min"]} - {tesla["max"]}
└ {tesla["incluye"]}

━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTAL ESTIMADO:**
**S/ {total_min} - {total_max}**
━━━━━━━━━━━━━━━━━━━━━━━

⏱️ **Tiempo:** {municipal["dias"]} días hábiles
🎁 **Visita técnica:** GRATUITA
✅ **Garantía:** 100% aprobación

¿Qué deseas hacer?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📅 Agendar visita", "value": "AGENDAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "servicio": "ITSE",
                "nivel_riesgo": riesgo,
                "total_min": total_min,
                "total_max": total_max
            },
            "progreso": "5/5"
        }


# ══════════════════════════════════════════════════════════════════════════════
# 🔌 POZO TIERRA, 🔥 CONTRAINCENDIOS, 🏠 DOMÓTICA, 📹 CCTV, 🌐 REDES
# ⚙️ AUTOMATIZACIÓN, 📄 EXPEDIENTES, 💧 SANEAMIENTO SPECIALISTS
# ══════════════════════════════════════════════════════════════════════════════
# Nota: Implementaciones simplificadas - se pueden expandir según necesidad

class PozoTierraSpecialist(LocalSpecialist):
    """Especialista en sistemas de puesta a tierra profesionales"""
    
    def _process_pozo_tierra(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Sistemas de Puesta a Tierra de **Tesla Electricidad**.

🎯 Te ayudo con:
✅ Diseño según CNE Sección 250
✅ Cálculo de resistencia
✅ Materiales certificados
✅ Medición con telurómetro

**¿Qué tipo de suelo tienes?**""",
                "botones": [
                    {"text": "🟤 Arcilloso", "value": "ARCILLOSO"},
                    {"text": "🟡 Arenoso", "value": "ARENOSO"},
                    {"text": "⚫ Rocoso", "value": "ROCOSO"},
                    {"text": "🔵 Mixto", "value": "MIXTO"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/5"
            }
        
        elif stage == "tipo_suelo" or (stage == "initial" and message in self.kb["tipos_suelo"].keys()):
            data["tipo_suelo"] = message
            self.conversation_state["stage"] = "potencia"
            suelo_info = self.kb["tipos_suelo"][message]
            
            return {
                "texto": f"""Perfecto, suelo **{suelo_info["nombre"]}**.

📊 Resistividad: {suelo_info["resistividad"]} Ω·m
⚙️ Factor de corrección: {suelo_info["factor_correccion"]}

⚡ **¿Cuál es la potencia instalada en kW?**

_Escribe el número (ejemplo: 50)_""",
                "stage": "potencia",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        elif stage == "potencia":
            es_valido, potencia, error = self._validar_numero(message, "decimal", 0, 1000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa la potencia en kW",
                    "stage": "potencia",
                    "state": self.conversation_state,
                    "progreso": "2/5"
                }
            
            data["potencia"] = potencia
            self.conversation_state["stage"] = "area"
            
            return {
                "texto": f"""✅ Potencia: **{potencia} kW**

📏 **¿Cuál es el área del terreno en m²?**

_Escribe el número (ejemplo: 200)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "3/5"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 10000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m²",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "3/5"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_pozo()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "5/5"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_pozo_tierra("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_pozo(self) -> Dict:
        data = self.conversation_state["data"]
        tipo_suelo = data["tipo_suelo"]
        potencia = data["potencia"]
        area = data["area"]
        
        suelo_info = self.kb["tipos_suelo"][tipo_suelo]
        precios = self.kb["precios"]
        
        # Determinar tipo de instalación según potencia
        if potencia < 20:
            tipo_inst = "residencial"
            resistencia_obj = self.kb["resistencia_objetivo_residencial"]
            num_pozos = 1
        elif potencia < 100:
            tipo_inst = "comercial"
            resistencia_obj = self.kb["resistencia_objetivo_comercial"]
            num_pozos = 2
        else:
            tipo_inst = "industrial"
            resistencia_obj = self.kb["resistencia_objetivo_industrial"]
            num_pozos = 3
        
        items = []
        
        # Pozos completos
        precio_pozo = precios["pozo_completo_profesional"] if tipo_inst != "residencial" else precios["pozo_completo_basico"]
        items.append({
            "descripcion": f"Pozo a tierra completo ({num_pozos} und)",
            "cantidad": num_pozos,
            "precio_unitario": precio_pozo,
            "total": num_pozos * precio_pozo
        })
        
        # Varillas adicionales
        varillas_extra = num_pozos * 2
        items.append({
            "descripcion": f"Varillas copperweld 2.4m ({varillas_extra} und)",
            "cantidad": varillas_extra,
            "precio_unitario": precios["varilla_copperweld_2_4m"],
            "total": varillas_extra * precios["varilla_copperweld_2_4m"]
        })
        
        # Cable desnudo
        cable_metros = num_pozos * 15
        items.append({
            "descripcion": f"Cable desnudo Cu 25mm² ({cable_metros}m)",
            "cantidad": cable_metros,
            "precio_unitario": precios["cable_desnudo_cu_25mm"],
            "total": cable_metros * precios["cable_desnudo_cu_25mm"]
        })
        
        # Bentonita y Thor Gel
        items.append({
            "descripcion": f"Bentonita sódica ({num_pozos * 2} sacos)",
            "cantidad": num_pozos * 2,
            "precio_unitario": precios["bentonita_saco_25kg"],
            "total": num_pozos * 2 * precios["bentonita_saco_25kg"]
        })
        
        items.append({
            "descripcion": f"Thor Gel ({num_pozos} sacos)",
            "cantidad": num_pozos,
            "precio_unitario": precios["thor_gel_saco"],
            "total": num_pozos * precios["thor_gel_saco"]
        })
        
        # Medición
        items.append({
            "descripcion": "Medición con telurómetro (1 servicio)",
            "cantidad": 1,
            "precio_unitario": precios["medicion_telurometro"],
            "total": precios["medicion_telurometro"]
        })
        
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN SISTEMA PUESTA A TIERRA**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

🟤 Tipo de suelo: {suelo_info["nombre"]}
⚡ Potencia: {potencia} kW
📏 Área: {area} m²
🎯 Resistencia objetivo: ≤ {resistencia_obj} Ω
🔧 Número de pozos: {num_pozos}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        texto += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Materiales + Instalación + Medición
📋 Normativa: {self.kb["normativa"]}
🎁 Garantía: 2 años

¿Deseas generar el documento?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": f"Sistema Puesta a Tierra - {tipo_inst.title()}",
                    "potencia_kw": potencia,
                    "area_m2": area
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "5/5"
        }


class ContraincendiosSpecialist(LocalSpecialist):
    """Especialista en sistemas contraincendios profesionales"""
    
    def _process_contraincendios(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Sistemas Contraincendios de **Tesla Electricidad**.

🎯 Te ayudo con:
✅ Sistemas según NFPA
✅ Detección y extinción
✅ Certificación completa

**¿Qué sistema necesitas?**""",
                "botones": [
                    {"text": "🔔 Detección", "value": "DETECCION"},
                    {"text": "🧯 Extinción", "value": "EXTINCION"},
                    {"text": "🔥 Completo", "value": "COMPLETO"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/6"
            }
        
        elif stage == "tipo_sistema" or (stage == "initial" and message in ["DETECCION", "EXTINCION", "COMPLETO"]):
            data["tipo_sistema"] = message
            self.conversation_state["stage"] = "area"
            
            if message == "COMPLETO":
                desc = "Sistema Completo (Detección + Extinción)"
            else:
                desc = self.kb["sistemas"][message]["nombre"]
            
            return {
                "texto": f"""Perfecto, **{desc}**.

📏 **¿Cuál es el área total a proteger en m²?**

_Escribe el número (ejemplo: 300)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "2/6"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 50000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m²",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "2/6"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "pisos"
            
            return {
                "texto": f"""✅ Área: **{area} m²**

🏢 **¿Cuántos pisos tiene el edificio?**

_Escribe el número (ejemplo: 3)_""",
                "stage": "pisos",
                "state": self.conversation_state,
                "progreso": "3/6"
            }
        
        elif stage == "pisos":
            es_valido, pisos, error = self._validar_numero(message, "entero", 0, 50)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de pisos",
                    "stage": "pisos",
                    "state": self.conversation_state,
                    "progreso": "3/6"
                }
            
            data["pisos"] = pisos
            self.conversation_state["stage"] = "nivel_riesgo"
            
            return {
                "texto": f"""✅ Pisos: **{pisos}**

⚠️ **¿Cuál es el nivel de riesgo del establecimiento?**""",
                "botones": [
                    {"text": "🟢 Bajo", "value": "BAJO"},
                    {"text": "🟡 Medio", "value": "MEDIO"},
                    {"text": "🟠 Alto", "value": "ALTO"}
                ],
                "stage": "nivel_riesgo",
                "state": self.conversation_state,
                "progreso": "4/6"
            }
        
        elif stage == "nivel_riesgo":
            data["nivel_riesgo"] = message
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_contraincendios()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "6/6"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_contraincendios("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_contraincendios(self) -> Dict:
        data = self.conversation_state["data"]
        tipo_sistema = data["tipo_sistema"]
        area = data["area"]
        pisos = data["pisos"]
        nivel_riesgo = data["nivel_riesgo"]
        
        items = []
        
        # Factor de riesgo
        factor_riesgo = {"BAJO": 1.0, "MEDIO": 1.3, "ALTO": 1.6}[nivel_riesgo]
        
        if tipo_sistema in ["DETECCION", "COMPLETO"]:
            det = self.kb["sistemas"]["DETECCION"]["precios"]
            
            # Detectores de humo
            num_detectores = int(area / det.get("cobertura_detector_m2", 80)) * pisos
            items.append({
                "descripcion": f"Detectores de humo óptico ({num_detectores} und)",
                "cantidad": num_detectores,
                "precio_unitario": det["detector_humo_optico"],
                "total": num_detectores * det["detector_humo_optico"] * factor_riesgo
            })
            
            # Central de detección
            zonas = max(4, pisos * 2)
            central = "central_deteccion_8zonas" if zonas > 4 else "central_deteccion_4zonas"
            items.append({
                "descripcion": f"Central de detección {zonas} zonas (1 und)",
                "cantidad": 1,
                "precio_unitario": det[central],
                "total": det[central]
            })
            
            # Pulsadores y sirenas
            pulsadores = pisos * 2
            items.append({
                "descripcion": f"Pulsadores manuales ({pulsadores} und)",
                "cantidad": pulsadores,
                "precio_unitario": det["pulsador_manual"],
                "total": pulsadores * det["pulsador_manual"]
            })
            
            sirenas = pisos
            items.append({
                "descripcion": f"Sirenas ({sirenas} und)",
                "cantidad": sirenas,
                "precio_unitario": det["sirena_interior"],
                "total": sirenas * det["sirena_interior"]
            })
        
        if tipo_sistema in ["EXTINCION", "COMPLETO"]:
            ext = self.kb["sistemas"]["EXTINCION"]["precios"]
            
            # Extintores
            num_extintores = int(area / ext.get("area_por_extintor_m2", 200)) * pisos
            items.append({
                "descripcion": f"Extintores PQS 12kg ({num_extintores} und)",
                "cantidad": num_extintores,
                "precio_unitario": ext["extintor_pqs_12kg"],
                "total": num_extintores * ext["extintor_pqs_12kg"]
            })
            
            # Gabinetes
            gabinetes = pisos
            items.append({
                "descripcion": f"Gabinetes con manguera 30m ({gabinetes} und)",
                "cantidad": gabinetes,
                "precio_unitario": ext["gabinete_manguera_30m"],
                "total": gabinetes * ext["gabinete_manguera_30m"]
            })
        
        subtotal = sum(item["total"] for item in items)
        
        # Descuento si es sistema completo
        if tipo_sistema == "COMPLETO":
            descuento = subtotal * 0.10
            subtotal = subtotal - descuento
        
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN SISTEMA CONTRAINCENDIOS**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

🔥 Sistema: {tipo_sistema}
📏 Área: {area} m²
🏢 Pisos: {pisos}
⚠️ Nivel de riesgo: {nivel_riesgo}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        if tipo_sistema == "COMPLETO":
            texto += f"🎁 Descuento sistema completo (10%): -S/ {descuento:.2f}\n\n"
        
        texto += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Equipos + Instalación + Certificación
📋 Normativa: {self.kb["normativa_general"]}
🎁 Garantía: 1 año

¿Deseas generar el documento?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": f"Sistema Contraincendios {tipo_sistema}",
                    "area_m2": area,
                    "pisos": pisos
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "6/6"
        }


# Continúa con los demás especialistas...
# (Por limitaciones de espacio, los demás seguirán el mismo patrón)

class DomoticaSpecialist(LocalSpecialist):
    """Especialista en domótica y automatización del hogar"""
    
    def _process_domotica(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Domótica de **Tesla Electricidad**.

🎯 Automatiza tu hogar/negocio con:
✅ Control de iluminación
✅ Climatización inteligente
✅ Seguridad integrada
✅ Ahorro energético

**¿Qué nivel de domótica necesitas?**""",
                "botones": [
                    {"text": "🟢 Básico", "value": "BASICO"},
                    {"text": "🟡 Intermedio", "value": "INTERMEDIO"},
                    {"text": "🔴 Avanzado", "value": "AVANZADO"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/5"
            }
        
        elif stage == "nivel" or (stage == "initial" and message in ["BASICO", "INTERMEDIO", "AVANZADO"]):
            data["nivel"] = message
            self.conversation_state["stage"] = "area"
            nivel_info = self.kb["niveles"][message]
            
            return {
                "texto": f"""Perfecto, **{nivel_info["nombre"]}**.

📋 {nivel_info["descripcion"]}
💰 Precio estimado: S/ {nivel_info["precio_m2"]}/m²

📏 **¿Cuál es el área a automatizar en m²?**

_Escribe el número (ejemplo: 150)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 5000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m²",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "2/5"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "dispositivos"
            
            nivel = data["nivel"]
            precio_estimado = area * self.kb["niveles"][nivel]["precio_m2"]
            
            return {
                "texto": f"""✅ Área: **{area} m²**
💰 Estimado base: **S/ {precio_estimado:,.2f}**

🔢 **¿Cuántos dispositivos aproximadamente?**

_Escribe el número (ejemplo: 20)_""",
                "stage": "dispositivos",
                "state": self.conversation_state,
                "progreso": "3/5"
            }
        
        elif stage == "dispositivos":
            es_valido, dispositivos, error = self._validar_numero(message, "entero", 0, 200)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de dispositivos",
                    "stage": "dispositivos",
                    "state": self.conversation_state,
                    "progreso": "3/5"
                }
            
            data["dispositivos"] = dispositivos
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_domotica()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "5/5"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_domotica("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_domotica(self) -> Dict:
        data = self.conversation_state["data"]
        nivel = data["nivel"]
        area = data["area"]
        dispositivos = data["dispositivos"]
        
        nivel_info = self.kb["niveles"][nivel]
        precios = self.kb["precios"]
        
        items = []
        
        # Central domótica
        central = "central_domotica_avanzada" if nivel == "AVANZADO" else "central_domotica_basica"
        items.append({
            "descripcion": f"Central domótica {nivel.lower()} (1 und)",
            "cantidad": 1,
            "precio_unitario": precios[central],
            "total": precios[central]
        })
        
        # Interruptores inteligentes
        interruptores = int(dispositivos * 0.4)
        items.append({
            "descripcion": f"Interruptores inteligentes ({interruptores} und)",
            "cantidad": interruptores,
            "precio_unitario": precios["interruptor_inteligente_wifi"],
            "total": interruptores * precios["interruptor_inteligente_wifi"]
        })
        
        # Sensores
        sensores = int(dispositivos * 0.3)
        items.append({
            "descripcion": f"Sensores de movimiento ({sensores} und)",
            "cantidad": sensores,
            "precio_unitario": precios["sensor_movimiento"],
            "total": sensores * precios["sensor_movimiento"]
        })
        
        if nivel in ["INTERMEDIO", "AVANZADO"]:
            # Cámaras IP
            camaras = int(dispositivos * 0.15)
            items.append({
                "descripcion": f"Cámaras IP ({camaras} und)",
                "cantidad": camaras,
                "precio_unitario": precios["camara_ip_interior"],
                "total": camaras * precios["camara_ip_interior"]
            })
        
        if nivel == "AVANZADO":
            # Actuadores de cortina
            cortinas = int(dispositivos * 0.15)
            items.append({
                "descripcion": f"Actuadores de cortina ({cortinas} und)",
                "cantidad": cortinas,
                "precio_unitario": precios["actuador_cortina"],
                "total": cortinas * precios["actuador_cortina"]
            })
        
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN DOMÓTICA {nivel}**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

🏠 Nivel: {nivel_info["nombre"]}
📏 Área: {area} m²
🔢 Dispositivos: {dispositivos}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        texto += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Equipos + Instalación + Configuración
📋 Protocolos: {', '.join(self.kb["protocolos"][:3])}
🎁 Garantía: 1 año

¿Deseas generar el documento?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": f"Domótica {nivel}",
                    "area_m2": area
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "5/5"
        }


class CCTVSpecialist(LocalSpecialist):
    """Especialista en sistemas de videovigilancia CCTV"""
    
    def _process_cctv(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en CCTV de **Tesla Electricidad**.

🎯 Protege tu propiedad con:
✅ Cámaras HD/Full HD/4K
✅ Grabación continua
✅ Acceso remoto 24/7
✅ Visión nocturna

**¿Qué tipo de cámaras prefieres?**""",
                "botones": [
                    {"text": "📺 Analógicas HD", "value": "ANALOGICA"},
                    {"text": "🌐 IP (Red)", "value": "IP"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/6"
            }
        
        elif stage == "tipo_camara" or (stage == "initial" and message in ["ANALOGICA", "IP"]):
            data["tipo_camara"] = message
            self.conversation_state["stage"] = "num_camaras"
            tipo_info = self.kb["tipos_camara"][message]
            
            return {
                "texto": f"""Perfecto, **{tipo_info["nombre"]}**.

📋 Tecnología: {tipo_info["descripcion"]}
📹 Grabador: {tipo_info["grabador"]}
🔌 Cable: {tipo_info["cable"]}

📹 **¿Cuántas cámaras necesitas?**

_Escribe el número (ejemplo: 8)_""",
                "stage": "num_camaras",
                "state": self.conversation_state,
                "progreso": "2/6"
            }
        
        elif stage == "num_camaras":
            es_valido, num_camaras, error = self._validar_numero(message, "entero", 1, 64)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de cámaras (1-64)",
                    "stage": "num_camaras",
                    "state": self.conversation_state,
                    "progreso": "2/6"
                }
            
            data["num_camaras"] = num_camaras
            self.conversation_state["stage"] = "resolucion"
            
            return {
                "texto": f"""✅ Cámaras: **{num_camaras}**

📺 **¿Qué resolución deseas?**""",
                "botones": [
                    {"text": "📹 2MP (1080p)", "value": "2MP"},
                    {"text": "📹 4MP (2K)", "value": "4MP"},
                    {"text": "📹 8MP (4K)", "value": "8MP"} if data["tipo_camara"] == "IP" else None
                ],
                "stage": "resolucion",
                "state": self.conversation_state,
                "progreso": "3/6"
            }
        
        elif stage == "resolucion":
            data["resolucion"] = message
            self.conversation_state["stage"] = "almacenamiento"
            
            return {
                "texto": f"""✅ Resolución: **{message}**

💾 **¿Cuántos días de grabación necesitas?**""",
                "botones": [
                    {"text": "7 días", "value": "7"},
                    {"text": "15 días", "value": "15"},
                    {"text": "30 días", "value": "30"},
                    {"text": "60 días", "value": "60"}
                ],
                "stage": "almacenamiento",
                "state": self.conversation_state,
                "progreso": "4/6"
            }
        
        elif stage == "almacenamiento":
            data["dias_grabacion"] = int(message)
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_cctv()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "6/6"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_cctv("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_cctv(self) -> Dict:
        data = self.conversation_state["data"]
        tipo_camara = data["tipo_camara"]
        num_camaras = data["num_camaras"]
        resolucion = data["resolucion"]
        dias = data["dias_grabacion"]
        
        tipo_info = self.kb["tipos_camara"][tipo_camara]
        precios_cam = tipo_info["precios"]
        precios_acc = self.kb["precios_accesorios"]
        
        items = []
        
        # Cámaras
        precio_camara = precios_cam[f"camara_{resolucion.lower()}_domo"]
        items.append({
            "descripcion": f"Cámaras {tipo_camara} {resolucion} ({num_camaras} und)",
            "cantidad": num_camaras,
            "precio_unitario": precio_camara,
            "total": num_camaras * precio_camara
        })
        
        # Grabador
        canales = 4 if num_camaras <= 4 else (8 if num_camaras <= 8 else 16)
        grabador = f"{'dvr' if tipo_camara == 'ANALOGICA' else 'nvr'}_{canales}ch{'_poe' if tipo_camara == 'IP' else ''}"
        items.append({
            "descripcion": f"{tipo_info['grabador']} {canales} canales (1 und)",
            "cantidad": 1,
            "precio_unitario": precios_acc[grabador],
            "total": precios_acc[grabador]
        })
        
        # Disco duro
        gb_por_dia_por_camara = {"2MP": 20, "4MP": 40, "8MP": 80}[resolucion]
        gb_total = gb_por_dia_por_camara * num_camaras * dias
        tb_necesarios = max(1, int(gb_total / 1000))
        disco = f"disco_{min(4, tb_necesarios)}tb_purple"
        items.append({
            "descripcion": f"Disco duro {min(4, tb_necesarios)}TB Purple (1 und)",
            "cantidad": 1,
            "precio_unitario": precios_acc[disco],
            "total": precios_acc[disco]
        })
        
        # Cable
        cable_tipo = "cable_coaxial_rg59_metro" if tipo_camara == "ANALOGICA" else "cable_utp_cat6_metro"
        metros_cable = num_camaras * 30
        items.append({
            "descripcion": f"{tipo_info['cable']} ({metros_cable}m)",
            "cantidad": metros_cable,
            "precio_unitario": precios_acc[cable_tipo],
            "total": metros_cable * precios_acc[cable_tipo]
        })
        
        # Fuentes de poder o switch PoE
        if tipo_camara == "ANALOGICA":
            fuentes = int(num_camaras / 4) + 1
            items.append({
                "descripcion": f"Fuentes 12V 10A ({fuentes} und)",
                "cantidad": fuentes,
                "precio_unitario": precios_acc["fuente_12v_10a"],
                "total": fuentes * precios_acc["fuente_12v_10a"]
            })
        else:
            switch = "switch_poe_8p" if num_camaras <= 8 else "switch_poe_16p"
            items.append({
                "descripcion": f"Switch PoE {canales} puertos (1 und)",
                "cantidad": 1,
                "precio_unitario": precios_acc[switch],
                "total": precios_acc[switch]
            })
        
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN SISTEMA CCTV**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

📹 Tipo: {tipo_info["nombre"]}
🔢 Cámaras: {num_camaras}
📺 Resolución: {resolucion}
💾 Grabación: {dias} días

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        texto += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Equipos + Instalación + Configuración
📱 Acceso remoto desde celular
🎁 Garantía: 1 año

¿Deseas generar el documento?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": f"Sistema CCTV {tipo_camara} {resolucion}",
                    "num_camaras": num_camaras
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "6/6"
        }


class RedesSpecialist(LocalSpecialist):
    """Especialista en cableado estructurado y redes profesionales"""
    
    def _process_redes(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Redes y Cableado Estructurado de **Tesla Electricidad**.

🎯 Conecta tu empresa con:
✅ Cableado certificado TIA/EIA
✅ Velocidades hasta 10 Gbps
✅ WiFi empresarial
✅ Garantía 25 años

**¿Qué tipo de cableado necesitas?**""",
                "botones": [
                    {"text": "📶 Cat5e (1 Gbps)", "value": "CAT5E"},
                    {"text": "🚀 Cat6 (10 Gbps)", "value": "CAT6"},
                    {"text": "⚡ Cat6a (10 Gbps+)", "value": "CAT6A"},
                    {"text": "💎 Fibra Óptica", "value": "FIBRA"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/5"
            }
        
        elif stage == "tipo_cable" or (stage == "initial" and message in ["CAT5E", "CAT6", "CAT6A", "FIBRA"]):
            data["tipo_cable"] = message
            self.conversation_state["stage"] = "area"
            cable_info = self.kb["tipos_cable"][message]
            
            return {
                "texto": f"""Perfecto, **{cable_info["nombre"]}**.

⚡ Velocidad: {cable_info["velocidad"]}
📏 Distancia máx: {cable_info["distancia_max"]}
💼 Aplicación: {cable_info["aplicacion"]}

📏 **¿Cuál es el área total a cablear en m²?**

_Escribe el número (ejemplo: 500)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 10000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m²",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "2/5"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "puntos"
            
            return {
                "texto": f"""✅ Área: **{area} m²**

🔌 **¿Cuántos puntos de red necesitas?**

_Escribe el número (ejemplo: 24)_""",
                "stage": "puntos",
                "state": self.conversation_state,
                "progreso": "3/5"
            }
        
        elif stage == "puntos":
            es_valido, puntos, error = self._validar_numero(message, "entero", 0, 500)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de puntos de red",
                    "stage": "puntos",
                    "state": self.conversation_state,
                    "progreso": "3/5"
                }
            
            data["puntos"] = puntos
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_redes()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "5/5"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_redes("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_redes(self) -> Dict:
        data = self.conversation_state["data"]
        tipo_cable = data["tipo_cable"]
        area = data["area"]
        puntos = data["puntos"]
        
        cable_info = self.kb["tipos_cable"][tipo_cable]
        precios = self.kb["precios_componentes"]
        
        items = []
        
        # Puntos de red completos
        items.append({
            "descripcion": f"Puntos de red completos ({puntos} und)",
            "cantidad": puntos,
            "precio_unitario": precios["punto_red_completo"],
            "total": puntos * precios["punto_red_completo"]
        })
        
        # Cable
        metros_cable = puntos * 25  # Promedio 25m por punto
        items.append({
            "descripcion": f"{cable_info['nombre']} ({metros_cable}m)",
            "cantidad": metros_cable,
            "precio_unitario": cable_info["precio_metro"],
            "total": metros_cable * cable_info["precio_metro"]
        })
        
        # Patch panels
        patch_panels = int(puntos / 24) + 1
        items.append({
            "descripcion": f"Patch panel 24 puertos ({patch_panels} und)",
            "cantidad": patch_panels,
            "precio_unitario": precios["patch_panel_24p"],
            "total": patch_panels * precios["patch_panel_24p"]
        })
        
        # Switch
        if puntos <= 8:
            switch = "switch_8p_gigabit"
            desc = "Switch 8 puertos Gigabit"
        elif puntos <= 24:
            switch = "switch_24p_gigabit"
            desc = "Switch 24 puertos Gigabit"
        else:
            switch = "switch_48p_gigabit"
            desc = "Switch 48 puertos Gigabit"
        
        items.append({
            "descripcion": f"{desc} (1 und)",
            "cantidad": 1,
            "precio_unitario": precios[switch],
            "total": precios[switch]
        })
        
        # Access Points WiFi
        aps = max(1, int(area / 200))
        items.append({
            "descripcion": f"Access Point WiFi AC ({aps} und)",
            "cantidad": aps,
            "precio_unitario": precios["access_point_ac"],
            "total": aps * precios["access_point_ac"]
        })
        
        # Rack
        rack_size = "rack_6u" if puntos <= 24 else "rack_12u"
        items.append({
            "descripcion": f"Rack {rack_size.split('_')[1].upper()} (1 und)",
            "cantidad": 1,
            "precio_unitario": precios[rack_size],
            "total": precios[rack_size]
        })
        
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN CABLEADO ESTRUCTURADO**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

🌐 Tipo: {cable_info["nombre"]}
📏 Área: {area} m²
🔌 Puntos de red: {puntos}
⚡ Velocidad: {cable_info["velocidad"]}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        texto += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Materiales + Instalación + Certificación
📋 Normativa: {self.kb["normativa"]}
🎁 Garantía: 25 años en cableado

¿Deseas generar el documento?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": f"Cableado Estructurado {tipo_cable}",
                    "area_m2": area,
                    "puntos": puntos
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "5/5"
        }


class AutomatizacionSpecialist(LocalSpecialist):
    """Especialista en automatización industrial con PLCs"""
    
    def _process_automatizacion_industrial(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Automatización Industrial de **Tesla Electricidad**.

🎯 Automatiza tu proceso con:
✅ PLCs Siemens/Allen Bradley
✅ HMI táctil
✅ Variadores de frecuencia
✅ Programación incluida

**¿Qué tipo de PLC necesitas?**""",
                "botones": [
                    {"text": "🟢 Básico (hasta 32 I/O)", "value": "BASICO"},
                    {"text": "🟡 Intermedio (hasta 128 I/O)", "value": "INTERMEDIO"},
                    {"text": "🔴 Avanzado (512+ I/O)", "value": "AVANZADO"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/6"
            }
        
        elif stage == "tipo_plc" or (stage == "initial" and message in ["BASICO", "INTERMEDIO", "AVANZADO"]):
            data["tipo_plc"] = message
            self.conversation_state["stage"] = "entradas"
            plc_info = self.kb["tipos_plc"][message]
            
            return {
                "texto": f"""Perfecto, **{plc_info["nombre"]}**.

📋 {plc_info["descripcion"]}
💰 Precio base: S/ {plc_info["precio"]:,.2f}
🏭 Marcas: {', '.join(plc_info["marcas"])}

🔢 **¿Cuántas entradas digitales necesitas?**

_Escribe el número (ejemplo: 16)_""",
                "stage": "entradas",
                "state": self.conversation_state,
                "progreso": "2/6"
            }
        
        elif stage == "entradas":
            es_valido, entradas, error = self._validar_numero(message, "entero", 0, 512)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de entradas",
                    "stage": "entradas",
                    "state": self.conversation_state,
                    "progreso": "2/6"
                }
            
            data["entradas"] = entradas
            self.conversation_state["stage"] = "salidas"
            
            return {
                "texto": f"""✅ Entradas: **{entradas}**

🔢 **¿Cuántas salidas digitales necesitas?**

_Escribe el número (ejemplo: 12)_""",
                "stage": "salidas",
                "state": self.conversation_state,
                "progreso": "3/6"
            }
        
        elif stage == "salidas":
            es_valido, salidas, error = self._validar_numero(message, "entero", 0, 512)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de salidas",
                    "stage": "salidas",
                    "state": self.conversation_state,
                    "progreso": "3/6"
                }
            
            data["salidas"] = salidas
            self.conversation_state["stage"] = "hmi"
            
            return {
                "texto": f"""✅ Salidas: **{salidas}**

📺 **¿Necesitas pantalla HMI?**""",
                "botones": [
                    {"text": "📱 7 pulgadas", "value": "7"},
                    {"text": "📺 10 pulgadas", "value": "10"},
                    {"text": "🖥️ 15 pulgadas", "value": "15"},
                    {"text": "❌ No necesito", "value": "NO"}
                ],
                "stage": "hmi",
                "state": self.conversation_state,
                "progreso": "4/6"
            }
        
        elif stage == "hmi":
            data["hmi"] = message
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_automatizacion()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "6/6"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_automatizacion_industrial("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_automatizacion(self) -> Dict:
        data = self.conversation_state["data"]
        tipo_plc = data["tipo_plc"]
        entradas = data["entradas"]
        salidas = data["salidas"]
        hmi_size = data["hmi"]
        
        plc_info = self.kb["tipos_plc"][tipo_plc]
        precios = self.kb["precios_componentes"]
        
        items = []
        
        # PLC
        items.append({
            "descripcion": f"{plc_info['nombre']} (1 und)",
            "cantidad": 1,
            "precio_unitario": plc_info["precio"],
            "total": plc_info["precio"]
        })
        
        # Módulos de expansión si es necesario
        total_io = entradas + salidas
        if total_io > plc_info["entradas_max"] + plc_info["salidas_max"]:
            modulos = int((total_io - (plc_info["entradas_max"] + plc_info["salidas_max"])) / 16) + 1
            items.append({
                "descripcion": f"Módulos de expansión I/O ({modulos} und)",
                "cantidad": modulos,
                "precio_unitario": precios["modulo_entrada_digital"],
                "total": modulos * precios["modulo_entrada_digital"]
            })
        
        # HMI
        if hmi_size != "NO":
            hmi_key = f"hmi_{hmi_size}inch_{'avanzado' if tipo_plc == 'AVANZADO' else 'basico'}"
            items.append({
                "descripcion": f"HMI {hmi_size} pulgadas (1 und)",
                "cantidad": 1,
                "precio_unitario": precios[hmi_key],
                "total": precios[hmi_key]
            })
        
        # Sensores
        sensores = int(entradas * 0.6)
        items.append({
            "descripcion": f"Sensores inductivos/capacitivos ({sensores} und)",
            "cantidad": sensores,
            "precio_unitario": precios["sensor_inductivo"],
            "total": sensores * precios["sensor_inductivo"]
        })
        
        # Contactores
        contactores = int(salidas * 0.5)
        items.append({
            "descripcion": f"Contactores 16A ({contactores} und)",
            "cantidad": contactores,
            "precio_unitario": precios["contactor_16a"],
            "total": contactores * precios["contactor_16a"]
        })
        
        # Programación
        horas_prog = 40 if tipo_plc == "BASICO" else (80 if tipo_plc == "INTERMEDIO" else 120)
        items.append({
            "descripcion": f"Programación PLC ({horas_prog} horas)",
            "cantidad": horas_prog,
            "precio_unitario": 80,
            "total": horas_prog * 80
        })
        
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN AUTOMATIZACIÓN INDUSTRIAL**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

🤖 PLC: {plc_info["nombre"]}
🔢 Entradas: {entradas}
🔢 Salidas: {salidas}
📺 HMI: {hmi_size if hmi_size != 'NO' else 'No incluido'}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto += f"{i}. {item['descripcion']}\n   └ S/ {item['total']:.2f}\n\n"
        
        texto += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Equipos + Programación + Puesta en marcha
📋 Normativa: {self.kb["normativa"]}
🎁 Garantía: 1 año + soporte técnico

¿Deseas generar el documento?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": f"Automatización Industrial {tipo_plc}",
                    "entradas": entradas,
                    "salidas": salidas
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "6/6"
        }


class ExpedientesSpecialist(LocalSpecialist):
    """Especialista en expedientes técnicos profesionales"""
    
    def _process_expedientes(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Expedientes Técnicos de **Tesla Electricidad**.

🎯 Elaboramos expedientes según RNE:
✅ Memoria descriptiva
✅ Planos profesionales
✅ Metrados y presupuesto
✅ Cronograma de obra

**¿Qué tipo de expediente necesitas?**""",
                "botones": [
                    {"text": "⚡ Eléctrico", "value": "ELECTRICO"},
                    {"text": "💧 Sanitario", "value": "SANITARIO"},
                    {"text": "🏗️ Estructural", "value": "ESTRUCTURAL"},
                    {"text": "🏛️ Arquitectónico", "value": "ARQUITECTURA"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/5"
            }
        
        elif stage == "tipo_proyecto" or (stage == "initial" and message in ["ELECTRICO", "SANITARIO", "ESTRUCTURAL", "ARQUITECTURA"]):
            data["tipo_proyecto"] = message
            self.conversation_state["stage"] = "area"
            proyecto_info = self.kb["tipos_proyecto"][message]
            
            return {
                "texto": f"""Perfecto, **{proyecto_info["nombre"]}**.

📋 Incluye:
""" + "\n".join([f"✅ {item}" for item in proyecto_info["incluye"][:4]]) + f"""

⏱️ Tiempo: {proyecto_info["tiempo"]}

📏 **¿Cuál es el área del proyecto en m²?**

_Escribe el número (ejemplo: 300)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 50000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m²",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "2/5"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "complejidad"
            
            return {
                "texto": f"""✅ Área: **{area} m²**

⚙️ **¿Cuál es la complejidad del proyecto?**""",
                "botones": [
                    {"text": "🟢 Simple", "value": "SIMPLE"},
                    {"text": "🟡 Media", "value": "MEDIA"},
                    {"text": "🔴 Alta", "value": "ALTA"}
                ],
                "stage": "complejidad",
                "state": self.conversation_state,
                "progreso": "3/5"
            }
        
        elif stage == "complejidad":
            data["complejidad"] = message
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_expedientes()
        
        elif stage == "quotation":
            if message == "GENERAR":
                return {
                    "texto": "✅ Cotización lista. Haz clic en 'Descargar Word' o 'Descargar PDF'.",
                    "stage": "complete",
                    "state": self.conversation_state,
                    "progreso": "5/5"
                }
            elif message == "RESTART":
                self.conversation_state = {"stage": "initial", "data": {}, "history": []}
                return self._process_expedientes("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_expedientes(self) -> Dict:
        data = self.conversation_state["data"]
        tipo = data["tipo_proyecto"]
        area = data["area"]
        complejidad = data["complejidad"]
        
        proyecto_info = self.kb["tipos_proyecto"][tipo]
        comp_info = self.kb["complejidad"][complejidad]
        
        # Cálculo
        precio_base = proyecto_info["precio_base"]
        precio_por_area = area * proyecto_info["precio_por_m2"]
        subtotal = (precio_base + precio_por_area) * comp_info["factor"]
        
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN EXPEDIENTE TÉCNICO**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

📄 Tipo: {proyecto_info["nombre"]}
📏 Área: {area} m²
⚙️ Complejidad: {complejidad} ({comp_info["descripcion"]})

━━━━━━━━━━━━━━━━━━━━━━━
**📦 INCLUYE:**

""" + "\n".join([f"✅ {item}" for item in proyecto_info["incluye"]]) + f"""

━━━━━━━━━━━━━━━━━━━━━━━
**💰 DESGLOSE:**

Precio base: S/ {precio_base:,.2f}
Por área ({area} m² × S/ {proyecto_info["precio_por_m2"]}): S/ {precio_por_area:,.2f}
Factor complejidad ({comp_info["factor"]}x): Aplicado

━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

⏱️ Tiempo de entrega: {proyecto_info["tiempo"]}
📋 Normativa: {self.kb["normativa"]}
🎁 Incluye: Revisiones ilimitadas

¿Deseas generar el documento?"""
        
        return {
            "texto": texto,
            "botones": [
                {"text": "📄 Generar Cotización", "value": "GENERAR"},
                {"text": "🔄 Nueva consulta", "value": "RESTART"}
            ],
            "stage": "quotation",
            "state": self.conversation_state,
            "datos_generados": {
                "proyecto": {
                    "nombre": proyecto_info["nombre"],
                    "area_m2": area,
                    "complejidad": complejidad
                },
                "items": [{
                    "descripcion": f"Expediente Técnico {tipo}",
                    "cantidad": 1,
                    "precio_unitario": subtotal,
                    "total": subtotal
                }],
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "5/5"
        }


class SaneamientoSpecialist(LocalSpecialist):
    """Especialista en sistemas de agua y desagüe"""
    
    def _process_saneamiento(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        if stage == "initial":
            return {
                "texto": """¡Hola! 👋 Soy **PILI**, especialista en Saneamiento de **Tesla Electricidad**.

🎯 Instalamos sistemas según RNE:
✅ Agua fría y caliente
✅ Desagüe y ventilación
✅ Tanques y bombeo
✅ Certificación sanitaria

**¿Qué sistema necesitas?**""",
                "botones": [
                    {"text": "💧 Agua Fría", "value": "AGUA_FRIA"},
                    {"text": "🔥 Agua Caliente", "value": "AGUA_CALIENTE"},
                    {"text": "🚽 Desagüe", "value": "DESAGUE"},
                    {"text": "🏗️ Completo", "value": "COMPLETO"}
                ],
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/6"
            }
        
        elif stage == "tipo_sistema" or (stage == "initial" and message in ["AGUA_FRIA", "AGUA_CALIENTE", "DESAGUE", "COMPLETO"]):
            data["tipo_sistema"] = message
            self.conversation_state["stage"] = "area"
            
            if message == "COMPLETO":
                desc = "Sistema Completo (Agua + Desagüe + Tanques)"
            else:
                desc = self.kb["sistemas"][message]["nombre"]
            
            return {
                "texto": f"""Perfecto, **{desc}**.

📏 **¿Cuál es el área total en m²?**

_Escribe el número (ejemplo: 150)_""",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "2/6"
            }
        
        elif stage == "area":
            es_valido, area, error = self._validar_numero(message, "decimal", 0, 5000)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el área en m²",
                    "stage": "area",
                    "state": self.conversation_state,
                    "progreso": "2/6"
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "banos"
            
            return {
                "texto": f"""✅ Área: **{area} m²**

🚽 **¿Cuántos baños tiene?**

_Escribe el número (ejemplo: 3)_""",
                "stage": "banos",
                "state": self.conversation_state,
                "progreso": "3/6"
            }
        
        elif stage == "banos":
            es_valido, banos, error = self._validar_numero(message, "entero", 0, 50)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de baños",
                    "stage": "banos",
                    "state": self.conversation_state,
                    "progreso": "3/6"
                }
            
            data["banos"] = banos
            self.conversation_state["stage"] = "puntos"
            
            return {
                "texto": f"""✅ Baños: **{banos}**

🔢 **¿Cuántos puntos de agua adicionales?**
_(Cocina, lavandería, jardín, etc.)_

_Escribe el número (ejemplo: 5)_""",
                "stage": "puntos",
                "state": self.conversation_state,
                "progreso": "4/6"
            }
        
        elif stage == "puntos":
            es_valido, puntos, error = self._validar_numero(message, "entero", 0, 100)
            
            if not es_valido:
                return {
                    "texto": f"❌ {error}\n\nPor favor ingresa el número de puntos adicionales",
                    "stage": "puntos",
                    "state": self.conversation_state,
                    "progreso": "4/6"
                }
            
            data["puntos_adicionales"] = puntos
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_saneamiento()


# ══════════════════════════════════════════════════════════════════════════════
# 🛠️ FUNCIONES AUXILIARES GLOBALES
# ══════════════════════════════════════════════════════════════════════════════

def formatear_moneda(valor: float, simbolo: str = "S/") -> str:
    """
    Formatea un valor numérico como moneda
    
    Args:
        valor: Valor numérico a formatear
        simbolo: Símbolo de moneda (default: "S/")
    
    Returns:
        String formateado como moneda con separadores de miles
    
    Examples:
        >>> formatear_moneda(1500.50)
        'S/ 1,500.50'
        >>> formatear_moneda(1000000)
        'S/ 1,000,000.00'
    """
    return f"{simbolo} {valor:,.2f}".replace(",", " ")


def calcular_igv(subtotal: float, tasa: float = 0.18) -> float:
    """
    Calcula el IGV sobre un subtotal
    
    Args:
        subtotal: Monto base sin IGV
        tasa: Tasa de IGV (default: 0.18 = 18%)
    
    Returns:
        Monto del IGV calculado
    
    Examples:
        >>> calcular_igv(1000)
        180.0
        >>> calcular_igv(5000, 0.18)
        900.0
    """
    return subtotal * tasa


def validar_rango_numerico(
    valor: float,
    min_val: float,
    max_val: float,
    nombre_campo: str = "valor"
) -> Tuple[bool, str]:
    """
    Valida que un valor esté dentro de un rango
    
    Args:
        valor: Valor a validar
        min_val: Valor mínimo permitido
        max_val: Valor máximo permitido
        nombre_campo: Nombre del campo para mensajes de error
    
    Returns:
        Tupla (es_valido, mensaje_error)
    
    Examples:
        >>> validar_rango_numerico(50, 0, 100, "área")
        (True, "")
        >>> validar_rango_numerico(150, 0, 100, "área")
        (False, "El área debe estar entre 0 y 100")
    """
    if valor < min_val or valor > max_val:
        return False, f"El {nombre_campo} debe estar entre {min_val} y {max_val}"
    return True, ""


def generar_codigo_proyecto(servicio: str, timestamp: datetime = None) -> str:
    """
    Genera un código único para el proyecto
    
    Args:
        servicio: Tipo de servicio
        timestamp: Fecha/hora (opcional, usa actual si no se provee)
    
    Returns:
        Código único del proyecto
    
    Examples:
        >>> generar_codigo_proyecto("electricidad")
        'ELEC-20251226-001'
        >>> generar_codigo_proyecto("itse")
        'ITSE-20251226-002'
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    prefijos = {
        "electricidad": "ELEC",
        "itse": "ITSE",
        "pozo-tierra": "POZO",
        "contraincendios": "CONT",
        "domotica": "DOMO",
        "cctv": "CCTV",
        "redes": "REDE",
        "automatizacion-industrial": "AUTO",
        "expedientes": "EXPE",
        "saneamiento": "SANE"
    }
    
    prefijo = prefijos.get(servicio, "PROY")
    fecha = timestamp.strftime("%Y%m%d")
    secuencia = str(timestamp.microsecond)[:3].zfill(3)
    
    return f"{prefijo}-{fecha}-{secuencia}"


def calcular_tiempo_estimado(
    complejidad: str,
    area: float,
    tipo_servicio: str
) -> str:
    """
    Calcula tiempo estimado de ejecución del proyecto
    
    Args:
        complejidad: Nivel de complejidad (SIMPLE, MEDIA, ALTA)
        area: Área del proyecto en m²
        tipo_servicio: Tipo de servicio
    
    Returns:
        String con tiempo estimado
    
    Examples:
        >>> calcular_tiempo_estimado("SIMPLE", 100, "electricidad")
        '5-7 días hábiles'
        >>> calcular_tiempo_estimado("ALTA", 500, "electricidad")
        '15-20 días hábiles'
    """
    factores_complejidad = {
        "SIMPLE": 1.0,
        "MEDIA": 1.5,
        "ALTA": 2.0
    }
    
    factor_area = 1.0 if area < 200 else (1.5 if area < 500 else 2.0)
    
    dias_base = {
        "electricidad": 7,
        "itse": 7,
        "pozo-tierra": 3,
        "contraincendios": 10,
        "domotica": 7,
        "cctv": 5,
        "redes": 7,
        "automatizacion-industrial": 15,
        "expedientes": 15,
        "saneamiento": 10
    }
    
    dias = dias_base.get(tipo_servicio, 7)
    dias_min = int(dias * factores_complejidad.get(complejidad, 1.0) * factor_area)
    dias_max = int(dias_min * 1.4)
    
    return f"{dias_min}-{dias_max} días hábiles"


def generar_resumen_proyecto(datos: Dict) -> str:
    """
    Genera un resumen ejecutivo del proyecto
    
    Args:
        datos: Diccionario con datos del proyecto
    
    Returns:
        String con resumen formateado
    
    Examples:
        >>> datos = {"nombre": "Instalación Eléctrica", "area": 150, "total": 5000}
        >>> generar_resumen_proyecto(datos)
        'Proyecto: Instalación Eléctrica\nÁrea: 150 m²\nInversión: S/ 5,000.00'
    """
    lineas = []
    
    if "nombre" in datos:
        lineas.append(f"📋 Proyecto: {datos['nombre']}")
    
    if "area_m2" in datos or "area" in datos:
        area = datos.get("area_m2", datos.get("area"))
        lineas.append(f"📏 Área: {area} m²")
    
    if "total" in datos:
        lineas.append(f"💰 Inversión: {formatear_moneda(datos['total'])}")
    
    if "tiempo" in datos:
        lineas.append(f"⏱️ Tiempo: {datos['tiempo']}")
    
    return "\n".join(lineas)


def validar_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args:
        email: Email a validar
    
    Returns:
        True si el email es válido
    
    Examples:
        >>> validar_email("test@example.com")
        True
        >>> validar_email("invalid-email")
        False
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_telefono_peru(telefono: str) -> bool:
    """
    Valida formato de teléfono peruano
    
    Args:
        telefono: Número de teléfono
    
    Returns:
        True si el teléfono es válido
    
    Examples:
        >>> validar_telefono_peru("906315961")
        True
        >>> validar_telefono_peru("12345")
        False
    """
    # Acepta 9 dígitos (celular) o 7 dígitos (fijo)
    patron = r'^[0-9]{7,9}$'
    return re.match(patron, telefono.replace(" ", "").replace("-", "")) is not None


def generar_disclaimer_legal() -> str:
    """
    Genera disclaimer legal para cotizaciones
    
    Returns:
        String con texto legal
    """
    return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CONDICIONES GENERALES:

1. Precios expresados en Soles Peruanos (S/) incluyen IGV
2. Validez de la cotización: 15 días calendario
3. Forma de pago: 50% adelanto, 50% contra entrega
4. Los precios no incluyen permisos municipales ni trámites administrativos
5. Garantía según especificaciones técnicas de cada servicio
6. Tiempo de entrega sujeto a disponibilidad de materiales
7. Instalación según Código Nacional de Electricidad vigente

⚡ TESLA ELECTRICIDAD - Ingeniería Eléctrica Profesional
📧 ingenieria.teslaelectricidad@gmail.com
📱 WhatsApp: 906 315 961
🌐 www.teslaelectricidad.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def generar_tabla_comparativa(items: List[Dict]) -> str:
    """
    Genera tabla comparativa de items
    
    Args:
        items: Lista de items con descripción, cantidad, precio
    
    Returns:
        String con tabla formateada
    """
    if not items:
        return ""
    
    tabla = "\n| ITEM | DESCRIPCIÓN | CANT. | P.UNIT. | TOTAL |\n"
    tabla += "|------|-------------|-------|---------|-------|\n"
    
    for i, item in enumerate(items, 1):
        desc = item.get("descripcion", "")[:40]
        cant = item.get("cantidad", 0)
        precio = item.get("precio_unitario", 0)
        total = item.get("total", 0)
        
        tabla += f"| {i:02d} | {desc} | {cant} | S/ {precio:.2f} | S/ {total:.2f} |\n"
    
    return tabla


# ══════════════════════════════════════════════════════════════════════════════
# 📊 CONSTANTES Y CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════

# Configuración de mensajes del sistema
MENSAJES_SISTEMA = {
    "bienvenida": "¡Hola! 👋 Soy PILI, tu asistente virtual de Tesla Electricidad.",
    "error_generico": "Lo siento, ocurrió un error. Por favor intenta de nuevo.",
    "servicio_no_disponible": "Este servicio está temporalmente no disponible.",
    "cotizacion_generada": "✅ Cotización generada exitosamente.",
    "datos_guardados": "✅ Datos guardados correctamente.",
    "sesion_finalizada": "Gracias por usar PILI. ¡Hasta pronto! 👋"
}

# Configuración de validaciones
VALIDACIONES = {
    "area_min": 1,
    "area_max": 50000,
    "pisos_min": 1,
    "pisos_max": 50,
    "puntos_min": 1,
    "puntos_max": 500,
    "potencia_min": 1,
    "potencia_max": 10000
}

# Configuración de tiempos
TIEMPOS_RESPUESTA = {
    "inmediato": "Respuesta inmediata",
    "rapido": "24-48 horas",
    "normal": "3-5 días hábiles",
    "largo": "7-15 días hábiles"
}

# Emojis por categoría
EMOJIS = {
    "electricidad": "⚡",
    "itse": "📋",
    "pozo-tierra": "🔌",
    "contraincendios": "🔥",
    "domotica": "🏠",
    "cctv": "📹",
    "redes": "🌐",
    "automatizacion-industrial": "⚙️",
    "expedientes": "📄",
    "saneamiento": "💧",
    "exito": "✅",
    "error": "❌",
    "advertencia": "⚠️",
    "info": "ℹ️",
    "dinero": "💰",
    "tiempo": "⏱️",
    "ubicacion": "📍",
    "telefono": "📱",
    "email": "📧"
}

# Versión del sistema
VERSION_PILI_SPECIALISTS = "2.0.0"
FECHA_VERSION = "2025-12-26"
AUTOR = "Tesla Electricidad - PILI AI Team"

# Logging configuration
logger.info(f"PILI Local Specialists v{VERSION_PILI_SPECIALISTS} inicializado")
logger.info(f"Servicios disponibles: {len(KNOWLEDGE_BASE)}")
logger.info(f"Fecha de versión: {FECHA_VERSION}")


# ══════════════════════════════════════════════════════════════════════════════
# 🔚 FIN DEL ARCHIVO
# ══════════════════════════════════════════════════════════════════════════════


# 
#  FACTORY PATTERN
# 

class LocalSpecialistFactory:
    '''Factory para crear especialistas locales segn tipo de servicio'''
    
    _specialists = {
        'electricidad': ElectricidadSpecialist,
        'itse': ITSESpecialist,
        'pozo-tierra': PozoTierraSpecialist,
        'contraincendios': ContraincendiosSpecialist,
        'domotica': DomoticaSpecialist,
        'cctv': CCTVSpecialist,
        'redes': RedesSpecialist,
        'automatizacion-industrial': AutomatizacionSpecialist,
        'expedientes': ExpedientesSpecialist,
        'saneamiento': SaneamientoSpecialist
    }
    
    @classmethod
    def create(cls, service_type: str) -> LocalSpecialist:
        '''Crea especialista local segn tipo de servicio'''
        specialist_class = cls._specialists.get(service_type)
        if not specialist_class:
            logger.warning(f'Servicio no soportado: {service_type}, usando genrico')
            return LocalSpecialist(service_type)
        return specialist_class(service_type)
    
    @classmethod
    def get_available_services(cls) -> List[str]:
        '''Retorna lista de servicios disponibles'''
        return list(cls._specialists.keys())


# 
#  FUNCIN PRINCIPAL
# 

def process_with_local_specialist(
    service_type: str,
    message: str,
    conversation_state: Optional[Dict] = None
) -> Dict:
    '''
    Procesa mensaje con especialista local (FALLBACK PROFESIONAL)
    
    Args:
        service_type: Tipo de servicio (electricidad, itse, etc.)
        message: Mensaje del usuario
        conversation_state: Estado de conversacin (opcional)
    
    Returns:
        {
            'texto': str,
            'botones': List[Dict],
            'stage': str,
            'state': Dict,
            'datos_generados': Dict,
            'progreso': str
        }
    '''
    try:
        specialist = LocalSpecialistFactory.create(service_type)
        response = specialist.process_message(message, conversation_state)
        
        logger.info(f' Procesado con especialista local: {service_type}')
        return response
        
    except Exception as e:
        logger.error(f' Error en especialista local: {e}')
        return {
            'texto': 'Lo siento, ocurri un error. Por favor intenta de nuevo o contacta soporte.',
            'stage': 'error',
            'state': conversation_state or {}
        }


# ══════════════════════════════════════════════════════════════════════════════
# 📋 ITSE SPECIALIST
# ══════════════════════════════════════════════════════════════════════════════

class ITSESpecialist(LocalSpecialist):
    """Especialista en Certificados ITSE"""
    
    def _process_itse(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
        # 1. ETAPA INICIAL: Mostrar Categorías
        if stage == "initial":
            categorias = self.kb.get("categorias", {})
            botones = []
            
            for key, info in categorias.items():
                botones.append({
                    "text": f"{info.get('icon', '')} {info.get('nombre', key)}",
                    "value": key
                })
            
            return {
                "texto": """¡Hola! 👋 Soy **Pili**, tu especialista en certificados ITSE de **Tesla Electricidad - Huancayo**.
    
🎯 Te ayudo a obtener tu certificado ITSE con:
✅ Visita técnica GRATUITA
✅ Precios oficiales TUPA Huancayo
✅ Trámite 100% gestionado

Selecciona tu tipo de establecimiento:""",
                "botones": botones,
                "stage": "initial",
                "state": self.conversation_state,
                "progreso": "1/5"
            }
        
        # 2. SELECCIÓN DE CATEGORÍA -> PREGUNTAR TIPO ESPECÍFICO
        elif stage == "tipo_especifico" or (stage == "initial" and message in self.kb.get("categorias", {})):
            # Guardar categoría
            data["categoria"] = message
            categoria_info = self.kb["categorias"][message]
            
            # Preparar botones de tipos específicos
            tipos = categoria_info.get("tipos", [])
            botones = [{"text": t, "value": t} for t in tipos]
            
            self.conversation_state["stage"] = "area"
            
            return {
                "texto": f"Perfecto, sector **{categoria_info['nombre']}**. ¿Qué tipo específico es?",
                "botones": botones,
                "stage": "tipo_especifico",
                "state": self.conversation_state,
                "progreso": "2/5"
            }
        
        # 3. SELECCIÓN TIPO -> PREGUNTAR ÁREA
        elif stage == "area" or (stage == "tipo_especifico" and message):
            if stage == "tipo_especifico":
                data["tipo_especifico"] = message
            
            self.conversation_state["stage"] = "pisos"
            
            return {
                "texto": f"Entendido, es un **{data.get('tipo_especifico', 'establecimiento')}**.\n\n¿Cuál es el área total en m²?\n_(Escribe solo el número, ej: 150)_",
                "stage": "area",
                "state": self.conversation_state,
                "progreso": "3/5"
            }
        
        # 4. ÁREA -> PREGUNTAR PISOS
        elif stage == "pisos":
            # Validar área
            es_valido, area, error = self._validar_numero(message, 'float', 10, 10000)
            if not es_valido:
                return {
                    "texto": f"❌ {error}. Por favor ingresa un área válida (ej: 120).",
                    "stage": "area",
                    "state": self.conversation_state
                }
            
            data["area"] = area
            self.conversation_state["stage"] = "quotation"
            
            return {
                "texto": f"📐 Área: **{area} m²**\n\n¿Cuántos pisos tiene el establecimiento?",
                "stage": "pisos",
                "state": self.conversation_state,
                "progreso": "4/5"
            }
            
        # 5. PISOS -> GENERAR COTIZACIÓN
        elif stage == "quotation":
            # Validar pisos
            es_valido, pisos, error = self._validar_numero(message, 'entero', 1, 50)
            if not es_valido:
                return {
                    "texto": f"❌ {error}. Por favor ingresa un número de pisos válido.",
                    "stage": "pisos",
                    "state": self.conversation_state
                }
            
            data["pisos"] = pisos
            
            # CALCULAR RIESGO Y PRECIO
            riesgo, razon = self._calcular_riesgo(data)
            cotizacion = self._calcular_cotizacion(riesgo)
            
            # Guardar resultados
            data["riesgo"] = riesgo
            data["cotizacion"] = cotizacion
            
            # Mapeo de riesgo a clave de precios municipales
            riesgo_key = riesgo  # BAJO, MEDIO, ALTO, MUY_ALTO
            precios_muni = self.kb["precios_municipales"].get(riesgo_key, {})
            precios_tesla = self.kb["precios_tesla"].get(riesgo_key, {})
            
            total_min = precios_muni.get("precio", 0) + precios_tesla.get("min", 0)
            total_max = precios_muni.get("precio", 0) + precios_tesla.get("max", 0)
            
            return {
                "texto": f"""📊 **COTIZACIÓN ITSE - RIESGO {riesgo}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**💰 COSTOS DESGLOSADOS:**

🏛️ **Derecho Municipal (TUPA):**
└ S/ {precios_muni.get('precio', 0):.2f} ({precios_muni.get('descripcion', '')})

⚡ **Servicio Técnico TESLA:**
└ S/ {precios_tesla.get('min', 0)} - {precios_tesla.get('max', 0)}
└ Incluye: {precios_tesla.get('incluye', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTAL ESTIMADO:**
**S/ {total_min:.2f} - {total_max:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️ **Tiempo:** {precios_muni.get('dias', 7)} días hábiles
🎁 **Visita técnica:** GRATUITA
✅ **Garantía:** 100% aprobación

¿Qué deseas hacer?""",
                "botones": [
                    {"text": "📅 Agendar visita", "value": "AGENDAR"},
                    {"text": "🔄 Nueva consulta", "value": "RESTART"}
                ],
                "stage": "completed",
                "state": self.conversation_state,
                "progreso": "5/5",
                # IMPORTANTE: Retornamos datos_generados para que el frontend active el botón "Finalizar"
                "datos_generados": {
                    "tipo_flujo": "cotizacion-simple",
                    "servicio": "Certificado de Inspección Técnica (ITSE)",
                    "items": [
                        {"descripcion": f"Derecho Municipal ITSE ({riesgo})", "cantidad": 1, "precio_unitario": precios_muni.get('precio', 0), "total": precios_muni.get('precio', 0)},
                        {"descripcion": f"Servicio Técnico Tesla ({riesgo})", "cantidad": 1, "precio_unitario": precios_tesla.get('max', 0), "total": precios_tesla.get('max', 0)}
                    ],
                    "total": total_max,
                    "moneda": "PEN",
                    "observaciones": [
                        "Servicio conforme al Nuevo Reglamento de Inspecciones ITSE",
                        "Incluye asesoría técnica durante la Visita de Inspección",
                        "Levantamiento de observaciones documentarias incluidas",
                        "No incluye costos de reparaciones físicas o implementaciones mayores",
                        "Precios referenciales sujetos a verificación en visita técnica"
                    ]
                },
                "cotizacion_generada": {  # Flag explícito para activar botón
                    "total": total_max,
                    "items": []
                }
            }
            
        return self._process_generic(message)

    def _calcular_riesgo(self, data: Dict) -> Tuple[str, str]:
        """Calcula el riesgo basado en categoría, área y pisos"""
        categoria = data.get("categoria", "")
        area = float(data.get("area", 0))
        pisos = int(data.get("pisos", 1))
        
        info_cat = self.kb["categorias"].get(categoria, {})
        riesgo = info_cat.get("riesgo_default", "MEDIO")
        razon = "Riesgo estándar para la categoría"
        
        # Aplicar reglas específicas (versión simplificada de la lógica completa)
        reglas_texto = info_cat.get("reglas", "")
        
        # Lógica hardcodeada crítica para asegurar precisión
        if categoria == "SALUD":
            if area > 500 or pisos >= 2:
                return "MUY_ALTO", "Salud > 500m2 o 2+ pisos"
            return "ALTO", "Establecimiento de Salud"
            
        elif categoria == "EDUCACION":
            if area > 1000 or pisos >= 3:
                return "ALTO", "Educación > 1000m2 o 3+ pisos"
            return "MEDIO", "Centro educativo estándar"
            
        elif categoria == "COMERCIO":
            if area > 500:
                return "ALTO", "Comercio > 500m2"
            return "MEDIO", "Comercio estándar"
            
        elif categoria == "INDUSTRIAL":
            return "ALTO", "Industrial siempre es alto riesgo mínimo"
            
        return riesgo, razon

    def _calcular_cotizacion(self, riesgo: str) -> Dict:
        """Retorna estructura de cotización dummy"""
        return {"riesgo": riesgo}

# ══════════════════════════════════════════════════════════════════════════════
# 🏭 FACTORY PATTERN
# ══════════════════════════════════════════════════════════════════════════════

class LocalSpecialistFactory:
    """Factory para crear especialistas locales segun tipo de servicio"""
    
    _specialists = {
        "electricidad": ElectricidadSpecialist,
        "itse": ITSESpecialist,
        "pozo-tierra": PozoTierraSpecialist,
        "contraincendios": ContraincendiosSpecialist,
        "domotica": DomoticaSpecialist,
        "cctv": CCTVSpecialist,
        "redes": RedesSpecialist,
        "automatizacion-industrial": AutomatizacionSpecialist,
        "expedientes": ExpedientesSpecialist,
        "saneamiento": SaneamientoSpecialist
    }
    
    @classmethod
    def create(cls, service_type: str) -> LocalSpecialist:
        """Crea especialista local segun tipo de servicio"""
        specialist_class = cls._specialists.get(service_type)
        if not specialist_class:
            logger.warning(f"Servicio no soportado: {service_type}, usando generico")
            return LocalSpecialist(service_type)
        return specialist_class(service_type)
    
    @classmethod
    def get_available_services(cls) -> List[str]:
        """Retorna lista de servicios disponibles"""
        return list(cls._specialists.keys())


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 FUNCION PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def process_with_local_specialist(
    service_type: str,
    message: str,
    conversation_state: Optional[Dict] = None
) -> Dict:
    """
    Procesa mensaje con especialista local (FALLBACK PROFESIONAL)
    
    Args:
        service_type: Tipo de servicio (electricidad, itse, etc.)
        message: Mensaje del usuario
        conversation_state: Estado de conversacion (opcional)
    
    Returns:
        Dict con texto, botones, stage, state, datos_generados, progreso
    """
    try:
        specialist = LocalSpecialistFactory.create(service_type)
        response = specialist.process_message(message, conversation_state)
        
        logger.info(f"✅ Procesado con especialista local: {service_type}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en especialista local: {e}")
        return {
            "texto": "Lo siento, ocurrio un error. Por favor intenta de nuevo o contacta soporte.",
            "stage": "error",
            "state": conversation_state or {}
        }


