"""
Utilidad OCR (Optical Character Recognition)
Extracción de texto de imágenes usando Tesseract
"""
import pytesseract
from PIL import Image
from typing import Optional, Dict, Any
from pathlib import Path
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class OCRProcessor:
    """
    Procesador OCR para extraer texto de imágenes
    """
    
    def __init__(self):
        """Inicializar procesador OCR"""
        # Intentar configurar Tesseract
        try:
            # En Windows, puede ser necesario especificar la ruta
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            
            # Verificar que Tesseract está instalado
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract OCR inicializado: v{version}")
            self.disponible = True
        except Exception as e:
            logger.warning(f"Tesseract no disponible: {str(e)}")
            self.disponible = False
    
    def extraer_texto_imagen(
        self,
        ruta_imagen: str,
        idioma: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extraer texto de una imagen usando OCR
        
        Args:
            ruta_imagen: Ruta al archivo de imagen
            idioma: Código de idioma (spa, eng, etc.)
        
        Returns:
            Dict con texto extraído y metadata
        """
        
        if not self.disponible:
            return {
                "texto": "",
                "error": "OCR no disponible. Instalar Tesseract-OCR",
                "metadata": {}
            }
        
        try:
            # Abrir imagen
            imagen = Image.open(ruta_imagen)
            
            # Configurar idioma
            if not idioma:
                idioma = settings.OCR_LANGUAGES
            
            # Extraer texto
            texto = pytesseract.image_to_string(
                imagen,
                lang=idioma,
                config='--psm 6'  # Assume a single uniform block of text
            )
            
            # Obtener metadata adicional
            try:
                data_detallada = pytesseract.image_to_data(
                    imagen,
                    lang=idioma,
                    output_type=pytesseract.Output.DICT
                )
                
                # Calcular confianza promedio
                confianzas = [
                    int(conf) for conf in data_detallada['conf'] 
                    if conf != '-1'
                ]
                confianza_promedio = sum(confianzas) / len(confianzas) if confianzas else 0
                
                metadata = {
                    "confianza_promedio": round(confianza_promedio, 2),
                    "palabras_detectadas": len([t for t in data_detallada['text'] if t.strip()]),
                    "idioma_usado": idioma
                }
            except Exception as e:
                logger.warning(f"Error al obtener metadata OCR: {str(e)}")
                metadata = {"idioma_usado": idioma}
            
            # Limpiar texto
            texto_limpio = self._limpiar_texto_ocr(texto)
            
            logger.info(f"OCR completado: {len(texto_limpio)} caracteres extraídos")
            
            return {
                "texto": texto_limpio,
                "texto_raw": texto,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error en OCR: {str(e)}")
            return {
                "texto": "",
                "error": str(e),
                "metadata": {}
            }
    
    def extraer_texto_pdf_imagen(
        self,
        ruta_pdf: str,
        idioma: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extraer texto de PDF escaneado (imágenes) usando OCR
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            idioma: Código de idioma
        
        Returns:
            Dict con texto extraído de todas las páginas
        """
        
        if not self.disponible:
            return {
                "texto": "",
                "error": "OCR no disponible",
                "metadata": {}
            }
        
        try:
            from pdf2image import convert_from_path
            
            # Convertir PDF a imágenes
            imagenes = convert_from_path(ruta_pdf)
            
            textos_paginas = []
            metadata_paginas = []
            
            # Procesar cada página
            for i, imagen in enumerate(imagenes, 1):
                logger.info(f"Procesando página {i}/{len(imagenes)} con OCR")
                
                # Configurar idioma
                if not idioma:
                    idioma = settings.OCR_LANGUAGES
                
                # Extraer texto
                texto = pytesseract.image_to_string(
                    imagen,
                    lang=idioma,
                    config='--psm 6'
                )
                
                textos_paginas.append(f"--- Página {i} ---\n{texto}")
                metadata_paginas.append({
                    "pagina": i,
                    "caracteres": len(texto)
                })
            
            # Combinar texto de todas las páginas
            texto_completo = "\n\n".join(textos_paginas)
            texto_limpio = self._limpiar_texto_ocr(texto_completo)
            
            metadata = {
                "total_paginas": len(imagenes),
                "paginas": metadata_paginas,
                "idioma_usado": idioma
            }
            
            logger.info(f"OCR PDF completado: {len(imagenes)} páginas procesadas")
            
            return {
                "texto": texto_limpio,
                "metadata": metadata
            }
            
        except ImportError:
            logger.error("pdf2image no está instalado")
            return {
                "texto": "",
                "error": "pdf2image no está instalado. Instalar: pip install pdf2image",
                "metadata": {}
            }
        except Exception as e:
            logger.error(f"Error en OCR de PDF: {str(e)}")
            return {
                "texto": "",
                "error": str(e),
                "metadata": {}
            }
    
    def _limpiar_texto_ocr(self, texto: str) -> str:
        """
        Limpiar texto extraído por OCR
        
        Args:
            texto: Texto raw del OCR
        
        Returns:
            Texto limpio
        """
        
        if not texto:
            return ""
        
        # Eliminar espacios múltiples
        texto = " ".join(texto.split())
        
        # Eliminar líneas vacías múltiples
        lineas = texto.split('\n')
        lineas_limpias = [linea.strip() for linea in lineas if linea.strip()]
        
        return "\n".join(lineas_limpias)
    
    def detectar_idioma(self, ruta_imagen: str) -> str:
        """
        Detectar idioma predominante en una imagen
        
        Args:
            ruta_imagen: Ruta a la imagen
        
        Returns:
            Código de idioma detectado
        """
        
        if not self.disponible:
            return "spa"  # Default español
        
        try:
            from PIL import Image
            
            imagen = Image.open(ruta_imagen)
            
            # Intentar con varios idiomas
            idiomas_test = ['spa', 'eng']
            mejores_resultados = []
            
            for idioma in idiomas_test:
                try:
                    data = pytesseract.image_to_data(
                        imagen,
                        lang=idioma,
                        output_type=pytesseract.Output.DICT
                    )
                    
                    confianzas = [
                        int(conf) for conf in data['conf'] 
                        if conf != '-1'
                    ]
                    
                    if confianzas:
                        promedio = sum(confianzas) / len(confianzas)
                        mejores_resultados.append((idioma, promedio))
                
                except Exception as e:
                    logger.warning(f"Error al probar idioma {idioma}: {str(e)}")
            
            # Retornar idioma con mejor confianza
            if mejores_resultados:
                mejores_resultados.sort(key=lambda x: x[1], reverse=True)
                return mejores_resultados[0][0]
            
            return "spa"  # Default
            
        except Exception as e:
            logger.error(f"Error al detectar idioma: {str(e)}")
            return "spa"
    
    def verificar_calidad_imagen(self, ruta_imagen: str) -> Dict[str, Any]:
        """
        Verificar si una imagen es adecuada para OCR
        
        Args:
            ruta_imagen: Ruta a la imagen
        
        Returns:
            Dict con evaluación de calidad
        """
        
        try:
            imagen = Image.open(ruta_imagen)
            
            # Obtener dimensiones
            ancho, alto = imagen.size
            
            # Calcular megapixeles
            megapixeles = (ancho * alto) / 1_000_000
            
            # Verificar modo de color
            modo = imagen.mode
            
            # Evaluación
            evaluacion = {
                "ancho": ancho,
                "alto": alto,
                "megapixeles": round(megapixeles, 2),
                "modo": modo,
                "apta_para_ocr": True,
                "recomendaciones": []
            }
            
            # Validaciones
            if ancho < 300 or alto < 300:
                evaluacion["apta_para_ocr"] = False
                evaluacion["recomendaciones"].append(
                    "Imagen muy pequeña. Resolución mínima recomendada: 300x300 px"
                )
            
            if megapixeles < 0.5:
                evaluacion["recomendaciones"].append(
                    "Resolución baja. Aumentar calidad para mejores resultados."
                )
            
            if modo not in ['L', 'RGB']:
                evaluacion["recomendaciones"].append(
                    "Convertir imagen a escala de grises o RGB para mejor OCR"
                )
            
            return evaluacion
            
        except Exception as e:
            logger.error(f"Error al verificar calidad de imagen: {str(e)}")
            return {
                "apta_para_ocr": False,
                "error": str(e)
            }

# Instancia global
ocr_processor = OCRProcessor()