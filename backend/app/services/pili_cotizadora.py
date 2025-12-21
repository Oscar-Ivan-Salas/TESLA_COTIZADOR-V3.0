"""
🎯 PILI COTIZADORA - Especialista en Cotizaciones Inteligentes
📁 RUTA: backend/app/services/pili_cotizadora.py

PILI Cotizadora es el agente especializado en generar cotizaciones profesionales
para los 10 servicios de Tesla Electricidad con conversación guiada paso a paso.

🔧 SERVICIOS MANEJADOS (10):
1. ⚡ Instalaciones Eléctricas (Residencial/Comercial/Industrial)
2. 📋 Certificados ITSE
3. 🔌 Puestas a Tierra (Pozos SPT)
4. 🔥 Sistemas Contra Incendios
5. 🏠 Domótica y Automatización
6. 📹 CCTV
7. 🌐 Redes de Datos
8. ⚙️ Automatización Industrial
9. 🚰 Saneamiento (Agua y Desagüe)
10. 📄 Expedientes Técnicos

🎯 CAPACIDADES:
- ✅ Conversación guiada paso a paso
- ✅ Preguntas específicas por servicio
- ✅ Validación de respuestas
- ✅ Cálculos automáticos según normativas
- ✅ Detección automática de servicio
- ✅ Generación de JSON estructurado
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Importar el cerebro base para reutilizar lógica
from app.services.pili_brain import PILIBrain, SERVICIOS_PILI

logger = logging.getLogger(__name__)


class PILICotizadora:
    """
    🎯 Especialista PILI en Cotizaciones

    Guía al usuario conversacionalmente para obtener toda la información
    necesaria y generar cotizaciones profesionales para 10 servicios.
    """

    def __init__(self):
        """Inicializa PILI Cotizadora"""
        self.brain = PILIBrain()
        self.servicios = SERVICIOS_PILI
        logger.info("🎯 PILI Cotizadora inicializada - 10 servicios activos")

    def procesar(self, mensaje: str, historial: List[Dict]) -> Dict[str, Any]:
        """
        Procesa mensaje del usuario y guía la cotización

        Args:
            mensaje: Mensaje del usuario
            historial: Historial de conversación

        Returns:
            Respuesta con pregunta siguiente o cotización generada
        """
        # 1. DETECTAR SERVICIO
        servicio = self._detectar_servicio_contexto(mensaje, historial)

        if not servicio:
            # Preguntar qué servicio necesita
            return self._preguntar_servicio()

        # 2. EXTRAER DATOS DEL HISTORIAL
        datos_recopilados = self._extraer_datos_historial(historial, mensaje)
        datos_recopilados["servicio"] = servicio

        # 3. VERIFICAR QUÉ DATOS FALTAN Y HACER PREGUNTAS
        pregunta = self._siguiente_pregunta(servicio, datos_recopilados)

        if pregunta:
            # AÚN FALTAN DATOS
            return pregunta

        # 4. YA TENEMOS TODO - GENERAR COTIZACIÓN
        return self._generar_cotizacion_final(servicio, datos_recopilados)

    def _detectar_servicio_contexto(self, mensaje: str, historial: List[Dict]) -> Optional[str]:
        """Detecta servicio usando mensaje actual e historial"""

        # Primero intentar detectar del mensaje actual
        servicio = self.brain.detectar_servicio(mensaje)

        # Si ya hay servicio en el historial, mantenerlo
        for msg in reversed(historial):
            contenido = msg.get("content", "").lower()

            # Buscar si ya eligió un servicio
            if "eléctric" in contenido or "electrico" in contenido or "instalacion" in contenido:
                if "residencial" in contenido or "casa" in contenido or "vivienda" in contenido:
                    return "electrico-residencial"
                elif "comercial" in contenido or "tienda" in contenido or "oficina" in contenido:
                    return "electrico-comercial"
                elif "industrial" in contenido or "fábrica" in contenido or "planta" in contenido:
                    return "electrico-industrial"

            if "itse" in contenido or "certificación" in contenido or "certificado" in contenido:
                return "itse"

            if "pozo" in contenido or "tierra" in contenido or "puesta" in contenido:
                return "pozo-tierra"

            if "contraincendio" in contenido or "incendio" in contenido or "sprinkler" in contenido:
                return "contraincendios"

            if "domótica" in contenido or "domotica" in contenido or "smart" in contenido:
                return "domotica"

            if "cctv" in contenido or "cámara" in contenido or "vigilancia" in contenido:
                return "redes-cctv"

            if "red" in contenido and ("datos" in contenido or "ethernet" in contenido):
                return "redes-cctv"

            if "saneamiento" in contenido or "agua" in contenido or "desagüe" in contenido:
                return "saneamiento"

            if "expediente" in contenido or "licencia" in contenido or "trámite" in contenido:
                return "expedientes"

        return servicio if servicio else None

    def _preguntar_servicio(self) -> Dict[str, Any]:
        """Pregunta qué servicio necesita cotizar"""
        return {
            "accion": "solicitar_info",
            "mensaje_pili": "¡Hola! Soy **PILI Cotizadora**, especialista en cotizaciones eléctricas. ⚡\n\n¿Qué servicio necesitas cotizar?",
            "botones": [
                "⚡ Instalación Eléctrica",
                "📋 Certificado ITSE",
                "🔌 Pozo a Tierra",
                "🔥 Contra Incendios",
                "🏠 Domótica",
                "📹 CCTV",
                "🌐 Redes de Datos",
                "⚙️ Automatización",
                "🚰 Saneamiento",
                "📄 Expediente Técnico"
            ],
            "campo_esperado": "servicio",
            "puede_generar": False
        }

    def _extraer_datos_historial(self, historial: List[Dict], mensaje_actual: str) -> Dict[str, Any]:
        """Extrae todos los datos ya recopilados del historial"""
        datos = {}

        # Combinar historial + mensaje actual
        todos_mensajes = " ".join([msg.get("content", "") for msg in historial]) + " " + mensaje_actual

        # Extraer con regex los datos clave
        datos["cliente"] = self._extraer_cliente(todos_mensajes)
        datos["area_m2"] = self._extraer_numero(todos_mensajes, ["metros", "m2", "m²", "área"])
        datos["puntos_luz"] = self._extraer_numero(todos_mensajes, ["puntos de luz", "luces", "luminarias"])
        datos["tomacorrientes"] = self._extraer_numero(todos_mensajes, ["tomacorrientes", "tomas", "enchufes"])
        datos["pisos"] = self._extraer_numero(todos_mensajes, ["pisos", "niveles", "plantas"])
        datos["tipo_instalacion"] = self._extraer_tipo(todos_mensajes)
        datos["descripcion"] = self._extraer_descripcion(todos_mensajes)

        return datos

    def _extraer_numero(self, texto: str, keywords: List[str]) -> Optional[float]:
        """Extrae un número asociado a palabras clave"""
        for keyword in keywords:
            # Buscar patrón: número + keyword o keyword + número
            patron1 = rf'(\d+(?:\.\d+)?)\s*{keyword}'
            patron2 = rf'{keyword}\s*(\d+(?:\.\d+)?)'

            match = re.search(patron1, texto, re.IGNORECASE)
            if not match:
                match = re.search(patron2, texto, re.IGNORECASE)

            if match:
                return float(match.group(1))

        return None

    def _extraer_cliente(self, texto: str) -> Optional[str]:
        """Extrae nombre del cliente"""
        # Buscar patrón: "cliente: X" o "para X"
        patron = r'(?:cliente|para|de)\s+([A-ZÁÉÍÓÚ][a-záéíóúñ\s]+(?:[A-ZÁÉÍÓÚ][a-záéíóúñ\s]+)*)'
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _extraer_tipo(self, texto: str) -> Optional[str]:
        """Extrae tipo de instalación"""
        texto_lower = texto.lower()
        if any(word in texto_lower for word in ["residencial", "casa", "vivienda", "departamento"]):
            return "residencial"
        elif any(word in texto_lower for word in ["comercial", "tienda", "local", "oficina"]):
            return "comercial"
        elif any(word in texto_lower for word in ["industrial", "fábrica", "planta"]):
            return "industrial"
        return None

    def _extraer_descripcion(self, texto: str) -> str:
        """Extrae descripción general del proyecto"""
        # Tomar las primeras 200 caracteres que no sean preguntas
        lineas = [l for l in texto.split(".") if "?" not in l and len(l) > 20]
        return lineas[0][:200] if lineas else "Proyecto eléctrico"

    def _siguiente_pregunta(self, servicio: str, datos: Dict) -> Optional[Dict]:
        """
        Determina cuál es la siguiente pregunta a hacer según el servicio

        Returns:
            None si ya tiene todos los datos, o dict con la pregunta
        """

        # SERVICIO: INSTALACIONES ELÉCTRICAS
        if servicio.startswith("electrico"):

            # Pregunta 1: Tipo de instalación (mejorada con contexto)
            if not datos.get("tipo_instalacion"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": """¡Hola! Soy especialista en **Instalaciones Eléctricas** según el **Código Nacional de Electricidad (CNE) - Utilización 2011**.

