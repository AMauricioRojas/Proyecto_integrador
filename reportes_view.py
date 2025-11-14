# reportes_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
# --- IMPORTAMOS EL NUEVO CONTROLADOR ---
from reporte_controller import ReporteController

class ReportesVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de Ventas - Fogón EMD")
        self.geometry("1100x700")
        
        self.transient(parent)
        self.grab_set()

        # --- CREAMOS LA INSTANCIA DEL CONTROLADOR ---
        self.controller = ReporteController()
        
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

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.cargar_cajeros()
        self.aplicar_filtros() # Carga inicial

    def cargar_cajeros(self):
        """Pide los cajeros al controlador y los carga en el ComboBox."""
        # 1. Pide los cajeros
        cajeros = self.controller.get_cajeros()
        
        # 2. Los procesa
        lista_cajeros = ["Todos"]
        self.cajeros_map = {} # Limpiamos el mapa
        
        for cajero in cajeros:
            self.cajeros_map[cajero['nombre']] = cajero['id_usuario']
            lista_cajeros.append(cajero['nombre'])
            
        self.cajero_combo.configure(values=lista_cajeros)

    def aplicar_filtros(self):
        """Función "tonta" de la vista. Pasa los filtros al controlador."""
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # 1. Recolecta datos de la vista
        fecha_ini = self.fecha_inicio.get()
        fecha_fin = self.fecha_fin.get()
        
        cajero_seleccionado = self.cajero_combo.get()
        id_cajero = None
        if cajero_seleccionado != "Todos":
            id_cajero = self.cajeros_map.get(cajero_seleccionado)

        # 2. Pide al controlador que haga el trabajo
        ventas, total_recaudado, num_ventas = self.controller.get_reporte_filtrado(
            fecha_ini, fecha_fin, id_cajero
        )

        # 3. Muestra los resultados que el controlador le devolvió
        for venta in ventas:
            self.tabla.insert("", "end", values=(
                venta['id_venta'],
                venta['fecha'].strftime('%Y-%m-%d %H:%M:%S'),
                venta['nombre'] if venta['nombre'] else "N/A",
                venta['metodo_pago'],
                f"${venta['total']:.2f}"
            ))
        
        self.total_ventas_label.configure(text=f"Total Recaudado: ${total_recaudado:.2f}")
        self.num_ventas_label.configure(text=f"Nº de Ventas: {num_ventas}")

    def limpiar_filtros(self):
        self.cajero_combo.set("Todos")
        self.fecha_inicio.set_date(datetime.now())
        self.fecha_fin.set_date(datetime.now())
        self.aplicar_filtros()