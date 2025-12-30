"""
🎯 UNIVERSAL SPECIALIST - Clase Universal para Todos los Servicios
📁 RUTA: backend/app/services/pili/specialist.py

Esta clase lee configuraciones YAML y procesa conversaciones para TODOS los servicios.
NO hay código duplicado - todo es genérico y reutilizable.

✨ NUEVO: Integración multi-IA con fallback automático
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class UniversalSpecialist:
    """
    Especialista universal que maneja TODOS los servicios basándose en configuración YAML.
    
    Características:
    - Lee configuración YAML del servicio
    - Carga knowledge base dinámicamente
    - Procesa conversación por etapas
    - ✨ NUEVO: Usa IA (Gemini/Claude/GPT-4) para respuestas inteligentes
    - Fallback a respuestas YAML si no hay IA disponible
    - Genera cotizaciones automáticamente
    - 0% código duplicado
    """
    
    def __init__(self, service_name: str, document_type: str = "cotizacion-simple"):
        """
        Inicializa el especialista universal.
        
        Args:
            service_name: Nombre del servicio (ej: "itse", "electricidad")
            document_type: Tipo de documento (ej: "cotizacion-simple", "proyecto-complejo")
        """
        self.service_name = service_name
        self.document_type = document_type
        
        # Cargar configuración YAML
        self.config = self._load_config()
        
        # Cargar knowledge base si existe
        self.kb = self._load_knowledge_base()
        
        # ✨ NUEVO: Inicializar multi-IA manager
        try:
            from ..core import get_multi_ia_manager
            self.multi_ia = get_multi_ia_manager()
            self.use_ia = True
            logger.info("✅ Multi-IA habilitado")
        except Exception as e:
            logger.warning(f"⚠️ Multi-IA no disponible: {e}")
            self.multi_ia = None
            self.use_ia = False
        
        # Obtener etapas del documento
        self.stages = self.config.get('documents', {}).get(document_type, {}).get('etapas', [])
        
        # Estado de conversación
        self.conversation_state = {
            'stage': 'initial',
            'data': {},
            'history': []
        }
        
        logger.info(f"UniversalSpecialist inicializado para {service_name} - {document_type}")
    
    def _load_config(self) -> Dict:
        """Carga la configuración YAML del servicio."""
        try:
            config_path = Path(__file__).parent / 'config' / f'{self.service_name}.yaml'
            
            if not config_path.exists():
                raise FileNotFoundError(f"Configuración no encontrada: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            logger.info(f"Configuración cargada: {config_path}")
            return config
        
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            return {}
    
    def _load_knowledge_base(self) -> Dict:
        """Carga el knowledge base del servicio si existe."""
        try:
            kb_path = Path(__file__).parent / 'knowledge' / f'{self.service_name}_kb.py'
            
            if not kb_path.exists():
                logger.warning(f"Knowledge base no encontrado: {kb_path}")
                return {}
            
            # Importar dinámicamente el módulo
            import importlib.util
            spec = importlib.util.spec_from_file_location(f"{self.service_name}_kb", kb_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Obtener el knowledge base
            kb = getattr(module, 'KNOWLEDGE_BASE', {})
            logger.info(f"Knowledge base cargado: {kb_path}")
            return kb
        
        except Exception as e:
            logger.warning(f"Error cargando knowledge base: {e}")
            return {}
    
    def process_message(self, message: str, state: Optional[Dict] = None) -> Dict:
        """
        Procesa un mensaje del usuario.
        
        Args:
            message: Mensaje del usuario
            state: Estado actual de la conversación (opcional)
        
        Returns:
            Dict con respuesta, botones, stage, etc.
        """
        # ✅ FIX CRÍTICO: Si viene state del frontend, usarlo COMPLETO
        if state and isinstance(state, dict):
            # Si el state tiene la estructura completa, usarlo directamente
            if 'stage' in state or 'data' in state or 'history' in state:
                self.conversation_state = state
                logger.info(f"✅ Estado restaurado desde frontend: stage={state.get('stage')}, data={list(state.get('data', {}).keys())}")
            else:
                # Si solo viene data, mantener estructura
                self.conversation_state['data'] = state
                logger.info(f"✅ Datos actualizados desde frontend: {list(state.keys())}")
        
        # Obtener stage actual
        current_stage_id = self.conversation_state.get('stage', 'initial')
        
        # Si es initial, empezar con la primera etapa
        if current_stage_id == 'initial' and self.stages:
            current_stage_id = self.stages[0]['id']
        
        # Buscar la etapa actual
        current_stage = self._find_stage(current_stage_id)
        
        if not current_stage:
            return {
                'texto': f'Error: Etapa "{current_stage_id}" no encontrada',
                'stage': 'error',
                'state': self.conversation_state
            }
        
        # Procesar según el tipo de etapa
        stage_type = current_stage.get('type')
        
        if stage_type == 'buttons':
            return self._process_buttons_stage(current_stage, message)
        
        elif stage_type == 'input_number':
            return self._process_input_number_stage(current_stage, message)
        
        elif stage_type == 'input_text':
            return self._process_input_text_stage(current_stage, message)
        
        elif stage_type == 'generate_quote':
            return self._process_quote_stage(current_stage, message)
        
        else:
            return {
                'texto': f'Error: Tipo de etapa "{stage_type}" no soportado',
                'stage': 'error',
                'state': self.conversation_state
            }
    
    def _find_stage(self, stage_id: str) -> Optional[Dict]:
        """Busca una etapa por su ID."""
        for stage in self.stages:
            if stage['id'] == stage_id:
                return stage
        return None
    
    def _process_buttons_stage(self, stage: Dict, message: str) -> Dict:
        """Procesa una etapa con botones."""
        # Si es la primera etapa Y el mensaje no coincide con ninguna opción válida,
        # mostrar el mensaje de presentación
        is_first_stage = (stage['id'] == self.stages[0]['id'] if self.stages else False)
        
        # Obtener opciones válidas para esta etapa
        valid_options = []
        if 'opciones' in stage:
            valid_options = [opt.get('value', opt.get('text', '')) for opt in stage['opciones']]
        else:
            # Si usa data_source, obtener las opciones dinámicamente
            buttons = self._get_buttons_for_stage(stage)
            valid_options = [btn.get('value', btn.get('text', '')) for btn in buttons]
        
        # Si es la primera etapa Y el mensaje no es una opción válida, mostrar presentación
        if is_first_stage and (not message or message not in valid_options):
            return self._render_stage(stage)
        
        # Si el mensaje está vacío, mostrar la etapa actual
        if not message or message == '':
            return self._render_stage(stage)
        
        # Guardar la selección
        self.conversation_state['data'][stage['id']] = message
        
        # Avanzar a la siguiente etapa
        next_stage_id = stage.get('next')
        if next_stage_id:
            self.conversation_state['stage'] = next_stage_id
            next_stage = self._find_stage(next_stage_id)
            if next_stage:
                return self._render_stage(next_stage)
        
        return {
            'texto': 'Conversación completada',
            'stage': 'completed',
            'state': self.conversation_state
        }
    
    def _process_input_number_stage(self, stage: Dict, message: str) -> Dict:
        """Procesa una etapa con input numérico."""
        # Si es la primera vez, mostrar el mensaje
        if not message or message == '':
            return self._render_stage(stage)
        
        # Validar el número
        validacion = stage.get('validacion', {})
        is_valid, value, error = self._validate_number(
            message,
            validacion.get('type', 'float'),
            validacion.get('min', 0),
            validacion.get('max', 999999)
        )
        
        if not is_valid:
            return {
                'texto': f"❌ {error}\n\n{validacion.get('mensaje_error', 'Por favor ingresa un valor válido')}",
                'stage': stage['id'],
                'state': self.conversation_state,
                'progreso': stage.get('progress', '')
            }
        
        # Guardar el valor
        self.conversation_state['data'][stage['id']] = value
        
        # Avanzar a la siguiente etapa
        next_stage_id = stage.get('next')
        if next_stage_id:
            self.conversation_state['stage'] = next_stage_id
            next_stage = self._find_stage(next_stage_id)
            if next_stage:
                return self._render_stage(next_stage)
        
        return {
            'texto': 'Conversación completada',
            'stage': 'completed',
            'state': self.conversation_state
        }
    
    def _process_input_text_stage(self, stage: Dict, message: str) -> Dict:
        """Procesa una etapa con input de texto."""
        # Si es la primera vez, mostrar el mensaje
        if not message or message == '':
            return self._render_stage(stage)
        
        # Validar el texto
        validacion = stage.get('validacion', {})
        min_length = validacion.get('min_length', 1)
        max_length = validacion.get('max_length', 1000)
        
        if len(message) < min_length:
            return {
                'texto': f"❌ El texto debe tener al menos {min_length} caracteres",
                'stage': stage['id'],
                'state': self.conversation_state
            }
        
        if len(message) > max_length:
            return {
                'texto': f"❌ El texto no puede exceder {max_length} caracteres",
                'stage': stage['id'],
                'state': self.conversation_state
            }
        
        # Guardar el valor
        self.conversation_state['data'][stage['id']] = message
        
        # Avanzar a la siguiente etapa
        next_stage_id = stage.get('next')
        if next_stage_id:
            self.conversation_state['stage'] = next_stage_id
            next_stage = self._find_stage(next_stage_id)
            if next_stage:
                return self._render_stage(next_stage)
        
        return {
            'texto': 'Conversación completada',
            'stage': 'completed',
            'state': self.conversation_state
        }
    
    def _process_quote_stage(self, stage: Dict, message: str) -> Dict:
        """Procesa la etapa de generación de cotización."""
        # Generar la cotización usando el calculator
        calculator_name = stage.get('calculator')
        
        if not calculator_name:
            return {
                'texto': 'Error: No se especificó calculator',
                'stage': 'error',
                'state': self.conversation_state
            }
        
        # ✅ Llamar al calculator real
        try:
            from ..utils import calculate_itse_quote
            
            # Preparar datos para calculadora
            data = self.conversation_state.get('data', {})
            
            # Calcular cotización
            quote_data = calculate_itse_quote(data)
            
            # Renderizar mensaje con datos reales
            message_template = stage.get('message_template', 'cotizacion')
            mensaje = self._render_message_with_data(message_template, quote_data)
            
            # Preparar respuesta
            response = {
                'texto': mensaje,
                'stage': stage['id'],
                'state': self.conversation_state,
                'datos_generados': quote_data,
                'cotizacion_generada': True
            }
            
            # Agregar botones de acciones si existen
            actions = stage.get('actions', [])
            if actions:
                botones = [
                    {'text': action['text'], 'value': action['value']}
                    for action in actions
                ]
                response['botones'] = botones
            
            logger.info(f"✅ Cotización generada: {quote_data.get('total_min')} - {quote_data.get('total_max')}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error generando cotización: {e}")
            return {
                'texto': f'Error generando cotización: {str(e)}',
                'stage': 'error',
                'state': self.conversation_state
            }
    
    def _render_message_with_data(self, template_key: str, data: Dict) -> str:
        """
        Renderiza mensaje con datos de cotización.
        Similar a _render_message pero usa datos de cotización.
        """
        # Obtener el template del YAML
        mensajes = self.config.get('mensajes', {})
        template = mensajes.get(template_key, template_key)
        
        # Combinar datos de conversación con datos de cotización
        all_data = {**self.conversation_state.get('data', {}), **data}
        
        try:
            return template.format(**all_data)
        except KeyError as e:
            logger.warning(f"Variable faltante en template: {e}")
            return template
    
    def _render_stage(self, stage: Dict) -> Dict:
        """Renderiza una etapa (genera el mensaje y botones)."""
        # Obtener el template del mensaje
        message_template = stage.get('message_template', '')
        
        # Renderizar el mensaje con los datos actuales
        mensaje = self._render_message(message_template)
        
        # Preparar respuesta
        response = {
            'texto': mensaje,
            'stage': stage['id'],
            'state': self.conversation_state,
            'progreso': stage.get('progress', '')
        }
        
        # Agregar botones si es una etapa de botones
        if stage.get('type') == 'buttons':
            botones = self._get_buttons_for_stage(stage)
            if botones:
                response['botones'] = botones
        
        return response
    
    def _render_message(self, template_key: str) -> str:
        """
        Renderiza un mensaje desde el template.
        ✨ MULTI-IA: Intenta Gemini → Fallback a template YAML
        """
        # Obtener el template del YAML
        mensajes = self.config.get('mensajes', {})
        template = mensajes.get(template_key, template_key)
        
        # Reemplazar variables con datos actuales
        data = self.conversation_state.get('data', {})
        
        try:
            mensaje_base = template.format(**data)
        except KeyError as e:
            # Si falta una variable, retornar el template sin formatear
            logger.warning(f"Variable faltante en template: {e}")
            mensaje_base = template
        
        # ✨ MULTI-IA: Intentar con Gemini si está disponible
        if self.use_ia and self.multi_ia:
            try:
                # Construir contexto para Gemini
                contexto = {
                    "servicio": self.service_name,
                    "document_type": self.document_type,
                    "datos_actuales": data,
                    "mensaje_base": mensaje_base
                }
                
                # Construir prompt para Gemini
                prompt = f"""Eres PILI, un asistente experto en {self.config.get('name', self.service_name)}.