⚡ **Primero necesito conocer el tipo de instalación:**

💡 **¿Por qué es importante?**
Cada tipo tiene requisitos ESPECÍFICOS según CNE:

🏠 **RESIDENCIAL** (Viviendas, Casas, Departamentos):
- **Carga mínima**: 3,000 W base + 1,500 W por circuito adicional
- **Circuitos**: Mínimo 2 (iluminación + tomacorrientes)
- **Protección**: Interruptores termomagnéticos 16A-20A
- **Cables**: THW o THHN calibre #14 o #12 AWG
- **Ejemplo típico**: Casa 100 m² → 5 circuitos, 6 kW

🏢 **COMERCIAL** (Oficinas, Tiendas, Locales):
- **Carga mínima**: 30 VA/m² (CNE Tabla 220-3b)
- **Circuitos**: Separación iluminación/tomacorrientes obligatoria
- **Tableros**: Mínimo 20% reserva para ampliaciones
- **Alumbrado emergencia**: Obligatorio según A.130
- **Ejemplo típico**: Oficina 200 m² → 6 kW, 8 circuitos

🏭 **INDUSTRIAL** (Fábricas, Talleres, Almacenes):
- **Carga**: Según maquinaria instalada (motores, hornos)
- **Tableros**: Trifásico 380V/220V
- **Conductores**: Calibre según caída de tensión ≤ 2.5%
- **Factor de potencia**: Corrección obligatoria (condensadores)
- **Ejemplo típico**: Taller 500 m² → 30 kW trifásico, 15 circuitos

