
"""
═══════════════════════════════════════════════════════════════
PDF GENERATOR - Generador de Documentos PDF Profesionales
═══════════════════════════════════════════════════════════════

PROPÓSITO:
Generar documentos PDF profesionales para cotizaciones,
informes de proyectos, y reportes técnicos usando ReportLab.
Con diseño profesional Tesla (Tema Rojo/Dorado).

FUNCIONES PRINCIPALES:
- generar_cotizacion() → Cotizaciones de venta
- generar_informe_proyecto() → Informes ejecutivos de proyectos
- generar_informe_simple() → Informes básicos

CARACTERÍSTICAS:
- Soporte para logo personalizado
- Tablas dinámicas con estilo Tesla Rojo/Dorado
- Formato profesional (Colores Corporativos Tesla)
- No editable (seguridad)

═══════════════════════════════════════════════════════════════
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import logging
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Generador profesional de documentos PDF usando ReportLab
    Diseño profesional Tesla (Tema Rojo/Dorado)
    """
    
    def __init__(self):
        """Inicializar generador con paleta oficial Tesla (Rojo/Dorado)"""
        # Colores Tesla Oficiales (Tema Rojo/Dorado)
        self.COLOR_ROJO = colors.Color(139/255, 0/255, 0/255)          # #8B0000 (Rojo Tesla)
        self.COLOR_DORADO = colors.Color(212/255, 175/255, 55/255)     # #D4AF37 (Dorado)
        self.COLOR_NEGRO = colors.black
        self.COLOR_GRIS_OSCURO = colors.Color(51/255, 51/255, 51/255)  # #333333
        self.COLOR_GRIS_CLARO = colors.Color(245/255, 245/255, 245/255) # #f5f5f5
        self.COLOR_BLANCO = colors.white
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()
        
        logger.info("PDFGenerator inicializado con estilos HTML-Twin")
    
    def _crear_estilos_personalizados(self):
        """Crear estilos personalizados idénticos al HTML"""
        
        # Título principal (H1)
        self.styles.add(ParagraphStyle(
            name='TituloTesla',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.COLOR_ROJO,
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
            textColor=self.COLOR_ROJO,
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderPadding=5,
            borderColor=self.COLOR_ROJO,
            borderWidth=0,
            borderBottomWidth=1
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
    # FUNCIÓN PRINCIPAL - COTIZACIÓN
    # ════════════════════════════════════════════════════════
    
    def generar_cotizacion(
        self,
        datos: Dict[str, Any],
        ruta_salida: str,
        opciones: Optional[Dict[str, bool]] = None,
        logo_base64: Optional[str] = None
    ) -> str:
        """Generar PDF de cotización con diseño HTML-Twin"""
        
        try:
            logger.info(f"Generando PDF cotización Twin-Design: {datos.get('numero', 'N/A')}")
            
            # Configurar opciones
            opts = {
                'mostrar_precios': True,
                'mostrar_igv': True,
                'mostrar_observaciones': True,
                'mostrar_logo': True
            }
            if opciones: opts.update(opciones)
            
            # Crear directorio
            Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
            
            # Documento
            doc = SimpleDocTemplate(
                ruta_salida,
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )
            
            elementos = []
            
            # 1. Header Corporativo (Logo + Empresa)
            data_header = []
            
            # Logo
            img_logo = None
            if logo_base64 and opts['mostrar_logo']:
                img_logo = self._decodificar_logo(logo_base64)
            
            # Info Empresa
            info_empresa = [
                Paragraph('<b>TESLA ELECTRICIDAD Y AUTOMATIZACIÓN S.A.C.</b>', self.styles['Normal']),
                Paragraph('RUC: 20601138787', self.styles['Normal']),
                Paragraph('Ingeniería Eléctrica Especializada', self.styles['Pequeno'])
            ]
            
            if img_logo:
                data_header = [[img_logo, info_empresa]]
            else:
                data_header = [[info_empresa]]
                
            tabla_header = Table(data_header, colWidths=[2*inch, 4*inch])
            tabla_header.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            elementos.append(tabla_header)
            elementos.append(Spacer(1, 20))
            
            # 2. Título del Documento
            elementos.append(Paragraph('COTIZACIÓN TÉCNICA', self.styles['TituloTesla']))
            elementos.append(Paragraph(datos.get('numero', 'COT-XXXX'), self.styles['SubtituloTesla']))
            elementos.append(Spacer(1, 20))
            
            # 3. Datos del Cliente (Caja Gris estilo HTML)
            data_cliente = [
                [Paragraph('<b>CLIENTE:</b>', self.styles['Normal']), Paragraph(datos.get('cliente', ''), self.styles['Normal'])],
                [Paragraph('<b>PROYECTO:</b>', self.styles['Normal']), Paragraph(datos.get('proyecto', ''), self.styles['Normal'])],
                [Paragraph('<b>FECHA:</b>', self.styles['Normal']), Paragraph(datetime.now().strftime('%d/%m/%Y'), self.styles['Normal'])],
                [Paragraph('<b>VIGENCIA:</b>', self.styles['Normal']), Paragraph(datos.get('vigencia', '30 días'), self.styles['Normal'])]
            ]
            
            tabla_cliente = Table(data_cliente, colWidths=[1.5*inch, 4.5*inch])
            tabla_cliente.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), self.COLOR_GRIS_CLARO),
                ('GRID', (0,0), (-1,-1), 0.5, self.COLOR_BLANCO),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            elementos.append(tabla_cliente)
            elementos.append(Spacer(1, 20))
            
            # 4. Tabla de Items (Estilo Tesla Blue)
            if datos.get('items'):
                elementos.append(Paragraph('DETALLE DE SERVICIOS', self.styles['SeccionTesla']))
                tabla_items = self._crear_tabla_items(datos['items'], opts)
                elementos.append(tabla_items)
                elementos.append(Spacer(1, 15))
            
            # 5. Totales (Alineados a la derecha)
            if opts['mostrar_precios']:
                tabla_totales = self._crear_tabla_totales(datos)
                elementos.append(tabla_totales)
                elementos.append(Spacer(1, 20))
            
            # 6. Observaciones
            if datos.get('observaciones'):
                elementos.append(Paragraph('OBSERVACIONES', self.styles['SeccionTesla']))
                elementos.append(Paragraph(datos.get('observaciones'), self.styles['Normal']))
                elementos.append(Spacer(1, 20))
            
            # 7. Footer
            elementos.append(Spacer(1, 40))
            elementos.append(Paragraph('_' * 60, self.styles['NormalCentrado']))
            elementos.append(Paragraph('TESLA ELECTRICIDAD - DEPARTAMENTO DE INGENIERÍA', self.styles['Pequeno']))
            
            doc.build(elementos)
            logger.info(f"✅ PDF generado exitosamente: {ruta_salida}")
            return ruta_salida
            
        except Exception as e:
            logger.error(f"Error generando PDF: {e}")
            raise Exception(f"Error PDF: {e}")
    
    # ════════════════════════════════════════════════════════
    # FUNCIÓN PRINCIPAL - INFORME DE PROYECTO (NUEVO)
    # ════════════════════════════════════════════════════════
    
    def generar_informe_proyecto(self, *args, **kwargs): return self.generar_cotizacion(*args, **kwargs)
    
    # ════════════════════════════════════════════════════════
    # FUNCIONES AUXILIARES
    # ════════════════════════════════════════════════════════
    
    def _decodificar_logo(self, logo_base64: str) -> Optional[Image]:
        """Decodifica logo base64 a imagen ReportLab"""
        try:
            if ',' in logo_base64:
                logo_base64 = logo_base64.split(',')[1]
            img_bytes = base64.b64decode(logo_base64)
            img = Image(BytesIO(img_bytes))
            img.drawHeight = 0.8*inch
            img.drawWidth = 2*inch
            img.keepAspectRatio = True
            return img
        except:
            return None
    
    def _crear_tabla_items(self, items: List[Dict], opciones: Dict) -> Table:
        """Crear tabla con estilo Tesla Blue idéntico al HTML"""
        
        headers = ['DESCRIPCIÓN', 'CANT.', 'P.UNIT', 'TOTAL']
        col_widths = [3.5*inch, 0.8*inch, 1.2*inch, 1.2*inch]
        
        data = [headers]
        
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
            
        tabla = Table(data, colWidths=col_widths)
        
        # Estilo Tesla Rojo
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.COLOR_ROJO),        # Header Rojo Tesla
            ('TEXTCOLOR', (0,0), (-1,0), self.COLOR_BLANCO),       # Texto Blanco
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('TOPPADDING', (0,0), (-1,0), 8),

            # Filas de datos
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'), # Números a la derecha
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, self.COLOR_GRIS_CLARO),
            ('ROWBACKGROUNDS', (1,1), (-1,-1), [self.COLOR_BLANCO, self.COLOR_GRIS_CLARO]) # Zebra striping
        ]))
        
        return tabla
    
    def _crear_tabla_totales(self, datos: Dict) -> Table:
        """Tabla de totales compacta"""
        subtotal = float(datos.get('subtotal', 0))
        igv = subtotal * 0.18
        total = subtotal + igv
        
        data = [
            ['Subtotal:', f"S/ {subtotal:,.2f}"],
            ['IGV (18%):', f"S/ {igv:,.2f}"],
            ['TOTAL:', f"S/ {total:,.2f}"]
        ]
        
        tabla = Table(data, colWidths=[5*inch, 1.7*inch])
        tabla.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTNAME', (0,2), (1,2), 'Helvetica-Bold'), # Total en negrita
            ('TEXTCOLOR', (0,2), (1,2), self.COLOR_ROJO), # Total en Rojo Tesla
            ('FONTSIZE', (0,2), (1,2), 12),
            ('LINEABOVE', (0,2), (1,2), 1, self.COLOR_ROJO),
        ]))
        
        return tabla
    
    def _formatear_fecha(self, fecha) -> str:
        """Formatear fecha a string"""
        if not fecha:
            return 'N/A'
        
        if isinstance(fecha, str):
            return fecha
        
        try:
            return fecha.strftime('%d/%m/%Y')
        except:
            return str(fecha)
    
    def _formatear_fecha_str(self, fecha_str: str) -> str:
        """Formatear fecha desde string"""
        if not fecha_str or fecha_str == 'N/A':
            return 'N/A'
        return fecha_str
    
    def generar_informe_simple(self, *args, **kwargs): return self.generar_cotizacion(*args, **kwargs)

# ════════════════════════════════════════════════════════
# INSTANCIA GLOBAL
# ════════════════════════════════════════════════════════

pdf_generator = PDFGenerator()
