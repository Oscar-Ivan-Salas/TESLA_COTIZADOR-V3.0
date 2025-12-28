# Script para agregar TODOS los especialistas restantes al archivo principal
# Este script agregará: ITSE, PozoTierra, Contraincendios, Domotica, CCTV, Redes, 
# Automatizacion, Expedientes, Saneamiento + Factory + Función principal

import os

archivo = r"e:\TESLA_COTIZADOR-V3.0\backend\app\services\pili_local_specialists.py"

# Código completo de todos los especialistas restantes
codigo_completo = '''

# ══════════════════════════════════════════════════════════════════════════════
# 📋 ITSE SPECIALIST
# ══════════════════════════════════════════════════════════════════════════════

class ITSESpecialist(LocalSpecialist):
    """Especialista en certificaciones ITSE profesionales"""
    
    def _process_itse(self, message: str) -> Dict:
        stage = self.conversation_state["stage"]
        data = self.conversation_state["data"]
        
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el área en m²",
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
                    "texto": f"❌ {error}\\n\\nPor favor ingresa el número de pisos",
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
                    "texto": "✅ Excelente! Para agendar tu visita técnica GRATUITA, contacta:\\n\\n📞 WhatsApp: 906 315 961\\n📧 Email: ingenieria.teslaelectricidad@gmail.com",
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
    def _process_pozo_tierra(self, message: str) -> Dict:
        return self._process_generic(message)

class ContraincendiosSpecialist(LocalSpecialist):
    def _process_contraincendios(self, message: str) -> Dict:
        return self._process_generic(message)

class DomoticaSpecialist(LocalSpecialist):
    def _process_domotica(self, message: str) -> Dict:
        return self._process_generic(message)

class CCTVSpecialist(LocalSpecialist):
    def _process_cctv(self, message: str) -> Dict:
        return self._process_generic(message)

class RedesSpecialist(LocalSpecialist):
    def _process_redes(self, message: str) -> Dict:
        return self._process_generic(message)

class AutomatizacionSpecialist(LocalSpecialist):
    def _process_automatizacion_industrial(self, message: str) -> Dict:
        return self._process_generic(message)

class ExpedientesSpecialist(LocalSpecialist):
    def _process_expedientes(self, message: str) -> Dict:
        return self._process_generic(message)

class SaneamientoSpecialist(LocalSpecialist):
    def _process_saneamiento(self, message: str) -> Dict:
        return self._process_generic(message)


# ══════════════════════════════════════════════════════════════════════════════
# 🏭 FACTORY PATTERN
# ══════════════════════════════════════════════════════════════════════════════

class LocalSpecialistFactory:
    """Factory para crear especialistas locales según tipo de servicio"""
    
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
        """Crea especialista local según tipo de servicio"""
        specialist_class = cls._specialists.get(service_type)
        if not specialist_class:
            logger.warning(f"Servicio no soportado: {service_type}, usando genérico")
            return LocalSpecialist(service_type)
        return specialist_class(service_type)
    
    @classmethod
    def get_available_services(cls) -> List[str]:
        """Retorna lista de servicios disponibles"""
        return list(cls._specialists.keys())


# ══════════════════════════════════════════════════════════════════════════════
# 🎯 FUNCIÓN PRINCIPAL
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
        conversation_state: Estado de conversación (opcional)
    
    Returns:
        {
            "texto": str,
            "botones": List[Dict],
            "stage": str,
            "state": Dict,
            "datos_generados": Dict,
            "progreso": str
        }
    """
    try:
        specialist = LocalSpecialistFactory.create(service_type)
        response = specialist.process_message(message, conversation_state)
        
        logger.info(f"✅ Procesado con especialista local: {service_type}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en especialista local: {e}")
        return {
            "texto": "Lo siento, ocurrió un error. Por favor intenta de nuevo o contacta soporte.",
            "stage": "error",
            "state": conversation_state or {}
        }
'''

# Agregar todo el código al archivo
with open(archivo, 'a', encoding='utf-8') as f:
    f.write(codigo_completo)

print("✅ Todos los especialistas agregados correctamente")
print(f"✅ Archivo completo: {archivo}")

# Contar líneas finales
with open(archivo, 'r', encoding='utf-8') as f:
    lineas = len(f.readlines())

print(f"✅ Total de líneas: {lineas}")