¿Qué tipo de instalación necesitas?""",
                    "botones": ["🏠 Residencial", "🏢 Comercial", "🏭 Industrial"],
                    "campo_esperado": "tipo_instalacion",
                    "puede_generar": False
                }

            # Pregunta 2: Área (con contexto experto según tipo)
            if not datos.get("area_m2"):
                tipo = datos.get("tipo_instalacion", "").lower()

                if "residencial" in tipo:
                    contexto = """**Instalación Residencial** - Perfecto.

📐 **¿Cuántos metros cuadrados (m²) tiene la vivienda/departamento?**

🏠 **Para viviendas, el área determina según CNE:**

**Área < 80 m²** (pequeña):
- Carga mínima: 3,000 W
- Circuitos: 2-3 (iluminación general + tomacorrientes + cocina)
- Alimentador: Cable 3x6 mm² o #10 AWG
- Interruptor general: 2x20A

**Área 80-150 m²** (mediana):
- Carga mínima: 3,000 W + 1,500 W/adicional = 4,500-6,000 W
- Circuitos: 4-6 (separar ambientes)
- Alimentador: Cable 3x10 mm² o #8 AWG
- Interruptor general: 2x32A

**Área > 150 m²** (grande):
- Carga mínima: 6,000-9,000 W
- Circuitos: 6-10 (iluminación, tomas, cocina, lavandería, A/C)
- Alimentador: Cable 3x16 mm² o #6 AWG
- Interruptor general: 2x40A o 2x50A

💡 **Normativa**: CNE Artículo 220.3 - Carga general iluminación y tomacorrientes

_Indica el área en m² (ejemplo: 120 m²)_"""

                elif "comercial" in tipo:
                    contexto = """**Instalación Comercial** - Excelente elección.

📐 **¿Cuántos metros cuadrados (m²) tiene el local/oficina?**

🏢 **Para comerciales, el área ES CRÍTICA porque determina:**

**CNE Tabla 220-3b** → Carga mínima **30 VA/m²** para oficinas/comercios

**Ejemplos concretos:**

📊 **Oficina 100 m²**:
- Carga: 100 m² × 30 VA/m² = 3,000 VA = 3 kW mínimo
- Circuitos: 5-6 (iluminación, tomas, equipos)
- Alimentador: 3x6 mm² (Trifásico) o 3x10 mm² (Monofásico)

📊 **Tienda 250 m²**:
- Carga: 250 m² × 30 VA/m² = 7,500 VA = 7.5 kW mínimo
- PLUS: Vitrinas refrigeradas (+30%), iluminación comercial (+50%)
- Carga real: ~12 kW
- Circuitos: 10-12
- Alimentador: Trifásico 3x16 mm² recomendado

📊 **Local grande 500 m²**:
- Carga base: 15 kW + cargas especiales (A/C, refrigeración)
- Carga total estimada: 20-25 kW
- Alimentador: Trifásico 3x25 mm² o superior
- Tablero: 36 polos mínimo con 20% reserva

⚠️ **IMPORTANTE**: Si tienes aires acondicionados, ascensores o maquinaria, la carga aumenta significativamente.

_Indica el área en m²_"""

                elif "industrial" in tipo:
                    contexto = """**Instalación Industrial** - Este tipo requiere análisis DETALLADO de cargas.

📐 **¿Cuántos metros cuadrados (m²) tiene la nave/taller?**

🏭 **Para industriales, el área SOLO es punto de partida, porque depende de:**

⚡ **Factores críticos**:
1. **Tipo de maquinaria** (motores, hornos, soldadoras, compresores)
2. **Potencia de equipos** (cada motor requiere circuito dedicado)
3. **Tipo de alimentación** (Monofásica 220V / Trifásica 380V)
4. **Factor de demanda** (no todos los equipos operan simultáneamente)

