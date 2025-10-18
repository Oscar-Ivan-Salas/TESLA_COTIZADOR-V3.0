from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from typing import Dict, Any
import os

class WordGenerator:
    
    def __init__(self):
        self.template_path = "templates/cotizacion_template.docx"
    
    def generar_cotizacion(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        """
        Genera un documento Word profesional de cotización
        """
        
        # Crear documento
        doc = Document()
        
        # Configurar márgenes
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        # === ENCABEZADO ===
        header = doc.add_paragraph()
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        run = header.add_run("COTIZACIÓN")
        run.font.size = Pt(28)
        run.font.bold = True
        run.font.color.rgb = RGBColor(139, 0, 0)  # Rojo oscuro
        
        # Fecha
        fecha_p = doc.add_paragraph()
        fecha_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fecha_run = fecha_p.add_run(f"Fecha: {datetime.now().strftime('%d de %B de %Y')}")
        fecha_run.font.size = Pt(11)
        
        # Número de cotización
        numero_p = doc.add_paragraph()
        numero_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        numero_run = numero_p.add_run(f"N° {datos.get('numero', 'COT-0001')}")
        numero_run.font.size = Pt(11)
        numero_run.font.bold = True
        
        doc.add_paragraph()  # Espaciado
        
        # === INFORMACIÓN DEL CLIENTE ===
        cliente_titulo = doc.add_paragraph()
        run = cliente_titulo.add_run("INFORMACIÓN DEL CLIENTE")
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(139, 0, 0)
        
        # Tabla de información
        table = doc.add_table(rows=2, cols=2)
        table.style = 'Light Grid Accent 1'
        
        # Cliente
        table.cell(0, 0).text = "Cliente:"
        table.cell(0, 1).text = datos.get('cliente', '')
        
        # Proyecto
        table.cell(1, 0).text = "Proyecto:"
        table.cell(1, 1).text = datos.get('proyecto', '')
        
        # Aplicar negrita a las etiquetas
        for row in table.rows:
            row.cells[0].paragraphs[0].runs[0].font.bold = True
        
        doc.add_paragraph()  # Espaciado
        
        # === DESCRIPCIÓN (si existe) ===
        if datos.get('descripcion'):
            desc_titulo = doc.add_paragraph()
            run = desc_titulo.add_run("DESCRIPCIÓN DEL PROYECTO")
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(139, 0, 0)
            
            desc_p = doc.add_paragraph(datos['descripcion'])
            desc_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            doc.add_paragraph()
        
        # === DETALLE DE SERVICIOS ===
        servicios_titulo = doc.add_paragraph()
        run = servicios_titulo.add_run("DETALLE DE SERVICIOS")
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(139, 0, 0)
        
        # Tabla de items
        items = datos.get('items', [])
        tabla_items = doc.add_table(rows=1, cols=4)
        tabla_items.style = 'Light Grid Accent 1'
        
        # Encabezados
        headers = tabla_items.rows[0].cells
        headers[0].text = "Descripción"
        headers[1].text = "Cantidad"
        headers[2].text = "P. Unitario"
        headers[3].text = "Total"
        
        for cell in headers:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Items
        for item in items:
            row = tabla_items.add_row().cells
            row[0].text = str(item.get('descripcion', ''))
            row[1].text = str(item.get('cantidad', ''))
            row[2].text = f"S/ {item.get('precioUnitario', 0):.2f}"
            row[3].text = f"S/ {item.get('total', 0):.2f}"
            
            # Alinear cantidades y precios
            row[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        doc.add_paragraph()
        
        # === TOTALES ===
        totales_tabla = doc.add_table(rows=3, cols=2)
        totales_tabla.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # Subtotal
        totales_tabla.cell(0, 0).text = "Subtotal:"
        totales_tabla.cell(0, 1).text = f"S/ {datos.get('subtotal', 0):.2f}"
        
        # IGV
        totales_tabla.cell(1, 0).text = "IGV (18%):"
        totales_tabla.cell(1, 1).text = f"S/ {datos.get('igv', 0):.2f}"
        
        # Total
        totales_tabla.cell(2, 0).text = "TOTAL:"
        totales_tabla.cell(2, 1).text = f"S/ {datos.get('total', 0):.2f}"
        
        # Formato totales
        for i, row in enumerate(totales_tabla.rows):
            row.cells[0].paragraphs[0].runs[0].font.bold = True
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            if i == 2:  # Fila de total
                row.cells[0].paragraphs[0].runs[0].font.size = Pt(14)
                row.cells[1].paragraphs[0].runs[0].font.size = Pt(14)
                row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(139, 0, 0)
                row.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(139, 0, 0)
        
        doc.add_paragraph()
        doc.add_paragraph()
        
        # === OBSERVACIONES ===
        if datos.get('observaciones'):
            obs_titulo = doc.add_paragraph()
            run = obs_titulo.add_run("OBSERVACIONES")
            run.font.size = Pt(12)
            run.font.bold = True
            
            doc.add_paragraph(datos['observaciones'])
        
        # === CONDICIONES ===
        cond_titulo = doc.add_paragraph()
        run = cond_titulo.add_run("CONDICIONES")
        run.font.size = Pt(12)
        run.font.bold = True
        
        condiciones = [
            f"• Vigencia de la cotización: {datos.get('vigencia', '30 días')}",
            "• Forma de pago: Por definir",
            "• Tiempo de entrega: Por definir según alcance",
            "• Los precios incluyen IGV"
        ]
        
        for condicion in condiciones:
            doc.add_paragraph(condicion)
        
        # === FOOTER ===
        doc.add_paragraph()
        doc.add_paragraph()
        
        footer_lines = [
            "TESLA COTIZADOR PRO",
            "📱 WhatsApp: +51 999 888 777",
            "📧 ventas@teslacotizador.com",
            "📍 Lima, Perú"
        ]
        
        for line in footer_lines:
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if line == footer_lines[0]:
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(12)
        
        # Guardar documento
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        doc.save(ruta_salida)
        
        return ruta_salida
    
    def generar_informe_ejecutivo(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        """
        Genera un informe ejecutivo completo del proyecto
        """
        
        doc = Document()
        
        # PORTADA
        portada = doc.add_paragraph()
        portada.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        run = portada.add_run("\n\n\nINFORME EJECUTIVO\n\n")
        run.font.size = Pt(32)
        run.font.bold = True
        run.font.color.rgb = RGBColor(139, 0, 0)
        
        run = portada.add_run(f"\n{datos.get('nombre', 'Proyecto')}\n\n")
        run.font.size = Pt(24)
        run.font.bold = True
        
        run = portada.add_run(f"\n{datetime.now().strftime('%d de %B de %Y')}")
        run.font.size = Pt(14)
        
        doc.add_page_break()
        
        # CONTENIDO
        # ... (puedes agregar más secciones según necesites)
        
        doc.save(ruta_salida)
        return ruta_salida

# Instancia global
word_generator = WordGenerator()