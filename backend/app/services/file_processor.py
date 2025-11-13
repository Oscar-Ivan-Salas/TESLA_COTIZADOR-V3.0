"""
📄 FILE PROCESSOR + PILI v3.0 - OCR INTELIGENTE MULTIMODAL
📁 RUTA: backend/app/services/file_processor.py

PILI (Procesadora Inteligente de Licitaciones Industriales) integrada con 
procesamiento de archivos para OCR inteligente y extracción especializada.

🎯 NUEVAS CARACTERÍSTICAS PILI v3.0:
- OCR inteligente especializado por tipo de documento
- Procesamiento multimodal (fotos, PDFs, Word, Excel, manuscritos)
- Extracción selectiva de información relevante por servicio
- Análisis automático de contenido técnico eléctrico
- Detección de elementos específicos (planos, especificaciones, etc.)
- Integración con agentes PILI especializados

🔄 CONSERVA TODO LO EXISTENTE:
- procesar_archivo() ✅
- Todos los extractores por tipo ✅  
- validar_archivo() ✅
- guardar_archivo() ✅
- extraer_metadata() ✅
- Todo el manejo de errores robusto ✅
"""

import os
import shutil
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import json

# Imports para procesamiento de archivos (conservados)
import PyPDF2
from docx import Document
from openpyxl import load_workbook
from PIL import Image
import pytesseract
import magic

# Imports PILI
from pathlib import Path
import re

# Configuración (conservada)
from app.core.config import settings

logger = logging.getLogger(__name__)

