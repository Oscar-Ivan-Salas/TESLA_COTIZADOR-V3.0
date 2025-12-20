"""
🎯 SCRIPT GENERADOR - 18 DOCUMENTOS WORD PROFESIONALES CON BD

Genera 18 documentos Word profesionales simulando conversaciones con PILI:
- 3 Cotizaciones Simples
- 3 Cotizaciones Complejas
- 3 Proyectos Simples
- 3 Proyectos PMI
- 3 Informes Técnicos
- 3 Informes Ejecutivos APA

IMPORTANTE: Este script guarda 18 clientes en la base de datos usando RUCs únicos.
"""

import sys
import os
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.word_generator import WordGenerator
from app.core.database import SessionLocal
from app.models.cliente import Cliente
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📋 DEFINIR 18 CLIENTES ÚNICOS CON DATOS COMPLETOS
CLIENTES = [
    # Cotizaciones Simples (3)
    {
        "nombre": "CONSTRUCTORA DEL SUR SAC",
        "ruc": "20601234567",
        "email": "contacto@constructoradelsur.pe",
        "telefono": "064-231234",
        "direccion": "Av. Mariscal Castilla 345, El Tambo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Ing. Roberto Pérez",
        "cargo_contacto": "Gerente de Proyectos",
        "industria": "Construcción",
        "tipo_servicio": "electrico-residencial",
        "area_m2": 150
    },
    {
        "nombre": "MINERA ANDINA EIRL",
        "ruc": "20601234568",
        "email": "operaciones@mineraandina.com.pe",
        "telefono": "964-555123",
        "direccion": "Carretera Central Km 12, Concepción",
        "ciudad": "Concepción",
        "departamento": "Junín",
        "persona_contacto": "Ing. María González",
        "cargo_contacto": "Jefe de Operaciones",
        "industria": "Minería",
        "tipo_servicio": "electrico-industrial",
        "area_m2": 500
    },
    {
        "nombre": "HOTEL COSTA VERDE SAC",
        "ruc": "20601234569",
        "email": "administracion@hotelcostaverde.com",
        "telefono": "064-242345",
        "direccion": "Jr. Loreto 456, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Sr. Carlos Ramos",
        "cargo_contacto": "Administrador General",
        "industria": "Hotelería",
        "tipo_servicio": "electrico-comercial",
        "area_m2": 300
    },

    # Cotizaciones Complejas (3)
    {
        "nombre": "INDUSTRIAS TEXTILES PERÚ SA",
        "ruc": "20601234570",
        "email": "proyectos@textilesperu.com.pe",
        "telefono": "064-256789",
        "direccion": "Parque Industrial El Tambo, Lote 15",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Ing. Jorge Silva",
        "cargo_contacto": "Gerente de Planta",
        "industria": "Textil",
        "tipo_servicio": "automatizacion",
        "area_m2": 800
    },
    {
        "nombre": "CLÍNICA SAN CARLOS SAC",
        "ruc": "20601234571",
        "email": "infraestructura@clinicasancarlos.pe",
        "telefono": "064-267890",
        "direccion": "Av. Ferrocarril 789, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Dr. Luis Mendoza",
        "cargo_contacto": "Director Administrativo",
        "industria": "Salud",
        "tipo_servicio": "electrico-comercial",
        "area_m2": 1200
    },
    {
        "nombre": "SUPERMERCADOS UNIDOS SA",
        "ruc": "20601234572",
        "email": "construcciones@supermercadosunidos.pe",
        "telefono": "064-278901",
        "direccion": "Av. Giraldez 123, Huancayo Centro",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Arq. Ana Torres",
        "cargo_contacto": "Jefe de Infraestructura",
        "industria": "Retail",
        "tipo_servicio": "contraincendios",
        "area_m2": 2500
    },

    # Proyectos Simples (3)
    {
        "nombre": "UNIVERSIDAD TECNOLÓGICA DEL CENTRO",
        "ruc": "20601234573",
        "email": "infraestructura@uteccent.edu.pe",
        "telefono": "064-289012",
        "direccion": "Av. Universitaria 234, El Tambo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Ing. Pedro Vargas",
        "cargo_contacto": "Director de Infraestructura",
        "industria": "Educación",
        "tipo_servicio": "redes-datos",
        "area_m2": 3000
    },
    {
        "nombre": "PLAZA COMERCIAL HUANCAYO SAC",
        "ruc": "20601234574",
        "email": "administracion@plazahuancayo.pe",
        "telefono": "064-290123",
        "direccion": "Av. Real 567, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Ing. Carmen López",
        "cargo_contacto": "Gerente de Operaciones",
        "industria": "Comercio",
        "tipo_servicio": "cctv",
        "area_m2": 5000
    },
    {
        "nombre": "AGROINDUSTRIAS DEL VALLE EIRL",
        "ruc": "20601234575",
        "email": "proyectos@agrovallle.com",
        "telefono": "964-567890",
        "direccion": "Km 8 Carretera Huancayo-Chupaca",
        "ciudad": "Chupaca",
        "departamento": "Junín",
        "persona_contacto": "Ing. Agr. Ricardo Salas",
        "cargo_contacto": "Gerente General",
        "industria": "Agroindustria",
        "tipo_servicio": "electrico-industrial",
        "area_m2": 1500
    },

    # Proyectos PMI (3)
    {
        "nombre": "FÁBRICA DE PLÁSTICOS ANDINOS SA",
        "ruc": "20601234576",
        "email": "gerencia@plasticosandinos.com.pe",
        "telefono": "064-301234",
        "direccion": "Parque Industrial Chilca, Lote 22",
        "ciudad": "Chilca",
        "departamento": "Junín",
        "persona_contacto": "Ing. Alberto Quispe",
        "cargo_contacto": "Gerente de Producción",
        "industria": "Manufactura",
        "tipo_servicio": "automatizacion",
        "area_m2": 3500
    },
    {
        "nombre": "CENTRO MÉDICO ESPECIALIZADO SAC",
        "ruc": "20601234577",
        "email": "obras@centromed.pe",
        "telefono": "064-312345",
        "direccion": "Jr. Ancash 890, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Dr. Raúl Chávez",
        "cargo_contacto": "Director General",
        "industria": "Salud",
        "tipo_servicio": "electrico-comercial",
        "area_m2": 2000
    },
    {
        "nombre": "CORPORACIÓN MINERA DEL PERÚ SA",
        "ruc": "20601234578",
        "email": "proyectos@corpminperu.com",
        "telefono": "964-678901",
        "direccion": "Av. Industrial 345, La Oroya",
        "ciudad": "La Oroya",
        "departamento": "Junín",
        "persona_contacto": "Ing. Oscar Morales",
        "cargo_contacto": "Jefe de Proyectos",
        "industria": "Minería",
        "tipo_servicio": "electrico-industrial",
        "area_m2": 10000
    },

    # Informes Técnicos (3)
    {
        "nombre": "TRANSPORTES RÁPIDOS SAC",
        "ruc": "20601234579",
        "email": "mantenimiento@transportesrapidos.pe",
        "telefono": "064-323456",
        "direccion": "Av. Evitamiento Sur 678, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Ing. Fernando Castro",
        "cargo_contacto": "Jefe de Mantenimiento",
        "industria": "Transporte",
        "tipo_servicio": "itse",
        "area_m2": 800
    },
    {
        "nombre": "RESTAURANTE CAMPESTRE EIRL",
        "ruc": "20601234580",
        "email": "administracion@campestre.pe",
        "telefono": "964-789012",
        "direccion": "Km 5 Carretera a Hualhuas",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Sr. Miguel Rojas",
        "cargo_contacto": "Propietario",
        "industria": "Restaurantes",
        "tipo_servicio": "pozo-tierra",
        "area_m2": 500
    },
    {
        "nombre": "LABORATORIO QUÍMICO CENTRAL SA",
        "ruc": "20601234581",
        "email": "calidad@labquimico.com.pe",
        "telefono": "064-334567",
        "direccion": "Jr. Puno 234, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Q.F. Patricia Herrera",
        "cargo_contacto": "Jefe de Calidad",
        "industria": "Química",
        "tipo_servicio": "electrico-comercial",
        "area_m2": 600
    },

    # Informes Ejecutivos APA (3)
    {
        "nombre": "EMPRESA DE TELECOMUNICACIONES SAC",
        "ruc": "20601234582",
        "email": "proyectos@telecom.pe",
        "telefono": "064-345678",
        "direccion": "Av. Torre Tagle 456, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Ing. Daniel Sánchez",
        "cargo_contacto": "Gerente de Infraestructura",
        "industria": "Telecomunicaciones",
        "tipo_servicio": "redes-datos",
        "area_m2": 1500
    },
    {
        "nombre": "DISTRIBUIDORA MAYORISTA LIMA SA",
        "ruc": "20601234583",
        "email": "logistica@dismaylima.com",
        "telefono": "064-356789",
        "direccion": "Parque Industrial Chilca, Lote 45",
        "ciudad": "Chilca",
        "departamento": "Junín",
        "persona_contacto": "Lic. Gabriela Flores",
        "cargo_contacto": "Gerente de Logística",
        "industria": "Distribución",
        "tipo_servicio": "cctv",
        "area_m2": 4000
    },
    {
        "nombre": "COMPAÑÍA INMOBILIARIA DEL SUR EIRL",
        "ruc": "20601234584",
        "email": "proyectos@inmosur.pe",
        "telefono": "964-890123",
        "direccion": "Jr. Real 789, Huancayo",
        "ciudad": "Huancayo",
        "departamento": "Junín",
        "persona_contacto": "Arq. Sofía Paredes",
        "cargo_contacto": "Directora de Proyectos",
        "industria": "Inmobiliaria",
        "tipo_servicio": "domotica",
        "area_m2": 2500
    }
]

