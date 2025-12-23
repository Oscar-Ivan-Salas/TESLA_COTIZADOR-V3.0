"""
Generador de Cotización Compleja
Cotización con capítulos, subtotales y notas técnicas
"""

from .base_generator import BaseDocumentGenerator
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class CotizacionComplejaGenerator(BaseDocumentGenerator):
    """Generador para cotizaciones complejas con capítulos"""
    
    def _agregar_titulo(self):
        """Agrega título del documento"""
        p_titulo = self.doc.add_paragraph()
        p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = p_titulo.add_run('COTIZACIÓN DE SERVICIOS')
        run_titulo.font.size = Pt(18)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        numero = self.datos.get('numero', 'COT-000')
        p_numero = self.doc.add_paragraph()
        p_numero.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_numero = p_numero.add_run(f'N° {numero}')
        run_numero.font.size = Pt(14)
        run_numero.font.color.rgb = self.COLOR_SECUNDARIO
        
        self.doc.add_paragraph()
    
    def _agregar_info_general(self):
        """Agrega información general en tabla"""
        table = self.doc.add_table(rows=1, cols=2)
        
        # Cliente
        cell_cliente = table.rows[0].cells[0]
        p1 = cell_cliente.paragraphs[0]
        run1 = p1.add_run('DATOS DEL CLIENTE')
        run1.font.size = Pt(11)
        run1.font.bold = True
        run1.font.color.rgb = self.COLOR_PRIMARIO
        
        cliente_data = self.datos.get('cliente', 'Cliente')
        if isinstance(cliente_data, dict):
            cliente = cliente_data.get('nombre', 'Cliente')
        else:
            cliente = str(cliente_data)
        
        proyecto = self.datos.get('proyecto', 'Proyecto')
        area = self.datos.get('area_m2', '0')
        
        cell_cliente.add_paragraph(f'Cliente: {cliente}').runs[0].font.size = Pt(10)
        cell_cliente.add_paragraph(f'Proyecto: {proyecto}').runs[0].font.size = Pt(10)
        cell_cliente.add_paragraph(f'Área: {area} m²').runs[0].font.size = Pt(10)
        
        # Cotización
        cell_cot = table.rows[0].cells[1]
        p2 = cell_cot.paragraphs[0]
        run2 = p2.add_run('DATOS DE LA COTIZACIÓN')
        run2.font.size = Pt(11)
        run2.font.bold = True
        run2.font.color.rgb = self.COLOR_PRIMARIO
        
        fecha = self.datos.get('fecha', '01/01/2025')
        vigencia = self.datos.get('vigencia', '30 días')
        servicio = self.datos.get('servicio', 'Servicios Eléctricos')
        
        cell_cot.add_paragraph(f'Fecha: {fecha}').runs[0].font.size = Pt(10)
        cell_cot.add_paragraph(f'Vigencia: {vigencia}').runs[0].font.size = Pt(10)
        cell_cot.add_paragraph(f'Servicio: {servicio}').runs[0].font.size = Pt(10)
        
        self.doc.add_paragraph()
    
    def _agregar_capitulos(self):
        """Agrega capítulos con items y subtotales"""
        capitulos = self.datos.get('capitulos', [])
        
        if not capitulos:
            # Si no hay capítulos, usar items directamente
            items = self.datos.get('items', [])
            if items:
                capitulos = [{'nombre': 'Detalle de la Cotización', 'items': items}]
        
        total_general = 0
        
        for cap_idx, capitulo in enumerate(capitulos, 1):
            # Título del capítulo
            p_cap = self.doc.add_paragraph()
            run_cap = p_cap.add_run(f"CAPÍTULO {cap_idx}: {capitulo.get('nombre', 'Sin nombre')}")
            run_cap.font.size = Pt(14)
            run_cap.font.bold = True
            run_cap.font.color.rgb = self.COLOR_PRIMARIO
            
            # Tabla de items del capítulo
            items = capitulo.get('items', [])
            if items:
                table = self.doc.add_table(rows=len(items) + 1, cols=6)
                table.style = 'Table Grid'
                
                # Header
                headers = ['ITEM', 'DESCRIPCIÓN', 'CANT.', 'UNIDAD', 'P. UNIT.', 'TOTAL']
                for idx, header in enumerate(headers):
                    cell = table.rows[0].cells[idx]
                    paragraph = cell.paragraphs[0]
                    run = paragraph.add_run(header)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    
                    # Fondo con color personalizado
                    shading_elm = OxmlElement('w:shd')
                    color_hex = self._rgb_to_hex(self.COLOR_PRIMARIO)
                    shading_elm.set(qn('w:fill'), color_hex)
                    cell._element.get_or_add_tcPr().append(shading_elm)
                
                # Items
                subtotal_cap = 0
                for idx, item in enumerate(items, 1):
                    row = table.rows[idx]
                    cantidad = float(item.get('cantidad', 0))
                    precio = float(item.get('precio_unitario', 0))
                    total_item = cantidad * precio
                    subtotal_cap += total_item
                    
                    row.cells[0].text = str(idx)
                    row.cells[1].text = item.get('descripcion', '')
                    row.cells[2].text = str(cantidad)
                    row.cells[3].text = item.get('unidad', 'und')
                    row.cells[4].text = f"S/ {precio:.2f}"
                    row.cells[5].text = f"S/ {total_item:.2f}"
                
                # Subtotal del capítulo
                p_subtotal = self.doc.add_paragraph()
                p_subtotal.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                run_subtotal = p_subtotal.add_run(f"Subtotal Capítulo {cap_idx}: S/ {subtotal_cap:.2f}")
                run_subtotal.font.size = Pt(12)
                run_subtotal.font.bold = True
                run_subtotal.font.color.rgb = self.COLOR_SECUNDARIO
                
                total_general += subtotal_cap
                self.doc.add_paragraph()
        
        return total_general
    
    def _agregar_totales(self, subtotal):
        """Agrega sección de totales"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('RESUMEN DE COSTOS')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        # Tabla de totales
        table = self.doc.add_table(rows=3, cols=2)
        table.style = 'Table Grid'
        
        igv = subtotal * 0.18
        total = subtotal + igv
        
        # Subtotal
        table.rows[0].cells[0].text = 'SUBTOTAL:'
        table.rows[0].cells[1].text = f'S/ {subtotal:.2f}'
        
        # IGV
        table.rows[1].cells[0].text = 'IGV (18%):'
        table.rows[1].cells[1].text = f'S/ {igv:.2f}'
        
        # Total
        cell_total_label = table.rows[2].cells[0]
        cell_total_valor = table.rows[2].cells[1]
        
        p_label = cell_total_label.paragraphs[0]
        run_label = p_label.add_run('TOTAL:')
        run_label.font.bold = True
        run_label.font.size = Pt(14)
        run_label.font.color.rgb = RGBColor(255, 255, 255)
        
        p_valor = cell_total_valor.paragraphs[0]
        run_valor = p_valor.add_run(f'S/ {total:.2f}')
        run_valor.font.bold = True
        run_valor.font.size = Pt(14)
        run_valor.font.color.rgb = RGBColor(255, 255, 255)
        
        # Fondo con color personalizado
        for cell in [cell_total_label, cell_total_valor]:
            shading_elm = OxmlElement('w:shd')
            color_hex = self._rgb_to_hex(self.COLOR_PRIMARIO)
            shading_elm.set(qn('w:fill'), color_hex)
            cell._element.get_or_add_tcPr().append(shading_elm)
        
        self.doc.add_paragraph()
    
    def _agregar_observaciones(self):
        """Agrega observaciones"""
        observaciones = self.datos.get('observaciones', 'Precios incluyen IGV')
        
        p_obs_titulo = self.doc.add_paragraph()
        run_obs_titulo = p_obs_titulo.add_run('OBSERVACIONES:')
        run_obs_titulo.font.size = Pt(11)
        run_obs_titulo.font.bold = True
        run_obs_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        p_obs = self.doc.add_paragraph(observaciones)
        p_obs.runs[0].font.size = Pt(10)
    
    def generar(self, ruta_salida):
        """Genera el documento completo"""
        self._agregar_header_basico()
        self._agregar_titulo()
        self._agregar_info_general()
        
        subtotal = self._agregar_capitulos()
        self._agregar_totales(subtotal)
        self._agregar_observaciones()
        
        self._agregar_footer_basico()
        
        self.doc.save(str(ruta_salida))
        return ruta_salida


def generar_cotizacion_compleja(datos, ruta_salida, opciones=None):
    """Función de entrada para generar cotización compleja"""
    generator = CotizacionComplejaGenerator(datos, opciones)
    return generator.generar(ruta_salida)
