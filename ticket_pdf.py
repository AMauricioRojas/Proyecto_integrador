# ticket_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_ticket_pdf(id_venta, productos, total, nombre_cliente="Cliente General"):
    """
    Genera un ticket en formato PDF para una venta.
    :param id_venta: int - ID de la venta
    :param productos: list - Lista de tuplas (nombre, cantidad, precio, subtotal)
    :param total: float - Total de la venta
    :param nombre_cliente: str - Nombre del cliente (opcional)
    """
    
    # 📁 Carpeta para guardar los tickets
    carpeta = "tickets_pdf"
    os.makedirs(carpeta, exist_ok=True)
    
    # 📄 Nombre del archivo
    nombre_archivo = f"{carpeta}/ticket_{id_venta}.pdf"
    
    # 🧾 Crear PDF
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    c.setTitle(f"Ticket Fogón EMD #{id_venta}")
    
    # 🕓 Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Fogón EMD POS")
    
    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 735, "Durango, México")
    c.drawCentredString(300, 720, datetime.now().strftime("Fecha: %d/%m/%Y  Hora: %H:%M"))
    c.drawCentredString(300, 705, f"Cliente: {nombre_cliente}")
    
    # 🔹 Línea separadora
    c.line(50, 695, 550, 695)
    
    # 🧮 Encabezados de tabla
    y = 675
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y, "Producto")
    c.drawString(250, y, "Cant.")
    c.drawString(300, y, "Precio")
    c.drawString(400, y, "Subtotal")
    
    # 🔹 Contenido de productos
    y -= 20
    c.setFont("Helvetica", 10)
    for nombre, cantidad, precio, subtotal in productos:
        c.drawString(60, y, nombre[:25])
        c.drawString(255, y, str(cantidad))
        c.drawString(305, y, f"${precio:.2f}")
        c.drawString(405, y, f"${subtotal:.2f}")
        y -= 15
        if y < 100:
            c.showPage()
            y = 750

    # 🔹 Línea final y total
    c.line(50, y - 5, 550, y - 5)
    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(550, y, f"TOTAL: ${total:.2f}")

    # ❤️ Mensaje final
    y -= 40
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(300, y, "¡Gracias por tu compra!")
    c.drawCentredString(300, y - 15, "Fogón EMD - Calidad y sabor en cada platillo")
    
    # 💾 Guardar PDF
    c.save()
    print(f"✅ Ticket generado correctamente: {nombre_archivo}")
