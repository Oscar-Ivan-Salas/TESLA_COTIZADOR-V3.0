"""
PILI ChatBot - Proyecto Complejo PMI (Electricidad)
Versión: 1.0
Metodología: PMI PMBOK 7th Edition

Genera PROJECT CHARTER profesional con:
- KPIs de gestión (SPI, CPI, EV, PV, AC)
- Cronograma Gantt (6 fases)
- Registro de Stakeholders
- Matriz RACI
- Registro de Riesgos (Top 5)
- 13 Entregables principales
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

class PILIElectricidadProyectoComplejoPMIChatBot:
    def __init__(self):
        self.version = "1.0 - PMI PMBOK 7th"
        self.contador = 1
        
    def procesar(self, mensaje: str, estado: Dict) -> Dict:
        """Procesa el mensaje del usuario y retorna respuesta"""
        
        # Inicializar estado si es necesario
        if not estado:
            estado = {}
        
        etapa = estado.get("etapa", "inicial")
        
        # ============================================
        # ETAPA: Inicial - Bienvenida
        # ============================================
        if etapa == "inicial":
            # Auto-detectar datos del frontend
            cliente_nombre = estado.get("cliente_nombre")
            proyecto_nombre = estado.get("nombre_proyecto")
            presupuesto = estado.get("presupuesto")
            moneda = estado.get("moneda", "PEN")
            duracion_total = estado.get("duracion_total")
            servicio = estado.get("servicio", "electricidad")
            industria = estado.get("industria", "construccion")
            
            # ✅ GUARDAR datos del formulario en el estado para usarlos después
            if cliente_nombre:
                estado["cliente_nombre"] = cliente_nombre
            if proyecto_nombre:
                estado["nombre_proyecto"] = proyecto_nombre
            if presupuesto:
                estado["presupuesto"] = presupuesto
            if moneda:
                estado["moneda"] = moneda
            if duracion_total:
                estado["duracion_total"] = duracion_total
            if servicio:
                estado["servicio"] = servicio
            if industria:
                estado["industria"] = industria
            
            # ✅ NUEVO: Guardar estado inicial completo para preservar servicio/industria
            estado["estado_inicial"] = {
                "servicio": servicio,
                "industria": industria,
                "cliente_nombre": cliente_nombre,
                "nombre_proyecto": proyecto_nombre,
                "presupuesto": presupuesto,
                "moneda": moneda,
                "duracion_total": duracion_total
            }
            
            # ✅ FLUJO ADAPTATIVO: Router de Inicio (Frontend First)
            complejidad_inicial = estado.get("complejidad")
            etapas_activas = estado.get("etapas_seleccionadas")
            incluir_metrado = estado.get("incluir_metrado")
            area_proyecto = estado.get("area_proyecto") # m2
            
            simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€', 'GBP': '£'}.get(moneda, '$')
            # Formatear presupuesto
            if presupuesto:
                presupuesto_texto = f"{simbolo} {presupuesto:,.2f}"
            else:
                presupuesto_texto = f"{simbolo} 0.00"

            # ✅ NUEVO: Leer datos del calendario si existen
            fecha_inicio = estado.get("fecha_inicio")
            fecha_fin = estado.get("fecha_fin")
            duracion_dias = estado.get("duracion_dias")
            
            # 🔍 DEBUG: Ver datos recibidos
            print(f"🔍 DEBUG CHATBOT - Fechas recibidas: Inicio={fecha_inicio}, Fin={fecha_fin}, Dias={duracion_dias}")

            # Construir texto de duración
            if fecha_inicio and fecha_fin and duracion_dias:
                duracion_texto = f"**{duracion_dias} días** (del {fecha_inicio} al {fecha_fin})"
            elif duracion_total:
                duracion_texto = f"**{duracion_total} días**"
            else:
                duracion_texto = "**No especificado**"

            if complejidad_inicial:
                # =======================================================
                # CASO 1: MODO EXPERTO (Configuración desde Frontend)
                # =======================================================
                estado["etapa"] = "ubicacion"
                
                # Construir resumen de configuración
                resumen_metrado = ""
                if incluir_metrado and area_proyecto:
                    resumen_metrado = f"\n✅ Metrado: **{area_proyecto} m²**"
                
                mensaje_bienvenida = f"""¡Hola! 👋 Soy **PILI**, tu asistente de proyectos eléctricos PMI.

━━━━━━━━━━━━━━━━━━━━━━━
**✅ DATOS DEL PROYECTO CONFIGURADOS**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Proyecto: **{proyecto_nombre or 'Sin Nombre'}**
✅ Presupuesto: **{presupuesto_texto}**
✅ Modalidad: **{complejidad_inicial} Fases (Pre-configurada)**{resumen_metrado}

He cargado tu checklist de etapas activas ({len(etapas_activas) if etapas_activas else 0} seleccionadas).
Comencemos definiendo el contexto geográfico.

📍 **¿Dónde se realizará el proyecto?**
_Ejemplo: Lima, Perú / Planta Industrial Callao_"""

                return {
                    'success': True, 
                    'respuesta': mensaje_bienvenida, 
                    'botones': None, 
                    'estado': estado,
                    'datos_generados': estado["estado_inicial"]
                }
            
            else:
                # =======================================================
                # CASO 2: MODO CONVERSACIONAL (Preguntar complejidad)
                # =======================================================
                estado["etapa"] = "complejidad"
                
                return {'success': True, 'respuesta': f"""¡Hola! 👋 Soy **PILI**, tu asistente de proyectos eléctricos PMI.

━━━━━━━━━━━━━━━━━━━━━━━
**✅ DATOS RECIBIDOS DEL FORMULARIO**
━━━━━━━━━━━━━━━━━━━━━━━

✅ Cliente: **{cliente_nombre or 'No especificado'}**
✅ Proyecto: **{proyecto_nombre or 'No especificado'}**
✅ Servicio: **{servicio.upper()}**
✅ Industria: **{industria.upper()}**
✅ Presupuesto: **{presupuesto_texto}**
✅ Duración: {duracion_texto}

💡 **Estos datos se usarán automáticamente en el documento.**
Solo te preguntaré información adicional necesaria para el Project Charter.

━━━━━━━━━━━━━━━━━━━━━━━
**NIVEL DE COMPLEJIDAD DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

Como experta en PMI PMBOK 7th Edition, adaptaré el análisis según la complejidad de tu proyecto.

📊 **¿Qué nivel de complejidad tiene tu proyecto?**

**5 FASES - Básico** 
• Proyectos estándar (<$50K)
• Documentación esencial
• Análisis simplificado
• ⏱️ ~5 minutos

**6 FASES - Intermedio**
• Proyectos con múltiples stakeholders ($50K-$200K)
• Control de calidad reforzado
• Gestión de riesgos moderada
• ⏱️ ~8 minutos

**7 FASES - Avanzado**
• Proyectos críticos/complejos (>$200K)
• Documentación completa PMI
• Gestión integral de riesgos
• Formularios interactivos
• ⏱️ ~15 minutos

