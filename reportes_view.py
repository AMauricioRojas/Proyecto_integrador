# reportes_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import os
from PIL import Image
from reporte_controller import ReporteController

class ReportesVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de Ventas - Fogón EMD")
        self.geometry("1100x700")
        
        self.parent = parent
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.controller = ReporteController()
        self.ventas_actuales = []
        self.total_actual = 0

        # Icono PDF
        try:
            path = os.path.join(os.path.dirname(__file__), "assets", "icon_pdf.png")
            self.icon_pdf = ctk.CTkImage(Image.open(path), size=(20, 20))
        except: self.icon_pdf = None

        # === HEADER ===
        frame_top = ctk.CTkFrame(self, height=80, fg_color="white") # Header blanco
        frame_top.pack(fill="x", side="top")

        frame_tit = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_tit.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(frame_tit, text="📊 Reportes Financieros", font=("Arial", 22, "bold"), text_color="#D35400").pack(anchor="w")
        ctk.CTkLabel(frame_tit, text="Historial de ventas", font=("Arial", 12), text_color="gray").pack(anchor="w")

        ctk.CTkButton(frame_top, text="🔙 Volver", fg_color="#555555", width=100, command=self.on_closing).pack(side="right", padx=20)

        # === FILTROS ===
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_filtros, text="Desde:").pack(side="left", padx=10)
        self.fecha_inicio = DateEntry(frame_filtros, width=12, background='#D35400', foreground='white', borderwidth=2, date_pattern='dd/mm/Y')
        self.fecha_inicio.pack(side="left", padx=10)

        ctk.CTkLabel(frame_filtros, text="Hasta:").pack(side="left", padx=10)
        self.fecha_fin = DateEntry(frame_filtros, width=12, background='#D35400', foreground='white', borderwidth=2, date_pattern='dd/mm/Y')
        self.fecha_fin.pack(side="left", padx=10)

        ctk.CTkLabel(frame_filtros, text="Cajero:").pack(side="left", padx=10)
        self.cajero_combo = ctk.CTkComboBox(frame_filtros, values=["Todos"], width=150)
        self.cajero_combo.pack(side="left", padx=10)
        self.cajero_combo.set("Todos")

        ctk.CTkButton(frame_filtros, text="Buscar", command=self.aplicar_filtros, width=100).pack(side="left", padx=20)
        
        ctk.CTkButton(frame_filtros, text="Exportar PDF", image=self.icon_pdf, compound="left", 
                      command=self.exportar_pdf, fg_color="#C0392B", hover_color="#922B21").pack(side="right", padx=20)

        # === TOTALES (AQUÍ ESTABA EL ERROR DEL COLOR OSCURO) ===
        # Cambiamos fg_color a un tono crema claro o blanco
        frame_sumario = ctk.CTkFrame(self, fg_color="#FAE5D3", border_color="#D35400", border_width=2)
        frame_sumario.pack(pady=5, padx=20, fill="x")

        self.total_ventas_label = ctk.CTkLabel(frame_sumario, text="Total Recaudado: $0.00", font=("Arial", 24, "bold"), text_color="#D35400")
        self.total_ventas_label.pack(side="left", padx=20, pady=15)
        
        self.num_ventas_label = ctk.CTkLabel(frame_sumario, text="Transacciones: 0", font=("Arial", 18, "bold"), text_color="#5D4037")
        self.num_ventas_label.pack(side="right", padx=20, pady=15)

        # === TABLA ===
        self.tabla = ttk.Treeview(self, columns=("ID", "Fecha", "Cajero", "Método", "Total"), show="headings", height=18)
        self.tabla.pack(padx=20, pady=10, fill="both", expand=True)

        columnas = [("ID", 60), ("Fecha", 150), ("Cajero", 200), ("Método", 120), ("Total", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.cargar_cajeros()
        self.aplicar_filtros()

    def on_closing(self):
        self.parent.deiconify()
        self.destroy()

    def cargar_cajeros(self):
        cajeros = self.controller.get_cajeros()
        lista = ["Todos"]
        self.cajeros_map = {}
        for c in cajeros:
            self.cajeros_map[c[1]] = c[0]
            lista.append(c[1])
        self.cajero_combo.configure(values=lista)

    def aplicar_filtros(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        f_ini = self.fecha_inicio.get()
        f_fin = self.fecha_fin.get()
        cajero_txt = self.cajero_combo.get()
        id_cajero = self.cajeros_map.get(cajero_txt) if cajero_txt != "Todos" else None
        
        ventas, total, num = self.controller.get_reporte_filtrado(f_ini, f_fin, id_cajero)
        self.ventas_actuales = ventas
        self.total_actual = total
        
        for v in ventas:
            fecha_str = v[1].strftime('%d/%m/%Y %H:%M')
            self.tabla.insert("", "end", values=(v[0], fecha_str, v[2], v[3], f"${v[4]:.2f}"))
            
        self.total_ventas_label.configure(text=f"Total Recaudado: ${total:,.2f}")
        self.num_ventas_label.configure(text=f"Transacciones: {num}")

    def exportar_pdf(self):
        txt_filtros = f"Del {self.fecha_inicio.get()} al {self.fecha_fin.get()} - Cajero: {self.cajero_combo.get()}"
        self.controller.exportar_pdf(self.ventas_actuales, self.total_actual, txt_filtros)