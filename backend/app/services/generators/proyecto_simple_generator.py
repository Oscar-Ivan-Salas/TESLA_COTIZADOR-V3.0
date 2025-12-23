"""
Generador de Proyecto Simple
Proyecto con cronograma, fases y recursos
"""

from .base_generator import BaseDocumentGenerator
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class ProyectoSimpleGenerator(BaseDocumentGenerator):
    """Generador para proyectos simples con cronograma"""
    
    def _agregar_titulo(self):
        """Agrega título del documento"""
        p_titulo = self.doc.add_paragraph()
        p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = p_titulo.add_run('PROYECTO DE SERVICIOS')
        run_titulo.font.size = Pt(18)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        nombre_proyecto = self.datos.get('nombre_proyecto', 'Proyecto Sin Nombre')
        p_nombre = self.doc.add_paragraph()
        p_nombre.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_nombre = p_nombre.add_run(nombre_proyecto)
        run_nombre.font.size = Pt(14)
        run_nombre.font.color.rgb = self.COLOR_SECUNDARIO
        
        self.doc.add_paragraph()
    
    def _agregar_resumen(self):
        """Agrega resumen ejecutivo"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('RESUMEN EJECUTIVO')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        resumen = self.datos.get('resumen', 'Descripción del proyecto...')
        p_resumen = self.doc.add_paragraph(resumen)
        p_resumen.runs[0].font.size = Pt(11)
        
        self.doc.add_paragraph()
    
    def _agregar_fases(self):
        """Agrega fases del proyecto"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('FASES DEL PROYECTO')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        fases = self.datos.get('fases', [])
        
        if fases:
            table = self.doc.add_table(rows=len(fases) + 1, cols=4)
            table.style = 'Table Grid'
            
            # Header
            headers = ['FASE', 'DESCRIPCIÓN', 'DURACIÓN', 'RESPONSABLE']
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
            
            # Fases
            for idx, fase in enumerate(fases, 1):
                row = table.rows[idx]
                row.cells[0].text = f"Fase {idx}"
                row.cells[1].text = fase.get('descripcion', '')
                row.cells[2].text = fase.get('duracion', '1 semana')
                row.cells[3].text = fase.get('responsable', 'Por asignar')
        
        self.doc.add_paragraph()
    
    def _agregar_cronograma(self):
        """Agrega cronograma"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('CRONOGRAMA')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        cronograma = self.datos.get('cronograma', {})
        inicio = cronograma.get('fecha_inicio', '01/01/2025')
        fin = cronograma.get('fecha_fin', '31/12/2025')
        duracion = cronograma.get('duracion_total', '12 meses')
        
        p_info = self.doc.add_paragraph()
        p_info.add_run(f'Fecha de Inicio: ').font.bold = True
        p_info.add_run(f'{inicio}\n')
        p_info.add_run(f'Fecha de Fin: ').font.bold = True
        p_info.add_run(f'{fin}\n')
        p_info.add_run(f'Duración Total: ').font.bold = True
        p_info.add_run(f'{duracion}')
        
        self.doc.add_paragraph()
    
    def _agregar_recursos(self):
        """Agrega recursos del proyecto"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('RECURSOS ASIGNADOS')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        recursos = self.datos.get('recursos', {})
        humanos = recursos.get('humanos', [])
        materiales = recursos.get('materiales', [])
        
        if humanos:
            p_humanos = self.doc.add_paragraph()
            p_humanos.add_run('Recursos Humanos:\n').font.bold = True
            for recurso in humanos:
                self.doc.add_paragraph(f"• {recurso}", style='List Bullet')
        
        if materiales:
            p_materiales = self.doc.add_paragraph()
            p_materiales.add_run('Recursos Materiales:\n').font.bold = True
            for material in materiales:
                self.doc.add_paragraph(f"• {material}", style='List Bullet')
        
        self.doc.add_paragraph()
    
    def generar(self, ruta_salida):
        """Genera el documento completo"""
        self._agregar_header_basico()
        self._agregar_titulo()
        self._agregar_resumen()
        self._agregar_fases()
        self._agregar_cronograma()
        self._agregar_recursos()
        self._agregar_footer_basico()
        
        self.doc.save(str(ruta_salida))
        return ruta_salida


def generar_proyecto_simple(datos, ruta_salida, opciones=None):
    """Función de entrada para generar proyecto simple"""
    generator = ProyectoSimpleGenerator(datos, opciones)
    return generator.generar(ruta_salida)
