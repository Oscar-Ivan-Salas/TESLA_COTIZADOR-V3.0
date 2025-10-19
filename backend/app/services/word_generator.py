"""
═══════════════════════════════════════════════════════════════
WORD GENERATOR - Generador de Documentos Word Profesionales
═══════════════════════════════════════════════════════════════

PROPÓSITO:
Generar documentos Word profesionales para cotizaciones,
informes de proyectos, y reportes técnicos.

FUNCIONES PRINCIPALES:
- generar_cotizacion() → Cotizaciones de venta
- generar_informe_proyecto() → Informes ejecutivos de proyectos
- generar_informe_simple() → Informes básicos

CARACTERÍSTICAS:
- Soporte para logo personalizado
- Tablas dinámicas
- Formato profesional
- Estilos Tesla (rojo, dorado, negro)

═══════════════════════════════════════════════════════════════
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import logging
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

class WordGenerator:
    """
    Generador profesional de documentos Word
    """
    
    def __init__(self):
        """Inicializar generador"""
        # Colores Tesla
        self.COLOR_ROJO = RGBColor(139, 0, 0)      # #8B0000
        self.COLOR_DORADO = RGBColor(218, 165, 32)  # #DAA520
        self.COLOR_NEGRO = RGBColor(0, 0, 0)        # #000000
        self.COLOR_GRIS = RGBColor(128, 128, 128)   # #808080
        
        logger.info("WordGenerator inicializado")
    
    # ════════════════════════════════════════════════════════
    # FUNCIÓN PRINCIPAL - COTIZACIÓN
    # ════════════════════════════════════════════════════════
    
    def generar_cotizacion(
        self,
        datos: Dict[str, Any],
        ruta_salida: str,
        opciones: Optional[Dict[str, bool]] = None,
        logo_base64: Optional[str] = None
    ) -> str:
        """
        Generar documento de cotización profesional
        
        Args:
            datos: Datos de la cotización
            ruta_salida: Ruta donde guardar el documento
            opciones: Opciones de visualización
            logo_base64: Logo en base64 (opcional)
        
        Returns:
            Ruta del documento generado
        """
        
        try:
            logger.info(f"Generando cotización: {datos.get('numero', 'N/A')}")
            
            # Crear documento
            doc = Document()
            
            # Configurar opciones por defecto
            opts = {
                'mostrar_precios': True,
                'mostrar_igv': True,
                'mostrar_observaciones': True,
                'mostrar_logo': True
            }
            
            if opciones:
                opts.update(opciones)
            
            # 1. Logo (si existe)
            if logo_base64 and opts['mostrar_logo']:
                self._insertar_logo(doc, logo_base64)
            
            # 2. Encabezado empresa
            self._agregar_encabezado_empresa(doc)
            
            # 3. Título
            titulo = doc.add_paragraph()
            run = titulo.add_run('COTIZACIÓN')
            run.font.size = Pt(24)
            run.font.bold = True
            run.font.color.rgb = self.COLOR_ROJO
            titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # 4. Número de cotización
            numero = doc.add_paragraph()
            run = numero.add_run(datos.get('numero', 'COT-XXXX-XXXX'))
            run.font.size = Pt(18)
            run.font.bold = True
            numero.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            doc.add_paragraph()  # Espacio
            
            # 5. Información del cliente
            self._agregar_seccion_cliente(doc, datos)
            
            # 6. Tabla de items
            if datos.get('items'):
                self._agregar_tabla_items(doc, datos['items'], opts)
            
            # 7. Totales
            if opts['mostrar_precios']:
                self._agregar_totales(doc, datos)
            
            # 8. Observaciones
            if opts['mostrar_observaciones'] and datos.get('observaciones'):
                self._agregar_observaciones(doc, datos.get('observaciones'))
            
            # 9. Condiciones
            self._agregar_condiciones(doc, datos.get('vigencia', '30 días'))
            
            # 10. Firma
            self._agregar_firma(doc)
            
            # Crear directorio si no existe
            Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar
            doc.save(ruta_salida)
            
            logger.info(f"✅ Cotización generada: {ruta_salida}")
            
            return ruta_salida
            
        except Exception as e:
            logger.error(f"Error al generar cotización: {str(e)}")
            raise Exception(f"Error al generar cotización: {str(e)}")
    
    # ════════════════════════════════════════════════════════
    # FUNCIÓN PRINCIPAL - INFORME DE PROYECTO (NUEVO)
    # ════════════════════════════════════════════════════════
    
    def generar_informe_proyecto(
        self,
        datos: Dict[str, Any],
        ruta_salida: str,
        opciones: Optional[Dict[str, bool]] = None,
        logo_base64: Optional[str] = None
    ) -> str:
        """
        Generar informe ejecutivo de proyecto
        
        MODO COMPLEJO - Para proyectos complejos
        
        Args:
            datos: Datos del proyecto
            ruta_salida: Ruta donde guardar el documento
            opciones: Opciones de visualización
            logo_base64: Logo en base64 (opcional)
        
        Returns:
            Ruta del documento generado
        """
        
        try:
            logger.info(f"Generando informe de proyecto: {datos.get('proyecto', 'N/A')}")
            
            # Crear documento
            doc = Document()
            
            # Configurar opciones
            opts = {
                'mostrar_logo': True,
                'incluir_cotizaciones': True,
                'incluir_documentos': True,
                'incluir_estadisticas': True
            }
            
            if opciones:
                opts.update(opciones)
            
            # ═══ PORTADA ═══
            
            # Logo
            if logo_base64 and opts['mostrar_logo']:
                self._insertar_logo(doc, logo_base64)
            
            # Título
            titulo = doc.add_paragraph()
            run = titulo.add_run('INFORME EJECUTIVO DE PROYECTO')
            run.font.size = Pt(26)
            run.font.bold = True
            run.font.color.rgb = self.COLOR_ROJO
            titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            doc.add_paragraph()
            
            # Nombre del proyecto
            nombre_proy = doc.add_paragraph()
            run = nombre_proy.add_run(datos.get('proyecto', 'Proyecto Sin Nombre'))
            run.font.size = Pt(20)
            run.font.bold = True
            nombre_proy.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            doc.add_paragraph()
            
            # Número de proyecto
            numero = doc.add_paragraph()
            run = numero.add_run(datos.get('numero', 'PROY-XXXX'))
            run.font.size = Pt(14)
            run.font.italic = True
            numero.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # Fecha
            fecha = doc.add_paragraph()
            fecha_texto = datetime.now().strftime("%d de %B de %Y")
            run = fecha.add_run(fecha_texto)
            run.font.size = Pt(12)
            fecha.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # Salto de página
            doc.add_page_break()
            
            # ═══ RESUMEN EJECUTIVO ═══
            
            self._agregar_encabezado_seccion(doc, '1. RESUMEN EJECUTIVO')
            
            # Información general
            tabla_resumen = doc.add_table(rows=6, cols=2)
            tabla_resumen.style = 'Light Grid Accent 1'
            
            datos_resumen = [
                ('Cliente:', datos.get('cliente', 'N/A')),
                ('Proyecto:', datos.get('proyecto', 'N/A')),
                ('Estado:', datos.get('estado', 'N/A').upper()),
                ('Fecha Inicio:', datos.get('fecha_inicio', 'N/A')),
                ('Fecha Fin:', datos.get('fecha_fin', 'En curso')),
                ('Valor Total:', f"S/ {float(datos.get('total', 0)):,.2f}")
            ]
            
            for i, (campo, valor) in enumerate(datos_resumen):
                row = tabla_resumen.rows[i]
                row.cells[0].text = campo
                row.cells[1].text = valor
                
                # Negrita en primera columna
                for p in row.cells[0].paragraphs:
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = self.COLOR_ROJO
            
            doc.add_paragraph()
            
            # Descripción del proyecto
            if datos.get('descripcion'):
                desc_heading = doc.add_paragraph()
                run = desc_heading.add_run('Descripción del Proyecto:')
                run.font.bold = True
                run.font.size = Pt(11)
                
                desc = doc.add_paragraph(datos.get('descripcion'))
                desc.style = 'Normal'
            
            doc.add_paragraph()
            
            # ═══ ESTADÍSTICAS ═══
            
            if opts['incluir_estadisticas']:
                self._agregar_encabezado_seccion(doc, '2. ESTADÍSTICAS DEL PROYECTO')
                
                # Crear tabla de estadísticas
                stats_data = [
                    ('Total de Cotizaciones:', str(datos.get('total_cotizaciones', 0))),
                    ('Cotizaciones Aprobadas:', str(datos.get('cotizaciones_aprobadas', 0))),
                    ('Total de Documentos:', str(datos.get('total_documentos', 0))),
                    ('Subtotal:', f"S/ {float(datos.get('subtotal', 0)):,.2f}"),
                    ('IGV (18%):', f"S/ {float(datos.get('igv', 0)):,.2f}"),
                    ('Total General:', f"S/ {float(datos.get('total', 0)):,.2f}")
                ]
                
                tabla_stats = doc.add_table(rows=len(stats_data), cols=2)
                tabla_stats.style = 'Light Grid Accent 1'
                
                for i, (label, value) in enumerate(stats_data):
                    row = tabla_stats.rows[i]
                    row.cells[0].text = label
                    row.cells[1].text = value
                    
                    # Formato
                    for p in row.cells[0].paragraphs:
                        for run in p.runs:
                            run.font.bold = True
                    
                    # Alinear valores a la derecha
                    row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
                
                doc.add_paragraph()
            
            # ═══ COTIZACIONES ASOCIADAS ═══
            
            if opts['incluir_cotizaciones'] and datos.get('cotizaciones'):
                self._agregar_encabezado_seccion(doc, '3. COTIZACIONES ASOCIADAS')
                
                cotizaciones = datos.get('cotizaciones', [])
                
                if cotizaciones:
                    # Crear tabla de cotizaciones
                    tabla_cot = doc.add_table(rows=1, cols=5)
                    tabla_cot.style = 'Light Grid Accent 1'
                    
                    # Encabezados
                    headers = ['Número', 'Cliente', 'Estado', 'Fecha', 'Total']
                    header_row = tabla_cot.rows[0]
                    
                    for i, header in enumerate(headers):
                        cell = header_row.cells[i]
                        cell.text = header
                        
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.font.bold = True
                                run.font.color.rgb = RGBColor(255, 255, 255)
                        
                        # Color de fondo
                        self._set_cell_background(cell, '8B0000')
                    
                    # Agregar cotizaciones
                    for cot in cotizaciones:
                        row = tabla_cot.add_row()
                        row.cells[0].text = cot.get('numero', 'N/A')
                        row.cells[1].text = cot.get('cliente', 'N/A')
                        row.cells[2].text = cot.get('estado', 'N/A').upper()
                        row.cells[3].text = cot.get('fecha_creacion', 'N/A')
                        row.cells[4].text = f"S/ {float(cot.get('total', 0)):,.2f}"
                        
                        # Alinear total a la derecha
                        row.cells[4].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
                
                else:
                    doc.add_paragraph('No hay cotizaciones asociadas a este proyecto.')
                
                doc.add_paragraph()
            
            # ═══ DOCUMENTOS DEL PROYECTO ═══
            
            if opts['incluir_documentos'] and datos.get('documentos'):
                self._agregar_encabezado_seccion(doc, '4. DOCUMENTOS DEL PROYECTO')
                
                documentos = datos.get('documentos', [])
                
                if documentos:
                    # Crear tabla de documentos
                    tabla_docs = doc.add_table(rows=1, cols=4)
                    tabla_docs.style = 'Light Grid Accent 1'
                    
                    # Encabezados
                    headers_docs = ['Nombre', 'Tipo', 'Tamaño', 'Fecha']
                    header_row = tabla_docs.rows[0]
                    
                    for i, header in enumerate(headers_docs):
                        cell = header_row.cells[i]
                        cell.text = header
                        
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.font.bold = True
                                run.font.color.rgb = RGBColor(255, 255, 255)
                        
                        self._set_cell_background(cell, '8B0000')
                    
                    # Agregar documentos
                    for doc_item in documentos:
                        row = tabla_docs.add_row()
                        row.cells[0].text = doc_item.get('nombre', 'N/A')
                        row.cells[1].text = doc_item.get('tipo', 'N/A')
                        row.cells[2].text = f"{doc_item.get('tamano_mb', 0)} MB"
                        row.cells[3].text = doc_item.get('fecha_subida', 'N/A')
                
                else:
                    doc.add_paragraph('No hay documentos asociados a este proyecto.')
                
                doc.add_paragraph()
            
            # ═══ CONCLUSIONES ═══
            
            self._agregar_encabezado_seccion(doc, '5. CONCLUSIONES Y RECOMENDACIONES')
            
            conclusiones = doc.add_paragraph(
                'El proyecto se encuentra en desarrollo según lo planificado. '
                'Se recomienda mantener el seguimiento de los hitos establecidos '
                'y asegurar la comunicación constante con el cliente.'
            )
            conclusiones.style = 'Normal'
            
            doc.add_paragraph()
            
            # ═══ PIE DEL INFORME ═══
            
            doc.add_paragraph('\n' * 2)
            
            # Línea de firma
            linea = doc.add_paragraph('_' * 50)
            linea.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # Firma
            firma = doc.add_paragraph()
            run = firma.add_run('TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.')
            run.font.bold = True
            run.font.size = Pt(11)
            firma.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            ruc = doc.add_paragraph('RUC: 20601138787')
            ruc.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            # Guardar
            Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
            doc.save(ruta_salida)
            
            logger.info(f"✅ Informe de proyecto generado: {ruta_salida}")
            
            return ruta_salida
            
        except Exception as e:
            logger.error(f"Error al generar informe de proyecto: {str(e)}")
            raise Exception(f"Error al generar informe: {str(e)}")
    
    # ════════════════════════════════════════════════════════
    # FUNCIONES AUXILIARES - SECCIONES DEL DOCUMENTO
    # ════════════════════════════════════════════════════════
    
    def _insertar_logo(self, doc: Document, logo_base64: str):
        """Insertar logo desde base64"""
        try:
            # Decodificar base64
            if ',' in logo_base64:
                logo_base64 = logo_base64.split(',')[1]
            
            imagen_bytes = base64.b64decode(logo_base64)
            imagen_io = BytesIO(imagen_bytes)
            
            # Insertar imagen
            paragraph = doc.add_paragraph()
            run = paragraph.add_run()
            run.add_picture(imagen_io, width=Inches(2))
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            logger.info("Logo insertado")
            
        except Exception as e:
            logger.warning(f"No se pudo insertar logo: {str(e)}")
    
    def _agregar_encabezado_empresa(self, doc: Document):
        """Agregar encabezado con datos de la empresa"""
        empresa = doc.add_paragraph()
        run = empresa.add_run('TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.')
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_ROJO
        empresa.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        ruc = doc.add_paragraph('RUC: 20601138787')
        ruc.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        doc.add_paragraph()
    
    def _agregar_seccion_cliente(self, doc: Document, datos: Dict):
        """Agregar sección con información del cliente"""
        # Encabezado
        heading = doc.add_paragraph()
        run = heading.add_run('INFORMACIÓN DEL CLIENTE')
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_ROJO
        
        # Datos
        doc.add_paragraph(f"Cliente: {datos.get('cliente', 'N/A')}")
        doc.add_paragraph(f"Proyecto: {datos.get('proyecto', 'N/A')}")
        
        if datos.get('descripcion'):
            doc.add_paragraph(f"Descripción: {datos.get('descripcion')}")
        
        # Fecha
        fecha = datetime.now().strftime("%d/%m/%Y")
        doc.add_paragraph(f"Fecha: {fecha}")
        
        doc.add_paragraph()
    
    def _agregar_tabla_items(
        self, 
        doc: Document, 
        items: List[Dict],
        opciones: Dict[str, bool]
    ):
        """Agregar tabla con items de la cotización"""
        
        # Encabezado
        heading = doc.add_paragraph()
        run = heading.add_run('DETALLE DE LA COTIZACIÓN')
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_ROJO
        
        # Crear tabla
        cols = 4 if opciones.get('mostrar_precios', True) else 2
        tabla = doc.add_table(rows=1, cols=cols)
        tabla.style = 'Light Grid Accent 1'
        
        # Encabezados
        headers_row = tabla.rows[0]
        headers_row.cells[0].text = 'Descripción'
        headers_row.cells[1].text = 'Cantidad'
        
        if opciones.get('mostrar_precios', True):
            headers_row.cells[2].text = 'P. Unitario'
            headers_row.cells[3].text = 'Total'
        
        # Formato encabezados
        for cell in headers_row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
            
            self._set_cell_background(cell, '8B0000')
        
        # Agregar items
        for item in items:
            row = tabla.add_row()
            
            row.cells[0].text = item.get('descripcion', '')
            
            cantidad = float(item.get('cantidad', 0))
            row.cells[1].text = f"{cantidad:.2f}"
            row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            
            if opciones.get('mostrar_precios', True):
                precio = float(item.get('precio_unitario', 0))
                total = cantidad * precio
                
                row.cells[2].text = f"S/ {precio:,.2f}"
                row.cells[2].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
                
                row.cells[3].text = f"S/ {total:,.2f}"
                row.cells[3].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        
        doc.add_paragraph()
    
    def _agregar_totales(self, doc: Document, datos: Dict):
        """Agregar sección de totales"""
        
        subtotal = float(datos.get('subtotal', 0))
        igv = float(datos.get('igv', 0))
        total = float(datos.get('total', 0))
        
        # Crear tabla de totales alineada a la derecha
        tabla_totales = doc.add_table(rows=3, cols=2)
        
        # Datos
        tabla_totales.rows[0].cells[0].text = 'Subtotal:'
        tabla_totales.rows[0].cells[1].text = f"S/ {subtotal:,.2f}"
        
        tabla_totales.rows[1].cells[0].text = 'IGV (18%):'
        tabla_totales.rows[1].cells[1].text = f"S/ {igv:,.2f}"
        
        tabla_totales.rows[2].cells[0].text = 'TOTAL:'
        tabla_totales.rows[2].cells[1].text = f"S/ {total:,.2f}"
        
        # Formato
        for row in tabla_totales.rows:
            # Negrita en labels
            for p in row.cells[0].paragraphs:
                for run in p.runs:
                    run.font.bold = True
            
            # Alinear valores a la derecha
            row.cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        
        # Última fila (total) más grande y roja
        for p in tabla_totales.rows[2].cells[0].paragraphs:
            for run in p.runs:
                run.font.size = Pt(12)
                run.font.color.rgb = self.COLOR_ROJO
        
        for p in tabla_totales.rows[2].cells[1].paragraphs:
            for run in p.runs:
                run.font.size = Pt(12)
                run.font.bold = True
                run.font.color.rgb = self.COLOR_ROJO
        
        doc.add_paragraph()
    
    def _agregar_observaciones(self, doc: Document, observaciones: str):
        """Agregar sección de observaciones"""
        
        heading = doc.add_paragraph()
        run = heading.add_run('OBSERVACIONES')
        run.font.size = Pt(11)
        run.font.bold = True
        
        doc.add_paragraph(observaciones)
        doc.add_paragraph()
    
    def _agregar_condiciones(self, doc: Document, vigencia: str):
        """Agregar condiciones generales"""
        
        heading = doc.add_paragraph()
        run = heading.add_run('CONDICIONES GENERALES')
        run.font.size = Pt(11)
        run.font.bold = True
        
        doc.add_paragraph(f"• Vigencia de la cotización: {vigencia}")
        doc.add_paragraph("• Precios en Soles (S/)")
        doc.add_paragraph("• Incluye IGV")
        doc.add_paragraph("• Condiciones de pago: Por definir")
        
        doc.add_paragraph()
    
    def _agregar_firma(self, doc: Document):
        """Agregar sección de firma"""
        
        doc.add_paragraph('\n' * 2)
        
        # Línea
        linea = doc.add_paragraph('_' * 50)
        linea.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        # Firma
        firma = doc.add_paragraph()
        run = firma.add_run('Gerente General')
        run.font.bold = True
        firma.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        empresa = doc.add_paragraph('TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.')
        empresa.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    def _agregar_encabezado_seccion(self, doc: Document, texto: str):
        """Agregar encabezado de sección"""
        
        heading = doc.add_paragraph()
        run = heading.add_run(texto)
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = self.COLOR_ROJO
        
        doc.add_paragraph()
    
    def _set_cell_background(self, cell, color_hex: str):
        """Establecer color de fondo de celda"""
        try:
            shading_elm = OxmlElement('w:shd')
            shading_elm.set(qn('w:fill'), color_hex)
            cell._element.get_or_add_tcPr().append(shading_elm)
        except Exception as e:
            logger.warning(f"No se pudo establecer color de fondo: {str(e)}")

# ════════════════════════════════════════════════════════
# INSTANCIA GLOBAL
# ════════════════════════════════════════════════════════

word_generator = WordGenerator()