Selecciona el nivel que mejor se adapte a tu proyecto.""", 'botones': [
                {"text": "5 fases - Básico", "value": "5"},
                {"text": "6 fases - Intermedio", "value": "6"},
                {"text": "7 fases - Avanzado", "value": "7"}
            ], 'estado': estado, 'datos_generados': estado["estado_inicial"]}
        
        # ============================================
        # ETAPA: Complejidad (NUEVA)
        # ============================================
        elif etapa == "complejidad":
            try:
                complejidad = int(mensaje)
                if complejidad not in [5, 6, 7]:
                    return {'success': False, 'respuesta': "❌ Por favor selecciona 5, 6 o 7 fases.", 'botones': [
                        {"text": "5 fases - Básico", "value": "5"},
                        {"text": "6 fases - Intermedio", "value": "6"},
                        {"text": "7 fases - Avanzado", "value": "7"}
                    ], 'estado': estado}
                
                estado["complejidad"] = complejidad
                estado["etapa"] = "ubicacion"
                
                nivel_texto = {5: "Básico", 6: "Intermedio", 7: "Avanzado"}.get(complejidad, "Básico")
                
                return {'success': True, 'respuesta': f"""✅ Nivel seleccionado: **{complejidad} fases - {nivel_texto}**

Perfecto. He configurado el análisis PMI para un proyecto de nivel {nivel_texto.lower()}.

━━━━━━━━━━━━━━━━━━━━━━━
**UBICACIÓN DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

