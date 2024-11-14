from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.conf import settings
from io import BytesIO
from datetime import datetime

class PDFGenerator:
    def generate_order_pdf(self, order, estimated_delivery):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Título
        title = Paragraph("factura del Pedido", styles['Title'])
        elements.append(title)

        # Información del pedido
        order_info = [
            ["Order ID:", order.id],
            ["Dirección:", order.address],
            ["Método de Pago:", order.payment_method],
            ["Precio Total:", f"${order.total_price()}"],
            ["Fecha de Emisión:", order.created_at.strftime("%Y-%m-%d %H:%M:%S")],
            ["Tiempo Estimado de Llegada:", estimated_delivery]
        ]
        order_table = Table(order_info, colWidths=[150, 300])
        order_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(order_table)

        # Información del cliente
        client_info = [
            ["Información del Cliente"],
            ["Nombre del Cliente:", order.user.username],
            ["Correo del Cliente:", order.user.email]
        ]
        client_table = Table(client_info, colWidths=[150, 300])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(client_table)

        # Información de la empresa
        company_info = [
            ["Información de la Empresa"],
            ["Nombre de la Empresa:", "Solarway"],
            ["Dirección:", "Universidad EAFIT"],
            ["Teléfono:", "+313 3467034"],
            ["Correo:", "dacruzj@eafit.edu.co - jsuarezb99@gmail.com"]
        ]
        company_table = Table(company_info, colWidths=[150, 300])
        company_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(company_table)

        # Gafas compradas
        gafas_info = [["Gafas Compradas"]]
        for gafa in order.gafas.all():
            gafas_info.append([f"{gafa.nombre} - ${gafa.precio}"])
        gafas_table = Table(gafas_info, colWidths=[450])
        gafas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(gafas_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer