# reporte_controller.py
from db import conectar
from tkinter import messagebox
from datetime import datetime

class ReporteController:

    def __init__(self):
        try:
            self.conexion = conectar()
            # Usamos dictionary=True para que la vista reciba los datos por nombre
            self.cursor = self.conexion.cursor(dictionary=True)
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{e}")
            self.cursor = None

    def get_cajeros(self):
        """Obtiene la lista de usuarios para el filtro."""
        if not self.cursor:
            return []
        try:
            self.cursor.execute("SELECT id_usuario, nombre FROM usuarios ORDER BY nombre")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los cajeros:\n{e}")
            return []

    def get_reporte_filtrado(self, fecha_ini_str, fecha_fin_str, id_cajero):
        """
        Construye y ejecuta la consulta de reporte con filtros.
        Retorna (lista_de_ventas, total_recaudado, num_ventas)
        """
        if not self.cursor:
            return [], 0, 0
            
        try:
            # --- Construcción de la consulta ---
            query = """
                SELECT v.id_venta, v.fecha, u.nombre, v.metodo_pago, v.total 
                FROM ventas v
                LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            """
            
            condiciones = []
            parametros = []
            
            # 1. Filtro de Fecha (siempre se aplica)
            fecha_ini_sql = datetime.strptime(fecha_ini_str, '%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
            fecha_fin_sql = datetime.strptime(fecha_fin_str, '%d/%m/%Y').strftime('%Y-%m-%d 23:59:59')
            
            condiciones.append("v.fecha BETWEEN %s AND %s")
            parametros.extend([fecha_ini_sql, fecha_fin_sql])
            
            # 2. Filtro de Cajero (opcional)
            if id_cajero is not None:
                condiciones.append("v.id_usuario = %s")
                parametros.append(id_cajero)

            # Unimos las condiciones
            if condiciones:
                query += " WHERE " + " AND ".join(condiciones)

            query += " ORDER BY v.fecha DESC"
            
            # --- Ejecución de la consulta ---
            self.cursor.execute(query, tuple(parametros))
            ventas = self.cursor.fetchall()
            
            # --- Cálculo de totales ---
            total_recaudado = sum(venta['total'] for venta in ventas)
            num_ventas = len(ventas)
            
            return ventas, total_recaudado, num_ventas

        except Exception as e:
            messagebox.showerror("Error de Consulta", f"No se pudo filtrar el reporte:\n{e}")
            return [], 0, 0