📊 **Ejemplos según área:**

**Taller pequeño 100-200 m²**:
- Iluminación industrial: 10-15 W/m² (fluorescentes/LED)
- Tomacorrientes: 1 cada 10 m²
- Carga base: 3-5 kW
- PLUS maquinaria: +10-20 kW típico
- **Total estimado**: 15-25 kW

**Nave mediana 300-600 m²**:
- Carga base: 10-15 kW (iluminación + tomas)
- Maquinaria típica: 30-60 kW
- **Total**: 40-75 kW
- Alimentación: Trifásico 380V obligatorio
- Cables: 3x50 mm² - 3x95 mm²

**Planta grande > 1000 m²**:
- Requiere subestación eléctrica propia
- Transformador dedicado
- Sistema de compensación reactiva
- Tablero general de distribución (TGD) + Tableros secundarios

💡 Después te preguntaré sobre la maquinaria específica.

_Por ahora, indica el área total en m²_"""

                else:
                    contexto = """📐 **¿Cuántos metros cuadrados (m²) tiene el área a instalar?**

⚡ **El área determina la carga eléctrica mínima según CNE 2011:**
- Residencial: No tiene mínimo por m², usa cargas típicas
- Comercial/Oficinas: 30 VA/m² (CNE Tabla 220-3b)
- Industrial: Depende de maquinaria instalada

_Indica el área en m² (ejemplo: 150)_"""

                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": contexto,
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            # Pregunta 3: Puntos de luz (con contexto experto)
            if not datos.get("puntos_luz"):
                tipo = datos.get("tipo_instalacion", "").lower()
                area = datos.get("area_m2", 0)

                # Calcular recomendación según normativa
                if "residencial" in tipo:
                    puntos_recomendados = max(8, int(area / 15))  # 1 cada 15 m² aprox
                    contexto_tipo = """🏠 **Viviendas según CNE**:
- Sala/comedor: 1 centro + apliques (2-3 puntos)
- Dormitorios: 1 centro + veladores (2-3 puntos cada uno)
- Cocina: 2-3 puntos (iluminación general + sobre mesada)
- Baños: 1-2 puntos
- Pasadizos: 1 cada 6 metros lineales"""

                elif "comercial" in tipo:
                    puntos_recomendados = max(12, int(area / 10))  # 1 cada 10 m²
                    contexto_tipo = """🏢 **Locales comerciales**:
- Iluminación uniforme: 300-500 lux (CNE y A.010)
- Oficinas: 1 luminaria cada 9-12 m²
- Tiendas: Mayor densidad en zona de exhibición
- Iluminación de emergencia: Obligatoria (A.130)"""

                elif "industrial" in tipo:
                    puntos_recomendados = max(15, int(area / 20))  # 1 cada 20 m² (naves altas)
                    contexto_tipo = """🏭 **Naves industriales**:
- Iluminación general: 200-300 lux mínimo
- Luminarias industriales: LED o fluorescentes 150W-400W
- Altura > 4m: Campanas industriales
- Zonas de trabajo: Iluminación localizada adicional"""

                else:
                    puntos_recomendados = int(area / 12)
                    contexto_tipo = ""

                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": f"""Perfecto, **{tipo}** de **{area} m²**.

💡 **¿Cuántos puntos de luz necesitas?**

📊 **Recomendación técnica para {area} m²**: ~**{puntos_recomendados} puntos de luz**

{contexto_tipo}

⚡ **Importante CNE**:
- Cada circuito de iluminación soporta máximo **15-20 puntos**
- Cable #14 AWG (2.5 mm²) para iluminación residencial/comercial
- Interruptores termomagnéticos 16A por circuito
- Si tienes > 20 puntos → Se divide en 2 circuitos automáticamente

💡 **Incluye**:
- Centros de luz (plafones, focos empotrables)
- Apliques de pared
- Iluminación exterior
- Iluminación de emergencia (si es comercial)

_Indica número total de puntos de luz (puedes ajustar la recomendación)_""",
                    "campo_esperado": "puntos_luz",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            # Pregunta 4: Tomacorrientes (con contexto experto)
            if not datos.get("tomacorrientes"):
                tipo = datos.get("tipo_instalacion", "").lower()
                area = datos.get("area_m2", 0)
                puntos_luz = datos.get("puntos_luz", 0)

                # Calcular recomendación según CNE
                if "residencial" in tipo:
                    tomas_recomendadas = max(10, int(area / 10))  # 1 cada 10 m²
                    contexto_tipo = """🏠 **Viviendas según CNE Artículo 210.52**:
