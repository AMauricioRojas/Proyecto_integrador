# ventas_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from db import conectar
from datetime import datetime
from ticket_final_view import TicketFinalVentana


class VentasVentana(ctk.CTkToplevel):
    def __init__(self, parent, id_usuario): # Aceptamos el id_usuario
        super().__init__(parent)
        self.id_usuario = id_usuario # Lo guardamos
        self.title("Ventas - Fogón EMD")
        self.geometry("1200x700")
        self.state("zoomed")  # Pantalla completa

        self.conexion = conectar()
        self.cursor = self.conexion.cursor()

        # Variables principales
        self.total = 0.0
        self.items_ticket = []  # [(id_producto, nombre, cantidad, subtotal)]
        self.metodo_pago = ctk.StringVar(value="Efectivo")

        # Título
        ctk.CTkLabel(self, text="🛒 Ventas", font=("Arial", 28, "bold")).pack(pady=10)

        # ==========================================================
        # === CORRECCIÓN DE LAYOUT ===
        # ==========================================================
        
        # Marco principal que contendrá ambos paneles
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Panel Derecho (Ticket y Acciones) ---
        # Lo creamos y empaquetamos PRIMERO, con side="right"
        # Su padre ahora es 'frame_principal'
        frame_derecho = ctk.CTkFrame(frame_principal, width=400)
        frame_derecho.pack(side="right", fill="y", padx=10, pady=10)

        # --- Panel Izquierdo (Productos) ---
        # Ocupará el resto del espacio
        frame_izquierdo = ctk.CTkFrame(frame_principal)
        frame_izquierdo.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # ==========================================================
        # === FIN DE CORRECCIÓN DE LAYOUT ===
        # ==========================================================
        
        # --- Contenido del Panel Izquierdo ---
        ctk.CTkLabel(frame_izquierdo, text="Productos Disponibles", font=("Arial", 20, "bold")).pack(pady=5)
        self.tabla_productos = ttk.Treeview(
            frame_izquierdo, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=18
        )
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        for col, ancho in [("ID", 60), ("Nombre", 300), ("Precio", 100), ("Stock", 100)]:
            self.tabla_productos.heading(col, text=col)
            self.tabla_productos.column(col, width=ancho, anchor="center")

        # Scrollbar para productos
        scrollbar_productos = ttk.Scrollbar(frame_izquierdo, orient="vertical", command=self.tabla_productos.yview)
        scrollbar_productos.pack(side="right", fill="y")
        self.tabla_productos.configure(yscrollcommand=scrollbar_productos.set)

        self.cargar_productos()

        # --- Contenido del Panel Derecho ---
        ctk.CTkLabel(frame_derecho, text="Ticket Actual", font=("Arial", 20, "bold")).pack(pady=10)

        # Ticket (productos seleccionados)
        self.ticket = ttk.Treeview(
            frame_derecho, columns=("Producto", "Cant.", "Subtotal"), show="headings", height=10
        )
        self.ticket.pack(padx=10)
        for col, ancho in [("Producto", 200), ("Cant.", 60), ("Subtotal", 100)]:
            self.ticket.heading(col, text=col)
            self.ticket.column(col, width=ancho, anchor="center")

        ctk.CTkLabel(frame_derecho, text="Cantidad:", font=("Arial", 16)).pack(pady=(15, 0))
        self.cantidad_entry = ctk.CTkEntry(frame_derecho, placeholder_text="1", width=120, justify="center")
        self.cantidad_entry.pack(pady=5)
        self.cantidad_entry.insert(0, "1")

        ctk.CTkButton(frame_derecho, text="➕ Agregar al Ticket", command=self.agregar_ticket).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(frame_derecho, text="➖ Eliminar del Ticket", command=self.eliminar_ticket, fg_color="#D9534F").pack(fill="x", padx=20, pady=5)

        # Método de pago
        ctk.CTkLabel(frame_derecho, text="Método de Pago:", font=("Arial", 16)).pack(pady=(15, 0))
        metodos = ["Efectivo", "Tarjeta", "Transferencia"]
        ctk.CTkComboBox(frame_derecho, variable=self.metodo_pago, values=metodos).pack(pady=5)

        # Total
        self.total_label = ctk.CTkLabel(frame_derecho, text="Total: $0.00", font=("Arial", 26, "bold"), text_color="#2ECC71")
        self.total_label.pack(pady=20)

        # --- ¡AQUÍ ESTÁ EL BOTÓN! ---
        # Ahora debería ser visible dentro del frame_derecho
        ctk.CTkButton(frame_derecho, text="✅ Finalizar Venta", height=50, font=("Arial", 20, "bold"), command=self.finalizar_venta).pack(fill="x", padx=20, pady=20)


    def cargar_productos(self):
        """Carga los productos desde la base de datos"""
        for row in self.tabla_productos.get_children():
            self.tabla_productos.delete(row)
        try:
            self.cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE stock > 0")
            for prod in self.cursor.fetchall():
                self.tabla_productos.insert("", "end", values=prod)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")

    def actualizar_total(self):
        """Calcula el total desde la lista y actualiza la etiqueta"""
        self.total = sum(item[3] for item in self.items_ticket)
        self.total_label.configure(text=f"Total: ${self.total:.2f}")

    def agregar_ticket(self):
        """Agrega el producto seleccionado al ticket"""
        seleccionado = self.tabla_productos.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto de la lista.")
            return

        cantidad_str = self.cantidad_entry.get()
        if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
            messagebox.showwarning("Cantidad inválida", "Ingresa una cantidad válida.")
            return
        
        datos = self.tabla_productos.item(seleccionado)["values"]
        
        try:
            id_producto = int(datos[0])
            nombre = str(datos[1])
            precio = float(datos[2])
            stock_actual = int(datos[3])
            cantidad = int(cantidad_str)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron leer los datos del producto: {e}")
            return
        
        if cantidad > stock_actual:
            messagebox.showwarning("Sin stock", f"No hay suficiente stock. Disponible: {stock_actual}")
            return

        subtotal = precio * cantidad

        # AÑADIMOS DATOS AL TICKET
        # [(id_producto, nombre, cantidad, subtotal)]
        self.items_ticket.append((id_producto, nombre, cantidad, subtotal))

        # Mostramos en la tabla
        self.ticket.insert("", "end", values=(nombre, cantidad, f"${subtotal:.2f}"))

        self.actualizar_total()
        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, "1")

    def eliminar_ticket(self):
        """Elimina un producto del ticket y de la lista interna"""
        seleccionado = self.ticket.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto del ticket para eliminar.")
            return

        # Obtenemos el índice del ítem seleccionado en la tabla visual
        try:
            indice_seleccionado = self.ticket.index(seleccionado)
            
            # Eliminamos el ítem de nuestra lista de datos (self.items_ticket)
            self.items_ticket.pop(indice_seleccionado)
            
            # Finalmente, borramos de la tabla visual
            self.ticket.delete(seleccionado)
            
            # Recalculamos el total
            self.actualizar_total()

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al intentar eliminar el producto: {e}")


    def finalizar_venta(self):
        """Guarda la venta y actualiza el inventario"""
        if not self.items_ticket:
            messagebox.showwarning("Vacío", "No hay productos en el ticket.")
            return

        try:
            # Insertar venta
            self.cursor.execute(
                "INSERT INTO ventas (fecha, total, metodo_pago, id_usuario) VALUES (%s, %s, %s, %s)",
                (datetime.now(), self.total, self.metodo_pago.get(), self.id_usuario), # Pasamos el ID
            )
            id_venta = self.cursor.lastrowid

            # Insertar detalle y actualizar stock
            for id_prod, nombre, cantidad, subtotal in self.items_ticket:
                self.cursor.execute(
                    "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                    (id_venta, id_prod, cantidad, subtotal),
                )
                self.cursor.execute(
                    "UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                    (cantidad, id_prod),
                )

            self.conexion.commit()

            # ✅ Mostrar ticket final
            TicketFinalVentana(self, id_venta, self.items_ticket, self.total, self.metodo_pago.get())

            # Reiniciar la venta actual sin cerrar la ventana
            self.ticket.delete(*self.ticket.get_children())
            self.items_ticket.clear()
            self.actualizar_total()
            self.cargar_productos() # Recargamos productos por si el stock llegó a 0

        except Exception as e:
            self.conexion.rollback()
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")