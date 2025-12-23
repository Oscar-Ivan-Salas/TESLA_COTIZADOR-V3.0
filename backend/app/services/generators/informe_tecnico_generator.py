"""
Generador de Informe Técnico
Informe con resumen ejecutivo, análisis técnico y conclusiones
"""

from .base_generator import BaseDocumentGenerator
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class InformeTecnicoGenerator(BaseDocumentGenerator):
    """Generador para informes técnicos"""
    
    def _agregar_titulo(self):
        """Agrega título del documento"""
        p_titulo = self.doc.add_paragraph()
        p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_titulo = p_titulo.add_run('INFORME TÉCNICO')
        run_titulo.font.size = Pt(18)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        titulo_informe = self.datos.get('titulo', 'Informe Técnico')
        p_subtitulo = self.doc.add_paragraph()
        p_subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_subtitulo = p_subtitulo.add_run(titulo_informe)
        run_subtitulo.font.size = Pt(14)
        run_subtitulo.font.color.rgb = self.COLOR_SECUNDARIO
        
        self.doc.add_paragraph()
    
    def _agregar_resumen_ejecutivo(self):
        """Agrega resumen ejecutivo"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('RESUMEN EJECUTIVO')
        run_titulo.font.size = Pt(14)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        resumen = self.datos.get('resumen_ejecutivo', 'Resumen del informe técnico...')
        p_resumen = self.doc.add_paragraph(resumen)
        p_resumen.runs[0].font.size = Pt(11)
        p_resumen.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        self.doc.add_paragraph()
    
    def _agregar_introduccion(self):
        """Agrega introducción"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('1. INTRODUCCIÓN')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        introduccion = self.datos.get('introduccion', 'Introducción del informe...')
        p_intro = self.doc.add_paragraph(introduccion)
        p_intro.runs[0].font.size = Pt(11)
        p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        self.doc.add_paragraph()
    
    def _agregar_analisis_tecnico(self):
        """Agrega análisis técnico detallado"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('2. ANÁLISIS TÉCNICO')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        analisis = self.datos.get('analisis_tecnico', {})
        secciones = analisis.get('secciones', [])
        
        for idx, seccion in enumerate(secciones, 1):
            # Subsección
            p_subseccion = self.doc.add_paragraph()
            run_subseccion = p_subseccion.add_run(f"2.{idx}. {seccion.get('titulo', 'Sección')}")
            run_subseccion.font.size = Pt(12)
            run_subseccion.font.bold = True
            run_subseccion.font.color.rgb = self.COLOR_SECUNDARIO
            
            # Contenido
            contenido = seccion.get('contenido', '')
            p_contenido = self.doc.add_paragraph(contenido)
            p_contenido.runs[0].font.size = Pt(11)
            p_contenido.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            # Hallazgos
            hallazgos = seccion.get('hallazgos', [])
            if hallazgos:
                p_hallazgos = self.doc.add_paragraph()
                p_hallazgos.add_run('Hallazgos:\n').font.bold = True
                for hallazgo in hallazgos:
                    self.doc.add_paragraph(f"• {hallazgo}", style='List Bullet')
        
        self.doc.add_paragraph()
    
    def _agregar_conclusiones(self):
        """Agrega conclusiones y recomendaciones"""
        p_titulo = self.doc.add_paragraph()
        run_titulo = p_titulo.add_run('3. CONCLUSIONES Y RECOMENDACIONES')
        run_titulo.font.size = Pt(13)
        run_titulo.font.bold = True
        run_titulo.font.color.rgb = self.COLOR_PRIMARIO
        
        # Conclusiones
        p_conclusiones_titulo = self.doc.add_paragraph()
        p_conclusiones_titulo.add_run('3.1. Conclusiones\n').font.bold = True
        
        conclusiones = self.datos.get('conclusiones', [])
        for conclusion in conclusiones:
            self.doc.add_paragraph(f"• {conclusion}", style='List Bullet')
        
        # Recomendaciones
        p_recomendaciones_titulo = self.doc.add_paragraph()
        p_recomendaciones_titulo.add_run('3.2. Recomendaciones\n').font.bold = True
        
        recomendaciones = self.datos.get('recomendaciones', [])
        for recomendacion in recomendaciones:
            self.doc.add_paragraph(f"• {recomendacion}", style='List Bullet')
        
        self.doc.add_paragraph()
    
    def _agregar_anexos(self):
        """Agrega anexos técnicos"""
        anexos = self.datos.get('anexos', [])
        
        if anexos:
            p_titulo = self.doc.add_paragraph()
            run_titulo = p_titulo.add_run('ANEXOS')
            run_titulo.font.size = Pt(13)
            run_titulo.font.bold = True
            run_titulo.font.color.rgb = self.COLOR_PRIMARIO
            
            for idx, anexo in enumerate(anexos, 1):
                p_anexo = self.doc.add_paragraph()
                run_anexo = p_anexo.add_run(f"Anexo {idx}: {anexo.get('titulo', 'Sin título')}")
                run_anexo.font.bold = True
                
                descripcion = anexo.get('descripcion', '')
                if descripcion:
                    p_desc = self.doc.add_paragraph(descripcion)
                    p_desc.runs[0].font.size = Pt(10)
    
    def generar(self, ruta_salida):
        """Genera el documento completo"""
        self._agregar_header_basico()
        self._agregar_titulo()
        self._agregar_resumen_ejecutivo()
        self._agregar_introduccion()
        self._agregar_analisis_tecnico()
        self._agregar_conclusiones()
        self._agregar_anexos()
        self._agregar_footer_basico()
        
        self.doc.save(str(ruta_salida))
        return ruta_salida


def generar_informe_tecnico(datos, ruta_salida, opciones=None):
    """Función de entrada para generar informe técnico"""
    generator = InformeTecnicoGenerator(datos, opciones)
    return generator.generar(ruta_salida)
