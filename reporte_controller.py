# reporte_controller.py
from db import conectar
from tkinter import messagebox
from datetime import datetime
import ticket_pdf # Importamos nuestra herramienta de PDF

class ReporteController:

    def __init__(self):
        self.conexion = conectar()
        if self.conexion:
            self.cursor = self.conexion.cursor()
        else:
            self.cursor = None

    def get_cajeros(self):
        """Obtiene lista de cajeros para el filtro"""
        if not self.cursor: return []
        try:
            self.cursor.execute("SELECT id_usuario, nombre FROM usuarios ORDER BY nombre")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cajeros: {e}")
            return []

    def get_reporte_filtrado(self, fecha_ini_str, fecha_fin_str, id_cajero):
        """Consulta la BD y devuelve las ventas filtradas"""
        if not self.cursor: return [], 0, 0
            
        try:
            query = """
                SELECT v.id_venta, v.fecha, u.nombre, v.metodo_pago, v.total 
                FROM ventas v
                LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            """
            condiciones = []
            parametros = []
            
            # Filtro Fechas
            f_ini = datetime.strptime(fecha_ini_str, '%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
            f_fin = datetime.strptime(fecha_fin_str, '%d/%m/%Y').strftime('%Y-%m-%d 23:59:59')
            condiciones.append("v.fecha BETWEEN %s AND %s")
            parametros.extend([f_ini, f_fin])
            
            # Filtro Cajero
            if id_cajero is not None:
                condiciones.append("v.id_usuario = %s")
                parametros.append(id_cajero)

            if condiciones:
                query += " WHERE " + " AND ".join(condiciones)

            query += " ORDER BY v.fecha DESC"
            
            self.cursor.execute(query, tuple(parametros))
            ventas = self.cursor.fetchall()
            
            total = sum(v[4] for v in ventas) # v[4] es el total
            num = len(ventas)
            
            return ventas, total, num

        except Exception as e:
            messagebox.showerror("Error", f"Error en reporte: {e}")
            return [], 0, 0

    def exportar_pdf(self, ventas, total, filtros_info):
        """Llama a ticket_pdf.py para generar el archivo"""
        if not ventas:
            messagebox.showwarning("Vacío", "No hay datos para exportar.")
            return
        
        exito = ticket_pdf.generar_reporte_pdf(ventas, total, filtros_info)
        
        if exito:
            messagebox.showinfo("Éxito", "PDF generado y abierto correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo generar el PDF.")