- Dormitorios: Mínimo 1 por cada 3.6 metros de pared
- Sala/comedor: 1 cada 3.6 m de pared
- Cocina: Mínimo 2 circuitos dedicados (tomacorrientes sobre mesada)
- Baños: 1 tomacorriente con GFCI (protección contra fuga a tierra)
- Lavandería: 1 circuito dedicado para lavadora"""

                elif "comercial" in tipo:
                    tomas_recomendadas = max(15, int(area / 8))  # 1 cada 8 m²
                    contexto_tipo = """🏢 **Locales comerciales**:
- Oficinas: 1 tomacorriente doble cada 3 metros de pared
- Tomacorrientes en piso: Para zonas de trabajo
- Tomacorrientes datos (RJ45): Junto a tomacorrientes eléctricos
- Circuitos dedicados: Para equipos (servidores, fotocopiadoras)"""

                elif "industrial" in tipo:
                    tomas_recomendadas = max(12, int(area / 15))  # Menos tomas, más circuitos para maquinaria
                    contexto_tipo = """🏭 **Instalaciones industriales**:
- Tomacorrientes de uso general: 1 cada 15-20 m²
- Tomacorrientes industriales: 380V trifásicos para maquinaria
- Circuitos dedicados: Cada máquina grande requiere circuito propio
- Tomacorrientes de servicio: Para herramientas portátiles"""

                else:
                    tomas_recomendadas = int(area / 10)
                    contexto_tipo = ""

                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": f"""Excelente, ya tienes **{puntos_luz} puntos de luz** definidos.

🔌 **¿Cuántos tomacorrientes necesitas?**

📊 **Recomendación técnica para {area} m²**: ~**{tomas_recomendadas} tomacorrientes**

{contexto_tipo}

⚡ **Normativa CNE**:
- Cada circuito de tomacorrientes: Máximo **10-12 tomacorrientes**
- Cable #12 AWG (4 mm²) obligatorio para tomacorrientes
- Interruptor termomagnético 20A por circuito
- Tomacorrientes con puesta a tierra (3 polos) obligatorios

💡 **Considera**:
- Tomacorrientes simples (1 salida) o dobles (2 salidas)
- Tomacorrientes especiales (cocina 20A, lavandería 20A)
- Tomacorrientes de datos/red (si los necesitas)

⚠️ **Para equipos de alta potencia** (cocina eléctrica, termas, aire acondicionado):
Te preguntaré después, cada uno requiere circuito DEDICADO.

_Indica número de tomacorrientes (puedes ajustar la recomendación)_""",
                    "campo_esperado": "tomacorrientes",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            # Pregunta 5: Cargas especiales (NUEVA - importante para cálculo)
            if not datos.get("cargas_especiales_confirmadas"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": """⚡ **¿Tienes equipos de ALTA POTENCIA que requieran circuitos dedicados?**

📋 **Equipos que REQUIEREN circuito dedicado según CNE:**

🔥 **Cocina/Terma**:
- Cocina eléctrica: 7,000-10,000 W → Cable 3x6 mm², interruptor 40A
- Horno empotrable: 3,000-4,000 W → Cable 3x4 mm², interruptor 20A
- Terma eléctrica: 3,500-6,000 W → Cable 3x4 mm² o 3x6 mm²

❄️ **Climatización**:
- Aire acondicionado 12,000 BTU: ~1,500 W → Cable 3x2.5 mm², 16A
- Aire acondicionado 18,000 BTU: ~2,300 W → Cable 3x4 mm², 20A
- Aire acondicionado 24,000 BTU: ~3,200 W → Cable 3x6 mm², 32A

🏭 **Industrial/Comercial**:
- Motores > 1 HP (750W): Circuito dedicado
- Soldadoras: Circuito trifásico dedicado
- Compresores: Circuito dedicado con protección térmica
- Hornos industriales: Circuito trifásico de alta corriente

🏠 **Otros**:
- Lavadora: 1,500-2,000 W (circuito compartido con tomas lavandería)
- Secadora: 3,000-5,000 W → Circuito dedicado
- Hidrolavadora: 2,000 W → Puede compartir circuito

💡 **Si no tienes equipos especiales o no estás seguro, podemos incluir provisión.**

¿Tienes equipos de alta potencia? Responde SÍ o NO (luego especificamos cuáles)""",
                    "botones": ["✅ Sí, tengo equipos especiales", "⏭️ No, solo instalación básica"],
                    "campo_esperado": "cargas_especiales_confirmadas",
                    "puede_generar": False
                }

            # Ya tenemos todo - Dar resumen
            return {
                "accion": "confirmar_datos",
                "mensaje_pili": f"""✅ **Perfecto! Tengo toda la información necesaria:**

