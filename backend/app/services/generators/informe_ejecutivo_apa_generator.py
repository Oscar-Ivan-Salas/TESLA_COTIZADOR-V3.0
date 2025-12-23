"""
Generador de Informe Ejecutivo (APA 7)
Informe con formato APA 7, referencias bibliográficas e índice
"""

from .base_generator import BaseDocumentGenerator
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class InformeEjecutivoAPAGenerator(BaseDocumentGenerator):
    """Generador para informes ejecutivos con formato APA 7"""
    
    def _agregar_portada(self):
        """Agrega portada estilo APA"""
        # Título
        p_titulo = self.doc.add_paragraph()
        p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = p_titulo.add_run(self.datos.get('titulo', 'INFORME EJECUTIVO'))
        run_titulo.font.size = Pt(16)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        self.doc.add_paragraph()
        
        # Autor
        autor = self.datos.get('autor', 'Autor')
        p_autor = self.doc.add_paragraph()
        p_autor.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_autor = p_autor.add_run(f'Por: {autor}')
        run_autor.font.size = Pt(12)
        
        # Institución
        institucion = self.datos.get('institucion', 'TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.')
        p_inst = self.doc.add_paragraph()
        p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_inst = p_inst.add_run(institucion)
        run_inst.font.size = Pt(12)
        
        # Fecha
        fecha = self.datos.get('fecha', '2025')
        p_fecha = self.doc.add_paragraph()
        p_fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_fecha = p_fecha.add_run(fecha)
        run_fecha.font.size = Pt(12)
        
        self.doc.add_page_break()
    
    def _agregar_resumen(self):
        """Agrega resumen (abstract) estilo APA"""
        p_titulo = self.doc.add_paragraph()
        p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = p_titulo.add_run('Resumen')
        run_titulo.font.size = Pt(12)
        run_titulo.font.bold = True
        
        resumen = self.datos.get('resumen', 'Resumen del informe ejecutivo...')
        p_resumen = self.doc.add_paragraph(resumen)
        p_resumen.runs[0].font.size = Pt(11)
        p_resumen.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        # Palabras clave
        palabras_clave = self.datos.get('palabras_clave', [])
        if palabras_clave:
            p_keywords = self.doc.add_paragraph()
            p_keywords.add_run('Palabras clave: ').font.italic = True
            p_keywords.add_run(', '.join(palabras_clave))
        
        self.doc.add_paragraph()
    
    def _agregar_introduccion(self):
        """Agrega introducción con numeración APA"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('Introducción')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        introduccion = self.datos.get('introduccion', 'Introducción del informe...')
        p_intro = self.doc.add_paragraph(introduccion)
        p_intro.runs[0].font.size = Pt(11)
        p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        self.doc.add_paragraph()
    
    def _agregar_metodologia(self):
        """Agrega metodología"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('Metodología')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        metodologia = self.datos.get('metodologia', 'Descripción de la metodología...')
        p_met = self.doc.add_paragraph(metodologia)
        p_met.runs[0].font.size = Pt(11)
        p_met.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        self.doc.add_paragraph()
    
    def _agregar_resultados(self):
        """Agrega resultados"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('Resultados')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        resultados = self.datos.get('resultados', {})
        secciones = resultados.get('secciones', [])
        
        for seccion in secciones:
            p_subseccion = self.doc.add_paragraph()
            run_subseccion = p_subseccion.add_run(seccion.get('titulo', 'Resultado'))
            run_subseccion.font.size = Pt(12)
            run_subseccion.font.bold = True
            
            contenido = seccion.get('contenido', '')
            p_contenido = self.doc.add_paragraph(contenido)
            p_contenido.runs[0].font.size = Pt(11)
            p_contenido.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        self.doc.add_paragraph()
    
    def _agregar_discusion(self):
        """Agrega discusión"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('Discusión')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        discusion = self.datos.get('discusion', 'Discusión de los resultados...')
        p_disc = self.doc.add_paragraph(discusion)
        p_disc.runs[0].font.size = Pt(11)
        p_disc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        self.doc.add_paragraph()
    
    def _agregar_conclusiones(self):
        """Agrega conclusiones"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('Conclusiones')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        conclusiones = self.datos.get('conclusiones', [])
        for conclusion in conclusiones:
            self.doc.add_paragraph(conclusion, style='List Bullet')
        
        self.doc.add_paragraph()
    
    def _agregar_referencias(self):
        """Agrega referencias bibliográficas estilo APA"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('Referencias')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        referencias = self.datos.get('referencias', [])
        
        for referencia in referencias:
            p_ref = self.doc.add_paragraph(referencia)
            p_ref.runs[0].font.size = Pt(11)
            # Sangría francesa (hanging indent)
            p_ref.paragraph_format.left_indent = Inches(0.5)
            p_ref.paragraph_format.first_line_indent = Inches(-0.5)
    
    def generar(self, ruta_salida):
        """Genera el documento completo"""
        self._agregar_portada()
        self._agregar_resumen()
        self._agregar_introduccion()
        self._agregar_metodologia()
        self._agregar_resultados()
        self._agregar_discusion()
        self._agregar_conclusiones()
        self._agregar_referencias()
        
        self.doc.save(str(ruta_salida))
        return ruta_salida


def generar_informe_ejecutivo_apa(datos, ruta_salida, opciones=None):
    """Función de entrada para generar informe ejecutivo APA"""
    generator = InformeEjecutivoAPAGenerator(datos, opciones)
    return generator.generar(ruta_salida)