# 📋 MAPEO DE SERVICIOS A DATOS DE ITEMS REALISTAS
ITEMS_POR_SERVICIO = {
    "electrico-residencial": [
        {"descripcion": "Tablero eléctrico trifásico 380V con interruptores termomagnéticos", "cantidad": 1, "unidad": "und", "precio_unitario": 850.0},
        {"descripcion": "Cableado eléctrico 2.5mm² (puntos de luz y tomacorrientes)", "cantidad": 35, "unidad": "pto", "precio_unitario": 45.0},
        {"descripcion": "Instalación de pozo a tierra con varilla cooperweld 2.40m", "cantidad": 1, "unidad": "und", "precio_unitario": 650.0},
        {"descripcion": "Luminarias LED empotrables 18W", "cantidad": 20, "unidad": "und", "precio_unitario": 75.0},
    ],
    "electrico-industrial": [
        {"descripcion": "Tablero de fuerza industrial 3Ø 380V - 200A", "cantidad": 1, "unidad": "und", "precio_unitario": 4500.0},
        {"descripcion": "Banco de condensadores para corrección de factor de potencia 50 kVAR", "cantidad": 1, "unidad": "und", "precio_unitario": 3200.0},
        {"descripcion": "Canalización con bandejas portacables 300mm", "cantidad": 80, "unidad": "m", "precio_unitario": 95.0},
        {"descripcion": "Cable de fuerza NYY 3x70mm² + 1x35mm²", "cantidad": 120, "unidad": "m", "precio_unitario": 125.0},
        {"descripcion": "Medidor de energía trifásico con comunicación Modbus", "cantidad": 1, "unidad": "und", "precio_unitario": 850.0},
    ],
    "electrico-comercial": [
        {"descripcion": "Tablero general 3Ø 380V - 100A con protecciones diferenciales", "cantidad": 1, "unidad": "und", "precio_unitario": 1800.0},
        {"descripcion": "Iluminación LED comercial (downlights + paneles)", "cantidad": 45, "unidad": "und", "precio_unitario": 85.0},
        {"descripcion": "Tomacorrientes dobles con puesta a tierra", "cantidad": 30, "unidad": "und", "precio_unitario": 35.0},
        {"descripcion": "Instalación de aire acondicionado (líneas eléctricas)", "cantidad": 5, "unidad": "pto", "precio_unitario": 450.0},
    ],
    "automatizacion": [
        {"descripcion": "PLC Siemens S7-1200 con módulos de E/S", "cantidad": 1, "unidad": "und", "precio_unitario": 5500.0},
        {"descripcion": "Variador de frecuencia ABB 15HP", "cantidad": 3, "unidad": "und", "precio_unitario": 2800.0},
        {"descripcion": "Panel HMI táctil 10\" Siemens KTP1000", "cantidad": 1, "unidad": "und", "precio_unitario": 3200.0},
        {"descripcion": "Sensores inductivos y capacitivos M18", "cantidad": 12, "unidad": "und", "precio_unitario": 85.0},
        {"descripcion": "Programación, configuración y puesta en marcha", "cantidad": 1, "unidad": "glb", "precio_unitario": 4500.0},
    ],
    "contraincendios": [
        {"descripcion": "Panel de control contra incendios direccionable", "cantidad": 1, "unidad": "und", "precio_unitario": 3800.0},
        {"descripcion": "Detectores de humo fotoeléctricos direccionables", "cantidad": 25, "unidad": "und", "precio_unitario": 180.0},
        {"descripcion": "Estación manual de alarma", "cantidad": 8, "unidad": "und", "precio_unitario": 120.0},
        {"descripcion": "Sirena estroboscópica audiovisual", "cantidad": 6, "unidad": "und", "precio_unitario": 250.0},
        {"descripcion": "Cableado resistente al fuego (cable FAS)", "cantidad": 200, "unidad": "m", "precio_unitario": 25.0},
    ],
    "redes-datos": [
        {"descripcion": "Switch POE+ Gigabit 24 puertos", "cantidad": 2, "unidad": "und", "precio_unitario": 1200.0},
        {"descripcion": "Rack de pared 12U con accesorios", "cantidad": 1, "unidad": "und", "precio_unitario": 850.0},
        {"descripcion": "Cableado estructurado Cat6A (certificado)", "cantidad": 48, "unidad": "pto", "precio_unitario": 120.0},
        {"descripcion": "Access Point WiFi 6 empresarial", "cantidad": 4, "unidad": "und", "precio_unitario": 650.0},
        {"descripcion": "Patch panels 24 puertos Cat6A", "cantidad": 2, "unidad": "und", "precio_unitario": 280.0},
    ],
    "cctv": [
        {"descripcion": "Cámara IP 4MP con IA (detección facial)", "cantidad": 16, "unidad": "und", "precio_unitario": 580.0},
        {"descripcion": "NVR 16 canales con disco duro 8TB", "cantidad": 1, "unidad": "und", "precio_unitario": 2200.0},
        {"descripcion": "Switch POE 16 puertos para cámaras", "cantidad": 1, "unidad": "und", "precio_unitario": 950.0},
        {"descripcion": "Monitor LED 43\" para visualización", "cantidad": 2, "unidad": "und", "precio_unitario": 1100.0},
        {"descripcion": "Cableado UTP Cat6 para cámaras", "cantidad": 300, "unidad": "m", "precio_unitario": 3.5},
    ],
    "itse": [
        {"descripcion": "Inspección técnica de seguridad en edificaciones", "cantidad": 1, "unidad": "glb", "precio_unitario": 1200.0},
        {"descripcion": "Elaboración de planos de seguridad (evacuación, señalización)", "cantidad": 1, "unidad": "glb", "precio_unitario": 800.0},
        {"descripcion": "Memoria descriptiva y cálculos de seguridad", "cantidad": 1, "unidad": "glb", "precio_unitario": 600.0},
        {"descripcion": "Tramitación de certificado ITSE ante autoridad", "cantidad": 1, "unidad": "glb", "precio_unitario": 450.0},
    ],
    "pozo-tierra": [
        {"descripcion": "Excavación de pozo a tierra (2.5m profundidad)", "cantidad": 1, "unidad": "und", "precio_unitario": 350.0},
        {"descripcion": "Varilla copperweld 2.40m x 5/8\" con accesorios", "cantidad": 3, "unidad": "und", "precio_unitario": 180.0},
        {"descripcion": "Tratamiento químico del terreno (THOR GEL)", "cantidad": 1, "unidad": "glb", "precio_unitario": 450.0},
        {"descripcion": "Cable desnudo de cobre 25mm²", "cantidad": 15, "unidad": "m", "precio_unitario": 28.0},
        {"descripcion": "Medición de resistencia de puesta a tierra (certificado)", "cantidad": 1, "unidad": "und", "precio_unitario": 250.0},
    ],
    "domotica": [
        {"descripcion": "Central de domótica (controlador inteligente)", "cantidad": 1, "unidad": "und", "precio_unitario": 2800.0},
        {"descripcion": "Interruptores inteligentes WiFi (dimmer)", "cantidad": 15, "unidad": "und", "precio_unitario": 95.0},
        {"descripcion": "Tomacorrientes inteligentes con medición de energía", "cantidad": 10, "unidad": "und", "precio_unitario": 85.0},
        {"descripcion": "Sensores de presencia y temperatura", "cantidad": 8, "unidad": "und", "precio_unitario": 120.0},
        {"descripcion": "Configuración de app móvil y automatizaciones", "cantidad": 1, "unidad": "glb", "precio_unitario": 1500.0},
    ],
}

