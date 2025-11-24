# ticket_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from tkinter import messagebox

def generar_reporte_pdf(ventas, total_general, filtros_texto):
    """
    Genera un reporte detallado en tamaño Carta.
    ventas: Lista de tuplas (id, fecha, cajero, metodo, total)
    """
    try:
        # Carpeta de reportes
        carpeta = "reportes_pdf"
        os.makedirs(carpeta, exist_ok=True)
        
        nombre_archivo = f"{carpeta}/Reporte_Ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        width, height = letter
        
        # --- Encabezado ---
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "Fogón EMD - Reporte de Ventas")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(50, height - 85, f"Filtros: {filtros_texto}")
        
        c.line(50, height - 100, width - 50, height - 100)
        
        # --- Tabla ---
        y = height - 130
        # Encabezados de columna
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "ID")
        c.drawString(100, y, "Fecha")
        c.drawString(250, y, "Cajero")
        c.drawString(380, y, "Método")
        c.drawString(480, y, "Total")
        
        y -= 20
        c.setFont("Helvetica", 10)
        
        for venta in ventas:
            # venta: (id, fecha_obj, nombre_cajero, metodo, total_float)
            
            if y < 50: # Si se acaba la hoja, nueva página
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            
            fecha_str = venta[1].strftime('%d/%m/%Y %H:%M') if hasattr(venta[1], 'strftime') else str(venta[1])
            
            c.drawString(50, y, str(venta[0]))
            c.drawString(100, y, fecha_str)
            c.drawString(250, y, str(venta[2]))
            c.drawString(380, y, str(venta[3]))
            c.drawString(480, y, f"${venta[4]:.2f}")
            y -= 20
            
        # --- Totales ---
        c.line(50, y - 10, width - 50, y - 10)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(350, y - 40, "TOTAL RECAUDADO:")
        c.drawString(480, y - 40, f"${total_general:.2f}")
        
        c.save()
        os.startfile(os.path.abspath(nombre_archivo)) # Abre el PDF automáticamente
        return True
        
    except Exception as e:
        print(f"Error PDF: {e}")
        return False