import os
import shutil
from typing import Dict, Any, Optional
from datetime import datetime
import PyPDF2
from docx import Document
from openpyxl import load_workbook
from PIL import Image
import pytesseract
import magic
from app.core.config import settings

class FileProcessor:
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        self.max_file_size = settings.MAX_UPLOAD_SIZE_MB
    
    async def procesar_archivo(self, archivo_path: str, nombre_original: str) -> Dict[str, Any]:
        """
        Procesa un archivo y extrae su contenido
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
        Detecta el tipo MIME del archivo
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
        Extrae texto de un archivo PDF
        """
        texto = []
        
        with open(archivo_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                texto.append(page.extract_text())
        
        return '\n'.join(texto)
    
    def _extraer_texto_docx(self, archivo_path: str) -> str:
        """
        Extrae texto de un archivo Word
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
        Extrae texto de un archivo Excel
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
        Extrae texto de un archivo de texto plano
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
        Extrae texto de una imagen usando OCR
        """
        try:
            image = Image.open(archivo_path)
            texto = pytesseract.image_to_string(image, lang='spa+eng')
            return texto
        except Exception as e:
            return f"Error en OCR: {str(e)}"
    
    def _extraer_metadata(self, archivo_path: str, extension: str) -> Dict[str, Any]:
        """
        Extrae metadata del archivo
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
        Valida si un archivo cumple con los requisitos
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
        Guarda un archivo en el sistema
        """
        ruta_completa = os.path.join(self.upload_dir, nombre_unico)
        
        with open(ruta_completa, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
        
        return ruta_completa
    
    def eliminar_archivo(self, ruta: str) -> bool:
        """
        Elimina un archivo del sistema
        """
        try:
            if os.path.exists(ruta):
                os.remove(ruta)
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar archivo: {e}")
            return False

# Instancia global
file_processor = FileProcessor()