📍 **¿Dónde se realizará el proyecto?**
_Ejemplo: Lima, Perú / Concepción, Chile_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Selección inválida. Por favor elige una opción.", 'botones': [
                    {"text": "5 fases - Básico", "value": "5"},
                    {"text": "6 fases - Intermedio", "value": "6"},
                    {"text": "7 fases - Avanzado", "value": "7"}
                ], 'estado': estado}
        
        # ============================================
        # ETAPA: Ubicación
        # ============================================
        # ============================================
        # ETAPA: Ubicación
        # ============================================
        elif etapa == "ubicacion":
            estado["ubicacion"] = mensaje
            
            # ✅ LÓGICA INTELIGENTE: Verificar si ya tenemos AREA definida (Frontend First)
            # Si el área ya viene del formulario, NO preguntar por área.
            area_definida = estado.get("area_proyecto")
            if area_definida:
                try:
                    # 🔴 FIX CRÍTICO: Asegurar que el area_m2 se actualice con el valor del formulario
                    estado["area_m2"] = float(str(area_definida).replace(',', ''))
                except:
                    estado["area_m2"] = 0
                
                # Ya tenemos área, saltamos al chequeo de alcance
                alcance_inicial = estado.get("alcance_proyecto", "")
                
                if alcance_inicial and len(alcance_inicial) > 10:
                    estado["etapa"] = "confirmar_alcance"
                    
                    return {'success': True, 'respuesta': f"""✅ Ubicación: **{mensaje}**
                    
━━━━━━━━━━━━━━━━━━━━━━━
**CONFIRMACIÓN DE ALCANCE**
━━━━━━━━━━━━━━━━━━━━━━━

He recibido la siguiente descripción inicial del proyecto:

📝 **"{alcance_inicial}"**

¿Esta información está completa o deseas agregar más detalles técnicos?
_(Sistemas, equipos, especificaciones)_""", 'botones': [
                        {"text": "✅ Es correcto, continuar", "value": "continuar"},
                        {"text": "✏️ Agregar detalles", "value": "agregar"}
                    ], 'estado': estado, 'datos_generados': {'alcance_proyecto': alcance_inicial}}
                else:
                    estado["etapa"] = "descripcion"
                    # Obtener nombre del proyecto del formulario inicial
                    nombre_proyecto = estado.get("proyecto_nombre", "")
                    
                    mensaje_descripcion = f"""✅ Ubicación: **{mensaje}**

📝 **Descripción del proyecto:**"""
                    
                    if nombre_proyecto:
                        mensaje_descripcion += f"""
Veo que el proyecto es: **{nombre_proyecto}**

¿Necesitas agregar más detalles técnicos? (sistemas, equipos, especificaciones)
_Ejemplo: Sistema eléctrico industrial completo con subestación de 1000 KVA, tableros de distribución, sistema de automatización SCADA, iluminación LED, sistema de respaldo UPS_

Si no necesitas agregar más, simplemente escribe "No" o "Continuar"."""
                    else:
                        mensaje_descripcion += """
_Incluye: tipo de instalación, sistemas, equipos principales, etc._
_Ejemplo: Sistema eléctrico industrial completo con subestación de 1000 KVA, tableros de distribución, sistema de automatización SCADA, iluminación LED, sistema de respaldo UPS_"""
                    
                    return {'success': True, 'respuesta': mensaje_descripcion, 'botones': None, 'estado': estado}
            
            # Si NO hay área definida, procedemos el flujo normal
            else:
                estado["etapa"] = "area"
                return {'success': True, 'respuesta': f"""✅ Ubicación: **{mensaje}**

📐 **¿Área total del proyecto (m²)?**
_Ejemplo: 5000_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Área
        # ============================================
        elif etapa == "area":
            try:
                area = float(mensaje.replace(',', ''))
                estado["area_m2"] = area
                
                # ✅ LÓGICA INTELIGENTE: Verificar si ya tenemos descripción inicial
                alcance_inicial = estado.get("alcance_proyecto", "")
                
                if alcance_inicial and len(alcance_inicial) > 10:
                    estado["etapa"] = "confirmar_alcance"
                    
                    return {'success': True, 'respuesta': f"""✅ Área: **{area:,.0f} m²**

━━━━━━━━━━━━━━━━━━━━━━━
**CONFIRMACIÓN DE ALCANCE**
━━━━━━━━━━━━━━━━━━━━━━━

He recibido la siguiente descripción inicial del proyecto:

📝 **"{alcance_inicial}"**

¿Esta información está completa o deseas agregar más detalles técnicos?
_(Sistemas, equipos, especificaciones)_""", 'botones': [
                        {"text": "✅ Es correcto, continuar", "value": "continuar"},
                        {"text": "✏️ Agregar detalles", "value": "agregar"}
                    ], 'estado': estado, 'datos_generados': {'alcance_proyecto': alcance_inicial}}
                else:
                    estado["etapa"] = "descripcion"
                    
                    # Obtener nombre del proyecto del formulario inicial
                    nombre_proyecto = estado.get("proyecto_nombre", "")
                    
                    mensaje_descripcion = f"""✅ Área: **{area:,.0f} m²**

📝 **Descripción del proyecto:**"""
                    
                    if nombre_proyecto:
                        mensaje_descripcion += f"""
Veo que el proyecto es: **{nombre_proyecto}**

¿Necesitas agregar más detalles técnicos? (sistemas, equipos, especificaciones)
_Ejemplo: Sistema eléctrico industrial completo con subestación de 1000 KVA, tableros de distribución, sistema de automatización SCADA, iluminación LED, sistema de respaldo UPS_

Si no necesitas agregar más, simplemente escribe "No" o "Continuar"."""
                    else:
                        mensaje_descripcion += """
_Incluye: tipo de instalación, sistemas, equipos principales, etc._
_Ejemplo: Sistema eléctrico industrial completo con subestación de 1000 KVA, tableros de distribución, sistema de automatización SCADA, iluminación LED, sistema de respaldo UPS_"""
                    
                    return {'success': True, 'respuesta': mensaje_descripcion, 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Área inválida. Por favor ingresa solo números.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Confirmar Alcance (NUEVA)
        # ============================================
        elif etapa == "confirmar_alcance":
            texto_usuario = mensaje.lower().strip()
            
            # Caso 1: Confirmación directa
            if texto_usuario in ["continuar", "si", "sí", "correcto", "ok", "listo", "no", "ninguno"]:
                estado["etapa"] = "kpi_spi" # ✅ RESTAURADO: Flujo hacia KPIs
                
                # Obtener alcance confirmado para mostrar en respuesta
                alcance_final = estado.get("alcance_proyecto", "")
                
                return {'success': True, 'respuesta': f"""✅ **Datos guardados correctamente.**
                
Entendido. El alcance del proyecto se mantiene como:
*"{alcance_final}"*

━━━━━━━━━━━━━━━━━━━━━━━
**KPIs DE GESTIÓN PMI**
━━━━━━━━━━━━━━━━━━━━━━━

Como proyecto complejo PMI, necesitamos definir los KPIs de gestión.
Te ayudaré con valores recomendados según mejores prácticas.

📊 **SPI (Schedule Performance Index)**
_Mide el desempeño del cronograma_

Valores:
• **1.0** = En tiempo (recomendado)
• > 1.0 = Adelantado
• < 1.0 = Retrasado

Rango válido: 0.8 - 1.2

**¿Valor de SPI?**
_Ejemplo: 1.0_""", 'botones': None, 'estado': estado, 'datos_generados': {'alcance_proyecto': alcance_final}}
            
            # Caso 2: Usuario decide agregar detalles (botón)
            elif texto_usuario == "agregar":
                 return {'success': True, 'respuesta': """📝 **Por favor escribe los detalles adicionales que deseas agregar:**""", 'botones': None, 'estado': estado}
            
            # Caso 3: Usuario escribe texto adicional
            else:
                 # Concatenar al alcance existente
                 alcance_actual = estado.get("alcance_proyecto", "")
                 nuevo_alcance = f"{alcance_actual}\n\nDetalles adicionales: {mensaje}"
                 estado["alcance_proyecto"] = nuevo_alcance
                 estado["etapa"] = "kpi_spi" # ✅ RESTAURADO: Flujo hacia KPIs
                 
                 return {'success': True, 'respuesta': f"""✅ **Datos guardados y actualizados correctamente.**

He agregado la información adicional al alcance del proyecto.

━━━━━━━━━━━━━━━━━━━━━━━
**KPIs DE GESTIÓN PMI**
━━━━━━━━━━━━━━━━━━━━━━━

Como proyecto complejo PMI, necesitamos definir los KPIs de gestión.

📊 **SPI (Schedule Performance Index)**
_Mide el desempeño del cronograma_

**¿Valor de SPI?**
_Ejemplo: 1.0_""", 'botones': None, 'estado': estado, 'datos_generados': {'alcance_proyecto': nuevo_alcance}}

        # ============================================
        # ETAPA: Descripción
        # ============================================
        elif etapa == "descripcion":
            # El usuario DEBE escribir la descripción detallada del proyecto
            # NO confundir con el nombre del proyecto
            estado["descripcion_inicial"] = mensaje
            estado["etapa"] = "descripcion_adicional"
            return {'success': True, 'respuesta': """✅ Descripción inicial guardada

💡 **¿Quieres agregar más detalles técnicos?**
_Ejemplo: especificaciones de equipos, sistemas adicionales, requisitos especiales_

[Sí, agregar más] [No, continuar]""", 'botones': [
                {'text': '✅ Sí, agregar más', 'value': 'SI_AGREGAR'},
                {'text': '➡️ No, continuar', 'value': 'NO_AGREGAR'}
            ], 'estado': estado}
        
        # ============================================
        # ETAPA: Descripción Adicional (Pregunta Sí/No)
        # ============================================
        elif etapa == "descripcion_adicional":
            if mensaje == "SI_AGREGAR":
                estado["etapa"] = "descripcion_extra"
                return {'success': True, 'respuesta': """📝 **Describe los detalles técnicos adicionales:**

_Ejemplo: Sistema de automatización SCADA, iluminación LED inteligente, sistema de respaldo UPS de 100 KVA, etc._""", 'botones': None, 'estado': estado}
            else:  # NO_AGREGAR
                # Solo usar descripción inicial
                estado["descripcion"] = estado.get("descripcion_inicial", "")
                estado["etapa"] = "normativa"
                return {'success': True, 'respuesta': f"""✅ Descripción: **{estado['descripcion']}**

📋 **Normativa aplicable:**
_Selecciona la normativa principal_

[CNE Suministro 2011] [NEC 2020] [IEC] [Otra]""", 'botones': [
                    {'text': 'CNE Suministro 2011', 'value': 'CNE Suministro 2011'},
                    {'text': 'NEC 2020', 'value': 'NEC 2020'},
                    {'text': 'IEC', 'value': 'IEC'},
                    {'text': 'Otra', 'value': 'OTRA'}
                ], 'estado': estado}
        
        # ============================================
        # ETAPA: Descripción Extra (Detalles Adicionales)
        # ============================================
        elif etapa == "descripcion_extra":
            # Concatenar descripción inicial + detalles adicionales
            desc_inicial = estado.get("descripcion_inicial", "")
            estado["descripcion"] = f"{desc_inicial}\n\n{mensaje}"
            estado["etapa"] = "normativa"
            return {'success': True, 'respuesta': f"""✅ Descripción completa guardada

📋 **Normativa aplicable:**
_Selecciona la normativa principal_

[CNE Suministro 2011] [NEC 2020] [IEC] [Otra]""", 'botones': [
                {'text': 'CNE Suministro 2011', 'value': 'CNE Suministro 2011'},
                {'text': 'NEC 2020', 'value': 'NEC 2020'},
                {'text': 'IEC', 'value': 'IEC'},
                {'text': 'Otra', 'value': 'OTRA'}
            ], 'estado': estado}
        
        # ============================================
        # ETAPA: Normativa
        # ============================================
        elif etapa == "normativa":
            if mensaje == "OTRA":
                estado["etapa"] = "normativa_otra"
                return {'success': True, 'respuesta': "📋 **Especifica la normativa:**", 'botones': None, 'estado': estado}
            else:
                estado["normativa"] = mensaje
                estado["etapa"] = "fecha_inicio"
                return {'success': True, 'respuesta': f"""✅ Normativa: **{mensaje}**

📅 **Fecha de inicio estimada (DD/MM/YYYY):**
_Ejemplo: 01/02/2026_""", 'botones': None, 'estado': estado}
        
        elif etapa == "normativa_otra":
            estado["normativa"] = mensaje
            estado["etapa"] = "fecha_inicio"
            return {'success': True, 'respuesta': f"""✅ Normativa: **{mensaje}**

📅 **Fecha de inicio estimada (DD/MM/YYYY):**""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Fecha inicio
        # ============================================
        elif etapa == "fecha_inicio":
            try:
                fecha = datetime.strptime(mensaje, "%d/%m/%Y")
                estado["fecha_inicio"] = mensaje
                estado["etapa"] = "kpi_spi"
                return {'success': True, 'respuesta': f"""✅ Fecha inicio: **{mensaje}**

━━━━━━━━━━━━━━━━━━━━━━━
**KPIs DE GESTIÓN PMI**
━━━━━━━━━━━━━━━━━━━━━━━

Como proyecto complejo PMI, necesitamos definir los KPIs de gestión.
Te ayudaré con valores recomendados según mejores prácticas.

📊 **SPI (Schedule Performance Index)**
_Mide el desempeño del cronograma_

Valores:
• **1.0** = En tiempo (recomendado)
• > 1.0 = Adelantado
• < 1.0 = Retrasado

Rango válido: 0.8 - 1.2

**¿Valor de SPI?**
_Ejemplo: 1.0_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Formato de fecha inválido. Usa DD/MM/YYYY", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - SPI
        # ============================================
        elif etapa == "kpi_spi":
            try:
                spi = float(mensaje)
                if spi < 0.5 or spi > 1.5:
                    return {'success': False, 'respuesta': "⚠️ SPI fuera de rango razonable (0.5-1.5). Por favor verifica.", 'botones': None, 'estado': estado}
                estado["spi"] = spi
                estado["etapa"] = "kpi_cpi"
                return {'success': True, 'respuesta': f"""✅ SPI: **{spi}**

📊 **CPI (Cost Performance Index)**
_Mide el desempeño del costo_

Valores:
• **1.0** = En presupuesto (recomendado)
• > 1.0 = Bajo presupuesto
• < 1.0 = Sobre presupuesto

Rango válido: 0.8 - 1.2

**¿Valor de CPI?**
_Ejemplo: 1.05_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número decimal (ej: 1.0)", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - CPI
        # ============================================
        elif etapa == "kpi_cpi":
            try:
                cpi = float(mensaje)
                if cpi < 0.5 or cpi > 1.5:
                    return {'success': False, 'respuesta': "⚠️ CPI fuera de rango razonable (0.5-1.5). Por favor verifica.", 'botones': None, 'estado': estado}
                estado["cpi"] = cpi
                estado["etapa"] = "kpi_ev"
                
                presupuesto = estado.get("presupuesto", 100000)
                sugerencia_ev = int(presupuesto * 0.70 / 1000)
                
                return {'success': True, 'respuesta': f"""✅ CPI: **{cpi}**

📊 **EV (Earned Value)**
_Valor ganado del proyecto en miles_

Sugerencia: **${sugerencia_ev}K** (70% del presupuesto)

**¿Valor de EV en miles?**
_Ejemplo: {sugerencia_ev}_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número decimal (ej: 1.05)", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - EV
        # ============================================
        elif etapa == "kpi_ev":
            try:
                ev = int(mensaje)
                estado["ev_k"] = ev
                estado["etapa"] = "kpi_pv"
                
                presupuesto = estado.get("presupuesto", 100000)
                sugerencia_pv = int(presupuesto * 0.75 / 1000)
                
                return {'success': True, 'respuesta': f"""✅ EV: **${ev}K**

📊 **PV (Planned Value)**
_Valor planificado del proyecto en miles_

Sugerencia: **${sugerencia_pv}K** (75% del presupuesto)

**¿Valor de PV en miles?**
_Ejemplo: {sugerencia_pv}_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número entero.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - PV
        # ============================================
        elif etapa == "kpi_pv":
            try:
                pv = int(mensaje)
                estado["pv_k"] = pv
                estado["etapa"] = "kpi_ac"
                
                presupuesto = estado.get("presupuesto", 100000)
                sugerencia_ac = int(presupuesto * 0.65 / 1000)
                
                return {'success': True, 'respuesta': f"""✅ PV: **${pv}K**

📊 **AC (Actual Cost)**
_Costo real del proyecto en miles_

Sugerencia: **${sugerencia_ac}K** (65% del presupuesto)

**¿Valor de AC en miles?**
_Ejemplo: {sugerencia_ac}_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número entero.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: KPI - AC
        # ============================================
        elif etapa == "kpi_ac":
            try:
                ac = int(mensaje)
                estado["ac_k"] = ac
                estado["etapa"] = "procesar_gantt"  # ✅ SALTAR ALCANCE (ya se captura en formulario)
                
                # ✅ Obtener símbolo de moneda dinámicamente
                moneda = estado.get('moneda', 'USD')
                simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€', 'GBP': '£'}.get(moneda, '$')
                
                # 🔍 DEBUG: Verificar moneda y símbolo
                print(f"🔍 DEBUG KPI - Moneda: {moneda}, Símbolo: {simbolo}")
                
                return {'success': True, 'respuesta': f"""✅ AC: **{simbolo}{ac}K**

━━━━━━━━━━━━━━━━━━━━━━━
✅ **KPIs PMI COMPLETADOS**
━━━━━━━━━━━━━━━━━━━━━━━

SPI: {estado.get('spi')} | CPI: {estado.get('cpi')}
EV: {simbolo}{estado.get('ev_k')}K | PV: {simbolo}{estado.get('pv_k')}K | AC: {simbolo}{ac}K

━━━━━━━━━━━━━━━━━━━━━━━
**CRONOGRAMA GANTT**
━━━━━━━━━━━━━━━━━━━━━━━

📅 **Definición de Duración de Fases:**
Usa el panel interactivo para ajustar los días.""", 'botones': None, 'estado': estado, 'datos_generados': {
                    'spi': estado.get('spi'),
                    'cpi': estado.get('cpi'),
                    'ev_k': estado.get('ev_k'),
                    'pv_k': estado.get('pv_k'),
                    'ac_k': ac
                }, 'formulario': {'tipo': 'gantt_dias'}}

            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa un número entero.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Alcance
        # ============================================
        elif etapa == "alcance":
            estado["alcance"] = mensaje
            estado["etapa"] = "procesar_gantt"
            return {'success': True, 'respuesta': f"""✅ Alcance definido

━━━━━━━━━━━━━━━━━━━━━━━
**CRONOGRAMA GANTT (6 FASES)**
━━━━━━━━━━━━━━━━━━━━━━━

El cronograma PMI tiene 6 fases:

**Fases fijas:**
1. Inicio y Planificación: **10 días**
2. Gestión Stakeholders: **3 días**
3. Ingeniería y Diseño: **[VARIABLE]**
4. Ejecución: **[VARIABLE]**
5. Pruebas y Puesta en Marcha: **8 días**
6. Cierre: **5 días**

Usa el panel interactivo para ajustar las fases variables.""", 'botones': None, 'estado': estado, 'formulario': {'tipo': 'gantt_dias'}}
        
        # ============================================
        # ETAPA: Procesar Gantt (NUEVA - Reemplaza dias individuales)
        # ============================================
        elif etapa == "procesar_gantt":
            import re
            try:
                # Intentar parsear el texto del formulario estructurado
                texto = mensaje.lower()
                
                # Valores por defecto (PMI estándar)
                dias_fases = {
                    "inicio": 5,
                    "planificacion": 10,
                    "riesgos": 5,
                    "ingenieria": 25,
                    "ejecucion": 45,
                    "pruebas": 10,
                    "cierre": 5
                }
                
                # Extraer duración total del mensaje "Duración Total: X días"
                match_total = re.search(r'duraci[oó]n total:\s*(\d+)', texto)
                duracion_total = int(match_total.group(1)) if match_total else 105
                
                # Extraer Ingeniería y Ejecución para compatibilidad
                match_ing = re.search(r'ingenier[ií]a.*?:\s*(\d+)', texto)
                match_ejec = re.search(r'ejecuci[oó]n.*?:\s*(\d+)', texto)
                
                if match_ing: dias_fases["ingenieria"] = int(match_ing.group(1))
                if match_ejec: dias_fases["ejecucion"] = int(match_ejec.group(1))
                
                # ✅ NUEVO: Extraer Configuración de Calendario
                config_calendario = {
                    "dias_semana": "LUN-SAB", # Default
                    "horas_dia": 8
                }
                
                match_cal = re.search(r'calendario:\s*([A-Z-]+)', texto, re.IGNORECASE)
                match_horas = re.search(r'\((\d+)h/día\)', texto)
                
                if match_cal: config_calendario["dias_semana"] = match_cal.group(1)
                if match_horas: config_calendario["horas_dia"] = int(match_horas.group(1))
                
                # Guardar en estado para uso posterior
                estado["dias_ingenieria"] = dias_fases["ingenieria"]
                estado["dias_ejecucion"] = dias_fases["ejecucion"]
                estado["cronograma_fases"] = dias_fases
                estado["duracion_total"] = duracion_total
                estado["configuracion_calendario"] = config_calendario # ✅ Guardamos config
                
                estado["etapa"] = "riesgo1_desc"
                return {'success': True, 'respuesta': f"""✅ Cronograma Maestro Configurado (7 Fases):
• Ingeniería y Diseño: **{dias_fases['ingenieria']} días**
• Ejecución y Obra: **{dias_fases['ejecucion']} días**
• Calendario: **{config_calendario['dias_semana']} ({config_calendario['horas_dia']}h/día)**

Duración Total Estimada: **{duracion_total} días hábiles**

━━━━━━━━━━━━━━━━━━━━━━━
**REGISTRO DE RIESGOS**
━━━━━━━━━━━━━━━━━━━━━━━

Según el nivel de complejidad seleccionado, identificaremos los riesgos principales.

Para cada riesgo necesito:
• Descripción
• Probabilidad (Alta/Media/Baja)
• Impacto (Alto/Medio/Bajo)
• Plan de Mitigación

━━━━━━━━━━━━━━━━━━━━━━━
**RIESGO 1 de {estado.get('complejidad', 7) - 2}**
━━━━━━━━━━━━━━━━━━━━━━━

📝 **Descripción del riesgo:**
_Ejemplo: Retrasos en entrega de equipos importados_""", 'botones': None, 'estado': estado}
            except Exception as e:
                 # Fallback manual si falla el regex
                print(f"Error parsing gantt: {e}")
                estado["etapa"] = "dias_ingenieria"
                return {'success': False, 'respuesta': "❌ No pude leer la configuración del Gantt completa. Por favor ingresa los días de Ingeniería manualmente.", 'botones': None, 'estado': estado}

        # ============================================
        # ETAPA: Días Ingeniería (Deprecated / Fallback)
        # ============================================
        elif etapa == "dias_ingenieria":
            try:
                dias = int(mensaje)
                if dias < 5 or dias > 90:
                    return {'success': False, 'respuesta': "⚠️ Duración fuera de rango razonable (5-90 días).", 'botones': None, 'estado': estado}
                estado["dias_ingenieria"] = dias
                estado["etapa"] = "dias_ejecucion"
                return {'success': True, 'respuesta': f"""✅ Ingeniería y Diseño: **{dias} días**

⏱️ **Días para Ejecución:**
_Sugerencia: 40-60 días_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa solo el número de días.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Días Ejecución
        # ============================================
        elif etapa == "dias_ejecucion":
            try:
                dias = int(mensaje)
                if dias < 10 or dias > 180:
                    return {'success': False, 'respuesta': "⚠️ Duración fuera de rango razonable (10-180 días).", 'botones': None, 'estado': estado}
                estado["dias_ejecucion"] = dias
                
                # Calcular duración total
                duracion_total = 10 + 3 + estado.get("dias_ingenieria", 25) + dias + 8 + 5
                estado["duracion_total"] = duracion_total
                
                estado["etapa"] = "riesgo1_desc"
                return {'success': True, 'respuesta': f"""✅ Ejecución: **{dias} días**

━━━━━━━━━━━━━━━━━━━━━━━
✅ **CRONOGRAMA COMPLETADO**
━━━━━━━━━━━━━━━━━━━━━━━

Duración total: **{duracion_total} días**

1. Inicio y Planificación: 10 días
2. Gestión Stakeholders: 3 días
3. Ingeniería y Diseño: {estado.get('dias_ingenieria')} días
4. Ejecución: {dias} días
5. Pruebas y Puesta en Marcha: 8 días
6. Cierre: 5 días

━━━━━━━━━━━━━━━━━━━━━━━
**REGISTRO DE RIESGOS**
━━━━━━━━━━━━━━━━━━━━━━━

Según el nivel de complejidad seleccionado, identificaremos los riesgos principales.

Para cada riesgo necesito:
• Descripción
• Probabilidad (Alta/Media/Baja)
• Impacto (Alto/Medio/Bajo)
• Plan de Mitigación

━━━━━━━━━━━━━━━━━━━━━━━
**RIESGO 1 de {estado.get('complejidad', 7) - 2}**
━━━━━━━━━━━━━━━━━━━━━━━

📝 **Descripción del riesgo:**
_Ejemplo: Retrasos en entrega de equipos importados_""", 'botones': None, 'estado': estado}
            except:
                return {'success': False, 'respuesta': "❌ Valor inválido. Ingresa solo el número de días.", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Riesgos (Loop de 5)
        # ============================================
        elif etapa.startswith("riesgo"):
            return self._procesar_riesgo(mensaje, estado)
        
        # ============================================
        # ETAPA: Recursos Humanos
        # ============================================
        # ============================================
        # ETAPA: Selección de Profesionales
        # ============================================
        elif etapa == "form_profesionales":
            # Procesar respuesta (llega texto desde el formulario)
            estado["recursos_humanos"] = [r.strip() for r in mensaje.split(',') if r.strip()]
            
            complejidad = estado.get('complejidad', 7)
            
            if complejidad >= 7:
                # Nivel Avanzado: Continuar con formulario de entregables
                estado["etapa"] = "form_entregables"
                
                return {
                    'success': True,
                    'respuesta': f"""✅ Equipo registrado correctamente.

━━━━━━━━━━━━━━━━━━━━━━━
**ENTREGABLES DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

Ahora define los entregables clave que se comprometen con el cliente.
He precargado una lista estándar según PMI. Selecciona los que apliquen.""",
                    'botones': None,
                    'estado': estado,
                    'formulario': {
                        'tipo': 'entregables',
                        'tipoProyecto': 'electricidad-complejo',
                        'presupuesto': estado.get('presupuesto'),
                        'area': estado.get('area_m2')
                    }
                }
            else:
                # Nivel Intermedio (6 fases): Pedir materiales como texto y generar
                estado["etapa"] = "materiales_texto"
                return {'success': True, 'respuesta': f"""✅ Equipo profesional registrado.

🔧 **Materiales principales (separados por coma):**
_Ejemplo: Tableros eléctricos, Cables THW, Protecciones termomagnéticas, Sistema de puesta a tierra_""", 'botones': None, 'estado': estado}

        # ============================================
        # ETAPA: Selección de Entregables
        # ============================================
        elif etapa == "form_entregables":
            estado["entregables_seleccionados"] = [e.strip() for e in mensaje.split(',') if e.strip()]
            
            estado["etapa"] = "form_suministros"
            
            return {
                'success': True,
                'respuesta': f"""✅ Entregables registrados.

━━━━━━━━━━━━━━━━━━━━━━━
**SUMINISTROS Y MATERIALES**
━━━━━━━━━━━━━━━━━━━━━━━

Finalmente, selecciona los suministros principales para calcular el presupuesto detallado.""",
                'botones': None,
                'estado': estado,
                'formulario': {
                    'tipo': 'suministros',
                    'tipoProyecto': 'electricidad-complejo',
                    'presupuesto': estado.get('presupuesto'),
                    'area': estado.get('area_m2')
                }
            }

        # ============================================
        # ETAPA: Selección de Suministros
        # ============================================
        elif etapa == "form_suministros":
            estado["materiales"] = [m.strip() for m in mensaje.split(',') if m.strip()]
            return self._generar_proyecto(estado)
        
        # ============================================
        # ETAPA: Recursos Texto (Para complejidad 5 - Básico)
        # ============================================
        elif etapa == "recursos_texto":
            recursos = [r.strip() for r in mensaje.split(',') if r.strip()]
            estado["recursos_humanos"] = recursos
            estado["etapa"] = "materiales_texto"
            return {'success': True, 'respuesta': f"""✅ Equipo: **{len(recursos)} roles** definidos

🔧 **Materiales principales (separados por coma):**
_Ejemplo: Tableros eléctricos, Cables THW, Protecciones termomagnéticas, Sistema de puesta a tierra_""", 'botones': None, 'estado': estado}
        
        # ============================================
        # ETAPA: Materiales Texto (Para complejidad 5 - Básico)
        # ============================================
        elif etapa == "materiales_texto":
            materiales = [m.strip() for m in mensaje.split(',') if m.strip()]
            estado["materiales"] = materiales
            return self._generar_proyecto(estado)
    
    def _procesar_riesgo(self, mensaje: str, estado: Dict) -> Dict:
        """Procesa el loop de 5 riesgos"""
        etapa = estado.get("etapa")
        
        # Inicializar lista de riesgos si no existe
        if "riesgos" not in estado:
            estado["riesgos"] = []
        
        # Extraer número de riesgo y campo
        partes = etapa.split("_")
        num_riesgo = int(partes[0].replace("riesgo", ""))
        campo = "_".join(partes[1:])
        
        # Inicializar riesgo temporal si no existe
        if "riesgo_temp" not in estado:
            estado["riesgo_temp"] = {}
        
        if campo == "desc":
            estado["riesgo_temp"]["descripcion"] = mensaje
            estado["etapa"] = f"riesgo{num_riesgo}_prob"
            return {'success': True, 'respuesta': f"""✅ Descripción: **{mensaje}**

📊 **Probabilidad del riesgo:**

[Alta] [Media] [Baja]""", 'botones': [
                {'text': 'Alta', 'value': 'Alta'},
                {'text': 'Media', 'value': 'Media'},
                {'text': 'Baja', 'value': 'Baja'}
            ], 'estado': estado}
        
        elif campo == "prob":
            estado["riesgo_temp"]["probabilidad"] = mensaje
            estado["etapa"] = f"riesgo{num_riesgo}_imp"
            return {'success': True, 'respuesta': f"""✅ Probabilidad: **{mensaje}**

💥 **Impacto del riesgo:**

[Alto] [Medio] [Bajo]""", 'botones': [
                {'text': 'Alto', 'value': 'Alto'},
                {'text': 'Medio', 'value': 'Medio'},
                {'text': 'Bajo', 'value': 'Bajo'}
            ], 'estado': estado}
        
        elif campo == "imp":
            estado["riesgo_temp"]["impacto"] = mensaje
            estado["etapa"] = f"riesgo{num_riesgo}_mit"
            
            # Calcular severidad
            prob = estado["riesgo_temp"]["probabilidad"]
            imp = mensaje
            severidad = self._calcular_severidad(prob, imp)
            estado["riesgo_temp"]["severidad"] = severidad
            
            return {'success': True, 'respuesta': f"""✅ Impacto: **{mensaje}**
✅ Severidad calculada: **{severidad}**

🛡️ **Plan de Mitigación:**
_Describe las acciones para reducir o eliminar el riesgo_
_Ejemplo: Compra anticipada de equipos críticos con proveedores alternativos_""", 'botones': None, 'estado': estado}
        
        elif campo == "mit":
            estado["riesgo_temp"]["mitigacion"] = mensaje
            estado["riesgo_temp"]["id"] = f"R{num_riesgo:02d}"
            
            # Guardar riesgo completo
            estado["riesgos"].append(estado["riesgo_temp"].copy())
            estado.pop("riesgo_temp")
            
            # Verificar si hay más riesgos (adaptativo según complejidad)
            complejidad = estado.get('complejidad', 7)
            max_riesgos = {5: 3, 6: 4, 7: 5}.get(complejidad, 5)
            
            if num_riesgo < max_riesgos:
                estado["etapa"] = f"riesgo{num_riesgo + 1}_desc"
                return {'success': True, 'respuesta': f"""✅ Plan de mitigación guardado

━━━━━━━━━━━━━━━━━━━━━━━
✅ **RIESGO {num_riesgo} COMPLETADO**
━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━
**RIESGO {num_riesgo + 1} de {max_riesgos}**
━━━━━━━━━━━━━━━━━━━━━━━

📝 **Descripción del riesgo:**""", 'botones': None, 'estado': estado}
            else:
                # Todos los riesgos completados - Flujo adaptativo
                complejidad = estado.get('complejidad', 7)
                
                if complejidad >= 7:
                    # Nivel Avanzado: Formulario de profesionales
                    estado["etapa"] = "form_profesionales"
                    return {
                        'success': True,
                        'respuesta': f"""✅ Plan de mitigación guardado

━━━━━━━━━━━━━━━━━━━━━━━
✅ **TODOS LOS RIESGOS COMPLETADOS**
━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━
**EQUIPO Y RECURSOS**
━━━━━━━━━━━━━━━━━━━━━━━

Ahora vamos a definir el equipo profesional necesario.
Usa el formulario interactivo para seleccionar roles y cantidades.""",
                        'botones': None,
                        'estado': estado,
                        'formulario': {
                            'tipo': 'profesionales',
                            'tipoProyecto': 'electricidad-complejo',
                            'presupuesto': estado.get('presupuesto'),
                            'area': estado.get('area_m2')
                        }
                    }
                elif complejidad == 6:
                    # Nivel Intermedio: Solo formulario de profesionales
                    estado["etapa"] = "form_profesionales"
                    return {
                        'success': True,
                        'respuesta': f"""✅ Plan de mitigación guardado

━━━━━━━━━━━━━━━━━━━━━━━
✅ **TODOS LOS RIESGOS COMPLETADOS**
━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━
**EQUIPO PROFESIONAL**
━━━━━━━━━━━━━━━━━━━━━━━

Define el equipo profesional usando el formulario interactivo.""",
                        'botones': None,
                        'estado': estado,
                        'formulario': {
                            'tipo': 'profesionales',
                            'tipoProyecto': 'electricidad-complejo',
                            'presupuesto': estado.get('presupuesto'),
                            'area': estado.get('area_m2')
                        }
                    }
                else:
                    return {
                        'success': True,
                        'respuesta': f"""✅ Plan de mitigación guardado

━━━━━━━━━━━━━━━━━━━━━━━
✅ **TODOS LOS RIESGOS COMPLETADOS**
━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━
**EQUIPO Y RECURSOS**
━━━━━━━━━━━━━━━━━━━━━━━

Aunque es un proyecto básico, definamos el equipo principal.
Usa el formulario interactivo para seleccionar roles.""",
                        'botones': None,
                        'estado': estado,
                        'formulario': {
                            'tipo': 'profesionales',
                            'tipoProyecto': 'electricidad-complejo',
                            'presupuesto': estado.get('presupuesto'),
                            'area': estado.get('area_m2')
                        }
                    }
        
        return {'success': False, 'respuesta': "❌ Campo de riesgo no reconocido", 'botones': None, 'estado': estado}
    
    def _calcular_severidad(self, probabilidad: str, impacto: str) -> str:
        """Calcula la severidad del riesgo según probabilidad e impacto"""
        matriz = {
            ('Alta', 'Alto'): 'Alta',
            ('Alta', 'Medio'): 'Alta',
            ('Alta', 'Bajo'): 'Media',
            ('Media', 'Alto'): 'Alta',
            ('Media', 'Medio'): 'Media',
            ('Media', 'Bajo'): 'Baja',
            ('Baja', 'Alto'): 'Media',
            ('Baja', 'Medio'): 'Baja',
            ('Baja', 'Bajo'): 'Baja'
        }
        return matriz.get((probabilidad, impacto), 'Media')
    
    def _generar_proyecto(self, estado: Dict) -> Dict:
        """Genera el proyecto completo con todos los datos"""
        
        # Datos del cliente y proyecto
        cliente = estado.get("cliente_nombre", "Cliente")
        nombre_proyecto = estado.get("nombre_proyecto", "Proyecto Eléctrico")
        ubicacion = estado.get("ubicacion", "Lima, Perú")
        area = estado.get("area_m2", 1000)
        descripcion = estado.get("descripcion", "Proyecto eléctrico")
        normativa = estado.get("normativa", "CNE Suministro 2011")
        presupuesto = estado.get("presupuesto", 100000)
        moneda = estado.get("moneda", "USD")
        
        # ✅ CORREGIDO: Leer servicio/industria de estado_inicial si no están en estado actual
        estado_inicial = estado.get("estado_inicial", {})
        servicio = estado.get("servicio") or estado_inicial.get("servicio", "electricidad")
        industria = estado.get("industria") or estado_inicial.get("industria", "construccion")
        
        # Fechas y duración
        fecha_inicio_str = estado.get("fecha_inicio", "01/01/2026")
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        except:
            fecha_inicio = datetime.now()

        # ✅ NUEVO: Priorizar datos del calendario
        duracion_dias = estado.get("duracion_dias")
        if duracion_dias:
            duracion_total = int(duracion_dias)
        else:
            # Fallback a lógica anterior
            duracion_total = estado.get("duracion_total", 100)
            if not duracion_total: duracion_total = 100

        # ✅ NUEVO: Priorizar fecha fin exacta del calendario
        fecha_fin_str = estado.get("fecha_fin")
        if fecha_fin_str:
            try:
                fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
            except:
                fecha_fin = fecha_inicio + timedelta(days=duracion_total)
        else:
            fecha_fin = fecha_inicio + timedelta(days=duracion_total)
        
        # Código proyecto
        codigo = f"PROY-PMI-{fecha_inicio.year}-{self.contador:03d}"
        self.contador += 1
        
        # KPIs
        spi = estado.get("spi", 1.0)
        cpi = estado.get("cpi", 1.0)
        ev_k = estado.get("ev_k", 70)
        pv_k = estado.get("pv_k", 75)
        ac_k = estado.get("ac_k", 65)
        
        # Alcance - ✅ CORREGIDO: Usar clave correcta que envía el frontend
        alcance = estado.get("alcance_proyecto", estado.get("alcance", "Alcance del proyecto"))
        
        # Cronograma
        dias_ingenieria = estado.get("dias_ingenieria", 25)
        dias_ejecucion = estado.get("dias_ejecucion", 50)
        
        # Stakeholders (siempre los 3 básicos)
        stakeholders = [
            {
                "nombre": cliente,
                "rol": "Cliente / Patrocinador Principal",
                "poder": "Alto",
                "interes": "Alto"
            },
            {
                "nombre": "Jefe de Proyecto",
                "rol": "Project Manager / Responsable de Ejecución",
                "poder": "Alto",
                "interes": "Alto"
            },
            {
                "nombre": "Equipo Técnico",
                "rol": "Ingenieros y Técnicos Instaladores",
                "poder": "Medio",
                "interes": "Alto"
            }
        ]
        
        # Riesgos
        riesgos = estado.get("riesgos", [])
        
        # Recursos
        recursos_humanos = estado.get("recursos_humanos", ["Project Manager", "Ing. Residente", "Técnicos"])
        materiales = estado.get("materiales", ["Tableros eléctricos", "Cables", "Protecciones"])
        
        # ✅ CORREGIDO: Usar cronograma configurado por el usuario en el formulario Gantt
        # Si el usuario configuró el Gantt manualmente, usar esos datos
        # De lo contrario, generar valores por defecto según complejidad
        complejidad = estado.get("complejidad", 7)
        
        if "cronograma_fases" in estado and isinstance(estado["cronograma_fases"], dict):
            # ✅ Usuario configuró el Gantt - convertir diccionario a formato visual
            fases_dict = estado["cronograma_fases"]
            duracion_total_real = estado.get("duracion_total", 105)
            
            # Función helper para calcular ancho porcentual
            def calc_width(dias):
                return f"{max(5, int((dias / duracion_total_real) * 100))}%"
            
            cronograma_fases = [
                {"label": "1. Inicio", "dias": f"{fases_dict.get('inicio', 5)} días", "width": calc_width(fases_dict.get('inicio', 5))},
                {"label": "2. Planificación Detallada", "dias": f"{fases_dict.get('planificacion', 10)} días", "width": calc_width(fases_dict.get('planificacion', 10))},
                {"label": "3. Gestión de Riesgos y Calidad", "dias": f"{fases_dict.get('riesgos', 5)} días", "width": calc_width(fases_dict.get('riesgos', 5))},
                {"label": "4. Ingeniería y Diseño", "dias": f"{fases_dict.get('ingenieria', 25)} días", "width": calc_width(fases_dict.get('ingenieria', 25))},
                {"label": "5. Ejecución y Monitoreo", "dias": f"{fases_dict.get('ejecucion', 45)} días", "width": calc_width(fases_dict.get('ejecucion', 45))},
                {"label": "6. Pruebas Integrales (FAT/SAT)", "dias": f"{fases_dict.get('pruebas', 10)} días", "width": calc_width(fases_dict.get('pruebas', 10))},
                {"label": "7. Cierre y Lecciones Aprendidas", "dias": f"{fases_dict.get('cierre', 5)} días", "width": calc_width(fases_dict.get('cierre', 5))}
            ]
        else:
            # Fallback: Generar cronograma por defecto según complejidad
            cronograma_fases = []
        
            if complejidad == 5:
                cronograma_fases = [
                    {"label": "1. Inicio y Planificación", "dias": "5 días", "width": "20%"},
                    {"label": "2. Ingeniería Básica", "dias": f"{int(dias_ingenieria/2)} días", "width": "15%"},
                    {"label": "3. Ejecución", "dias": f"{dias_ejecucion} días", "width": "40%"},
                    {"label": "4. Pruebas", "dias": "5 días", "width": "15%"},
                    {"label": "5. Cierre", "dias": "2 días", "width": "10%"}
                ]
            elif complejidad == 6:
                cronograma_fases = [
                    {"label": "1. Inicio y Planificación", "dias": "10 días", "width": "15%"},
                    {"label": "2. Gestión Stakeholders", "dias": "3 días", "width": "10%"},
                    {"label": "3. Ingeniería y Diseño", "dias": f"{dias_ingenieria} días", "width": "20%"},
                    {"label": "4. Ejecución", "dias": f"{dias_ejecucion} días", "width": "35%"},
                    {"label": "5. Pruebas y Puesta en Marcha", "dias": "8 días", "width": "12%"},
                    {"label": "6. Cierre", "dias": "5 días", "width": "8%"}
                ]
            else: # 7 Fases
                cronograma_fases = [
                    {"label": "1. Inicio", "dias": "5 días", "width": "10%"},
                    {"label": "2. Planificación Detallada", "dias": "10 días", "width": "15%"},
                    {"label": "3. Gestión de Riesgos y Calidad", "dias": "5 días", "width": "10%"},
                    {"label": "4. Ingeniería y Diseño", "dias": f"{dias_ingenieria} días", "width": "20%"},
                    {"label": "5. Ejecución y Monitoreo", "dias": f"{dias_ejecucion} días", "width": "30%"},
                    {"label": "6. Pruebas Integrales (FAT/SAT)", "dias": "10 días", "width": "10%"},
                    {"label": "7. Cierre y Lecciones Aprendidas", "dias": "5 días", "width": "5%"}
                ]
            
        # ✅ NUEVO: Generar RACI por defecto según complejidad
        raci_actividades = estado.get("raci_actividades", [])
        if not raci_actividades and complejidad >= 6:
            # Solo generar RACI si complejidad >= 6 y no existe
            raci_actividades = [
                {"actividad": "Planificación del Proyecto", "roles": ["A", "R", "I", "C", "C"]},
                {"actividad": "Diseño e Ingeniería", "roles": ["A", "R", "C", "C", "I"]},
                {"actividad": "Ejecución de Obra", "roles": ["A", "A", "R", "C", "I"]},
                {"actividad": "Control de Calidad", "roles": ["A", "C", "C", "R", "I"]},
                {"actividad": "Aprobación de Entregables", "roles": ["R", "C", "I", "C", "A"]}
            ]
            
        # Generar datos completos
        datos_generados = {
            "complejidad": complejidad,
            "codigo": codigo,
            "nombre_proyecto": nombre_proyecto,
            "servicio": servicio,
            "industria": industria,
            "cliente": {
                "nombre": estado.get("cliente_nombre", cliente),
                "ruc": estado.get("cliente_ruc"),
                "direccion": estado.get("cliente_direccion"),
                "telefono": estado.get("cliente_telefono"),
                "email": estado.get("cliente_email")
            },
            "ubicacion": ubicacion,
            "area_m2": area,

            "normativa": normativa,
            
            # ✅ DATOS PLANOS para compatibilidad con frontend
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
            "duracion_total": duracion_total,

            "cronograma": {
                "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
                "fecha_fin": fecha_fin.strftime("%d/%m/%Y"),
                "duracion_total": duracion_total
            },
            "presupuesto": presupuesto,
            "moneda": moneda,
            
            # ✅ KPIs en formato anidado (para frontend)
            "kpis": {
                "spi": spi,
                "cpi": cpi,
                "ev_k": ev_k,
                "pv_k": pv_k,
                "ac_k": ac_k
            },
            
            # ✅ KPIs también como campos planos (para plantillas Word)
            "spi": spi,
            "cpi": cpi,
            "ev_k": ev_k,
            "pv_k": pv_k,
            "ac_k": ac_k,
            
            "alcance_proyecto": alcance,
            "cronograma_fases": cronograma_fases,  # ✅ RENOMBRADO Y DINÁMICO
            "stakeholders": stakeholders,
            "riesgos": riesgos,
            # ✅ CORREGIDO: Recursos en formato correcto (no anidados)
            "recursos_humanos": recursos_humanos,
            "materiales": materiales,
            "entregables_seleccionados": estado.get("entregables_seleccionados", []),  # ✅ NUEVO
            "raci_actividades": raci_actividades  # ✅ CORREGIDO: Usar variable generada
        }
        
        simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€', 'GBP': '£'}.get(moneda, '$')
        
        return {
            'success': True,
            'respuesta': f"""🎉 **PROJECT CHARTER GENERADO**

━━━━━━━━━━━━━━━━━━━━━━━
**RESUMEN DEL PROYECTO**
━━━━━━━━━━━━━━━━━━━━━━━

📋 **Código:** {codigo}
🏢 **Cliente:** {cliente}
📍 **Ubicación:** {ubicacion}
📐 **Área:** {area:,.0f} m²

**CRONOGRAMA:**
• Inicio: {fecha_inicio.strftime("%d/%m/%Y")}
• Fin: {fecha_fin.strftime("%d/%m/%Y")}
• Duración: {duracion_total} días

**PRESUPUESTO:**
• Total: {simbolo} {presupuesto:,.2f}

**KPIs PMI:**
• SPI: {spi} | CPI: {cpi}
• EV: {simbolo}{ev_k}K | PV: {simbolo}{pv_k}K | AC: {simbolo}{ac_k}K

**RIESGOS:** {len(riesgos)} identificados
**STAKEHOLDERS:** {len(stakeholders)} registrados

✅ **Documento listo para generar**

Haz clic en "Finalizar" para ver la vista previa y generar el PROJECT CHARTER en Word/PDF.""",
            'botones': None,
            'estado': estado,
            'datos_generados': datos_generados
        }