def generar_items_realistas(tipo_servicio: str, area_m2: float):
    """Genera items realistas según el tipo de servicio"""

    # Obtener plantilla base
    items_base = ITEMS_POR_SERVICIO.get(tipo_servicio, ITEMS_POR_SERVICIO["electrico-residencial"])

    # Ajustar cantidades según área
    factor_escala = area_m2 / 150  # 150m² es referencia base

    items_ajustados = []
    for item in items_base:
        item_copy = item.copy()

        # Solo escalar items que dependen del área (no globales)
        if item_copy["unidad"] not in ["glb", "und"] or "Tablero" in item_copy["descripcion"]:
            # Escalar cantidad
            cantidad_base = item_copy["cantidad"]
            item_copy["cantidad"] = max(1, round(cantidad_base * factor_escala))

        items_ajustados.append(item_copy)

    return items_ajustados


def generar_documento_tipo(
    tipo: str,
    cliente_data: dict,
    word_gen: WordGenerator,
    db: SessionLocal
) -> dict:
    """
    Genera documento según tipo

    Args:
        tipo: "cotizacion-simple", "cotizacion-compleja", "proyecto-simple",
              "proyecto-pmi", "informe-tecnico", "informe-ejecutivo"
        cliente_data: Datos del cliente
        word_gen: Instancia de WordGenerator
        db: Sesión de base de datos

    Returns:
        Diccionario con resultado de la generación
    """

    logger.info(f"🎯 Generando {tipo} para {cliente_data['nombre']}")

    # Generar items realistas
    items = generar_items_realistas(
        cliente_data.get("tipo_servicio", "electrico-residencial"),
        cliente_data.get("area_m2", 150)
    )

    # Calcular totales
    subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items)
    igv = subtotal * 0.18
    total = subtotal + igv

    # Datos base para todos los documentos
    datos_base = {
        "cliente": {
            "nombre": cliente_data["nombre"],
            "ruc": cliente_data["ruc"],
            "email": cliente_data.get("email", ""),
            "telefono": cliente_data.get("telefono", ""),
            "direccion": cliente_data.get("direccion", ""),
            "ciudad": cliente_data.get("ciudad", "Huancayo"),
            "departamento": cliente_data.get("departamento", "Junín"),
            "persona_contacto": cliente_data.get("persona_contacto", ""),
            "cargo_contacto": cliente_data.get("cargo_contacto", "")
        }
    }

    # Generar datos específicos según tipo
    if "cotizacion" in tipo:
        datos_documento = {
            **datos_base,
            "proyecto": f"Proyecto {cliente_data.get('tipo_servicio', 'eléctrico').replace('-', ' ').title()} - {cliente_data['nombre'][:30]}",
            "servicio": cliente_data.get("tipo_servicio", "electrico-residencial"),
            "area_m2": cliente_data.get("area_m2", 150),
            "items": items,
            "subtotal": subtotal,
            "igv": igv,
            "total": total,
            "vigencia": "30 días calendario",
            "observaciones": f"Instalación según normativa peruana vigente. Precios incluyen IGV. Área: {cliente_data.get('area_m2', 150)} m²."
        }

        if "compleja" in tipo:
            datos_documento["complejidad"] = "complejo"
            datos_documento["descripcion"] = f"Proyecto integral de {cliente_data.get('tipo_servicio', 'instalación eléctrica').replace('-', ' ')} para {cliente_data.get('industria', 'empresa')} con área de {cliente_data.get('area_m2', 150)} m². Incluye diseño, suministro, instalación y puesta en marcha."

        agente = "PILI Cotizadora"
        tipo_doc = "cotizacion"

    elif "proyecto" in tipo:
        datos_documento = {
            **datos_base,
            "nombre_proyecto": f"Modernización {cliente_data.get('industria', 'Industrial')} - {cliente_data['nombre'][:40]}",
            "descripcion": f"Proyecto de {cliente_data.get('tipo_servicio', 'instalación').replace('-', ' ')} para {cliente_data.get('industria', 'empresa')}.",
            "fecha_inicio": "15/01/2025",
            "duracion_estimada": "12 semanas",
            "estado": "En Planificación",
            "presupuesto": total,
            "items": items,
            "subtotal": subtotal,
            "igv": igv,
            "total": total
        }

        if "pmi" in tipo:
            datos_documento["fases"] = [
                {"nombre": "Iniciación", "duracion": "2 semanas", "estado": "planificado"},
                {"nombre": "Planificación", "duracion": "3 semanas", "estado": "planificado"},
                {"nombre": "Ejecución", "duracion": "5 semanas", "estado": "planificado"},
                {"nombre": "Cierre", "duracion": "2 semanas", "estado": "planificado"}
            ]
            datos_documento["metodologia"] = "PMI PMBOK 7"

        agente = "PILI Coordinadora"
        tipo_doc = "proyecto"

    elif "informe" in tipo:
        datos_documento = {
            **datos_base,
            "titulo_informe": f"INFORME {'EJECUTIVO' if 'ejecutivo' in tipo else 'TÉCNICO'} - {cliente_data.get('tipo_servicio', 'SERVICIO').upper()}",
            "fecha_informe": datetime.now().strftime("%d/%m/%Y"),
            "autor": "TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.",
            "resumen_ejecutivo": f"El presente informe {'ejecutivo' if 'ejecutivo' in tipo else 'técnico'} analiza el proyecto de {cliente_data.get('tipo_servicio', 'instalación').replace('-', ' ')} para {cliente_data['nombre']}. Se evaluó un área de {cliente_data.get('area_m2', 150)} m² con inversión estimada de S/ {total:,.2f}.",
            "conclusiones": f"1. El proyecto es técnicamente viable.\n2. Inversión estimada: S/ {total:,.2f} (incluye IGV).\n3. Plazo de ejecución: 12 semanas.\n4. Cumple normativa peruana vigente.",
            "recomendaciones": "1. Iniciar proyecto en Q1 2025.\n2. Contratar empresa certificada.\n3. Implementar supervisión permanente.\n4. Realizar pruebas de calidad.",
            "items": items,
            "subtotal": subtotal,
            "igv": igv,
            "total": total
        }

        if "ejecutivo" in tipo:
            datos_documento["analisis_financiero"] = {
                "roi": "18% anual",
                "tir": "22%",
                "payback": "4.5 años",
                "van": f"S/ {total * 0.35:,.2f}"
            }

        agente = "PILI Reportera"
        tipo_doc = "informe"

    # Crear JSON PILI
    datos_json = {
        "datos_extraidos": datos_documento,
        "agente_responsable": agente,
        "tipo_servicio": cliente_data.get("tipo_servicio", "electrico-residencial")
    }

    # Generar nombre de archivo
    tipo_slug = tipo.replace("-", "_").upper()
    cliente_slug = cliente_data["nombre"][:30].replace(" ", "_").replace(".", "")
    ruta_salida = f"/home/user/TESLA_COTIZADOR-V3.0/storage/generados/EJEMPLOS_PROFESIONALES/{tipo_slug}_{cliente_slug}.docx"

    # 🎯 GENERAR DOCUMENTO CON BD
    resultado = word_gen.generar_desde_json_pili(
        datos_json=datos_json,
        tipo_documento=tipo_doc,
        db=db,  # ← Sesión de BD para guardar cliente
        opciones=None,
        logo_base64=None,
        ruta_salida=ruta_salida
    )

    return resultado