class FileProcessor:
    """
    🔄 PROCESADOR ORIGINAL CONSERVADO + 🤖 PILI INTEGRADA
    
    Mantiene toda la funcionalidad existente pero agrega capacidades
    inteligentes de PILI para procesamiento especializado por servicio.
    """
    
    def __init__(self):
        """🔄 CONSERVADO + 🤖 PILI mejorado"""
        
        # Configuración original conservada
        self.upload_dir = settings.UPLOAD_DIR
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        self.max_file_size = settings.MAX_UPLOAD_SIZE_MB
        
        # 🤖 Configuración PILI especializada
        self.pili_patterns = {
            "electricas": [
                r"instalaci[oó]n\s+el[eé]ctrica",
                r"punto\s+de\s+luz",
                r"tomacorriente",
                r"tablero\s+el[eé]ctrico",
                r"cable\s+THW",
                r"pozo\s+a\s+tierra",
                r"CNE",
                r"voltaje",
                r"amperaje",
                r"circuito",
                r"interruptor",
                r"carga\s+el[eé]ctrica"
            ],
            "automatizacion": [
                r"automatizaci[oó]n",
                r"control\s+automatico",
                r"sensor",
                r"PLC",
                r"SCADA",
                r"domótica",
                r"motor",
                r"actuador"
            ],
            "cctv": [
                r"c[aá]mara",
                r"CCTV",
                r"vigilancia",
                r"monitoreo",
                r"grabaci[oó]n",
                r"DVR",
                r"IP\s+camera"
            ],
            "redes": [
                r"red\s+de\s+datos",
                r"cableado\s+estructurado",
                r"switch",
                r"router",
                r"fibra\s+[oó]ptica",
                r"ethernet",
                r"WiFi"
            ],
            "financieros": [
                r"S/\s*[\d,]+\.?\d*",
                r"precio",
                r"costo",
                r"presupuesto",
                r"cotizaci[oó]n",
                r"total",
                r"subtotal",
                r"IGV"
            ],
            "cantidades": [
                r"\d+\s*(metros?|mts?|m)\b",
                r"\d+\s*(unidades?|und|u)\b",
                r"\d+\s*(puntos?|ptos?)\b",
                r"\d+\s*mm²",
                r"\d+\s*AWG"
            ]
        }
        
        logger.info("✅ FileProcessor + PILI inicializado")

    # ═══════════════════════════════════════════════════════════════
    # 🤖 NUEVOS MÉTODOS PILI v3.0
    # ═══════════════════════════════════════════════════════════════
    
    async def procesar_archivo_con_pili(
        self, 
        archivo_path: str, 
        nombre_original: str,
        tipo_servicio: str = "cotizacion-simple",
        agente_pili: str = "PILI",
        contexto_adicional: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        🤖 NUEVO PILI v3.0 - Procesa archivo con inteligencia especializada por servicio
        
        Args:
            archivo_path: Ruta del archivo
            nombre_original: Nombre original del archivo
            tipo_servicio: Tipo de servicio PILI
            agente_pili: Agente PILI responsable
            contexto_adicional: Contexto adicional del proyecto
            
        Returns:
            Resultado de procesamiento inteligente PILI
        """
        
        try:
            logger.info(f"🤖 {agente_pili} procesando archivo: {nombre_original}")
            
            # 1. Procesamiento básico (usando método original)
            resultado_base = await self.procesar_archivo(archivo_path, nombre_original)
            
            if not resultado_base.get("exito"):
                return resultado_base
            
            # 2. Análisis inteligente PILI por tipo de servicio
            analisis_pili = self._analizar_contenido_pili(
                contenido=resultado_base["contenido_texto"],
                tipo_servicio=tipo_servicio,
                agente_pili=agente_pili,
                nombre_archivo=nombre_original
            )
            
            # 3. Extracción especializada
            datos_especializados = self._extraer_datos_especializados_pili(
                contenido=resultado_base["contenido_texto"],
                tipo_servicio=tipo_servicio
            )
            
            # 4. Combinar resultados
            resultado_pili = {
                **resultado_base,
                "pili_analisis": analisis_pili,
                "datos_especializados": datos_especializados,
                "agente_responsable": agente_pili,
                "tipo_servicio": tipo_servicio,
                "timestamp_pili": datetime.now().isoformat(),
                "contexto_adicional": contexto_adicional or ""
            }
            
            logger.info(f"✅ {agente_pili} completó procesamiento inteligente")
            return resultado_pili
            
        except Exception as e:
            logger.error(f"❌ Error {agente_pili} procesando archivo: {str(e)}")
            return {
                "exito": False,
                "error": str(e),
                "agente_responsable": agente_pili,
                "mensaje_pili": f"Error procesando {nombre_original}: {str(e)}"
            }
    
    def _analizar_contenido_pili(
        self, 
        contenido: str, 
        tipo_servicio: str, 
        agente_pili: str,
        nombre_archivo: str
    ) -> Dict[str, Any]:
        """Analiza contenido con inteligencia PILI especializada"""
        
        analisis = {
            "tipo_documento_detectado": self._detectar_tipo_documento(contenido, nombre_archivo),
            "relevancia_por_servicio": {},
            "elementos_tecnicos": [],
            "informacion_critica": [],
            "sugerencias_pili": [],
            "confianza_analisis": 0.0
        }
        
        # Análisis de relevancia por categorías
        for categoria, patterns in self.pili_patterns.items():
            coincidencias = 0
            elementos_encontrados = []
            
            for pattern in patterns:
                matches = re.findall(pattern, contenido, re.IGNORECASE)
                coincidencias += len(matches)
                elementos_encontrados.extend(matches)
            
            if coincidencias > 0:
                analisis["relevancia_por_servicio"][categoria] = {
                    "coincidencias": coincidencias,
                    "elementos": elementos_encontrados[:10],  # Limitar a 10
                    "relevancia": min(coincidencias / 10.0, 1.0)  # Normalizar a 0-1
                }
        
        # Detectar elementos técnicos específicos
        analisis["elementos_tecnicos"] = self._detectar_elementos_tecnicos(contenido)
        
        # Información crítica según tipo de servicio
        analisis["informacion_critica"] = self._extraer_informacion_critica(
            contenido, tipo_servicio
        )
        
        # Sugerencias específicas del agente PILI
        analisis["sugerencias_pili"] = self._generar_sugerencias_pili(
            analisis, tipo_servicio, agente_pili
        )
        
        # Calcular confianza general
        total_relevancia = sum(
            cat.get("relevancia", 0) 
            for cat in analisis["relevancia_por_servicio"].values()
        )
        analisis["confianza_analisis"] = min(total_relevancia / 2.0, 0.95)  # Max 95%
        
        return analisis
    
    def _detectar_tipo_documento(self, contenido: str, nombre_archivo: str) -> Dict[str, Any]:
        """Detecta tipo de documento usando patrones PILI"""
        
        tipos_detectados = []
        
        # Patrones por tipo de documento
        patrones_documento = {
            "plano_electrico": [
                r"plano\s+el[eé]ctrico",
                r"diagrama\s+unifilar",
                r"esquema\s+el[eé]ctrico",
                r"layout\s+el[eé]ctrico"
            ],
            "especificacion_tecnica": [
                r"especificaci[oó]n\s+t[eé]cnica",
                r"memoria\s+descriptiva", 
                r"bases\s+t[eé]cnicas",
                r"requerimientos\s+t[eé]cnicos"
            ],
            "cotizacion": [
                r"cotizaci[oó]n",
                r"presupuesto",
                r"proforma",
                r"oferta\s+econ[oó]mica"
            ],
            "informe": [
                r"informe",
                r"reporte",
                r"an[aá]lisis",
                r"evaluaci[oó]n"
            ],
            "manual": [
                r"manual\s+de\s+usuario",
                r"gu[ií]a\s+de\s+instalaci[oó]n",
                r"instructivo",
                r"procedimiento"
            ]
        }
        
        # Detectar por contenido
        for tipo, patterns in patrones_documento.items():
            for pattern in patterns:
                if re.search(pattern, contenido, re.IGNORECASE):
                    tipos_detectados.append(tipo)
                    break
        
        # Detectar por nombre de archivo
        nombre_lower = nombre_archivo.lower()
        if "plano" in nombre_lower or "dwg" in nombre_lower:
            tipos_detectados.append("plano_electrico")
        elif "espec" in nombre_lower or "memoria" in nombre_lower:
            tipos_detectados.append("especificacion_tecnica")
        elif "cotiz" in nombre_lower or "presup" in nombre_lower:
            tipos_detectados.append("cotizacion")
        
        return {
            "tipos_detectados": list(set(tipos_detectados)),
            "tipo_principal": tipos_detectados[0] if tipos_detectados else "documento_general",
            "confianza": 0.8 if tipos_detectados else 0.3
        }
    
    def _detectar_elementos_tecnicos(self, contenido: str) -> List[Dict[str, Any]]:
        """Detecta elementos técnicos específicos"""
        
        elementos = []
        
        # Especificaciones de cables
        cables = re.findall(r"cable\s+(?:THW|THHN|NYY)\s+(\d+(?:\.\d+)?)\s*mm²?", contenido, re.IGNORECASE)
        for cable in cables:
            elementos.append({
                "tipo": "especificacion_cable",
                "valor": f"{cable}mm²",
                "descripcion": f"Cable {cable}mm² detectado"
            })
        
        # Voltajes
        voltajes = re.findall(r"(\d+(?:\.\d+)?)\s*(?:V|voltios?)", contenido, re.IGNORECASE)
        for voltaje in voltajes:
            elementos.append({
                "tipo": "voltaje",
                "valor": f"{voltaje}V",
                "descripcion": f"Voltaje {voltaje}V detectado"
            })
        
        # Corrientes
        corrientes = re.findall(r"(\d+(?:\.\d+)?)\s*(?:A|amperios?)", contenido, re.IGNORECASE)
        for corriente in corrientes:
            elementos.append({
                "tipo": "corriente",
                "valor": f"{corriente}A",
                "descripcion": f"Corriente {corriente}A detectada"
            })
        
        # Potencias
        potencias = re.findall(r"(\d+(?:\.\d+)?)\s*(?:W|KW|watts?)", contenido, re.IGNORECASE)
        for potencia in potencias:
            elementos.append({
                "tipo": "potencia",
                "valor": f"{potencia}W",
                "descripcion": f"Potencia {potencia}W detectada"
            })
        
        return elementos[:20]  # Limitar a 20 elementos más relevantes
    
    def _extraer_datos_especializados_pili(
        self, 
        contenido: str, 
        tipo_servicio: str
    ) -> Dict[str, Any]:
        """Extrae datos específicos según tipo de servicio PILI"""
        
        datos_especializados = {
            "precios_detectados": [],
            "cantidades_detectadas": [],
            "materiales_detectados": [],
            "especificaciones_tecnicas": [],
            "fechas_relevantes": [],
            "contactos_detectados": []
        }
        
        # Extraer precios
        precios = re.findall(r"S/\s*[\d,]+\.?\d*", contenido)
        datos_especializados["precios_detectados"] = precios[:10]
        
        # Extraer cantidades con unidades
        cantidades = re.findall(r"\d+\s*(?:metros?|mts?|unidades?|und|puntos?|ptos?)", contenido, re.IGNORECASE)
        datos_especializados["cantidades_detectadas"] = cantidades[:15]
        
        # Extraer materiales eléctricos
        materiales_patterns = [
            r"cable\s+(?:THW|THHN|NYY)\s+\d+(?:\.\d+)?\s*mm²?",
            r"interruptor\s+(?:termomagnético|diferencial)",
            r"tablero\s+(?:eléctrico|de\s+distribución)",
            r"tomacorriente\s+(?:doble|simple|polarizado)",
            r"punto\s+de\s+luz"
        ]
        
        for pattern in materiales_patterns:
            matches = re.findall(pattern, contenido, re.IGNORECASE)
            datos_especializados["materiales_detectados"].extend(matches)
        
        # Extraer especificaciones técnicas
        if "cotizacion" in tipo_servicio:
            # Buscar especificaciones de cotización
            specs = re.findall(r"(?:instalación|montaje|suministro)\s+de\s+[^.]+", contenido, re.IGNORECASE)
            datos_especializados["especificaciones_tecnicas"] = specs[:10]
        
        elif "proyecto" in tipo_servicio:
            # Buscar cronogramas y fases
            cronograma = re.findall(r"(?:fase|etapa|semana|mes)\s+\d+", contenido, re.IGNORECASE)
            datos_especializados["cronograma_detectado"] = cronograma[:8]
        
        # Extraer fechas
        fechas = re.findall(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", contenido)
        datos_especializados["fechas_relevantes"] = fechas[:5]
        
        # Extraer contactos (teléfonos, emails)
        telefonos = re.findall(r"(?:\+51\s*)?[9]\d{8}", contenido)
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", contenido)
        datos_especializados["contactos_detectados"] = {
            "telefonos": telefonos[:3],
            "emails": emails[:3]
        }
        
        return datos_especializados
    
    def _extraer_informacion_critica(self, contenido: str, tipo_servicio: str) -> List[str]:
        """Extrae información crítica específica del tipo de servicio"""
        
        info_critica = []
        
        if "cotizacion" in tipo_servicio:
            # Información crítica para cotizaciones
            if re.search(r"instalaci[oó]n\s+el[eé]ctrica", contenido, re.IGNORECASE):
                info_critica.append("📋 Documento contiene información de instalación eléctrica")
            
            if re.search(r"S/\s*[\d,]+", contenido):
                info_critica.append("💰 Precios detectados en el documento")
            
            if re.search(r"(?:metros?|puntos?|unidades?)", contenido, re.IGNORECASE):
                info_critica.append("📏 Cantidades específicas detectadas")
        
        elif "proyecto" in tipo_servicio:
            # Información crítica para proyectos
            if re.search(r"(?:cronograma|planificaci[oó]n)", contenido, re.IGNORECASE):
                info_critica.append("📅 Información de cronograma detectada")
            
            if re.search(r"(?:fase|etapa)", contenido, re.IGNORECASE):
                info_critica.append("🔄 Fases del proyecto identificadas")
        
        elif "informe" in tipo_servicio:
            # Información crítica para informes
            if re.search(r"(?:conclusi[oó]n|recomendaci[oó]n)", contenido, re.IGNORECASE):
                info_critica.append("📊 Conclusiones o recomendaciones detectadas")
        
        # Información crítica general
        if re.search(r"(?:cliente|empresa)", contenido, re.IGNORECASE):
            info_critica.append("🏢 Información del cliente identificada")
        
        if re.search(r"(?:urgente|prioritario|inmediato)", contenido, re.IGNORECASE):
            info_critica.append("⚡ Documento marcado como prioritario")
        
        return info_critica[:10]  # Máximo 10 puntos críticos
    
    def _generar_sugerencias_pili(
        self, 
        analisis: Dict[str, Any], 
        tipo_servicio: str, 
        agente_pili: str
    ) -> List[str]:
        """Genera sugerencias específicas del agente PILI"""
        
        sugerencias = []
        
        # Sugerencias basadas en relevancia
        relevancia = analisis.get("relevancia_por_servicio", {})
        
        if relevancia.get("electricas", {}).get("relevancia", 0) > 0.3:
            sugerencias.append(f"✨ {agente_pili}: Detecté información eléctrica relevante. Puedo generar cotización especializada.")
        
        if relevancia.get("financieros", {}).get("relevancia", 0) > 0.2:
            sugerencias.append(f"💰 {agente_pili}: Hay datos financieros. Puedo validar precios del mercado peruano.")
        
        if relevancia.get("cantidades", {}).get("relevancia", 0) > 0.2:
            sugerencias.append(f"📏 {agente_pili}: Cantidades detectadas. Puedo calcular metrados automáticamente.")
        
        # Sugerencias específicas por tipo de servicio
        if "cotizacion" in tipo_servicio:
            if analisis["confianza_analisis"] > 0.6:
                sugerencias.append(f"🎯 {agente_pili}: Confianza alta. Listo para generar cotización completa.")
            else:
                sugerencias.append(f"🔍 {agente_pili}: Necesito más información. ¿Puedes subir planos o especificaciones?")
        
        elif "proyecto" in tipo_servicio:
            sugerencias.append(f"📋 {agente_pili}: Puedo estructurar este contenido en fases de proyecto.")
        
        elif "informe" in tipo_servicio:
            sugerencias.append(f"📊 {agente_pili}: Puedo generar informe ejecutivo con este contenido.")
        
        # Sugerencias adicionales
        if len(analisis.get("elementos_tecnicos", [])) > 5:
            sugerencias.append(f"⚡ {agente_pili}: Muchos elementos técnicos detectados. Excelente para análisis detallado.")
        
        return sugerencias[:6]  # Máximo 6 sugerencias

    # ═══════════════════════════════════════════════════════════════
    # 🔄 MÉTODOS ORIGINALES CONSERVADOS (COMPATIBILIDAD)
    # ═══════════════════════════════════════════════════════════════
    
    async def procesar_archivo(self, archivo_path: str, nombre_original: str) -> Dict[str, Any]:
        """
        🔄 CONSERVADO - Procesa un archivo y extrae su contenido
        
        Método original mantenido para compatibilidad hacia atrás.
        """
        
        # Detectar tipo de archivo
        tipo_mime = self._detectar_tipo_mime(archivo_path)
        extension = nombre_original.split('.')[-1].lower()
        
        resultado = {
            "exito": False,
            "nombre_original": nombre_original,
            "tipo_mime": tipo_mime,
            "extension": extension,
            "contenido_texto": "",
            "metadata": {},
            "error": None
        }
        
        try:
            # Procesar según tipo
            if extension in ['pdf']:
                contenido = self._extraer_texto_pdf(archivo_path)
            elif extension in ['doc', 'docx']:
                contenido = self._extraer_texto_docx(archivo_path)
            elif extension in ['xls', 'xlsx']:
                contenido = self._extraer_texto_excel(archivo_path)
            elif extension in ['txt']:
                contenido = self._extraer_texto_txt(archivo_path)
            elif extension in ['jpg', 'jpeg', 'png']:
                contenido = self._extraer_texto_imagen(archivo_path)
            else:
                contenido = f"Tipo de archivo no soportado para extracción: {extension}"
            
            resultado["exito"] = True
            resultado["contenido_texto"] = contenido
            resultado["metadata"] = self._extraer_metadata(archivo_path, extension)
            
        except Exception as e:
            resultado["error"] = str(e)
        
        return resultado
    
    def _detectar_tipo_mime(self, archivo_path: str) -> str:
        """
        🔄 CONSERVADO - Detecta el tipo MIME del archivo
        """
        try:
            mime = magic.Magic(mime=True)
            return mime.from_file(archivo_path)
        except:
            # Fallback basado en extensión
            extension = archivo_path.split('.')[-1].lower()
            mime_types = {
                'pdf': 'application/pdf',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'doc': 'application/msword',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'xls': 'application/vnd.ms-excel',
                'txt': 'text/plain',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png'
            }
            return mime_types.get(extension, 'application/octet-stream')
    
    def _extraer_texto_pdf(self, archivo_path: str) -> str:
        """
        🔄 CONSERVADO - Extrae texto de un archivo PDF
        """
        texto = []
        
        with open(archivo_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                texto.append(page.extract_text())
        
        return '\n'.join(texto)
    
    def _extraer_texto_docx(self, archivo_path: str) -> str:
        """
        🔄 CONSERVADO - Extrae texto de un archivo Word
        """
        doc = Document(archivo_path)
        texto = []
        
        for paragraph in doc.paragraphs:
            texto.append(paragraph.text)
        
        # Extraer texto de tablas
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    texto.append(cell.text)
        
        return '\n'.join(texto)
    
    def _extraer_texto_excel(self, archivo_path: str) -> str:
        """
        🔄 CONSERVADO - Extrae texto de un archivo Excel
        """
        workbook = load_workbook(archivo_path, data_only=True)
        texto = []
        
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            texto.append(f"\n=== Hoja: {sheet_name} ===\n")
            
            for row in sheet.iter_rows(values_only=True):
                row_text = [str(cell) if cell is not None else '' for cell in row]
                texto.append(' | '.join(row_text))
        
        return '\n'.join(texto)
    
    def _extraer_texto_txt(self, archivo_path: str) -> str:
        """
        🔄 CONSERVADO - Extrae texto de un archivo de texto plano
        """
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(archivo_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        
        return "Error: No se pudo decodificar el archivo de texto"
    
    def _extraer_texto_imagen(self, archivo_path: str) -> str:
        """
        🔄 CONSERVADO - Extrae texto de una imagen usando OCR
        """
        try:
            image = Image.open(archivo_path)
            texto = pytesseract.image_to_string(image, lang='spa+eng')
            return texto
        except Exception as e:
            return f"Error en OCR: {str(e)}"
    
    def _extraer_metadata(self, archivo_path: str, extension: str) -> Dict[str, Any]:
        """
        🔄 CONSERVADO - Extrae metadata del archivo
        """
        metadata = {
            "tamano_bytes": os.path.getsize(archivo_path),
            "fecha_modificacion": datetime.fromtimestamp(
                os.path.getmtime(archivo_path)
            ).isoformat()
        }
        
        # Metadata específica por tipo
        if extension == 'pdf':
            try:
                with open(archivo_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    metadata["num_paginas"] = len(pdf_reader.pages)
                    if pdf_reader.metadata:
                        metadata["autor"] = pdf_reader.metadata.get('/Author', '')
                        metadata["titulo"] = pdf_reader.metadata.get('/Title', '')
            except:
                pass
        
        elif extension in ['docx']:
            try:
                doc = Document(archivo_path)
                metadata["num_parrafos"] = len(doc.paragraphs)
                metadata["num_tablas"] = len(doc.tables)
            except:
                pass
        
        elif extension in ['jpg', 'jpeg', 'png']:
            try:
                image = Image.open(archivo_path)
                metadata["ancho"], metadata["alto"] = image.size
                metadata["formato"] = image.format
            except:
                pass
        
        return metadata
    
    def validar_archivo(self, nombre: str, tamano: int) -> Dict[str, Any]:
        """
        🔄 CONSERVADO - Valida si un archivo cumple con los requisitos
        """
        extension = nombre.split('.')[-1].lower()
        
        if extension not in self.allowed_extensions:
            return {
                "valido": False,
                "error": f"Extensión no permitida. Permitidas: {', '.join(self.allowed_extensions)}"
            }
        
        if tamano > self.max_file_size:
            return {
                "valido": False,
                "error": f"Archivo muy grande. Máximo: {self.max_file_size / 1024 / 1024:.2f} MB"
            }
        
        return {"valido": True}
    
    def guardar_archivo(self, archivo, nombre_unico: str) -> str:
        """
        🔄 CONSERVADO - Guarda un archivo en el sistema
        """
        ruta_completa = os.path.join(self.upload_dir, nombre_unico)
        
        with open(ruta_completa, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
        
        return ruta_completa
    
    def eliminar_archivo(self, ruta: str) -> bool:
        """
        🔄 CONSERVADO - Elimina un archivo del sistema
        """
        try:
            if os.path.exists(ruta):
                os.remove(ruta)
                return True
            return False
        except Exception as e:
            logger.error(f"Error al eliminar archivo: {e}")
            return False

# ═══════════════════════════════════════════════════════════════
# 🎯 INSTANCIA GLOBAL MEJORADA CON PILI
# ═══════════════════════════════════════════════════════════════

# Crear instancia global con manejo robusto de errores
try:
    file_processor = FileProcessor()
    logger.info("✅ FileProcessor + PILI inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error crítico inicializando FileProcessor: {e}")
    file_processor = None

# Función auxiliar para obtener instancia segura
def get_file_processor():
    """Obtiene instancia de FileProcessor de forma segura"""
    global file_processor
    if file_processor is None:
        try:
            file_processor = FileProcessor()
        except Exception as e:
            logger.error(f"Error creando FileProcessor: {e}")
    return file_processor