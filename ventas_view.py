# ventas_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
import os
from PIL import Image 
from venta_controller import VentaController
from ticket_simple_view import TicketSimpleVentana

class VentasVentana(ctk.CTkToplevel):
    def __init__(self, parent, id_usuario): 
        super().__init__(parent)
        self.parent = parent 
        self.id_usuario = id_usuario 
        self.title("Ventas - Fogón EMD")
        self.geometry("1200x700")
        self.state("zoomed")  
        
        # --- SALSEO: Fondo Crema ---
        self.configure(fg_color="#FFF6F3") 

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.controller = VentaController()
        self.total = 0.0
        self.items_ticket = []  
        self.metodo_pago = ctk.StringVar(value="Efectivo")
        self.lista_productos_completa = []

        # HEADER (Blanco)
        frame_header = ctk.CTkFrame(self, height=80, fg_color="white", corner_radius=0)
        frame_header.pack(fill="x", side="top")

        # Logo
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
            img = Image.open(ruta_logo)
            self.logo_small = ctk.CTkImage(light_image=img, dark_image=img, size=(50, 50))
            ctk.CTkLabel(frame_header, image=self.logo_small, text="").pack(side="left", padx=20, pady=10)
        except: pass

        # Titulos
        frame_titulos = ctk.CTkFrame(frame_header, fg_color="transparent")
        frame_titulos.pack(side="left", padx=10)
        ctk.CTkLabel(frame_titulos, text="Punto de Venta", font=("Arial", 22, "bold"), text_color="#D35400").pack(anchor="w")
        
        ctk.CTkButton(frame_header, text="🔙 Menú Principal", fg_color="transparent", border_width=1, border_color="#555", text_color="#555", hover_color="#EEE",
                      command=self.on_closing).pack(side="right", padx=20)

        # CUERPO
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=15, pady=15)

        # PANEL IZQUIERDO (Productos)
        frame_izquierdo = ctk.CTkFrame(frame_principal, fg_color="white", corner_radius=15) # Tarjeta blanca
        frame_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Buscador
        frame_bus = ctk.CTkFrame(frame_izquierdo, fg_color="transparent")
        frame_bus.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(frame_bus, text="🔍 Buscar:", text_color="gray", font=("Arial", 14, "bold")).pack(side="left")
        self.entry_busqueda = ctk.CTkEntry(frame_bus, placeholder_text="Escribe para filtrar...", height=40, font=("Arial", 16), border_color="#D35400")
        self.entry_busqueda.pack(side="left", fill="x", expand=True, padx=10)
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_productos)

        # Tabla
        self.tabla_productos = ttk.Treeview(frame_izquierdo, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=18)
        self.tabla_productos.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))
        
        for col, ancho in [("ID", 50), ("Nombre", 350), ("Precio", 100), ("Stock", 80)]:
            self.tabla_productos.heading(col, text=col)
            self.tabla_productos.column(col, width=ancho, anchor="center")
            
        scrollbar_productos = ttk.Scrollbar(frame_izquierdo, orient="vertical", command=self.tabla_productos.yview)
        scrollbar_productos.pack(side="right", fill="y", pady=(0, 15))
        self.tabla_productos.configure(yscrollcommand=scrollbar_productos.set)
        self.tabla_productos.bind("<Double-1>", lambda e: self.agregar_ticket())

        # PANEL DERECHO (Ticket)
        frame_derecho = ctk.CTkFrame(frame_principal, width=450, fg_color="white", corner_radius=15) # Tarjeta blanca
        frame_derecho.pack(side="right", fill="y", padx=0)

        # Cabecera Ticket
        frame_ticket_header = ctk.CTkFrame(frame_derecho, fg_color="#D35400", corner_radius=0, height=50)
        frame_ticket_header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(frame_ticket_header, text="Ticket de Venta", font=("Arial", 18, "bold"), text_color="white").pack(pady=10)
        
        self.ticket = ttk.Treeview(frame_derecho, columns=("Producto", "Cant.", "Subtotal"), show="headings", height=12)
        self.ticket.pack(padx=15, fill="both", expand=True)
        for col, ancho in [("Producto", 200), ("Cant.", 60), ("Subtotal", 100)]:
            self.ticket.heading(col, text=col)
            self.ticket.column(col, width=ancho, anchor="center")
        
        # Controles
        frame_controles = ctk.CTkFrame(frame_derecho, fg_color="transparent")
        frame_controles.pack(fill="x", padx=15, pady=10)
        
        self.cantidad_entry = ctk.CTkEntry(frame_controles, placeholder_text="1", width=60, justify="center", font=("Arial", 14))
        self.cantidad_entry.pack(side="left")
        self.cantidad_entry.insert(0, "1")
        
        ctk.CTkButton(frame_controles, text="➕", width=50, command=self.agregar_ticket, fg_color="#28a745").pack(side="left", padx=5)
        ctk.CTkButton(frame_controles, text="🗑️", width=50, command=self.eliminar_ticket, fg_color="#dc3545").pack(side="left", padx=5)
        
        metodos = ["Efectivo", "Tarjeta", "Transferencia"]
        ctk.CTkComboBox(frame_controles, variable=self.metodo_pago, values=metodos, width=150).pack(side="right")

        # Total y Botón
        frame_total = ctk.CTkFrame(frame_derecho, fg_color="#FFF6F3", border_color="#D35400", border_width=2)
        frame_total.pack(fill="x", padx=15, pady=10)
        self.total_label = ctk.CTkLabel(frame_total, text="$0.00", font=("Arial", 36, "bold"), text_color="#D35400")
        self.total_label.pack(pady=10)
        
        ctk.CTkButton(frame_derecho, text="COBRAR (F5)", height=60, font=("Arial", 18, "bold"), 
                      fg_color="#D35400", hover_color="#A04000", 
                      command=self.finalizar_venta).pack(fill="x", padx=15, pady=(0, 15))
        
        self.cargar_productos()

    # ... (El resto de funciones: on_closing, cargar_productos, filtrar, etc. son IGUALES al código anterior) ...
    # Copia las funciones lógicas del código anterior aquí abajo.
    # Si quieres te paso el archivo completo para que no haya errores de copiado.
    
    def on_closing(self):
        self.parent.deiconify() 
        self.destroy() 

    def cargar_productos(self):
        for row in self.tabla_productos.get_children():
            self.tabla_productos.delete(row)
        datos = self.controller.get_productos_para_venta()
        self.lista_productos_completa = datos 
        self.actualizar_tabla_productos(datos)

    def actualizar_tabla_productos(self, lista):
        for row in self.tabla_productos.get_children():
            self.tabla_productos.delete(row)
        if lista:
            for prod in lista:
                self.tabla_productos.insert("", "end", values=(prod[0], prod[1], f"${prod[2]}", prod[3]))

    def filtrar_productos(self, event=None):
        texto = self.entry_busqueda.get().lower()
        if texto == "":
            self.actualizar_tabla_productos(self.lista_productos_completa)
        else:
            lista_filtrada = []
            for prod in self.lista_productos_completa:
                nombre_prod = str(prod[1]).lower()
                if texto in nombre_prod:
                    lista_filtrada.append(prod)
            self.actualizar_tabla_productos(lista_filtrada)

    def actualizar_total(self):
        self.total = sum(item[3] for item in self.items_ticket)
        self.total_label.configure(text=f"${self.total:.2f}")

    def actualizar_tabla_ticket(self):
        for row in self.ticket.get_children():
            self.ticket.delete(row)
        for id_prod, nombre, cantidad, subtotal in self.items_ticket:
            self.ticket.insert("", "end", values=(nombre, cantidad, f"${subtotal:.2f}"))
        self.actualizar_total()

    def agregar_ticket(self):
        seleccionado = self.tabla_productos.selection()
        if not seleccionado: return
        datos = self.tabla_productos.item(seleccionado)["values"]
        try:
            id_producto = int(datos[0])
            nombre = str(datos[1])
            precio_str = str(datos[2]).replace("$", "")
            precio = float(precio_str)
            stock_actual = int(datos[3])
            cantidad_str = self.cantidad_entry.get()
            if not cantidad_str.isdigit() or int(cantidad_str) <= 0: return
            cantidad_a_agregar = int(cantidad_str)
        except: return
            
        item_encontrado = False
        for i, item in enumerate(self.items_ticket):
            if item[0] == id_producto: 
                nueva_cantidad_total = item[2] + cantidad_a_agregar
                if nueva_cantidad_total > stock_actual:
                    messagebox.showwarning("Sin stock", "Stock insuficiente")
                    return
                nuevo_subtotal = item[3] + (precio * cantidad_a_agregar)
                self.items_ticket[i] = (id_producto, nombre, nueva_cantidad_total, nuevo_subtotal)
                item_encontrado = True
                break
        
        if not item_encontrado:
            if cantidad_a_agregar > stock_actual:
                messagebox.showwarning("Sin stock", "Stock insuficiente")
                return
            subtotal = precio * cantidad_a_agregar
            self.items_ticket.append((id_producto, nombre, cantidad_a_agregar, subtotal))
            
        self.actualizar_tabla_ticket() 
        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, "1")
        self.entry_busqueda.delete(0, "end")
        self.entry_busqueda.focus()

    def eliminar_ticket(self):
        seleccionado = self.ticket.selection()
        if not seleccionado: return
        try:
            indice_seleccionado = self.ticket.index(seleccionado)
            self.items_ticket.pop(indice_seleccionado)
            self.actualizar_tabla_ticket()
        except: pass
    
    def finalizar_venta(self):
        success, id_venta, productos_para_ticket = self.controller.finalizar_venta(
            self.items_ticket, self.total, self.metodo_pago.get(), self.id_usuario
        )
        if success:
            TicketSimpleVentana(self, id_venta, productos_para_ticket, self.total, self.metodo_pago.get())
            self.ticket.delete(*self.ticket.get_children())
            self.items_ticket.clear()
            self.actualizar_total()
            self.cargar_productos()
            self.entry_busqueda.focus()