def main():
    """Función principal - genera los 18 documentos"""

    logger.info("=" * 80)
    logger.info("🎯 GENERADOR DE 18 DOCUMENTOS WORD PROFESIONALES + BD")
    logger.info("=" * 80)

    # Inicializar WordGenerator
    word_gen = WordGenerator()

    # Crear sesión de BD
    db = SessionLocal()

    # Contador de éxitos
    documentos_generados = []
    clientes_guardados = []
    errores = []

    try:
        # TIPOS DE DOCUMENTOS (6 tipos × 3 = 18)
        tipos_documentos = [
            # Cotizaciones Simples (3)
            "cotizacion-simple",
            "cotizacion-simple",
            "cotizacion-simple",

            # Cotizaciones Complejas (3)
            "cotizacion-compleja",
            "cotizacion-compleja",
            "cotizacion-compleja",

            # Proyectos Simples (3)
            "proyecto-simple",
            "proyecto-simple",
            "proyecto-simple",

            # Proyectos PMI (3)
            "proyecto-pmi",
            "proyecto-pmi",
            "proyecto-pmi",

            # Informes Técnicos (3)
            "informe-tecnico",
            "informe-tecnico",
            "informe-tecnico",

            # Informes Ejecutivos APA (3)
            "informe-ejecutivo",
            "informe-ejecutivo",
            "informe-ejecutivo"
        ]

        # Generar los 18 documentos
        for idx, (tipo, cliente_data) in enumerate(zip(tipos_documentos, CLIENTES), 1):
            logger.info(f"\n{'=' * 80}")
            logger.info(f"📄 DOCUMENTO {idx}/18: {tipo.upper()}")
            logger.info(f"👤 CLIENTE: {cliente_data['nombre']} (RUC: {cliente_data['ruc']})")
            logger.info(f"{'=' * 80}\n")

            try:
                # Generar documento
                resultado = generar_documento_tipo(tipo, cliente_data, word_gen, db)

                if resultado.get("exito"):
                    logger.info(f"✅ Documento generado: {resultado['nombre_archivo']}")
                    logger.info(f"📦 Tamaño: {resultado['tamano_bytes']:,} bytes")

                    documentos_generados.append({
                        "numero": idx,
                        "tipo": tipo,
                        "cliente": cliente_data["nombre"],
                        "ruc": cliente_data["ruc"],
                        "archivo": resultado["nombre_archivo"],
                        "tamano": resultado["tamano_bytes"]
                    })

                    clientes_guardados.append(cliente_data["nombre"])

                else:
                    logger.error(f"❌ Error: {resultado.get('error', 'Desconocido')}")
                    errores.append({
                        "numero": idx,
                        "tipo": tipo,
                        "cliente": cliente_data["nombre"],
                        "error": resultado.get("error", "Desconocido")
                    })

            except Exception as e:
                logger.error(f"❌ Error generando documento {idx}: {e}")
                errores.append({
                    "numero": idx,
                    "tipo": tipo,
                    "cliente": cliente_data["nombre"],
                    "error": str(e)
                })

        # Verificar clientes en BD
        logger.info(f"\n{'=' * 80}")
        logger.info("🔍 VERIFICANDO CLIENTES EN BASE DE DATOS")
        logger.info(f"{'=' * 80}\n")

        clientes_bd = db.query(Cliente).filter(
            Cliente.ruc.in_([c["ruc"] for c in CLIENTES])
        ).all()

        logger.info(f"✅ Clientes encontrados en BD: {len(clientes_bd)}/18")

        for cliente in clientes_bd:
            logger.info(f"  - {cliente.nombre} (RUC: {cliente.ruc})")

        # Generar reporte final
        logger.info(f"\n{'=' * 80}")
        logger.info("📊 RESUMEN FINAL")
        logger.info(f"{'=' * 80}\n")

        logger.info(f"✅ Documentos generados: {len(documentos_generados)}/18")
        logger.info(f"✅ Clientes guardados en BD: {len(clientes_bd)}/18")
        logger.info(f"❌ Errores: {len(errores)}")

        # Crear reporte MD
        reporte_path = "/home/user/TESLA_COTIZADOR-V3.0/storage/generados/EJEMPLOS_PROFESIONALES/REPORTE_18_DOCUMENTOS.md"

        with open(reporte_path, "w", encoding="utf-8") as f:
            f.write("# ✅ 18 DOCUMENTOS WORD PROFESIONALES GENERADOS\n\n")
            f.write(f"**Fecha de generación**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

            f.write("## 📊 Resumen:\n\n")
            f.write(f"- ✅ **Documentos generados**: {len(documentos_generados)}/18\n")
            f.write(f"- ✅ **Clientes guardados en BD**: {len(clientes_bd)}/18\n")
            f.write(f"- ❌ **Errores**: {len(errores)}\n\n")

            f.write("## 📁 Documentos generados:\n\n")

            # Agrupar por tipo
            tipos = {}
            for doc in documentos_generados:
                tipo = doc["tipo"]
                if tipo not in tipos:
                    tipos[tipo] = []
                tipos[tipo].append(doc)

            for tipo, docs in sorted(tipos.items()):
                f.write(f"### {tipo.upper().replace('-', ' ')} ({len(docs)} documentos)\n\n")
                for doc in docs:
                    f.write(f"{doc['numero']}. **{doc['archivo']}**\n")
                    f.write(f"   - Cliente: {doc['cliente']}\n")
                    f.write(f"   - RUC: {doc['ruc']}\n")
                    f.write(f"   - Tamaño: {doc['tamano']:,} bytes\n\n")

            f.write("## 👥 Clientes en Base de Datos:\n\n")
            f.write(f"Total: {len(clientes_bd)} clientes con RUCs únicos\n\n")

            f.write("```sql\n")
            f.write("SELECT id, nombre, ruc, ciudad FROM clientes\n")
            f.write("WHERE ruc IN (\n")
            f.write(",\n".join([f"  '{c['ruc']}'" for c in CLIENTES]))
            f.write("\n)\n")
            f.write("ORDER BY fecha_creacion DESC;\n")
            f.write("```\n\n")

            for cliente in clientes_bd:
                f.write(f"- ✅ **{cliente.nombre}** (RUC: {cliente.ruc}) - {cliente.ciudad}, {cliente.departamento}\n")

            if errores:
                f.write("\n## ❌ Errores encontrados:\n\n")
                for error in errores:
                    f.write(f"{error['numero']}. **{error['tipo']}** - {error['cliente']}\n")
                    f.write(f"   Error: {error['error']}\n\n")

        logger.info(f"\n✅ Reporte generado: {reporte_path}")

    finally:
        db.close()

    logger.info(f"\n{'=' * 80}")
    logger.info("🎉 PROCESO COMPLETADO")
    logger.info(f"{'=' * 80}\n")

    return {
        "total_documentos": len(documentos_generados),
        "total_clientes_bd": len(clientes_bd),
        "errores": len(errores)
    }


if __name__ == "__main__":
    resultado = main()

    print("\n" + "=" * 80)
    print("🎯 RESULTADO FINAL:")
    print("=" * 80)
    print(f"✅ Documentos generados: {resultado['total_documentos']}/18")
    print(f"✅ Clientes en BD: {resultado['total_clientes_bd']}/18")
    print(f"❌ Errores: {resultado['errores']}")
    print("=" * 80 + "\n")
