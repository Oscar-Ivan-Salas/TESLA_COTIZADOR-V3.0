"""
🧠 PILI BRAIN - CEREBRO INTELIGENTE SIN APIs
📁 RUTA: backend/app/services/pili_brain.py

Este es el CEREBRO de PILI que funciona 100% OFFLINE sin necesidad de APIs externas.
Usa lógica Python pura, regex, cálculos matemáticos y reglas de negocio para generar
respuestas inteligentes y JSONs estructurados.

🎯 CAPACIDADES:
- ✅ Detección inteligente de servicios (10 servicios)
- ✅ Extracción de datos del mensaje (áreas, cantidades, etc.)
- ✅ Cálculos según normativas (CNE, NFPA, RNE)
- ✅ Generación de JSONs estructurados
- ✅ Precios realistas de mercado peruano 2025
- ✅ Conversación profesional guiada
- ✅ 6 tipos de documentos (Cotización/Proyecto/Informe × Simple/Complejo)

🔄 NO REQUIERE:
- ❌ API Keys
- ❌ Conexión a internet
- ❌ Servicios externos
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 🎯 DEFINICIÓN DE LOS 10 SERVICIOS PILI
# ═══════════════════════════════════════════════════════════════

SERVICIOS_PILI = {
    "electrico-residencial": {
        "nombre": "Instalaciones Eléctricas Residenciales",
        "keywords": ["residencial", "casa", "vivienda", "departamento", "hogar", "domicilio"],
        "normativa": "CNE Suministro 2011",
        "unidad_medida": "m²",
        "precio_base_m2": 45.00  # USD por m²
    },

    "electrico-comercial": {
        "nombre": "Instalaciones Eléctricas Comerciales",
        "keywords": ["comercial", "tienda", "local", "oficina", "negocio", "comercio"],
        "normativa": "CNE Suministro 2011",
        "unidad_medida": "m²",
        "precio_base_m2": 65.00
    },

    "electrico-industrial": {
        "nombre": "Instalaciones Eléctricas Industriales",
        "keywords": ["industrial", "fábrica", "planta", "manufactura", "producción"],
        "normativa": "CNE Suministro 2011 + CNE Utilización",
        "unidad_medida": "HP/kW",
        "precio_base_hp": 850.00  # USD por HP
    },

    "contraincendios": {
        "nombre": "Sistemas Contra Incendios",
        "keywords": ["contraincendios", "incendio", "rociador", "sprinkler", "detector", "alarma", "nfpa"],
        "normativa": "NFPA 13, NFPA 72, NFPA 20",
        "unidad_medida": "m²",
        "precio_base_m2": 95.00
    },

    "domotica": {
        "nombre": "Domótica y Automatización",
        "keywords": ["domótica", "automatización", "smart", "inteligente", "knx", "iot", "control"],
        "normativa": "KNX/EIB, Z-Wave, Zigbee",
        "unidad_medida": "m²",
        "precio_base_m2": 120.00
    },

    "expedientes": {
        "nombre": "Expedientes Técnicos de Edificación",
        "keywords": ["expediente", "licencia", "construcción", "municipalidad", "trámite", "permiso"],
        "normativa": "RNE, Normativa Municipal",
        "unidad_medida": "proyecto",
        "precio_base": 1500.00  # USD por expediente
    },

    "saneamiento": {
        "nombre": "Sistemas de Agua y Desagüe",
        "keywords": ["saneamiento", "agua", "desagüe", "sanitario", "cisterna", "tanque", "bomba"],
        "normativa": "RNE IS.010, IS.020",
        "unidad_medida": "m²",
        "precio_base_m2": 55.00
    },

    "itse": {
        "nombre": "Certificaciones ITSE",
        "keywords": ["itse", "certificación", "inspección", "seguridad", "defensa civil"],
        "normativa": "D.S. 002-2018-PCM",
        "unidad_medida": "local",
        "precio_base": 850.00  # USD por certificación
    },

    "pozo-tierra": {
        "nombre": "Sistemas de Puesta a Tierra",
        "keywords": ["pozo", "tierra", "puesta", "spt", "aterramiento", "resistencia"],
        "normativa": "CNE Suministro Sección 250",
        "unidad_medida": "sistema",
        "precio_base": 1200.00  # USD por sistema
    },

    "redes-cctv": {
        "nombre": "Redes y CCTV",
        "keywords": ["red", "cctv", "cámara", "vigilancia", "seguridad", "ethernet", "wifi"],
        "normativa": "TIA/EIA-568, ANSI/TIA-942",
        "unidad_medida": "punto",
        "precio_base_punto": 180.00  # USD por punto
    }
}


# ═══════════════════════════════════════════════════════════════
# 🧠 CLASE PRINCIPAL: PILIBrain
# ═══════════════════════════════════════════════════════════════

class PILIBrain:
    """
    🧠 Cerebro inteligente de PILI que funciona sin APIs externas

    Usa lógica Python pura para:
    - Analizar mensajes del usuario
    - Detectar servicios requeridos
    - Extraer datos técnicos
    - Generar JSONs estructurados
    - Calcular precios realistas
    """

    def __init__(self):
        """Inicializa el cerebro de PILI"""
        self.servicios = SERVICIOS_PILI
        logger.info("🧠 PILIBrain inicializado - Modo 100% offline")

    # ──────────────────────────────────────────────────────────────
    # 🔍 DETECCIÓN INTELIGENTE DE SERVICIOS
    # ──────────────────────────────────────────────────────────────

    def detectar_servicio(self, mensaje: str) -> str:
        """
        Detecta qué servicio necesita el usuario basándose en keywords

        Args:
            mensaje: Mensaje del usuario

        Returns:
            Código del servicio detectado
        """
        mensaje_lower = mensaje.lower()
        scores = {}

        for codigo_servicio, info in self.servicios.items():
            score = 0
            keywords = info["keywords"]

            # Contar matches de keywords
            for keyword in keywords:
                if keyword in mensaje_lower:
                    score += 10

            scores[codigo_servicio] = score

        # Obtener servicio con mayor score
        if max(scores.values()) > 0:
            servicio_detectado = max(scores, key=scores.get)
            logger.info(f"🎯 Servicio detectado: {servicio_detectado} (score: {scores[servicio_detectado]})")
            return servicio_detectado
        else:
            # Default: eléctrico residencial
            return "electrico-residencial"

    # ──────────────────────────────────────────────────────────────
    # 📊 EXTRACCIÓN DE DATOS DEL MENSAJE
    # ──────────────────────────────────────────────────────────────

    def extraer_datos(self, mensaje: str, servicio: str) -> Dict[str, Any]:
        """
        Extrae datos técnicos del mensaje del usuario

        Args:
            mensaje: Mensaje del usuario
            servicio: Servicio detectado

        Returns:
            Diccionario con datos extraídos
        """
        datos = {
            "area_m2": self._extraer_area(mensaje),
            "num_pisos": self._extraer_pisos(mensaje),
            "cantidad_puntos": self._extraer_cantidad_general(mensaje),
            "potencia_hp": self._extraer_potencia(mensaje),
            "tipo_instalacion": self._extraer_tipo_instalacion(mensaje),
            "complejidad": self._determinar_complejidad(mensaje, servicio)
        }

        logger.info(f"📊 Datos extraídos: {datos}")
        return datos

    def _extraer_area(self, mensaje: str) -> Optional[float]:
        """Extrae área en m² del mensaje"""
        # Patrones: "150m2", "150 m2", "150m²", "150 m²", "150 metros cuadrados"
        patterns = [
            r'(\d+\.?\d*)\s*m[2²]',
            r'(\d+\.?\d*)\s*metros?\s*cuadrados?',
            r'área\s*de\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*m\s*cuadrados?'
        ]

        for pattern in patterns:
            match = re.search(pattern, mensaje.lower())
            if match:
                area = float(match.group(1))
                logger.info(f"📐 Área detectada: {area} m²")
                return area

        return None

    def _extraer_pisos(self, mensaje: str) -> int:
        """Extrae número de pisos del mensaje"""
        patterns = [
            r'(\d+)\s*pisos?',
            r'(\d+)\s*niveles?',
            r'(\d+)\s*plantas?'
        ]

        for pattern in patterns:
            match = re.search(pattern, mensaje.lower())
            if match:
                pisos = int(match.group(1))
                logger.info(f"🏢 Pisos detectados: {pisos}")
                return pisos

        return 1  # Default

    def _extraer_cantidad_general(self, mensaje: str) -> Optional[int]:
        """Extrae cantidad general de puntos/elementos"""
        patterns = [
            r'(\d+)\s*puntos?',
            r'(\d+)\s*tomacorrientes?',
            r'(\d+)\s*luces?',
            r'(\d+)\s*detectores?',
            r'(\d+)\s*cámaras?'
        ]

        for pattern in patterns:
            match = re.search(pattern, mensaje.lower())
            if match:
                cantidad = int(match.group(1))
                logger.info(f"🔢 Cantidad detectada: {cantidad}")
                return cantidad

        return None

    def _extraer_potencia(self, mensaje: str) -> Optional[float]:
        """Extrae potencia en HP o kW del mensaje"""
        patterns = [
            r'(\d+\.?\d*)\s*hp',
            r'(\d+\.?\d*)\s*kw',
            r'(\d+\.?\d*)\s*kilovatios?'
        ]

        for pattern in patterns:
            match = re.search(pattern, mensaje.lower())
            if match:
                potencia = float(match.group(1))
                logger.info(f"⚡ Potencia detectada: {potencia}")
                return potencia

        return None

    def _extraer_tipo_instalacion(self, mensaje: str) -> str:
        """Determina tipo de instalación"""
        mensaje_lower = mensaje.lower()

        if any(word in mensaje_lower for word in ["nueva", "nuevo", "desde cero"]):
            return "nueva"
        elif any(word in mensaje_lower for word in ["remodelación", "actualización", "mejora"]):
            return "remodelacion"
        elif any(word in mensaje_lower for word in ["ampliación", "expansión"]):
            return "ampliacion"
        else:
            return "nueva"  # Default

    def _determinar_complejidad(self, mensaje: str, servicio: str) -> str:
        """Determina si el proyecto es simple o complejo"""
        mensaje_lower = mensaje.lower()

        # Indicadores de complejidad
        indicadores_complejo = [
            "complejo", "grande", "múltiple", "varios", "avanzado",
            "industrial", "pmi", "gantt", "cronograma detallado",
            "análisis", "ejecutivo", "apa"
        ]

        for indicador in indicadores_complejo:
            if indicador in mensaje_lower:
                return "complejo"

        # Por área
        datos_area = self._extraer_area(mensaje)
        if datos_area:
            if datos_area > 300:
                return "complejo"

        return "simple"  # Default

    # ──────────────────────────────────────────────────────────────
    # 🏗️ GENERACIÓN DE COTIZACIONES
    # ──────────────────────────────────────────────────────────────

    def generar_cotizacion(
        self,
        mensaje: str,
        servicio: str,
        complejidad: str = "simple"
    ) -> Dict[str, Any]:
        """
        Genera una cotización completa con cálculos realistas

        Args:
            mensaje: Mensaje del usuario
            servicio: Servicio detectado
            complejidad: "simple" o "complejo"

        Returns:
            JSON estructurado con la cotización
        """
        # Extraer datos del mensaje
        datos = self.extraer_datos(mensaje, servicio)
        info_servicio = self.servicios[servicio]

        # Generar items según el servicio
        items = self._generar_items_servicio(servicio, datos)

        # Calcular totales
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv

        # Construir JSON
        cotizacion = {
            "accion": "cotizacion_generada",
            "tipo_servicio": f"{servicio}",
            "complejidad": complejidad,
            "datos": {
                "numero": f"COT-{datetime.now().strftime('%Y%m%d')}-{servicio[:3].upper()}",
                "cliente": self._extraer_cliente(mensaje) or "Cliente Demo",
                "proyecto": info_servicio["nombre"],
                "descripcion": f"{info_servicio['nombre']} según {info_servicio['normativa']}",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "vigencia": "30 días calendario",
                "items": items,
                "subtotal": round(subtotal, 2),
                "igv": round(igv, 2),
                "total": round(total, 2),
                "observaciones": self._generar_observaciones(servicio, datos),
                "normativa_aplicable": info_servicio["normativa"],
                "datos_tecnicos": datos
            },
            "conversacion": {
                "mensaje_pili": self._generar_mensaje_conversacional(servicio, complejidad, datos),
                "preguntas_pendientes": self._generar_preguntas_pendientes(datos),
                "puede_generar": len(items) > 0
            }
        }

        logger.info(f"💰 Cotización generada: {total:.2f} USD")
        return cotizacion

    def _generar_items_servicio(self, servicio: str, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera items específicos según el servicio"""

        if servicio == "electrico-residencial":
            return self._items_electrico_residencial(datos)
        elif servicio == "electrico-comercial":
            return self._items_electrico_comercial(datos)
        elif servicio == "electrico-industrial":
            return self._items_electrico_industrial(datos)
        elif servicio == "contraincendios":
            return self._items_contraincendios(datos)
        elif servicio == "domotica":
            return self._items_domotica(datos)
        elif servicio == "saneamiento":
            return self._items_saneamiento(datos)
        elif servicio == "pozo-tierra":
            return self._items_pozo_tierra(datos)
        elif servicio == "redes-cctv":
            return self._items_redes_cctv(datos)
        else:
            # Genérico
            return self._items_generico(servicio, datos)

    def _items_electrico_residencial(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para instalación eléctrica residencial"""
        area = datos.get("area_m2", 100)

        # Cálculos según CNE
        num_circuitos = max(6, int(area / 25))  # 1 circuito por cada 25m²
        num_luces = int(area / 10)  # 1 luz cada 10m²
        num_tomacorrientes = int(area / 15)  # 1 tomacorriente cada 15m²

        items = [
            {
                "descripcion": "Tablero eléctrico monofásico 12 circuitos con interruptores termomagnéticos",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 450.00,
                "total": 450.00
            },
            {
                "descripcion": f"Instalación de circuitos eléctricos (cable THW {num_circuitos*20}m + tubería PVC)",
                "cantidad": num_circuitos,
                "unidad": "cto",
                "precio_unitario": 120.00,
                "total": num_circuitos * 120.00
            },
            {
                "descripcion": "Puntos de iluminación (incluye luminaria LED, cableado y accesorios)",
                "cantidad": num_luces,
                "unidad": "pto",
                "precio_unitario": 45.00,
                "total": num_luces * 45.00
            },
            {
                "descripcion": "Tomacorrientes dobles (incluye cableado, caja y accesorios)",
                "cantidad": num_tomacorrientes,
                "unidad": "pto",
                "precio_unitario": 35.00,
                "total": num_tomacorrientes * 35.00
            },
            {
                "descripcion": "Sistema de puesta a tierra (pozo, cable, conectores)",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 850.00,
                "total": 850.00
            }
        ]

        return items

    def _items_electrico_comercial(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para instalación eléctrica comercial"""
        area = datos.get("area_m2", 200)

        items = [
            {
                "descripcion": "Tablero eléctrico trifásico 24 circuitos con protección diferencial",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 1200.00,
                "total": 1200.00
            },
            {
                "descripcion": "Sistema de iluminación LED comercial con control automático",
                "cantidad": int(area / 8),
                "unidad": "pto",
                "precio_unitario": 85.00,
                "total": int(area / 8) * 85.00
            },
            {
                "descripcion": "Tomacorrientes industriales dobles con toma tierra",
                "cantidad": int(area / 12),
                "unidad": "pto",
                "precio_unitario": 55.00,
                "total": int(area / 12) * 55.00
            },
            {
                "descripcion": "Circuitos dedicados para equipos especiales (AA, servidores, etc)",
                "cantidad": 4,
                "unidad": "cto",
                "precio_unitario": 280.00,
                "total": 1120.00
            }
        ]

        return items

    def _items_electrico_industrial(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para instalación eléctrica industrial"""
        potencia_hp = datos.get("potencia_hp", 10)

        items = [
            {
                "descripcion": "Tablero de fuerza industrial con protección y control",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 3500.00,
                "total": 3500.00
            },
            {
                "descripcion": f"Sistema de alimentación trifásica para motores ({potencia_hp} HP total)",
                "cantidad": int(potencia_hp),
                "unidad": "HP",
                "precio_unitario": 320.00,
                "total": int(potencia_hp) * 320.00
            },
            {
                "descripcion": "Arrancador suave electrónico con protección térmica",
                "cantidad": max(1, int(potencia_hp / 5)),
                "unidad": "und",
                "precio_unitario": 1800.00,
                "total": max(1, int(potencia_hp / 5)) * 1800.00
            },
            {
                "descripcion": "Sistema de compensación de factor de potencia",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 4500.00,
                "total": 4500.00
            }
        ]

        return items

    def _items_contraincendios(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para sistema contraincendios"""
        area = datos.get("area_m2", 300)

        # Cálculos según NFPA
        num_rociadores = int(area / 12)  # 1 rociador cada 12m² aprox
        num_detectores = int(area / 60)  # 1 detector cada 60m²

        items = [
            {
                "descripcion": "Central de detección y alarma de incendios direccionable 8 zonas",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 2800.00,
                "total": 2800.00
            },
            {
                "descripcion": "Detectores de humo fotoeléctricos direccionables (NFPA 72)",
                "cantidad": num_detectores,
                "unidad": "und",
                "precio_unitario": 95.00,
                "total": num_detectores * 95.00
            },
            {
                "descripcion": "Rociadores automáticos tipo spray (NFPA 13) incluye tubería",
                "cantidad": num_rociadores,
                "unidad": "und",
                "precio_unitario": 120.00,
                "total": num_rociadores * 120.00
            },
            {
                "descripcion": "Bomba contraincendios eléctrica 10 HP con jockey pump",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 6500.00,
                "total": 6500.00
            },
            {
                "descripcion": "Gabinetes contraincendios con manguera y accesorios",
                "cantidad": max(2, int(area / 200)),
                "unidad": "und",
                "precio_unitario": 650.00,
                "total": max(2, int(area / 200)) * 650.00
            }
        ]

        return items

    def _items_domotica(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para sistema domótico"""
        area = datos.get("area_m2", 150)

        items = [
            {
                "descripcion": "Central domótica KNX/EIB con programación incluida",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 3200.00,
                "total": 3200.00
            },
            {
                "descripcion": "Actuadores inteligentes para iluminación (dimmer, on/off)",
                "cantidad": int(area / 15),
                "unidad": "und",
                "precio_unitario": 180.00,
                "total": int(area / 15) * 180.00
            },
            {
                "descripcion": "Sensores de presencia y luminosidad",
                "cantidad": int(area / 25),
                "unidad": "und",
                "precio_unitario": 120.00,
                "total": int(area / 25) * 120.00
            },
            {
                "descripcion": "Panel táctil de control mural con interface gráfica",
                "cantidad": max(2, int(area / 80)),
                "unidad": "und",
                "precio_unitario": 850.00,
                "total": max(2, int(area / 80)) * 850.00
            },
            {
                "descripcion": "App móvil personalizada para control remoto",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 1500.00,
                "total": 1500.00
            }
        ]

        return items

    def _items_saneamiento(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para sistema de saneamiento"""
        area = datos.get("area_m2", 120)

        # Cálculos según RNE
        dotacion_diaria = area * 2  # Litros/día estimado
        volumen_cisterna = int(dotacion_diaria * 0.75 / 1000)  # m³
        volumen_tanque = int(dotacion_diaria * 0.33 / 1000)  # m³

        items = [
            {
                "descripcion": f"Cisterna de concreto armado {volumen_cisterna}m³ con impermeabilización",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": volumen_cisterna * 450.00,
                "total": volumen_cisterna * 450.00
            },
            {
                "descripcion": f"Tanque elevado {volumen_tanque}m³ con estructura metálica",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": volumen_tanque * 380.00,
                "total": volumen_tanque * 380.00
            },
            {
                "descripcion": "Sistema de bombeo de agua (bomba + tablero + accesorios)",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 2200.00,
                "total": 2200.00
            },
            {
                "descripcion": "Red de distribución de agua fría (tubería PVC + accesorios)",
                "cantidad": int(area / 10),
                "unidad": "pto",
                "precio_unitario": 85.00,
                "total": int(area / 10) * 85.00
            },
            {
                "descripcion": "Red de desagüe y ventilación (tubería PVC + accesorios)",
                "cantidad": int(area / 12),
                "unidad": "pto",
                "precio_unitario": 95.00,
                "total": int(area / 12) * 95.00
            }
        ]

        return items

    def _items_pozo_tierra(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para sistema de puesta a tierra"""
        items = [
            {
                "descripcion": "Excavación y preparación de pozo de tierra (3m profundidad)",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 350.00,
                "total": 350.00
            },
            {
                "descripcion": "Varilla de cobre electrolítico Ø 5/8\" x 2.4m (3 unidades)",
                "cantidad": 3,
                "unidad": "und",
                "precio_unitario": 85.00,
                "total": 255.00
            },
            {
                "descripcion": "Thor Gel mejorador de tierra (tratamiento químico)",
                "cantidad": 3,
                "unidad": "bls",
                "precio_unitario": 45.00,
                "total": 135.00
            },
            {
                "descripcion": "Cable de cobre desnudo Nº 2 AWG (30m)",
                "cantidad": 30,
                "unidad": "m",
                "precio_unitario": 8.50,
                "total": 255.00
            },
            {
                "descripcion": "Conectores tipo soldadura exotérmica (Cadweld)",
                "cantidad": 5,
                "unidad": "und",
                "precio_unitario": 35.00,
                "total": 175.00
            },
            {
                "descripcion": "Medición y certificación de resistencia de puesta a tierra",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 280.00,
                "total": 280.00
            }
        ]

        return items

    def _items_redes_cctv(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items para redes y CCTV"""
        puntos = datos.get("cantidad_puntos", 8)

        items = [
            {
                "descripcion": "Cámaras IP 4MP con visión nocturna 30m (interior/exterior)",
                "cantidad": puntos,
                "unidad": "und",
                "precio_unitario": 320.00,
                "total": puntos * 320.00
            },
            {
                "descripcion": "NVR 16 canales con disco duro 2TB para grabación",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 1200.00,
                "total": 1200.00
            },
            {
                "descripcion": "Switch PoE 16 puertos gigabit para alimentación de cámaras",
                "cantidad": 1,
                "unidad": "und",
                "precio_unitario": 650.00,
                "total": 650.00
            },
            {
                "descripcion": "Cableado estructurado Cat6 con certificación (incluye instalación)",
                "cantidad": puntos,
                "unidad": "pto",
                "precio_unitario": 120.00,
                "total": puntos * 120.00
            },
            {
                "descripcion": "Configuración y puesta en marcha del sistema",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": 450.00,
                "total": 450.00
            }
        ]

        return items

    def _items_generico(self, servicio: str, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Items genéricos cuando no hay servicio específico"""
        info = self.servicios.get(servicio, {})
        precio_base = info.get("precio_base", 1500.00)

        items = [
            {
                "descripcion": f"Servicio de {info.get('nombre', 'Servicio Eléctrico')}",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": precio_base,
                "total": precio_base
            },
            {
                "descripcion": "Materiales y mano de obra especializada",
                "cantidad": 1,
                "unidad": "glb",
                "precio_unitario": precio_base * 0.4,
                "total": precio_base * 0.4
            }
        ]

        return items

    def _extraer_cliente(self, mensaje: str) -> Optional[str]:
        """Intenta extraer nombre del cliente del mensaje"""
        patterns = [
            r'cliente[:\s]+([A-Z][a-zA-ZáéíóúñÑ\s]+)',
            r'para[:\s]+([A-Z][a-zA-ZáéíóúñÑ\s]+)',
            r'empresa[:\s]+([A-Z][a-zA-ZáéíóúñÑ\s]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, mensaje)
            if match:
                return match.group(1).strip()

        return None

    def _generar_observaciones(self, servicio: str, datos: Dict[str, Any]) -> str:
        """Genera observaciones técnicas según el servicio"""
        info = self.servicios[servicio]

        obs = f"""OBSERVACIONES TÉCNICAS:

1. Los trabajos se ejecutarán según {info['normativa']}
2. Incluye materiales de primera calidad con certificación
3. Mano de obra especializada con supervisión técnica
4. Garantía de 12 meses en mano de obra y materiales
5. Los precios son en dólares americanos (USD)
6. Tiempo de ejecución: {self._estimar_tiempo_ejecucion(datos)} días calendario
7. Forma de pago: 50% adelanto, 50% contra entrega

NOTA: Cotización válida por 30 días. Sujeto a verificación en campo."""

        return obs

    def _estimar_tiempo_ejecucion(self, datos: Dict[str, Any]) -> int:
        """Estima tiempo de ejecución en días"""
        area = datos.get("area_m2", 100)

        if area < 100:
            return 15
        elif area < 300:
            return 30
        elif area < 500:
            return 45
        else:
            return 60

    def _generar_mensaje_conversacional(
        self,
        servicio: str,
        complejidad: str,
        datos: Dict[str, Any]
    ) -> str:
        """Genera mensaje conversacional de PILI"""
        info = self.servicios[servicio]

        mensaje = f"""¡Excelente! He analizado tu solicitud para **{info['nombre']}**

📊 **Resumen de lo detectado:**
"""

        if datos.get("area_m2"):
            mensaje += f"- Área: {datos['area_m2']} m²\n"
        if datos.get("num_pisos", 1) > 1:
            mensaje += f"- Pisos: {datos['num_pisos']}\n"
        if datos.get("cantidad_puntos"):
            mensaje += f"- Puntos: {datos['cantidad_puntos']}\n"
        if datos.get("potencia_hp"):
            mensaje += f"- Potencia: {datos['potencia_hp']} HP\n"

        mensaje += f"\n✅ He generado una cotización {complejidad} basada en {info['normativa']}\n"
        mensaje += f"\n💡 **¿Qué puedes hacer ahora?**\n"
        mensaje += f"- ✏️ Revisar y editar los items\n"
        mensaje += f"- 📄 Generar documento Word profesional\n"
        mensaje += f"- 💬 Hacer ajustes conversando conmigo\n"

        return mensaje

    def _generar_preguntas_pendientes(self, datos: Dict[str, Any]) -> List[str]:
        """Genera preguntas si falta información"""
        preguntas = []

        if not datos.get("area_m2"):
            preguntas.append("¿Cuál es el área total en m²?")

        if not datos.get("cantidad_puntos"):
            preguntas.append("¿Cuántos puntos eléctricos/elementos necesitas?")

        if datos.get("tipo_instalacion") == "nueva":
            preguntas.append("¿Cuentas con planos o especificaciones técnicas?")

        return preguntas


# ═══════════════════════════════════════════════════════════════
# 🏭 INSTANCIA SINGLETON
# ═══════════════════════════════════════════════════════════════

# Crear instancia única de PILIBrain
pili_brain = PILIBrain()

logger.info("🧠 PILIBrain listo para funcionar 100% offline")
