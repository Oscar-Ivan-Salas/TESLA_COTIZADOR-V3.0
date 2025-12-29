# 🔧 SCRIPT PARA AGREGAR KNOWLEDGE_BASE DE ITSE
# Este script inserta el knowledge base de ITSE en pili_local_specialists.py

import os

file_path = r'e:\TESLA_COTIZADOR-V3.0\backend\app\services\pili_local_specialists.py'

# Leer archivo
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Código ITSE a insertar (después de línea 685, antes del cierre del dict)
itse_kb = ''',
    
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
'''

# Insertar después de línea 685 (índice 684), antes del cierre }
# Línea 685 es:     }
# Línea 686 es: }
# Necesitamos insertar entre ellas

# Reemplazar línea 685 con línea 685 + código ITSE
lines[684] = lines[684].rstrip() + itse_kb + '\r\n'

# Escribir archivo
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ KNOWLEDGE_BASE de ITSE agregado exitosamente")
print(f"📝 Líneas agregadas: {len(itse_kb.split(chr(10)))}")
