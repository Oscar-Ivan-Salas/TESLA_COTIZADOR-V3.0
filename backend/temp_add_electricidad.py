# Script temporal para generar el código completo de PILI Local Specialists
# Este script generará el código restante y lo agregará al archivo principal

import os

# Ruta del archivo principal
archivo_principal = r"e:\TESLA_COTIZADOR-V3.0\backend\app\services\pili_local_specialists.py"

# Código a agregar (continuación después de la clase base)
codigo_electricidad = '''

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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el área en m² (ejemplo: 120)",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de pisos (ejemplo: 2)",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de puntos de luz (ejemplo: 25)",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de tomacorrientes (ejemplo: 15)",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de tableros (ejemplo: 2)",
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
            "descripcion": f"Tubería PVC 3/4\\" ({tuberia_metros:.0f}m)",
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
            texto_cotizacion += f"{i}. {item['descripcion']}\\n   └ S/ {item['total']:.2f}\\n\\n"
        
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
'''

# Agregar al archivo
with open(archivo_principal, 'a', encoding='utf-8') as f:
    f.write(codigo_electricidad)

print("✅ Código de ElectricidadSpecialist agregado")
print(f"Archivo: {archivo_principal}")
