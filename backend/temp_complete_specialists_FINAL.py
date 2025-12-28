# Script FINAL para completar los últimos 4 especialistas
# Redes, Automatización Industrial, Expedientes Técnicos, Saneamiento
# Cada uno con ~250-300 líneas de lógica profesional completa

import os

archivo = r"e:\TESLA_COTIZADOR-V3.0\backend\app\services\pili_local_specialists.py"

# Leer archivo
with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
    contenido = f.read()

# Encontrar las clases simplificadas
inicio = contenido.find("class RedesSpecialist(LocalSpecialist):")
fin = contenido.find("class LocalSpecialistFactory:")

if inicio == -1 or fin == -1:
    print("❌ No se encontraron las clases")
    exit(1)

# Código COMPLETO de los 4 especialistas finales
codigo_final = '''class RedesSpecialist(LocalSpecialist):
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el área en m²",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de puntos de red",
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
            texto += f"{i}. {item['descripcion']}\\n   └ S/ {item['total']:.2f}\\n\\n"
        
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de entradas",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de salidas",
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
            texto += f"{i}. {item['descripcion']}\\n   └ S/ {item['total']:.2f}\\n\\n"
        
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
""" + "\\n".join([f"✅ {item}" for item in proyecto_info["incluye"][:4]]) + f"""

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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el área en m²",
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

""" + "\\n".join([f"✅ {item}" for item in proyecto_info["incluye"]]) + f"""

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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el área en m²",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de baños",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de puntos adicionales",
                    "stage": "puntos",
                    "state": self.conversation_state,
                    "progreso": "4/6"
                }
            
            data["puntos_adicionales"] = puntos
            self.conversation_state["stage"] = "quotation"
            
            return self._generar_cotizacion_saneamiento()
        
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
                return self._process_saneamiento("")
        
        return self._process_generic(message)
    
    def _generar_cotizacion_saneamiento(self) -> Dict:
        data = self.conversation_state["data"]
        tipo_sistema = data["tipo_sistema"]
        area = data["area"]
        banos = data["banos"]
        puntos_adic = data["puntos_adicionales"]
        
        items = []
        
        # Puntos por baño (promedio 8 puntos por baño completo)
        puntos_por_bano = 8
        total_puntos_bano = banos * puntos_por_bano
        
        if tipo_sistema in ["AGUA_FRIA", "COMPLETO"]:
            precios_agua = self.kb["sistemas"]["AGUA_FRIA"]["precios"]
            
            # Puntos de agua fría
            total_agua_fria = total_puntos_bano + puntos_adic
            items.append({
                "descripcion": f"Puntos de agua fría ({total_agua_fria} und)",
                "cantidad": total_agua_fria,
                "precio_unitario": precios_agua["punto_agua_fria"],
                "total": total_agua_fria * precios_agua["punto_agua_fria"]
            })
            
            # Tubería PVC
            metros_tuberia = total_agua_fria * 5
            items.append({
                "descripcion": f"Tubería PVC 1/2\\\" ({metros_tuberia}m)",
                "cantidad": metros_tuberia,
                "precio_unitario": precios_agua["tuberia_pvc_1_2"],
                "total": metros_tuberia * precios_agua["tuberia_pvc_1_2"]
            })
        
        if tipo_sistema in ["DESAGUE", "COMPLETO"]:
            precios_desague = self.kb["sistemas"]["DESAGUE"]["precios"]
            
            # Puntos de desagüe
            items.append({
                "descripcion": f"Puntos de desagüe ({total_puntos_bano} und)",
                "cantidad": total_puntos_bano,
                "precio_unitario": precios_desague["punto_desague"],
                "total": total_puntos_bano * precios_desague["punto_desague"]
            })
            
            # Tubería desagüe
            metros_desague = total_puntos_bano * 4
            items.append({
                "descripcion": f"Tubería PVC 4\\\" ({metros_desague}m)",
                "cantidad": metros_desague,
                "precio_unitario": precios_desague["tuberia_pvc_4"],
                "total": metros_desague * precios_desague["tuberia_pvc_4"]
            })
        
        if tipo_sistema == "COMPLETO":
            precios_tanques = self.kb["sistemas"]["ALMACENAMIENTO"]["precios"]
            
            # Tanque elevado
            items.append({
                "descripcion": "Tanque elevado 1100L (1 und)",
                "cantidad": 1,
                "precio_unitario": precios_tanques["tanque_elevado_1100lt"],
                "total": precios_tanques["tanque_elevado_1100lt"]
            })
            
            # Bomba
            items.append({
                "descripcion": "Bomba de agua 1HP (1 und)",
                "cantidad": 1,
                "precio_unitario": precios_tanques["bomba_agua_1hp"],
                "total": precios_tanques["bomba_agua_1hp"]
            })
        
        subtotal = sum(item["total"] for item in items)
        igv = subtotal * 0.18
        total = subtotal + igv
        
        texto = f"""📊 **COTIZACIÓN SISTEMA SANITARIO**

━━━━━━━━━━━━━━━━━━━━━━━
**📋 DATOS DEL PROYECTO:**

💧 Sistema: {tipo_sistema.replace('_', ' ')}
📏 Área: {area} m²
🚽 Baños: {banos}
🔢 Puntos adicionales: {puntos_adic}

━━━━━━━━━━━━━━━━━━━━━━━
**💰 ITEMS CALCULADOS:**

"""
        for i, item in enumerate(items, 1):
            texto += f"{i}. {item['descripcion']}\\n   └ S/ {item['total']:.2f}\\n\\n"
        
        texto += f"""━━━━━━━━━━━━━━━━━━━━━━━
**📈 TOTALES:**

Subtotal: S/ {subtotal:.2f}
IGV (18%): S/ {igv:.2f}
**TOTAL: S/ {total:.2f}**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Incluye: Materiales + Instalación
📋 Normativa: {self.kb["normativa"]}
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
                    "nombre": f"Sistema Sanitario {tipo_sistema}",
                    "area_m2": area,
                    "banos": banos
                },
                "items": items,
                "subtotal": subtotal,
                "igv": igv,
                "total": total
            },
            "progreso": "6/6"
        }


'''

# Reemplazar
nuevo_contenido = contenido[:inicio] + codigo_final + contenido[fin:]

# Escribir
with open(archivo, 'w', encoding='utf-8') as f:
    f.write(nuevo_contenido)

print("✅ ¡TODOS los especialistas completados!")
print("✅ Redes, Automatización, Expedientes, Saneamiento - COMPLETOS")

# Contar líneas finales
with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
    lineas = len(f.readlines())

print(f"✅ TOTAL FINAL: {lineas} líneas")
print(f"✅ Objetivo: 3500+ líneas")
print(f"✅ Estado: {'COMPLETADO ✓' if lineas >= 3500 else f'Faltan {3500 - lineas} líneas'}")
