#!/usr/bin/env python3
"""
Script para generar 30 documentos profesionales con 10 servicios diferentes
Autor: Claude (Sonnet 4.5)
Fecha: 2025-12-12
"""

import requests
import json
import time
from datetime import datetime

# Configuración
API_URL = "http://localhost:8000/api/generar-documento-directo"
OUTPUT_DIR = "/home/user/TESLA_COTIZADOR-V3.0/storage/generados"

# 10 Servicios con 3 documentos cada uno = 30 documentos
DOCUMENTOS = [
    # ============================================
    # SERVICIO 1: ELÉCTRICO RESIDENCIAL (3 docs)
    # ============================================
    {
        "nombre": "01_ELECTRICO_RESIDENCIAL_AZUL_Condominio_SanIsidro",
        "datos": {
            "cliente": "CONDOMINIO RESIDENCIAL SAN ISIDRO",
            "proyecto": "Instalación Eléctrica Residencial - 24 Departamentos",
            "servicio": "electrico-residencial",
            "area_m2": 1200,
            "items": [
                {"descripcion": "Tablero general TG trifásico 200A", "cantidad": 1, "unidad": "und", "precio_unitario": 3500.00},
                {"descripcion": "Tablero de distribución TD monofásico 60A", "cantidad": 24, "unidad": "und", "precio_unitario": 450.00},
                {"descripcion": "Cable NYY 3x6mm² + 1x6mm²", "cantidad": 850, "unidad": "m", "precio_unitario": 18.50},
                {"descripcion": "Luminarias LED empotradas 18W", "cantidad": 96, "unidad": "und", "precio_unitario": 45.00},
                {"descripcion": "Tomacorrientes dobles 20A", "cantidad": 144, "unidad": "und", "precio_unitario": 15.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "02_ELECTRICO_RESIDENCIAL_VERDE_Casa_Ecologica",
        "datos": {
            "cliente": "FAMILIA RODRIGUEZ GARCÍA",
            "proyecto": "Casa Ecológica con Sistema Solar",
            "servicio": "electrico-residencial",
            "area_m2": 280,
            "items": [
                {"descripcion": "Sistema eléctrico residencial completo", "cantidad": 1, "unidad": "glb", "precio_unitario": 12500.00},
                {"descripcion": "Paneles solares 450W (integración)", "cantidad": 12, "unidad": "und", "precio_unitario": 850.00},
                {"descripcion": "Inversor híbrido 5kW", "cantidad": 1, "unidad": "und", "precio_unitario": 4500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "verde-ecologico",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "03_ELECTRICO_RESIDENCIAL_AZUL_Villa_Deportiva",
        "datos": {
            "cliente": "ASOCIACIÓN DE PROPIETARIOS VILLA DEPORTIVA",
            "proyecto": "Remodelación Eléctrica Áreas Comunes",
            "servicio": "electrico-residencial",
            "area_m2": 650,
            "items": [
                {"descripcion": "Rediseño sistema eléctrico áreas comunes", "cantidad": 1, "unidad": "glb", "precio_unitario": 8500.00},
                {"descripcion": "Reflectores LED 100W para canchas", "cantidad": 16, "unidad": "und", "precio_unitario": 180.00},
                {"descripcion": "Cableado subterráneo NYY", "cantidad": 320, "unidad": "m", "precio_unitario": 22.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 2: ELÉCTRICO COMERCIAL (3 docs)
    # ============================================
    {
        "nombre": "04_ELECTRICO_COMERCIAL_AZUL_Centro_Comercial",
        "datos": {
            "cliente": "INVERSIONES REAL PLAZA HUANCAYO S.A.C.",
            "proyecto": "Sistema Eléctrico Centro Comercial 3 Pisos",
            "servicio": "electrico-comercial",
            "area_m2": 4500,
            "items": [
                {"descripcion": "Subestación eléctrica 500kVA", "cantidad": 1, "unidad": "und", "precio_unitario": 85000.00},
                {"descripcion": "Tableros de distribución TD", "cantidad": 12, "unidad": "und", "precio_unitario": 3500.00},
                {"descripcion": "Sistema de iluminación LED completo", "cantidad": 1, "unidad": "glb", "precio_unitario": 45000.00},
                {"descripcion": "Cableado general (materiales)", "cantidad": 1, "unidad": "glb", "precio_unitario": 38000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "05_ELECTRICO_COMERCIAL_ROJO_Restaurante",
        "datos": {
            "cliente": "RESTAURANTE TURÍSTICO LA CHOZA S.R.L.",
            "proyecto": "Instalación Eléctrica Restaurante + Cocina Industrial",
            "servicio": "electrico-comercial",
            "area_m2": 380,
            "items": [
                {"descripcion": "Tablero general trifásico 150A", "cantidad": 1, "unidad": "und", "precio_unitario": 4200.00},
                {"descripcion": "Circuitos cocina industrial 380V", "cantidad": 4, "unidad": "und", "precio_unitario": 1800.00},
                {"descripcion": "Sistema de iluminación decorativa", "cantidad": 1, "unidad": "glb", "precio_unitario": 5500.00},
                {"descripcion": "Tomacorrientes industriales 30A", "cantidad": 12, "unidad": "und", "precio_unitario": 85.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "rojo-energia",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "06_ELECTRICO_COMERCIAL_AZUL_Hotel",
        "datos": {
            "cliente": "HOTEL TURISMO HUANCAYO S.A.",
            "proyecto": "Remodelación Sistema Eléctrico Hotel 4 Estrellas",
            "servicio": "electrico-comercial",
            "area_m2": 2800,
            "items": [
                {"descripcion": "Rediseño sistema eléctrico completo", "cantidad": 1, "unidad": "glb", "precio_unitario": 125000.00},
                {"descripcion": "Grupo electrógeno 75kVA", "cantidad": 1, "unidad": "und", "precio_unitario": 45000.00},
                {"descripcion": "Sistema automatización iluminación", "cantidad": 1, "unidad": "glb", "precio_unitario": 28000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 3: ELÉCTRICO INDUSTRIAL (3 docs)
    # ============================================
    {
        "nombre": "07_ELECTRICO_INDUSTRIAL_AZUL_Textil",
        "datos": {
            "cliente": "CORPORACIÓN TEXTIL ANDINA S.A.C.",
            "proyecto": "Sistema Eléctrico Planta Industrial 5000m²",
            "servicio": "electrico-industrial",
            "area_m2": 5000,
            "items": [
                {"descripcion": "Subestación industrial 1000kVA", "cantidad": 1, "unidad": "und", "precio_unitario": 185000.00},
                {"descripcion": "Tableros de fuerza motriz", "cantidad": 8, "unidad": "und", "precio_unitario": 8500.00},
                {"descripcion": "Sistema puesta a tierra industrial", "cantidad": 1, "unidad": "glb", "precio_unitario": 35000.00},
                {"descripcion": "Canalización bandejas portacables", "cantidad": 450, "unidad": "m", "precio_unitario": 125.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "08_ELECTRICO_INDUSTRIAL_ROJO_Minera",
        "datos": {
            "cliente": "MINERA HUANCAYO GOLD S.A.C.",
            "proyecto": "Sistema Eléctrico Campamento Minero",
            "servicio": "electrico-industrial",
            "area_m2": 3200,
            "items": [
                {"descripcion": "Grupo electrógeno 250kVA resistente", "cantidad": 2, "unidad": "und", "precio_unitario": 95000.00},
                {"descripcion": "Sistema eléctrico alta montaña", "cantidad": 1, "unidad": "glb", "precio_unitario": 220000.00},
                {"descripcion": "Iluminación antiexplosiva ATEX", "cantidad": 45, "unidad": "und", "precio_unitario": 850.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "rojo-energia",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "09_ELECTRICO_INDUSTRIAL_AZUL_Procesadora",
        "datos": {
            "cliente": "PROCESADORA DE ALIMENTOS JUNÍN S.A.",
            "proyecto": "Instalación Eléctrica Planta Procesamiento",
            "servicio": "electrico-industrial",
            "area_m2": 2400,
            "items": [
                {"descripcion": "Diseño y cálculo eléctrico industrial", "cantidad": 1, "unidad": "glb", "precio_unitario": 15000.00},
                {"descripcion": "Subestación 500kVA", "cantidad": 1, "unidad": "und", "precio_unitario": 95000.00},
                {"descripcion": "Sistema control motores trifásicos", "cantidad": 12, "unidad": "und", "precio_unitario": 3500.00},
                {"descripcion": "Cámaras frigoríficas (circuitos)", "cantidad": 6, "unidad": "und", "precio_unitario": 4200.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 4: CONTRAINCENDIOS (3 docs)
    # ============================================
    {
        "nombre": "10_CONTRAINCENDIOS_ROJO_Fabrica",
        "datos": {
            "cliente": "MANUFACTURAS INDUSTRIALES DEL PERÚ S.A.",
            "proyecto": "Sistema Contra Incendios Planta Industrial",
            "servicio": "contraincendios",
            "area_m2": 6000,
            "items": [
                {"descripcion": "Rociadores automáticos (sprinklers)", "cantidad": 180, "unidad": "und", "precio_unitario": 380.00},
                {"descripcion": "Red de tuberías CPVC Schedule 40", "cantidad": 1200, "unidad": "m", "precio_unitario": 45.00},
                {"descripcion": "Bomba jockey + bomba principal", "cantidad": 1, "unidad": "set", "precio_unitario": 35000.00},
                {"descripcion": "Tanque cisterna 50m³", "cantidad": 1, "unidad": "und", "precio_unitario": 28000.00},
                {"descripcion": "Panel de control alarmas NFPA", "cantidad": 1, "unidad": "und", "precio_unitario": 12000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "rojo-energia",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "11_CONTRAINCENDIOS_ROJO_Hospital",
        "datos": {
            "cliente": "CLÍNICA ESPECIALIZADA SALUD TOTAL E.I.R.L.",
            "proyecto": "Sistema Detección y Extinción Hospital",
            "servicio": "contraincendios",
            "area_m2": 3500,
            "items": [
                {"descripcion": "Detectores de humo fotoeléctricos", "cantidad": 120, "unidad": "und", "precio_unitario": 85.00},
                {"descripcion": "Sirenas audiovisuales", "cantidad": 35, "unidad": "und", "precio_unitario": 220.00},
                {"descripcion": "Extintores PQS 12kg", "cantidad": 45, "unidad": "und", "precio_unitario": 180.00},
                {"descripcion": "Sistema sprinklers quirófanos", "cantidad": 1, "unidad": "glb", "precio_unitario": 45000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "rojo-energia",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "12_CONTRAINCENDIOS_ROJO_Bodega",
        "datos": {
            "cliente": "ALMACENES Y DISTRIBUIDORA LOGÍSTICA S.A.C.",
            "proyecto": "Protección Contra Incendios Almacén 8000m²",
            "servicio": "contraincendios",
            "area_m2": 8000,
            "items": [
                {"descripcion": "Rociadores ESFR (Early Suppression)", "cantidad": 240, "unidad": "und", "precio_unitario": 450.00},
                {"descripcion": "Red hidráulica industrial", "cantidad": 1, "unidad": "glb", "precio_unitario": 95000.00},
                {"descripcion": "Bombas diesel 1500GPM", "cantidad": 2, "unidad": "und", "precio_unitario": 55000.00},
                {"descripcion": "Gabinetes contraincendios", "cantidad": 24, "unidad": "und", "precio_unitario": 850.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "rojo-energia",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 5: DOMÓTICA (3 docs)
    # ============================================
    {
        "nombre": "13_DOMOTICA_VERDE_Smart_Home",
        "datos": {
            "cliente": "RESIDENCIA INTELIGENTE FAMILIA TORRES",
            "proyecto": "Sistema Domótica + Solar Fotovoltaico",
            "servicio": "domotica",
            "area_m2": 450,
            "items": [
                {"descripcion": "Paneles solares 450W monocristalinos", "cantidad": 20, "unidad": "und", "precio_unitario": 850.00},
                {"descripcion": "Inversor híbrido 8kW con baterías", "cantidad": 1, "unidad": "und", "precio_unitario": 12000.00},
                {"descripcion": "Sistema domótico KNX completo", "cantidad": 1, "unidad": "glb", "precio_unitario": 18000.00},
                {"descripcion": "Control iluminación inteligente", "cantidad": 1, "unidad": "glb", "precio_unitario": 6500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "verde-ecologico",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "14_DOMOTICA_AZUL_Edificio",
        "datos": {
            "cliente": "CONDOMINIO TORRES DEL PARQUE",
            "proyecto": "Automatización Edificio 8 Pisos",
            "servicio": "domotica",
            "area_m2": 3200,
            "items": [
                {"descripcion": "Sistema BMS (Building Management)", "cantidad": 1, "unidad": "glb", "precio_unitario": 45000.00},
                {"descripcion": "Control climatización automático", "cantidad": 8, "unidad": "und", "precio_unitario": 3500.00},
                {"descripción": "Ascensores inteligentes (integración)", "cantidad": 2, "unidad": "und", "precio_unitario": 8500.00},
                {"descripcion": "Sistema control accesos biométrico", "cantidad": 1, "unidad": "glb", "precio_unitario": 12000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "15_DOMOTICA_VERDE_Cooperativa",
        "datos": {
            "cliente": "COOPERATIVA AGROPECUARIA VALLE VERDE",
            "proyecto": "Sistema Solar + Automatización Agrícola",
            "servicio": "domotica",
            "area_m2": 1500,
            "items": [
                {"descripcion": "Paneles solares 450W agrícola", "cantidad": 60, "unidad": "und", "precio_unitario": 820.00},
                {"descripcion": "Inversor trifásico 25kW", "cantidad": 1, "unidad": "und", "precio_unitario": 28000.00},
                {"descripcion": "Sistema riego automatizado", "cantidad": 1, "unidad": "glb", "precio_unitario": 15000.00},
                {"descripcion": "Monitoreo IoT cultivos", "cantidad": 1, "unidad": "glb", "precio_unitario": 8500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "verde-ecologico",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 6: ITSE (3 docs)
    # ============================================
    {
        "nombre": "16_ITSE_AZUL_Restaurante",
        "datos": {
            "cliente": "RESTAURANTE EL BUEN SABOR E.I.R.L.",
            "proyecto": "Certificado ITSE Tipo A - Local Comercial",
            "servicio": "itse",
            "area_m2": 180,
            "items": [
                {"descripcion": "Inspección técnica completa", "cantidad": 1, "unidad": "glb", "precio_unitario": 1500.00},
                {"descripcion": "Planos eléctricos As-Built", "cantidad": 1, "unidad": "glb", "precio_unitario": 800.00},
                {"descripcion": "Memoria descriptiva ITSE", "cantidad": 1, "unidad": "und", "precio_unitario": 500.00},
                {"descripcion": "Tramitación completa municipalidad", "cantidad": 1, "unidad": "glb", "precio_unitario": 600.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "17_ITSE_AZUL_Centro_Medico",
        "datos": {
            "cliente": "CENTRO MÉDICO ESPECIALIZADO VIDA S.A.C.",
            "proyecto": "Certificado ITSE Tipo B - Establecimiento Salud",
            "servicio": "itse",
            "area_m2": 650,
            "items": [
                {"descripcion": "Inspección ITSE Tipo B detallada", "cantidad": 1, "unidad": "glb", "precio_unitario": 3500.00},
                {"descripcion": "Planos seguridad contraincendios", "cantidad": 1, "unidad": "glb", "precio_unitario": 1200.00},
                {"descripcion": "Protocolo mediciones eléctricas", "cantidad": 1, "unidad": "und", "precio_unitario": 800.00},
                {"descripcion": "Levantamiento observaciones Defensa Civil", "cantidad": 1, "unidad": "glb", "precio_unitario": 1500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "18_ITSE_AZUL_Discoteca",
        "datos": {
            "cliente": "CLUB NOCTURNO LA NOCHE E.I.R.L.",
            "proyecto": "Certificado ITSE Tipo C - Local Espectáculos",
            "servicio": "itse",
            "area_m2": 950,
            "items": [
                {"descripcion": "ITSE Tipo C alto riesgo", "cantidad": 1, "unidad": "glb", "precio_unitario": 5500.00},
                {"descripcion": "Actualización sistema contraincendios", "cantidad": 1, "unidad": "glb", "precio_unitario": 12000.00},
                {"descripcion": "Señalización evacuación completa", "cantidad": 1, "unidad": "glb", "precio_unitario": 2500.00},
                {"descripcion": "Capacitación brigada emergencias", "cantidad": 1, "unidad": "glb", "precio_unitario": 1200.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 7: POZO A TIERRA (3 docs)
    # ============================================
    {
        "nombre": "19_POZO_TIERRA_AZUL_Empresa",
        "datos": {
            "cliente": "EMPRESA DE TELECOMUNICACIONES FIBERNET S.A.C.",
            "proyecto": "Sistema Puesta a Tierra Torre Telecom",
            "servicio": "pozo-tierra",
            "area_m2": 50,
            "items": [
                {"descripcion": "Pozo a tierra tipo electrodo vertical", "cantidad": 4, "unidad": "und", "precio_unitario": 1800.00},
                {"descripcion": "Malla equipotencial cobre desnudo", "cantidad": 150, "unidad": "m", "precio_unitario": 35.00},
                {"descripcion": "Medición resistividad del terreno", "cantidad": 1, "unidad": "glb", "precio_unitario": 800.00},
                {"descripcion": "Tratamiento químico bentonita", "cantidad": 8, "unidad": "saco", "precio_unitario": 120.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "20_POZO_TIERRA_AZUL_Industrial",
        "datos": {
            "cliente": "METALÚRGICA CENTRAL S.A.",
            "proyecto": "Puesta a Tierra Sistema Industrial 500kVA",
            "servicio": "pozo-tierra",
            "area_m2": 200,
            "items": [
                {"descripcion": "Diseño sistema puesta tierra industrial", "cantidad": 1, "unidad": "glb", "precio_unitario": 2500.00},
                {"descripcion": "Pozos tierra electrodos copperweld", "cantidad": 12, "unidad": "und", "precio_unitario": 2200.00},
                {"descripcion": "Conductor cobre desnudo calibre 2/0", "cantidad": 350, "unidad": "m", "precio_unitario": 45.00},
                {"descripcion": "Caja registro inspección pozo", "cantidad": 12, "unidad": "und", "precio_unitario": 180.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "21_POZO_TIERRA_AZUL_Hospital",
        "datos": {
            "cliente": "HOSPITAL REGIONAL DANIEL ALCIDES CARRIÓN",
            "proyecto": "Puesta a Tierra Equipos Médicos Críticos",
            "servicio": "pozo-tierra",
            "area_m2": 120,
            "items": [
                {"descripcion": "Sistema tierra aislada quirófanos", "cantidad": 1, "unidad": "glb", "precio_unitario": 8500.00},
                {"descripcion": "Pozos tierra grado médico", "cantidad": 6, "unidad": "und", "precio_unitario": 3500.00},
                {"descripcion": "Mediciones certificadas IEC", "cantidad": 1, "unidad": "glb", "precio_unitario": 1500.00},
                {"descripcion": "Informe técnico puesta tierra", "cantidad": 1, "unidad": "und", "precio_unitario": 800.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 8: REDES Y CCTV (3 docs)
    # ============================================
    {
        "nombre": "22_REDES_CCTV_AZUL_Corporativo",
        "datos": {
            "cliente": "CORPORACIÓN FINANCIERA PERÚ S.A.",
            "proyecto": "Red de Datos + CCTV Oficinas Corporativas",
            "servicio": "redes-cctv",
            "area_m2": 1200,
            "items": [
                {"descripcion": "Cableado estructurado Cat6A certificado", "cantidad": 1, "unidad": "glb", "precio_unitario": 25000.00},
                {"descripcion": "Rack 42U con accesorios", "cantidad": 2, "unidad": "und", "precio_unitario": 3500.00},
                {"descripcion": "Switch core 48 puertos PoE+", "cantidad": 2, "unidad": "und", "precio_unitario": 8500.00},
                {"descripcion": "Cámaras IP 4MP con IA", "cantidad": 32, "unidad": "und", "precio_unitario": 650.00},
                {"descripcion": "NVR 64 canales enterprise", "cantidad": 1, "unidad": "und", "precio_unitario": 5500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "23_REDES_CCTV_AZUL_Universidad",
        "datos": {
            "cliente": "UNIVERSIDAD CONTINENTAL HUANCAYO",
            "proyecto": "Red Campus + Videovigilancia 5 Edificios",
            "servicio": "redes-cctv",
            "area_m2": 8500,
            "items": [
                {"descripcion": "Fibra óptica multimodo campus", "cantidad": 2400, "unidad": "m", "precio_unitario": 25.00},
                {"descripcion": "Switches distribución PoE", "cantidad": 15, "unidad": "und", "precio_unitario": 4500.00},
                {"descripcion": "Cámaras domo PTZ exterior", "cantidad": 85, "unidad": "und", "precio_unitario": 1200.00},
                {"descripcion": "Sistema videoanalítica IA", "cantidad": 1, "unidad": "glb", "precio_unitario": 35000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "24_REDES_CCTV_AZUL_Municipalidad",
        "datos": {
            "cliente": "MUNICIPALIDAD PROVINCIAL DE HUANCAYO",
            "proyecto": "Sistema Seguridad Ciudadana - CCTV Inteligente",
            "servicio": "redes-cctv",
            "area_m2": 15000,
            "items": [
                {"descripcion": "Cámaras LPR reconocimiento placas", "cantidad": 24, "unidad": "und", "precio_unitario": 3500.00},
                {"descripcion": "Postes metálicos para cámaras", "cantidad": 24, "unidad": "und", "precio_unitario": 2800.00},
                {"descripcion": "Centro monitoreo municipal", "cantidad": 1, "unidad": "glb", "precio_unitario": 95000.00},
                {"descripcion": "Radioenlaces punto-multipunto", "cantidad": 6, "unidad": "und", "precio_unitario": 8500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 9: EXPEDIENTES TÉCNICOS (3 docs)
    # ============================================
    {
        "nombre": "25_EXPEDIENTE_AZUL_Colegio",
        "datos": {
            "cliente": "GOBIERNO REGIONAL JUNÍN - EDUCACIÓN",
            "proyecto": "Expediente Técnico Colegio 3 Niveles",
            "servicio": "expedientes",
            "area_m2": 3500,
            "items": [
                {"descripcion": "Planos eléctricos completos", "cantidad": 1, "unidad": "glb", "precio_unitario": 8500.00},
                {"descripcion": "Memoria descriptiva y cálculos", "cantidad": 1, "unidad": "und", "precio_unitario": 3500.00},
                {"descripcion": "Especificaciones técnicas", "cantidad": 1, "unidad": "und", "precio_unitario": 2500.00},
                {"descripcion": "Metrados y presupuesto", "cantidad": 1, "unidad": "und", "precio_unitario": 2000.00},
                {"descripcion": "Análisis costos unitarios", "cantidad": 1, "unidad": "und", "precio_unitario": 1500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "26_EXPEDIENTE_AZUL_Posta",
        "datos": {
            "cliente": "MINISTERIO DE SALUD - DIRESA JUNÍN",
            "proyecto": "Expediente Técnico Centro de Salud Tipo II",
            "servicio": "expedientes",
            "area_m2": 1800,
            "items": [
                {"descripcion": "Diseño instalaciones eléctricas salud", "cantidad": 1, "unidad": "glb", "precio_unitario": 12000.00},
                {"descripcion": "Sistema eléctrico emergencia", "cantidad": 1, "unidad": "glb", "precio_unitario": 5500.00},
                {"descripcion": "Planos señalización evacuación", "cantidad": 1, "unidad": "glb", "precio_unitario": 1500.00},
                {"descripcion": "Expediente completo aprobación", "cantidad": 1, "unidad": "glb", "precio_unitario": 4500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "27_EXPEDIENTE_AZUL_Mercado",
        "datos": {
            "cliente": "MUNICIPALIDAD DISTRITAL EL TAMBO",
            "proyecto": "Expediente Técnico Mercado Municipal Modelo",
            "servicio": "expedientes",
            "area_m2": 4500,
            "items": [
                {"descripcion": "Planos instalaciones eléctricas", "cantidad": 1, "unidad": "glb", "precio_unitario": 9500.00},
                {"descripcion": "Sistema contraincendios (diseño)", "cantidad": 1, "unidad": "glb", "precio_unitario": 6500.00},
                {"descripcion": "Red datos y comunicaciones", "cantidad": 1, "unidad": "glb", "precio_unitario": 3500.00},
                {"descripcion": "Presupuesto valorizado S10", "cantidad": 1, "unidad": "und", "precio_unitario": 2500.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },

    # ============================================
    # SERVICIO 10: SANEAMIENTO (3 docs)
    # ============================================
    {
        "nombre": "28_SANEAMIENTO_VERDE_Rural",
        "datos": {
            "cliente": "COMUNIDAD CAMPESINA SAN PEDRO DE SAÑO",
            "proyecto": "Sistema Agua Potable + Desagüe 450 Familias",
            "servicio": "saneamiento",
            "area_m2": 25000,
            "items": [
                {"descripcion": "Captación + Línea conducción", "cantidad": 1, "unidad": "glb", "precio_unitario": 85000.00},
                {"descripcion": "Reservorio 150m³ + caseta", "cantidad": 1, "unidad": "und", "precio_unitario": 95000.00},
                {"descripcion": "Red distribución agua potable", "cantidad": 5400, "unidad": "m", "precio_unitario": 45.00},
                {"descripcion": "Planta tratamiento aguas residuales", "cantidad": 1, "unidad": "glb", "precio_unitario": 125000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "verde-ecologico",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "29_SANEAMIENTO_AZUL_Urbanizacion",
        "datos": {
            "cliente": "INMOBILIARIA PARQUE RESIDENCIAL S.A.C.",
            "proyecto": "Red Alcantarillado Urbanización 120 Lotes",
            "servicio": "saneamiento",
            "area_m2": 18000,
            "items": [
                {"descripcion": "Red alcantarillado PVC ISO", "cantidad": 3200, "unidad": "m", "precio_unitario": 85.00},
                {"descripcion": "Buzones concreto tipo estándar", "cantidad": 45, "unidad": "und", "precio_unitario": 1200.00},
                {"descripcion": "Conexiones domiciliarias", "cantidad": 120, "unidad": "und", "precio_unitario": 850.00},
                {"descripcion": "Cámara bombeo desagüe", "cantidad": 1, "unidad": "und", "precio_unitario": 35000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "azul-tesla",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    },
    {
        "nombre": "30_SANEAMIENTO_VERDE_Turistico",
        "datos": {
            "cliente": "COMPLEJO TURÍSTICO TERMAS DEL MANTARO S.A.",
            "proyecto": "Sistema Tratamiento Aguas Residuales Ecológico",
            "servicio": "saneamiento",
            "area_m2": 2500,
            "items": [
                {"descripcion": "Planta tratamiento biodigestores", "cantidad": 1, "unidad": "glb", "precio_unitario": 45000.00},
                {"descripcion": "Humedales artificiales 500m²", "cantidad": 1, "unidad": "glb", "precio_unitario": 28000.00},
                {"descripcion": "Sistema reutilización aguas grises", "cantidad": 1, "unidad": "glb", "precio_unitario": 18000.00},
                {"descripcion": "Monitoreo calidad agua automático", "cantidad": 1, "unidad": "glb", "precio_unitario": 12000.00}
            ],
            "opciones_personalizacion": {
                "esquema_colores": "verde-ecologico",
                "fuente": "Calibri",
                "tamaño_fuente": 11,
                "mostrar_logo": False,
                "ocultar_igv": False,
                "ocultar_precios_unitarios": False
            }
        }
    }
]

def generar_documento(nombre, datos):
    """Genera un documento llamando al API"""
    print(f"Generando: {nombre}...")

    try:
        response = requests.post(
            f"{API_URL}?formato=word",
            json=datos,
            timeout=60
        )

        if response.status_code == 200:
            filename = f"{OUTPUT_DIR}/{nombre}.docx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ Generado: {nombre}.docx")
            return True
        else:
            print(f"  ❌ Error {response.status_code}: {nombre}")
            return False
    except Exception as e:
        print(f"  ❌ Excepción en {nombre}: {str(e)}")
        return False

def main():
    """Función principal"""
    print("=" * 80)
    print("GENERACIÓN DE 30 DOCUMENTOS PROFESIONALES")
    print("Tesla Electricidad y Automatización S.A.C.")
    print("=" * 80)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total documentos: {len(DOCUMENTOS)}")
    print(f"Servicios: 10 diferentes (3 docs por servicio)")
    print("\n" + "=" * 80 + "\n")

    exitosos = 0
    fallidos = 0

    for i, doc in enumerate(DOCUMENTOS, 1):
        print(f"\n[{i}/30] ", end="")
        if generar_documento(doc["nombre"], doc["datos"]):
            exitosos += 1
        else:
            fallidos += 1

        # Pequeña pausa para no saturar el servidor
        time.sleep(0.5)

    print("\n" + "=" * 80)
    print("RESUMEN DE GENERACIÓN")
    print("=" * 80)
    print(f"✅ Exitosos: {exitosos}/30")
    print(f"❌ Fallidos: {fallidos}/30")
    print(f"📊 Tasa éxito: {(exitosos/30)*100:.1f}%")
    print("\n✅ Proceso completado!")
    print("=" * 80)

if __name__ == "__main__":
    main()
