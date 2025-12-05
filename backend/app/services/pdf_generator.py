
"""
═══════════════════════════════════════════════════════════════
PDF GENERATOR + PILI v3.0 - DOCUMENTOS PERFECTOS (TWIN DESIGN)
═══════════════════════════════════════════════════════════════

PROPÓSITO:
Generar documentos PDF profesionales con PARIDAD TOTAL funcional
respecto al generador de Word. Implementa el patrón "Twin Design"
para asegurar que el PDF se vea idéntico a los prototipos HTML.

CAPACIDADES:
- Cotizaciones (Simple/Compleja)
- Proyectos (Gestión/Gantt Tabular)
- Informes (Técnico/Ejecutivo)
- Despachador Polimórfico Inteligente

═══════════════════════════════════════════════════════════════
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import logging
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Generador profesional de documentos PDF usando ReportLab.
    Implementa la misma lógica de negocio que WordGenerator pero
    adaptada para renderizado vectorial PDF de alta calidad.
    """
    
    def __init__(self):
        """Inicializar generador con paleta oficial Tesla"""
        # Colores Tesla Oficiales (Coincidentes con HTML y Word)
        self.COLOR_TESLA_BLUE = colors.Color(26/255, 60/255, 110/255)  # #1a3c6e (Azul Corporativo)
        self.COLOR_TESLA_RED = colors.Color(204/255, 0/255, 0/255)     # #cc0000 (Rojo Acento)
        self.COLOR_DORADO = colors.Color(218/255, 165/255, 32/255)     # #DAA520
        self.COLOR_NEGRO = colors.black
        self.COLOR_GRIS_OSCURO = colors.Color(51/255, 51/255, 51/255)  # #333333
        self.COLOR_GRIS_CLARO = colors.Color(245/255, 245/255, 245/255) # #f5f5f5
        self.COLOR_BLANCO = colors.white
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()
        
        logger.info("✅ PDFGenerator Twin-Design inicializado")
    
    def _crear_estilos_personalizados(self):
        """Crear estilos personalizados idénticos al HTML"""
        
        # Título principal (H1)
        self.styles.add(ParagraphStyle(
            name='TituloTesla',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.COLOR_TESLA_BLUE,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo (H2)
        self.styles.add(ParagraphStyle(
            name='SubtituloTesla',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.COLOR_GRIS_OSCURO,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Encabezado de sección (H3)
        self.styles.add(ParagraphStyle(
            name='SeccionTesla',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.COLOR_TESLA_BLUE,
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderPadding=5,
            borderColor=self.COLOR_TESLA_BLUE,
            borderWidth=0,
            borderBottomWidth=1
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='NormalJustificado',
            parent=self.styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=10,
            textColor=self.COLOR_GRIS_OSCURO,
            leading=14
        ))

        # Texto normal centrado
        self.styles.add(ParagraphStyle(
            name='NormalCentrado',
            parent=self.styles['Normal'],
            alignment=TA_CENTER,
            fontSize=10,
            textColor=self.COLOR_GRIS_OSCURO
        ))
        
        # Texto pequeño
        self.styles.add(ParagraphStyle(
            name='Pequeno',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=self.COLOR_GRIS_OSCURO,
            alignment=TA_CENTER
        ))

    # ════════════════════════════════════════════════════════
    # 🧠 CEREBRO CENTRAL (DISPATCHER)
    # ════════════════════════════════════════════════════════

    def generar_desde_json_pili(
        self,
        datos_json: Dict[str, Any],
        tipo_documento: str = "cotizacion",
        opciones: Optional[Dict[str, Any]] = None,
        logo_base64: Optional[str] = None,
        ruta_salida: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Método maestro que decide qué tipo de PDF generar.
        Paridad total con WordGenerator.
        """
        try:
            logger.info(f"🤖 PILI PDF generando documento {tipo_documento}")
            
            # 1. Procesar datos (Normalización)
            datos_procesados = self._procesar_datos_entrada(datos_json)
            agente_pili = datos_json.get("agente_responsable", "PILI")
            
            # 2. Determinar ruta de salida si no existe
            if not ruta_salida:
                ruta_salida = self._generar_ruta_salida(datos_procesados, tipo_documento)

            # 3. Despachar al generador específico
            if "cotizacion" in tipo_documento:
                self._generar_cotizacion_pili(datos_procesados, ruta_salida, opciones, logo_base64, agente_pili)
            elif "proyecto" in tipo_documento:
                self._generar_proyecto_pili(datos_procesados, ruta_salida, opciones, logo_base64, agente_pili)
            elif "informe" in tipo_documento:
                self._generar_informe_pili(datos_procesados, ruta_salida, opciones, logo_base64, agente_pili)
            else:
                # Fallback
                self._generar_cotizacion_pili(datos_procesados, ruta_salida, opciones, logo_base64, agente_pili)

            return {
                "exito": True,
                "ruta_archivo": ruta_salida,
                "tipo_documento": tipo_documento,
                "mensaje": "PDF Generado Exitosamente"
            }

        except Exception as e:
            logger.error(f"❌ Error crítico generando PDF: {e}")
            return {"exito": False, "error": str(e)}

    # ════════════════════════════════════════════════════════
    # 1. GENERADOR DE COTIZACIONES (VENTAS)
    # ════════════════════════════════════════════════════════
    
    def _generar_cotizacion_pili(self, datos, ruta, opciones, logo, agente):
        """Genera cotización detallada (Simple o Compleja)"""
        doc = self._crear_documento_base(ruta)
        elementos = []
        
        # Header
        elementos.extend(self._crear_header(logo, agente))
        
        # Título
        elementos.append(Paragraph('COTIZACIÓN TÉCNICA', self.styles['TituloTesla']))
        elementos.append(Paragraph(datos.get('numero', 'COT-0000'), self.styles['SubtituloTesla']))
        elementos.append(Spacer(1, 20))
        
        # Datos Cliente
        elementos.append(self._crear_tabla_cliente(datos))
        elementos.append(Spacer(1, 20))
        
        # Descripción
        if datos.get('descripcion'):
            elementos.append(Paragraph('DESCRIPCIÓN DEL ALCANCE', self.styles['SeccionTesla']))
            elementos.append(Paragraph(datos.get('descripcion'), self.styles['NormalJustificado']))
            elementos.append(Spacer(1, 15))
        
        # Items
        if datos.get('items'):
            elementos.append(Paragraph('DETALLE ECONÓMICO', self.styles['SeccionTesla']))
            elementos.append(self._crear_tabla_items(datos['items']))
            elementos.append(Spacer(1, 10))
            
        # Totales
        elementos.append(self._crear_tabla_totales(datos))
        elementos.append(Spacer(1, 20))
        
        # Condiciones
        elementos.append(Paragraph('CONDICIONES COMERCIALES', self.styles['SeccionTesla']))
        condiciones = [
            f"• Validez de la oferta: {datos.get('vigencia', '15 días')}",
            "• Forma de pago: 50% adelanto, 50% contra entrega",
            "• Tiempo de entrega: A coordinar según disponibilidad",
            "• Garantía: 12 meses por defectos de fábrica"
        ]
        for cond in condiciones:
            elementos.append(Paragraph(cond, self.styles['NormalJustificado']))
            
        # Footer
        elementos.extend(self._crear_footer(agente))
        
        doc.build(elementos)

    # ════════════════════════════════════════════════════════
    # 2. GENERADOR DE PROYECTOS (GESTIÓN)
    # ════════════════════════════════════════════════════════

    def _generar_proyecto_pili(self, datos, ruta, opciones, logo, agente):
        """Genera documento de gestión de proyectos (Fases, Hitos)"""
        doc = self._crear_documento_base(ruta)
        elementos = []
        
        # Header
        elementos.extend(self._crear_header(logo, agente))
        
        # Título
        elementos.append(Paragraph('PLAN DE PROYECTO', self.styles['TituloTesla']))
        elementos.append(Paragraph(datos.get('nombre_proyecto', 'Proyecto Sin Nombre'), self.styles['SubtituloTesla']))
        elementos.append(Spacer(1, 20))
        
        # Info General Proyecto
        data_info = [
            ['Cliente:', datos.get('cliente', '')],
            ['Fecha Inicio:', datos.get('fecha_inicio', datetime.now().strftime('%d/%m/%Y'))],
            ['Duración Est.:', datos.get('duracion_estimada', 'Por definir')],
            ['Estado:', datos.get('estado', 'Planificación').upper()]
        ]
        t_info = Table(data_info, colWidths=[2*inch, 4*inch])
        t_info.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0,0), (0,-1), self.COLOR_TESLA_BLUE),
            ('GRID', (0,0), (-1,-1), 0.5, self.COLOR_GRIS_CLARO),
            ('BACKGROUND', (0,0), (0,-1), self.COLOR_GRIS_CLARO),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        elementos.append(t_info)
        elementos.append(Spacer(1, 20))
        
        # Fases del Proyecto (Gantt Tabular)
        if datos.get('fases'):
            elementos.append(Paragraph('CRONOGRAMA DE FASES', self.styles['SeccionTesla']))
            
            headers = ['FASE', 'DURACIÓN', 'ENTREGABLE', 'ESTADO']
            data_fases = [headers]
            
            for fase in datos['fases']:
                row = [
                    Paragraph(fase.get('nombre', ''), self.styles['NormalJustificado']),
                    fase.get('duracion', ''),
                    Paragraph(fase.get('entregable', '-'), self.styles['Pequeno']),
                    fase.get('estado', 'Pendiente')
                ]
                data_fases.append(row)
                
            t_fases = Table(data_fases, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1*inch])
            t_fases.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), self.COLOR_TESLA_BLUE),
                ('TEXTCOLOR', (0,0), (-1,0), self.COLOR_BLANCO),
                ('ALIGN', (0,0), (-1,0), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 0.5, self.COLOR_GRIS_CLARO),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (1,1), (-1,-1), [self.COLOR_BLANCO, self.COLOR_GRIS_CLARO])
            ]))
            elementos.append(t_fases)
            elementos.append(Spacer(1, 20))
            
        # Recursos
        if datos.get('recursos'):
            elementos.append(Paragraph('RECURSOS ASIGNADOS', self.styles['SeccionTesla']))
            for recurso in datos['recursos']:
                elementos.append(Paragraph(f"• {recurso}", self.styles['NormalJustificado']))

        # Footer
        elementos.extend(self._crear_footer(agente))
        doc.build(elementos)

    # ════════════════════════════════════════════════════════
    # 3. GENERADOR DE INFORMES (REPORTING)
    # ════════════════════════════════════════════════════════

    def _generar_informe_pili(self, datos, ruta, opciones, logo, agente):
        """Genera informe técnico o ejecutivo"""
        doc = self._crear_documento_base(ruta)
        elementos = []
        
        # Header
        elementos.extend(self._crear_header(logo, agente))
        
        # Título
        titulo_texto = datos.get('titulo_informe', 'INFORME TÉCNICO').upper()
        elementos.append(Paragraph(titulo_texto, self.styles['TituloTesla']))
        elementos.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", self.styles['NormalCentrado']))
        elementos.append(Spacer(1, 20))
        
        # Resumen Ejecutivo
        if datos.get('resumen_ejecutivo'):
            elementos.append(Paragraph('RESUMEN EJECUTIVO', self.styles['SeccionTesla']))
            elementos.append(Paragraph(datos['resumen_ejecutivo'], self.styles['NormalJustificado']))
            elementos.append(Spacer(1, 15))
            
        # Cuerpo del Informe (Secciones dinámicas)
        if datos.get('secciones'):
            for seccion in datos['secciones']:
                elementos.append(Paragraph(seccion.get('titulo', '').upper(), self.styles['SeccionTesla']))
                elementos.append(Paragraph(seccion.get('contenido', ''), self.styles['NormalJustificado']))
                elementos.append(Spacer(1, 10))
                
        # Conclusiones
        if datos.get('conclusiones'):
            elementos.append(Paragraph('CONCLUSIONES', self.styles['SeccionTesla']))
            if isinstance(datos['conclusiones'], list):
                for con in datos['conclusiones']:
                    elementos.append(Paragraph(f"• {con}", self.styles['NormalJustificado']))
            else:
                elementos.append(Paragraph(datos['conclusiones'], self.styles['NormalJustificado']))
                
        # Footer
        elementos.extend(self._crear_footer(agente))
        doc.build(elementos)

    # ════════════════════════════════════════════════════════
    # COMPONENTES REUTILIZABLES (UI KIT)
    # ════════════════════════════════════════════════════════

    def _crear_documento_base(self, ruta):
        return SimpleDocTemplate(
            ruta,
            pagesize=A4,
            rightMargin=50, leftMargin=50,
            topMargin=50, bottomMargin=50
        )

    def _crear_header(self, logo_base64, agente):
        elems = []
        # Tabla Header: Logo | Info Empresa
        info_empresa = [
            Paragraph('<b>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</b>', self.styles['Normal']),
            Paragraph('RUC: 20601138787', self.styles['Pequeno']),
            Paragraph(f'Generado por Agente IA: {agente}', self.styles['Pequeno'])
        ]
        
        img_logo = self._decodificar_logo(logo_base64) if logo_base64 else None
        
        data = [[img_logo if img_logo else '', info_empresa]]
        t = Table(data, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'LEFT'),
        ]))
        elems.append(t)
        elems.append(Spacer(1, 20))
        return elems

    def _crear_tabla_cliente(self, datos):
        data = [
            [Paragraph('<b>CLIENTE:</b>', self.styles['Normal']), Paragraph(datos.get('cliente', ''), self.styles['Normal'])],
            [Paragraph('<b>PROYECTO:</b>', self.styles['Normal']), Paragraph(datos.get('proyecto', ''), self.styles['Normal'])],
            [Paragraph('<b>FECHA:</b>', self.styles['Normal']), Paragraph(datetime.now().strftime('%d/%m/%Y'), self.styles['Normal'])]
        ]
        t = Table(data, colWidths=[1.5*inch, 4.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), self.COLOR_GRIS_CLARO),
            ('GRID', (0,0), (-1,-1), 0.5, self.COLOR_BLANCO),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    def _crear_tabla_items(self, items):
        headers = ['DESCRIPCIÓN', 'CANT.', 'P.UNIT', 'TOTAL']
        data = [headers]
        col_widths = [3.5*inch, 0.8*inch, 1.2*inch, 1.2*inch]
        
        for item in items:
            cant = float(item.get('cantidad', 0))
            precio = float(item.get('precio_unitario', 0))
            total = cant * precio
            row = [
                Paragraph(item.get('descripcion', ''), self.styles['Normal']),
                f"{cant}",
                f"S/ {precio:,.2f}",
                f"S/ {total:,.2f}"
            ]
            data.append(row)
            
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.COLOR_TESLA_BLUE),
            ('TEXTCOLOR', (0,0), (-1,0), self.COLOR_BLANCO),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('GRID', (0,0), (-1,-1), 0.5, self.COLOR_GRIS_CLARO),
            ('ROWBACKGROUNDS', (1,1), (-1,-1), [self.COLOR_BLANCO, self.COLOR_GRIS_CLARO])
        ]))
        return t

    def _crear_tabla_totales(self, datos):
        subtotal = float(datos.get('subtotal', 0))
        igv = subtotal * 0.18
        total = subtotal + igv
        
        data = [
            ['Subtotal:', f"S/ {subtotal:,.2f}"],
            ['IGV (18%):', f"S/ {igv:,.2f}"],
            ['TOTAL:', f"S/ {total:,.2f}"]
        ]
        t = Table(data, colWidths=[5*inch, 1.7*inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,2), (1,2), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0,2), (1,2), self.COLOR_TESLA_BLUE),
            ('LINEABOVE', (0,2), (1,2), 1, self.COLOR_TESLA_BLUE),
        ]))
        return t

    def _crear_footer(self, agente):
        elems = []
        elems.append(Spacer(1, 40))
        elems.append(Paragraph('_' * 60, self.styles['NormalCentrado']))
        elems.append(Paragraph(f'Documento generado automáticamente por {agente} - Tesla AI System', self.styles['Pequeno']))
        return elems

    def _decodificar_logo(self, logo_base64):
        try:
            if ',' in logo_base64: logo_base64 = logo_base64.split(',')[1]
            img = Image(BytesIO(base64.b64decode(logo_base64)))
            img.drawHeight = 0.8*inch
            img.drawWidth = 2*inch
            img.keepAspectRatio = True
            return img
        except: return None

    def _procesar_datos_entrada(self, datos_json):
        """Normaliza los datos de entrada"""
        datos = datos_json.get("datos_extraidos", {})
        # Asegurar campos mínimos
        if "items" not in datos: datos["items"] = []
        return datos

    def _generar_ruta_salida(self, datos, tipo):
        """Genera ruta temporal si no se especifica"""
        import tempfile
        filename = f"{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return str(Path(tempfile.gettempdir()) / filename)

    # Métodos legacy para compatibilidad
    def generar_cotizacion(self, datos, ruta, **kwargs):
        return self.generar_desde_json_pili({"datos_extraidos": datos}, "cotizacion", ruta_salida=ruta, **kwargs)
    
    def generar_informe_proyecto(self, datos, ruta, **kwargs):
        return self.generar_desde_json_pili({"datos_extraidos": datos}, "proyecto", ruta_salida=ruta, **kwargs)
        
    def generar_informe_simple(self, datos, ruta, **kwargs):
        return self.generar_desde_json_pili({"datos_extraidos": datos}, "informe", ruta_salida=ruta, **kwargs)

# Instancia Global
pdf_generator = PDFGenerator()
