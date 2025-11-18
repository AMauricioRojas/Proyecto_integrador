# ventas_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from venta_controller import VentaController
from ticket_simple_view import TicketSimpleVentana


class VentasVentana(ctk.CTkToplevel):
    def __init__(self, parent, id_usuario): 
        super().__init__(parent)
        
        self.parent = parent # Guardamos la referencia
        self.id_usuario = id_usuario 
        self.title("Ventas - Fogón EMD")
        self.geometry("1200x700")
        self.state("zoomed")  

        # --- AÑADIMOS ESTA LÍNEA ---
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # -----------------------------
        
        self.controller = VentaController()
        
        # ... (El resto de tu código de __init__ no cambia) ...
        self.total = 0.0
        self.items_ticket = []  
        self.metodo_pago = ctk.StringVar(value="Efectivo")
        ctk.CTkLabel(self, text="🛒 Ventas", font=("Arial", 28, "bold")).pack(pady=10)
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        frame_derecho = ctk.CTkFrame(frame_principal, width=400)
        frame_derecho.pack(side="right", fill="y", padx=10, pady=10)
        frame_izquierdo = ctk.CTkFrame(frame_principal)
        frame_izquierdo.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frame_izquierdo, text="Productos Disponibles", font=("Arial", 20, "bold")).pack(pady=5)
        self.tabla_productos = ttk.Treeview(frame_izquierdo, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=18)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        for col, ancho in [("ID", 60), ("Nombre", 300), ("Precio", 100), ("Stock", 100)]:
            self.tabla_productos.heading(col, text=col)
            self.tabla_productos.column(col, width=ancho, anchor="center")
        scrollbar_productos = ttk.Scrollbar(frame_izquierdo, orient="vertical", command=self.tabla_productos.yview)
        scrollbar_productos.pack(side="right", fill="y")
        self.tabla_productos.configure(yscrollcommand=scrollbar_productos.set)
        ctk.CTkLabel(frame_derecho, text="Ticket Actual", font=("Arial", 20, "bold")).pack(pady=10)
        self.ticket = ttk.Treeview(frame_derecho, columns=("Producto", "Cant.", "Subtotal"), show="headings", height=10)
        self.ticket.pack(padx=10)
        for col, ancho in [("Producto", 200), ("Cant.", 60), ("Subtotal", 100)]:
            self.tabla_productos.heading(col, text=col)
            self.tabla_productos.column(col, width=ancho, anchor="center")
        ctk.CTkLabel(frame_derecho, text="Cantidad:", font=("Arial", 16)).pack(pady=(15, 0))
        self.cantidad_entry = ctk.CTkEntry(frame_derecho, placeholder_text="1", width=120, justify="center")
        self.cantidad_entry.pack(pady=5)
        self.cantidad_entry.insert(0, "1")
        ctk.CTkButton(frame_derecho, text="➕ Agregar al Ticket", command=self.agregar_ticket).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(frame_derecho, text="➖ Eliminar del Ticket", command=self.eliminar_ticket, fg_color="#D9534F").pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame_derecho, text="Método de Pago:", font=("Arial", 16)).pack(pady=(15, 0))
        metodos = ["Efectivo", "Tarjeta", "Transferencia"]
        ctk.CTkComboBox(frame_derecho, variable=self.metodo_pago, values=metodos).pack(pady=5)
        self.total_label = ctk.CTkLabel(frame_derecho, text="Total: $0.00", font=("Arial", 26, "bold"), text_color="#2ECC71")
        self.total_label.pack(pady=20)
        ctk.CTkButton(frame_derecho, text="✅ Finalizar Venta", height=50, font=("Arial", 20, "bold"), command=self.finalizar_venta).pack(fill="x", padx=20, pady=20)
        self.cargar_productos()

    # --- AÑADIMOS ESTA NUEVA FUNCIÓN ---
    def on_closing(self):
        """Se ejecuta al presionar la 'X'."""
        self.parent.deiconify() # Le dice al menú admin que reaparezca
        self.destroy() # Se destruye a sí misma
    # -----------------------------------

    def cargar_productos(self):
        for row in self.tabla_productos.get_children():
            self.tabla_productos.delete(row)
        productos = self.controller.get_productos_para_venta()
        if productos:
            for prod in productos:
                self.tabla_productos.insert("", "end", values=(
                    prod['id_producto'], 
                    prod['nombre'], 
                    prod['precio'], 
                    prod['stock']
                ))

    def actualizar_total(self):
        self.total = sum(item[3] for item in self.items_ticket)
        self.total_label.configure(text=f"Total: ${self.total:.2f}")

    def actualizar_tabla_ticket(self):
        for row in self.ticket.get_children():
            self.ticket.delete(row)
        for id_prod, nombre, cantidad, subtotal in self.items_ticket:
            self.ticket.insert("", "end", values=(nombre, cantidad, f"${subtotal:.2f}"))
        self.actualizar_total()

    def agregar_ticket(self):
        seleccionado = self.tabla_productos.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto de la lista.")
            return
        datos = self.tabla_productos.item(seleccionado)["values"]
        try:
            id_producto = int(datos[0])
            nombre = str(datos[1])
            precio = float(datos[2])
            stock_actual = int(datos[3])
            cantidad_str = self.cantidad_entry.get()
            if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
                messagebox.showwarning("Cantidad inválida", "Ingresa una cantidad válida.")
                return
            cantidad_a_agregar = int(cantidad_str)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron leer los datos del producto: {e}")
            return
        item_encontrado = False
        for i, item in enumerate(self.items_ticket):
            if item[0] == id_producto: 
                nueva_cantidad_total = item[2] + cantidad_a_agregar
                if nueva_cantidad_total > stock_actual:
                    msg = f"No hay suficiente stock.\n\nStock disponible: {stock_actual}\nYa tienes: {item[2]} en el ticket"
                    messagebox.showwarning("Sin stock", msg)
                    return
                nuevo_subtotal = item[3] + (precio * cantidad_a_agregar)
                self.items_ticket[i] = (id_producto, nombre, nueva_cantidad_total, nuevo_subtotal)
                item_encontrado = True
                break
        if not item_encontrado:
            if cantidad_a_agregar > stock_actual:
                messagebox.showwarning("Sin stock", f"No hay suficiente stock. Disponible: {stock_actual}")
                return
            subtotal = precio * cantidad_a_agregar
            self.items_ticket.append((id_producto, nombre, cantidad_a_agregar, subtotal))
        self.actualizar_tabla_ticket() 
        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, "1")

    def eliminar_ticket(self):
        seleccionado = self.ticket.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto del ticket para eliminar.")
            return
        try:
            indice_seleccionado = self.ticket.index(seleccionado)
            self.items_ticket.pop(indice_seleccionado)
            self.actualizar_tabla_ticket()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {e}")
    
    def finalizar_venta(self):
        success, id_venta, productos_para_ticket = self.controller.finalizar_venta(
            self.items_ticket, 
            self.total, 
            self.metodo_pago.get(), 
            self.id_usuario
        )
        if success:
            TicketSimpleVentana(self, id_venta, productos_para_ticket, self.total, self.metodo_pago.get())
            self.ticket.delete(*self.ticket.get_children())
            self.items_ticket.clear()
            self.actualizar_total()
            self.cargar_productos()