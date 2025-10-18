from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import Dict, Any, List
import os

class PDFGenerator:
    
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 0.75 * inch
    
    def generar_cotizacion(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        """
        Genera un PDF profesional de cotización
        """
        
        # Crear documento
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        doc = SimpleDocTemplate(
            ruta_salida,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Contenedor de elementos
        elementos = []
        
        # Estilos
        estilos = getSampleStyleSheet()
        
        # Estilo personalizado para título
        estilo_titulo = ParagraphStyle(
            'CustomTitle',
            parent=estilos['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#8B0000'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        estilo_subtitulo = ParagraphStyle(
            'CustomSubtitle',
            parent=estilos['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#8B0000'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        estilo_normal = ParagraphStyle(
            'CustomNormal',
            parent=estilos['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY
        )
        
        estilo_centrado = ParagraphStyle(
            'CustomCenter',
            parent=estilos['Normal'],
            fontSize=10,
            alignment=TA_CENTER
        )
        
        # === ENCABEZADO ===
        elementos.append(Paragraph("COTIZACIÓN", estilo_titulo))
        elementos.append(Paragraph(
            f"Fecha: {datetime.now().strftime('%d de %B de %Y')}", 
            estilo_centrado
        ))
        elementos.append(Paragraph(
            f"N° {datos.get('numero', 'COT-0001')}", 
            estilo_centrado
        ))
        elementos.append(Spacer(1, 20))
        
        # === INFORMACIÓN DEL CLIENTE ===
        elementos.append(Paragraph("INFORMACIÓN DEL CLIENTE", estilo_subtitulo))
        
        datos_cliente = [
            ['Cliente:', datos.get('cliente', '')],
            ['Proyecto:', datos.get('proyecto', '')]
        ]
        
        tabla_cliente = Table(datos_cliente, colWidths=[2*inch, 4.5*inch])
        tabla_cliente.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F0F0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elementos.append(tabla_cliente)
        elementos.append(Spacer(1, 20))
        
        # === DESCRIPCIÓN ===
        if datos.get('descripcion'):
            elementos.append(Paragraph("DESCRIPCIÓN DEL PROYECTO", estilo_subtitulo))
            elementos.append(Paragraph(datos['descripcion'], estilo_normal))
            elementos.append(Spacer(1, 20))
        
        # === DETALLE DE SERVICIOS ===
        elementos.append(Paragraph("DETALLE DE SERVICIOS", estilo_subtitulo))
        
        # Encabezados de la tabla
        datos_items = [['Descripción', 'Cant.', 'P. Unitario', 'Total']]
        
        # Items
        items = datos.get('items', [])
        for item in items:
            datos_items.append([
                item.get('descripcion', ''),
                str(item.get('cantidad', '')),
                f"S/ {item.get('precioUnitario', 0):.2f}",
                f"S/ {item.get('total', 0):.2f}"
            ])
        
        tabla_items = Table(
            datos_items, 
            colWidths=[3.5*inch, 0.8*inch, 1.2*inch, 1.2*inch]
        )
        
        tabla_items.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            # Cuerpo
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Filas alternas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ]))
        
        elementos.append(tabla_items)
        elementos.append(Spacer(1, 30))
        
        # === TOTALES ===
        datos_totales = [
            ['Subtotal:', f"S/ {datos.get('subtotal', 0):.2f}"],
            ['IGV (18%):', f"S/ {datos.get('igv', 0):.2f}"],
            ['TOTAL:', f"S/ {datos.get('total', 0):.2f}"]
        ]
        
        tabla_totales = Table(datos_totales, colWidths=[4.5*inch, 2*inch])
        tabla_totales.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 1), 11),
            ('FONTSIZE', (0, 2), (-1, 2), 14),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#8B0000')),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.HexColor('#8B0000')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elementos.append(tabla_totales)
        elementos.append(Spacer(1, 30))
        
        # === OBSERVACIONES ===
        if datos.get('observaciones'):
            elementos.append(Paragraph("OBSERVACIONES", estilo_subtitulo))
            elementos.append(Paragraph(datos['observaciones'], estilo_normal))
            elementos.append(Spacer(1, 20))
        
        # === CONDICIONES ===
        elementos.append(Paragraph("CONDICIONES", estilo_subtitulo))
        
        condiciones = [
            f"• Vigencia de la cotización: {datos.get('vigencia', '30 días')}",
            "• Forma de pago: Por definir",
            "• Tiempo de entrega: Por definir según alcance",
            "• Los precios incluyen IGV"
        ]
        
        for condicion in condiciones:
            elementos.append(Paragraph(condicion, estilo_normal))
        
        elementos.append(Spacer(1, 40))
        
        # === FOOTER ===
        elementos.append(Spacer(1, 20))
        elementos.append(Paragraph("<b>TESLA COTIZADOR PRO</b>", estilo_centrado))
        elementos.append(Paragraph("📱 WhatsApp: +51 999 888 777", estilo_centrado))
        elementos.append(Paragraph("📧 ventas@teslacotizador.com", estilo_centrado))
        elementos.append(Paragraph("📍 Lima, Perú", estilo_centrado))
        
        # Construir PDF
        doc.build(elementos)
        
        return ruta_salida
    
    def generar_informe_simple(self, datos: Dict[str, Any], ruta_salida: str) -> str:
        """
        Genera un informe PDF simple
        """
        
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        
        c = canvas.Canvas(ruta_salida, pagesize=A4)
        width, height = A4
        
        # Título
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor('#8B0000'))
        c.drawCentredString(width/2, height - 100, "INFORME")
        
        # Contenido básico
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        
        y_position = height - 150
        
        for key, value in datos.items():
            if y_position < 100:
                c.showPage()
                y_position = height - 100
            
            c.drawString(100, y_position, f"{key}: {value}")
            y_position -= 25
        
        c.save()
        return ruta_salida

# Instancia global
pdf_generator = PDFGenerator()