📋 **Resumen de tu Instalación Eléctrica:**
- **Tipo**: {datos.get('tipo_instalacion', 'No especificado')}
- **Área**: {datos.get('area_m2', 0)} m²
- **Puntos de luz**: {datos.get('puntos_luz', 0)} unidades
- **Tomacorrientes**: {datos.get('tomacorrientes', 0)} unidades
- **Cargas especiales**: {datos.get('cargas_especiales_confirmadas', 'Instalación básica')}

⚡ **Cálculo según CNE 2011:**

📊 **Carga instalada estimada**:
- Iluminación: {datos.get('puntos_luz', 0)} × 100W = {datos.get('puntos_luz', 0) * 100 / 1000:.1f} kW
- Tomacorrientes: {datos.get('tomacorrientes', 0)} × 180W = {datos.get('tomacorrientes', 0) * 180 / 1000:.1f} kW
- Cargas especiales: (a calcular según equipos)

🔧 **El sistema incluirá:**

✅ **Tablero de distribución**:
   - Interruptor general termomagnético 2×{max(32, int((datos.get('puntos_luz', 0) * 100 + datos.get('tomacorrientes', 0) * 180) / 220 / 0.8) + 10)}A
   - Interruptores por circuito (16A iluminación, 20A tomacorrientes)
   - Barra de puesta a tierra
   - Reserva 20% para ampliaciones futuras

