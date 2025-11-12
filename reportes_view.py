# reportes_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from db import conectar
from tkcalendar import DateEntry # La nueva librería
from datetime import datetime

class ReportesVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de Ventas - Fogón EMD")
        self.geometry("1100x700")
        
        self.transient(parent)
        self.grab_set()

        self.conexion = conectar()
        self.cursor = self.conexion.cursor(dictionary=True) # dictionary=True es clave
        
        self.cajeros_map = {} # Para mapear Nombre -> ID

        # === Frame de Filtros ===
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_filtros, text="Desde:").grid(row=0, column=0, padx=5, pady=10)
        self.fecha_inicio = DateEntry(frame_filtros, width=12, background='darkblue',
                                      foreground='white', borderwidth=2, date_pattern='dd/mm/Y')
        self.fecha_inicio.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(frame_filtros, text="Hasta:").grid(row=0, column=2, padx=5)
        self.fecha_fin = DateEntry(frame_filtros, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='dd/mm/Y')
        self.fecha_fin.grid(row=0, column=3, padx=5)

        ctk.CTkLabel(frame_filtros, text="Cajero:").grid(row=0, column=4, padx=5)
        self.cajero_combo = ctk.CTkComboBox(frame_filtros, values=["Todos"])
        self.cajero_combo.grid(row=0, column=5, padx=5)
        self.cajero_combo.set("Todos")

        ctk.CTkButton(frame_filtros, text="🔍 Filtrar", command=self.aplicar_filtros).grid(row=0, column=6, padx=10)
        ctk.CTkButton(frame_filtros, text="Limpiar", fg_color="gray", command=self.limpiar_filtros).grid(row=0, column=7, padx=5)

        # === Frame de Sumario (Totales) ===
        frame_sumario = ctk.CTkFrame(self, fg_color="#333333")
        frame_sumario.pack(pady=10, padx=20, fill="x")

        self.total_ventas_label = ctk.CTkLabel(frame_sumario, text="Total Recaudado: $0.00", font=("Arial", 18, "bold"))
        self.total_ventas_label.pack(side="left", padx=20, pady=10)
        
        self.num_ventas_label = ctk.CTkLabel(frame_sumario, text="Nº de Ventas: 0", font=("Arial", 18, "bold"))
        self.num_ventas_label.pack(side="right", padx=20, pady=10)

        # === Tabla de Reportes ===
        self.tabla = ttk.Treeview(self, columns=("ID Venta", "Fecha", "Cajero", "Método Pago", "Total"), show="headings", height=20)
        self.tabla.pack(padx=20, pady=10, fill="both", expand=True)

        columnas = [("ID Venta", 80), ("Fecha", 150), ("Cajero", 200), ("Método Pago", 120), ("Total", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.cargar_cajeros()
        self.aplicar_filtros() # Carga inicial

    def cargar_cajeros(self):
        try:
            self.cursor.execute("SELECT id_usuario, nombre FROM usuarios")
            cajeros = self.cursor.fetchall()
            
            lista_cajeros = ["Todos"]
            for cajero in cajeros:
                self.cajeros_map[cajero['nombre']] = cajero['id_usuario']
                lista_cajeros.append(cajero['nombre'])
                
            self.cajero_combo.configure(values=lista_cajeros)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los cajeros:\n{e}", parent=self)

    def aplicar_filtros(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Construcción de la consulta SQL dinámica
        query = """
            SELECT v.id_venta, v.fecha, u.nombre, v.metodo_pago, v.total 
            FROM ventas v
            LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
        """
        
        condiciones = []
        parametros = []
        
        # 1. Filtro de Fecha
        # Convertimos la fecha de DateEntry (ej. 07/11/2025) a formato SQL (2025-11-07)
        fecha_ini_obj = datetime.strptime(self.fecha_inicio.get(), '%d/%m/%Y')
        fecha_fin_obj = datetime.strptime(self.fecha_fin.get(), '%d/%m/%Y')
        
        # Ajustamos para que incluya todo el día
        fecha_ini_sql = fecha_ini_obj.strftime('%Y-%m-%d 00:00:00')
        fecha_fin_sql = fecha_fin_obj.strftime('%Y-%m-%d 23:59:59')

        condiciones.append("v.fecha BETWEEN %s AND %s")
        parametros.extend([fecha_ini_sql, fecha_fin_sql])
        
        # 2. Filtro de Cajero
        cajero_seleccionado = self.cajero_combo.get()
        if cajero_seleccionado != "Todos":
            id_cajero = self.cajeros_map.get(cajero_seleccionado)
            if id_cajero:
                condiciones.append("v.id_usuario = %s")
                parametros.append(id_cajero)

        # Unimos las condiciones
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        query += " ORDER BY v.fecha DESC"
        
        # Ejecutamos
        try:
            self.cursor.execute(query, tuple(parametros))
            ventas = self.cursor.fetchall()
            
            total_recaudado = 0
            num_ventas = 0
            
            for venta in ventas:
                self.tabla.insert("", "end", values=(
                    venta['id_venta'],
                    venta['fecha'].strftime('%Y-%m-%d %H:%M:%S'), # Formateamos fecha
                    venta['nombre'] if venta['nombre'] else "N/A",
                    venta['metodo_pago'],
                    f"${venta['total']:.2f}"
                ))
                total_recaudado += venta['total']
                num_ventas += 1
            
            # Actualizar sumario
            self.total_ventas_label.configure(text=f"Total Recaudado: ${total_recaudado:.2f}")
            self.num_ventas_label.configure(text=f"Nº de Ventas: {num_ventas}")

        except Exception as e:
            messagebox.showerror("Error de Consulta", f"No se pudo filtrar el reporte:\n{e}", parent=self)

    def limpiar_filtros(self):
        self.cajero_combo.set("Todos")
        # Reseteamos las fechas a hoy
        self.fecha_inicio.set_date(datetime.now())
        self.fecha_fin.set_date(datetime.now())
        
        self.aplicar_filtros()