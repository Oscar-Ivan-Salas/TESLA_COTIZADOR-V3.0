"""
Generador de Proyecto Complejo (PMI)
Proyecto con métricas PMI, análisis de riesgos y plan de calidad
"""

from .base_generator import BaseDocumentGenerator
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class ProyectoComplejoPMIGenerator(BaseDocumentGenerator):
    """Generador para proyectos complejos con estándares PMI"""
    
    def _agregar_titulo(self):
        """Agrega título del documento"""
        p_titulo = self.doc.add_paragraph()
        p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = p_titulo.add_run('PLAN DE PROYECTO PMI')
        run_titulo.font.size = Pt(18)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        nombre_proyecto = self.datos.get('nombre_proyecto', 'Proyecto PMI')
        p_nombre = self.doc.add_paragraph()
        p_nombre.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_nombre = p_nombre.add_run(nombre_proyecto)
        run_nombre.font.size = Pt(14)
        run_nombre.font.color.rgb = self.COLOR_SECUNDARIO
        
        self.doc.add_paragraph()
    
    def _agregar_metricas_pmi(self):
        """Agrega métricas PMI"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('MÉTRICAS PMI')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        metricas = self.datos.get('metricas_pmi', {})
        
        table = self.doc.add_table(rows=5, cols=2)
        table.style = 'Table Grid'
        
        metricas_data = [
            ('CPI (Cost Performance Index)', metricas.get('cpi', '1.0')),
            ('SPI (Schedule Performance Index)', metricas.get('spi', '1.0')),
            ('EAC (Estimate at Completion)', metricas.get('eac', 'S/ 0.00')),
            ('ETC (Estimate to Complete)', metricas.get('etc', 'S/ 0.00')),
            ('VAC (Variance at Completion)', metricas.get('vac', 'S/ 0.00')),
        ]
        
        for idx, (label, valor) in enumerate(metricas_data):
            table.rows[idx].cells[0].text = label
            table.rows[idx].cells[1].text = str(valor)
        
        self.doc.add_paragraph()
    
    def _agregar_analisis_riesgos(self):
        """Agrega análisis de riesgos"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('ANÁLISIS DE RIESGOS')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        riesgos = self.datos.get('riesgos', [])
        
        if riesgos:
            table = self.doc.add_table(rows=len(riesgos) + 1, cols=4)
            table.style = 'Table Grid'
            
            # Header
            headers = ['RIESGO', 'PROBABILIDAD', 'IMPACTO', 'MITIGACIÓN']
            for idx, header in enumerate(headers):
                cell = table.rows[0].cells[idx]
                paragraph = cell.paragraphs[0]
                run = paragraph.add_run(header)
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                shading_elm = OxmlElement('w:shd')
                color_hex = self._rgb_to_hex(self.COLOR_PRIMARIO)
                shading_elm.set(qn('w:fill'), color_hex)
                cell._element.get_or_add_tcPr().append(shading_elm)
            
            # Riesgos
            for idx, riesgo in enumerate(riesgos, 1):
                row = table.rows[idx]
                row.cells[0].text = riesgo.get('descripcion', '')
                row.cells[1].text = riesgo.get('probabilidad', 'Media')
                row.cells[2].text = riesgo.get('impacto', 'Medio')
                row.cells[3].text = riesgo.get('mitigacion', '')
        
        self.doc.add_paragraph()
    
    def _agregar_plan_calidad(self):
        """Agrega plan de calidad"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('PLAN DE CALIDAD')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        calidad = self.datos.get('plan_calidad', {})
        objetivos = calidad.get('objetivos', [])
        metricas = calidad.get('metricas', [])
        
        if objetivos:
            p_obj = self.doc.add_paragraph()
            p_obj.add_run('Objetivos de Calidad:\n').font.bold = True
            for obj in objetivos:
                self.doc.add_paragraph(f"• {obj}", style='List Bullet')
        
        if metricas:
            p_met = self.doc.add_paragraph()
            p_met.add_run('Métricas de Calidad:\n').font.bold = True
            for metrica in metricas:
                self.doc.add_paragraph(f"• {metrica}", style='List Bullet')
        
        self.doc.add_paragraph()
    
    def generar(self, ruta_salida):
        """Genera el documento completo"""
        self._agregar_header_basico()
        self._agregar_titulo()
        self._agregar_metricas_pmi()
        self._agregar_analisis_riesgos()
        self._agregar_plan_calidad()
        self._agregar_footer_basico()
        
        self.doc.save(str(ruta_salida))
        return ruta_salida


def generar_proyecto_complejo_pmi(datos, ruta_salida, opciones=None):
    """Función de entrada para generar proyecto complejo PMI"""
    generator = ProyectoComplejoPMIGenerator(datos, opciones)
    return generator.generar(ruta_salida)