✅ **Circuitos eléctricos**:
   - Iluminación: {max(1, datos.get('puntos_luz', 0) // 15)} circuito(s)
   - Tomacorrientes: {max(1, datos.get('tomacorrientes', 0) // 10)} circuito(s)
   - Cable THW/THHN calibre según circuito

✅ **Materiales certificados**:
   - Cables con certificación INDECOPI
   - Interruptores termomagnéticos ABB/Schneider/Legrand
   - Tomacorrientes con puesta a tierra

✅ **Instalación según CNE 2011**:
   - Tuberías PVC-P (pesado) empotradas
   - Cajas octogonales y rectangulares metálicas
   - Pozo a tierra independiente (< 25 Ω)

💰 **Generando cotización profesional con precios actualizados 2025...**""",
                "puede_generar": True
            }

        # SERVICIO: ITSE
        elif servicio == "itse":

            if not datos.get("tipo_local"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "🏢 ¿Qué tipo de local es?\n\n_Ejemplo: Restaurante, Consultorio, Tienda, Oficina_",
                    "campo_esperado": "tipo_local",
                    "puede_generar": False
                }

            if not datos.get("area_m2"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📐 ¿Cuántos **metros cuadrados (m²)** tiene el local?\n\n_Ejemplo: 80 m²_",
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            return None

        # SERVICIO: POZO A TIERRA
        elif servicio == "pozo-tierra":

            if not datos.get("tipo_instalacion"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "⚡ ¿Es para instalación **residencial**, **comercial** o **industrial**?",
                    "botones": ["🏠 Residencial", "🏢 Comercial", "🏭 Industrial"],
                    "campo_esperado": "tipo_instalacion",
                    "puede_generar": False
                }

            if not datos.get("potencia_instalada"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "⚡ ¿Cuál es la **potencia instalada** aproximada?\n\n_Ejemplo: 10 kW, 50 kW, 200 kW_",
                    "campo_esperado": "potencia_instalada",
                    "puede_generar": False
                }

            return None

        # SERVICIO: CONTRA INCENDIOS
        elif servicio == "contraincendios":

            # Pregunta 1: Tipo de establecimiento (NUEVA - más específica)
            if not datos.get("tipo_local"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": """¡Perfecto! Soy especialista en **Sistemas Contra Incendios** según normativa NFPA.

🏢 **Primero necesito conocer: ¿Qué tipo de establecimiento es?**

💡 **¿Por qué es importante?**
Cada tipo de local tiene requisitos ESPECÍFICOS según NFPA 13 y RNE:

🍽️ **Restaurante/Cocina** → Requiere sistema Clase K (grasas y aceites)
🏪 **Comercio/Tienda** → Rociadores automáticos (1 cada 12m²)
🏭 **Industrial/Almacén** → Sistema según materiales almacenados
🏢 **Oficinas** → Sistema estándar (riesgo ordinario)
🏥 **Salud/Clínica** → Alta densidad de rociadores
🎓 **Educativo** → Alarmas + evacuación obligatoria
🏨 **Hotel/Hospedaje** → Detección en cada habitación

¿Cuál describe mejor tu caso?""",
                    "campo_esperado": "tipo_local",
                    "puede_generar": False
                }

            # Pregunta 2: Área (con contexto experto)
            if not datos.get("area_m2"):
                tipo_local = datos.get("tipo_local", "").lower()

                # Contexto específico según tipo de local
                if "restaurante" in tipo_local or "cocina" in tipo_local:
                    contexto = """**Restaurante** - Excelente elección compartir este dato.

📐 **¿Cuántos metros cuadrados (m²) tiene el establecimiento?**

🔥 **Para restaurantes, el área determina:**
- **Rociadores**: 1 cada 9-12 m² (alta densidad por riesgo de cocina)
- **Detectores de humo**: Mínimo 1 cada 60 m² en comedor
- **Sistema especial en cocina**: Campana extractora con supresión automática
- **Extintores**: Clase K cada 15 m en zona de cocina

💡 **Ejemplo**: Restaurante de 200 m² → ~20 rociadores + 4 detectores + sistema campana

_Escribe el área en m² (ejemplo: 200 m²)_"""

                elif "comercio" in tipo_local or "tienda" in tipo_local:
                    contexto = """**Local Comercial** - Perfecto.

📐 **¿Cuántos metros cuadrados (m²) tiene la tienda/local?**

🛒 **Para comercios, el área determina:**
- **Rociadores automáticos**: 1 cada 12 m² (NFPA 13)
- **Detectores de humo**: 1 cada 80 m²
- **Extintores portátiles**: 1 cada 200 m² (mínimo 2)
- **Gabinetes contra incendios**: 1 cada 500 m² o cada piso

💡 **Ejemplo**: Tienda 150 m² → 13 rociadores + 2 detectores + 2 extintores

_Escribe el área en m² (ejemplo: 150)_"""

                elif "industrial" in tipo_local or "almacén" in tipo_local or "fábrica" in tipo_local:
                    contexto = """**Industrial/Almacén** - Este tipo requiere análisis DETALLADO.

📐 **¿Cuántos metros cuadrados (m²) tiene la nave/almacén?**

🏭 **Para industriales, el área ES CRÍTICA porque determina:**
- **Tipo de sistema**: Rociadores, diluvio, espuma o gas según materiales
- **Densidad de descarga**: 6-12 L/min/m² según altura de almacenamiento
- **Presión de bomba**: Calculada según área y altura
- **Reserva de agua**: Mínimo 60 minutos de operación

⚠️ **IMPORTANTE**: Si almacenan materiales inflamables, el sistema puede cambiar TOTALMENTE.

💡 **Ejemplo**: Almacén 500 m² × 8m altura → Sistema de diluvio con 60 rociadores

_Escribe el área en m²_"""

                else:
                    contexto = """📐 **¿Cuántos metros cuadrados (m²) tiene el área a proteger?**

🔥 **El área determina directamente:**
- **Cantidad de rociadores automáticos** (1 cada 9-12 m² según NFPA 13)
- **Número de detectores de humo** (1 cada 60-80 m²)
- **Extintores portátiles necesarios** (1 cada 200 m²)
- **Capacidad de la bomba contra incendios**
- **Reserva de agua requerida**

💡 **Normativa aplicable**: NFPA 13 + RNE A.130 (Perú)

_Ejemplo: 250 m² o 250 metros cuadrados_"""

                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": contexto,
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            # Pregunta 3: Nivel de riesgo (con explicación experta)
            if not datos.get("riesgo"):
                tipo_local = datos.get("tipo_local", "").lower()
                area = datos.get("area_m2", 0)

                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": f"""Perfecto, **{tipo_local}** de **{area} m²**.

🔥 **Ahora necesito clasificar el nivel de riesgo según NFPA 13:**

📊 **RIESGO LEVE** (Light Hazard):
- Oficinas, instituciones educativas, iglesias
- Baja carga combustible
- **Densidad**: 2.5 L/min/m²
- Ejemplo: Oficinas administrativas

📊 **RIESGO ORDINARIO** (Ordinary Hazard):
- Comercios, restaurantes, hoteles, talleres ligeros
- Carga combustible moderada
- **Densidad**: 6-8 L/min/m²
- Ejemplo: Tiendas retail, restaurantes

📊 **RIESGO ALTO** (Extra Hazard):
- Industrias con líquidos inflamables, almacenes altos
- Alta carga combustible o materiales peligrosos
- **Densidad**: 12-15 L/min/m²
- Ejemplo: Almacenes de pinturas, industrias químicas

💡 **Impacto directo**:
- Riesgo LEVE → Sistema más económico (~40% menos)
- Riesgo ALTO → Bomba más potente + más rociadores

Según tu tipo de local (**{tipo_local}**), ¿cuál es el nivel de riesgo?""",
                    "botones": ["🟢 Riesgo Leve", "🟡 Riesgo Ordinario", "🔴 Riesgo Alto"],
                    "campo_esperado": "riesgo",
                    "puede_generar": False
                }

            # Pregunta 4: Altura de techo (NUEVA - importante para cálculos)
            if not datos.get("altura_techo"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": """📏 **¿Cuál es la altura del techo?**

🔥 **La altura es CRÍTICA porque afecta:**

**Altura ≤ 3.5m** (estándar):
- Rociadores estándar
- Presión mínima 1 bar
- Sistema convencional

**Altura 3.5m - 6m** (media):
- Rociadores de respuesta rápida
- Presión 1.5-2 bar
- Puede requerir Early Suppression Fast Response (ESFR)

**Altura > 6m** (alta):
- Sistema ESFR obligatorio
- Presión > 2.5 bar
- Bomba de mayor potencia
- Costo aumenta ~50%

💡 **Normativa**: NFPA 13 limita altura según tipo de rociador

_Indica altura en metros (ejemplo: 3.5 o 4)_""",
                    "campo_esperado": "altura_techo",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            # Pregunta 5: Número de pisos (NUEVA - para detectores y alarmas)
            if not datos.get("pisos"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": """🏢 **¿Cuántos pisos/niveles tiene el edificio?**

⚠️ **Edificios de múltiples pisos requieren:**

**1 Piso** (simple):
- Sistema básico por piso
- 1 panel de alarma central

**2-3 Pisos** (medio):
- Rociadores en CADA piso
- Detectores de humo en escaleras
- Panel repetidor en cada nivel
- Sistema de alarma interconectado

**4+ Pisos** (alto):
- Sistema de bombeo por zonas
- Tanque cisterna mayor (+ 50%)
- Gabinetes en cada piso
- Alarma evacuación general
- Cumple RNE A.130 (edificios altos)

💡 **Costo adicional**: ~30% por cada piso adicional

_Indica número de pisos (ejemplo: 1, 2, 3...)_""",
                    "campo_esperado": "pisos",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            # YA TENEMOS TODO - Dar resumen antes de generar
            return {
                "accion": "confirmar_datos",
                "mensaje_pili": f"""✅ **Excelente, tengo toda la información necesaria:**

📋 **Resumen del Proyecto:**
- **Tipo**: {datos.get('tipo_local', 'No especificado')}
- **Área**: {datos.get('area_m2', 0)} m²
- **Riesgo**: {datos.get('riesgo', 'No especificado')}
- **Altura techo**: {datos.get('altura_techo', 3.5)} m
- **Pisos**: {datos.get('pisos', 1)} nivel(es)

🔥 **Sistema recomendado incluirá:**

✅ **Detección automática**:
   - Detectores de humo: ~{int(datos.get('area_m2', 0) / 60)} unidades
   - Central de alarma direccionable

✅ **Supresión automática**:
   - Rociadores automáticos: ~{int(datos.get('area_m2', 0) / 10)} unidades
   - Red de tuberías Schedule 40
   - Bomba contra incendios (presión según altura)

✅ **Extinción manual**:
   - Extintores PQS 12 kg: {max(2, int(datos.get('area_m2', 0) / 200))} unidades
   - Gabinetes con manguera: {max(1, int(datos.get('area_m2', 0) / 500))} unidades

✅ **Señalización** según NTP 399.010-1

💰 **Generando cotización profesional con precios actualizados 2025...**""",
                "puede_generar": True
            }

        # SERVICIOS SIMPLES (CCTV, Redes, Domótica, Saneamiento, Expedientes)
        else:

            if not datos.get("area_m2") and servicio in ["domotica", "redes-cctv", "saneamiento"]:
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📐 ¿Cuántos **metros cuadrados (m²)** tiene el área?",
                    "campo_esperado": "area_m2",
                    "tipo_input": "numero",
                    "puede_generar": False
                }

            if not datos.get("descripcion"):
                return {
                    "accion": "solicitar_info",
                    "mensaje_pili": "📝 Por favor describe brevemente el proyecto:\n\n_Ejemplo: Sistema de CCTV para vigilancia perimetral_",
                    "campo_esperado": "descripcion",
                    "puede_generar": False
                }

            return None

    def _generar_cotizacion_final(self, servicio: str, datos: Dict) -> Dict[str, Any]:
        """
        Genera la cotización final con todos los datos

        Returns:
            JSON estructurado con la cotización completa
        """

        logger.info(f"💰 Generando cotización para servicio: {servicio}")

        # Usar el brain para generar la estructura base
        cotizacion = self.brain.generar_cotizacion(
            servicio=servicio,
            datos=datos
        )

        # Enriquecer con información adicional
        cotizacion["conversacion"] = {
            "mensaje_pili": f"✅ ¡Excelente! He generado tu cotización para **{self.servicios.get(servicio, {}).get('nombre', servicio)}**.\n\n"
                          f"📊 Total: **S/ {cotizacion['datos_cotizacion']['total']:,.2f}**\n\n"
                          f"Puedes revisar la vista previa y descargar el documento.",
            "puede_generar": True
        }

        return cotizacion


# ═══════════════════════════════════════════════════════════════
# INSTANCIA GLOBAL
# ═══════════════════════════════════════════════════════════════

pili_cotizadora = PILICotizadora()