Contexto del servicio: {self.config.get('description', '')}

Datos actuales de la conversación:
{data}

Mensaje base a mejorar:
{mensaje_base}

Por favor, genera una respuesta amigable, profesional y útil basándote en el mensaje base.
Mantén el tono conversacional y ayuda al usuario a avanzar en el proceso.
Si el mensaje base tiene botones o opciones, menciónalos de forma natural."""
                
                # Generar respuesta con Gemini
                ia_response = self.multi_ia.generate_response(
                    prompt=prompt,
                    context=contexto,
                    max_tokens=500
                )
                
                if ia_response and len(ia_response.strip()) > 10:
                    logger.info("✅ Respuesta generada con Gemini")
                    return ia_response
                else:
                    logger.warning("⚠️ Gemini respondió vacío, usando template")
            
            except Exception as e:
                logger.warning(f"⚠️ Error usando Gemini: {e}, usando template")
        
        # Fallback: retornar mensaje del template
        logger.info("📝 Usando template YAML (fallback)")
        return mensaje_base
    
    def _get_buttons_for_stage(self, stage: Dict) -> List[Dict]:
        """Obtiene los botones para una etapa."""
        # Si hay opciones definidas directamente
        if 'opciones' in stage:
            return stage['opciones']
        
        # Si hay data_source, obtener desde el knowledge base o config
        data_source = stage.get('data_source', '')
        if data_source.startswith('kb.'):
            # Ejemplo: "kb.categorias" o "kb.tipos[{categoria}]"
            # Reemplazar placeholders con valores del state
            import re
            placeholders = re.findall(r'\{(\w+)\}', data_source)
            for placeholder in placeholders:
                value = self.conversation_state.get('data', {}).get(placeholder, '')
                data_source = data_source.replace(f'{{{placeholder}}}', value)
            
            # Ahora parsear el path: "kb.categorias" o "kb.tipos.SALUD"
            path = data_source.replace('kb.', '').split('.')
            
            # Intentar primero desde knowledge base
            data = self.kb
            for key in path:
                if isinstance(data, dict) and key in data:
                    data = data[key]
                else:
                    data = None
                    break
            
            # Si no hay KB, intentar desde config YAML
            if not data:
                data = self.config
                for key in path:
                    if isinstance(data, dict) and key in data:
                        data = data[key]
                    else:
                        return []
            
            # Convertir a botones
            if isinstance(data, dict):
                # Si es un dict con estructura {key: {nombre, icon}}, convertir a botones
                if all(isinstance(v, dict) for v in data.values()):
                    return [
                        {'text': f"{info.get('icon', '')} {info.get('nombre', key)}", 'value': key}
                        for key, info in data.items()
                    ]
                # Si es un dict simple, usar las keys como botones
                else:
                    return [{'text': str(v), 'value': str(v)} for v in data.values()]
            elif isinstance(data, list):
                # Si es una lista, convertir cada elemento a botón
                return [{'text': str(item), 'value': str(item)} for item in data]
        
        return []
    
    def _validate_number(self, value: str, tipo: str, min_val: float, max_val: float) -> tuple:
        """
        Valida un número.
        
        Returns:
            (is_valid, value, error_message)
        """
        try:
            # Limpiar el valor
            value_clean = value.strip().replace(',', '.')
            
            # Convertir según el tipo
            if tipo == 'int':
                num = int(float(value_clean))
            else:
                num = float(value_clean)
            
            # Validar rango
            if num < min_val:
                return False, None, f'El valor debe ser mayor o igual a {min_val}'
            
            if num > max_val:
                return False, None, f'El valor debe ser menor o igual a {max_val}'
            
            return True, num, ''
        
        except ValueError:
            return False, None, 'Por favor ingresa un número válido'
