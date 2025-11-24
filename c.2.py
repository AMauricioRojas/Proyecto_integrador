import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import ttk # Importamos ttk para el Treeview (tablas)

# --- CONFIGURACIÓN DE PANTALLAS ---

# La clase principal que maneja el cambio de pantallas
class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Sistema de Caja - Fogón del Menudo")
        self.geometry("1440x1024")
        self.configure(bg='#FAA18F')
        
        # Configuración de fuentes (accesibles globalmente) - **DEFINIR PRIMERO**
        self.fonts = {
            "inter_italic_20": tkfont.Font(family="Inter", size=20, slant="italic"),
            "inter_bold_48": tkfont.Font(family="Inter", size=48, weight="bold"), 
            "crimson_90": tkfont.Font(family="Crimson Text", size=90, slant="italic"),
            "inter_italic_24": tkfont.Font(family="Inter", size=24, slant="italic"),
            "inter_italic_32": tkfont.Font(family="Inter", size=32, slant="italic"),
            "inter_normal_24": tkfont.Font(family="Inter", size=24, weight="normal"),
            "inter_10": tkfont.Font(family="Inter", size=10, slant="italic"),
            "inter_64_italic": tkfont.Font(family="Inter", size=64, slant="italic")
        }

        # Contenedor principal donde se apilan las vistas
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Inicializar todas las páginas
        for F in (LoginApp, CajeroApp, VentasApp):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Empezar con la página de Login
        self.show_frame("LoginApp")

    def show_frame(self, page_name):
        '''Muestra un frame específico para el nombre de página dado'''
        frame = self.frames[page_name]
        frame.tkraise()


# --- CLASE LOGIN (LoginApp) ---

class LoginApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#FAA18F", width=1440, height=1024)

        # Configuramos un frame central para la vista de login (más pequeño)
        login_frame = tk.Frame(self, bg="#FAA18F", width=500, height=450)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        titulo = tk.Label(
            login_frame,
            text="Inicia sesión",
            font=("Inter", 28, "bold"),
            bg="#FAA18F",
            fg="#013D5B"
        )
        titulo.pack(pady=30)

        # --- Campo de usuario ---
        frame_usuario = tk.Frame(login_frame, bg="#FAA18F")
        frame_usuario.pack(pady=10)

        label_usuario = tk.Label(frame_usuario, text="Usuario:", font=("Inter", 14, "italic"), bg="#FAA18F")
        label_usuario.pack(side="left", padx=5)

        self.entry_usuario = tk.Entry(frame_usuario, width=25, bg="#F87C63", relief="solid", borderwidth=1)
        self.entry_usuario.pack(side="left", padx=5)

        # --- Campo de contraseña ---
        frame_contra = tk.Frame(login_frame, bg="#FAA18F")
        frame_contra.pack(pady=10)

        label_contra = tk.Label(frame_contra, text="Contraseña:", font=("Inter", 14, "italic"), bg="#FAA18F")
        label_contra.pack(side="left", padx=5)

        self.entry_contrasena = tk.Entry(frame_contra, width=25, show="*", bg="#F87C63", relief="solid", borderwidth=1)
        self.entry_contrasena.pack(side="left", padx=5)

        # --- Botón iniciar sesión ---
        btn_iniciar = tk.Button(
            login_frame,
            text="Iniciar sesión",
            font=("Inter", 14, "italic"),
            bg="#F87C63",
            fg="black",
            relief="raised",
            borderwidth=2,
            command=self.iniciar_sesion
        )
        btn_iniciar.pack(pady=30, ipadx=10, ipady=5)

        # --- Pie de página ---
        pie = tk.Label(
            self, # Usamos 'self' para que cubra todo el ancho inferior del frame principal
            text="Fogón del Menudo © 2025",
            font=("Inter", 10, "italic"),
            bg="#013D5B",
            fg="white",
            height=2
        )
        pie.pack(side="bottom", fill="x")


    def iniciar_sesion(self):
        """Valida las credenciales y lanza la aplicación principal."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        
        # Credenciales de prueba
        if usuario == "admin" and contrasena == "1234":
            # Si el login es exitoso, vamos al menú principal
            self.controller.show_frame("CajeroApp")
        else:
            messagebox.showerror("Error de Sesión", "Usuario o contraseña incorrectos")


# --- CLASE MENÚ PRINCIPAL (CajeroApp) ---

class CajeroApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#FAA18F', width=1440, height=1024)

        self.create_widgets()

    def create_widgets(self):
        # Referencias a las fuentes
        f = self.controller.fonts

        # --- Barra Superior (Encabezado Azul Oscuro) ---
        header_frame = tk.Frame(self, bg='#013D5B', height=164)
        header_frame.place(x=0, y=0, width=1440, height=164)
        header_frame.lower() # Aseguramos que el frame azul vaya detrás del logo

        # --- Título Principal ---
        title_label = tk.Label(
            self,
            text="Fogón EMD Cajero",
            font=f["inter_bold_48"],
            fg='#013D5B',
            bg='#FAA18F',
            bd=1, relief="solid"
        )
        title_label.place(x=426, y=180)

        # --- Logo ---
        # 1. Etiqueta "FM" (Initials)
        fm_label = tk.Label(
            self, text="FM", font=f["crimson_90"], fg='#013D5B', bg='#FAA18F'
        )
        fm_label.place(x=1170, y=44, width=110, height=117)
        fm_label.lift() 
        
        # 2. Etiqueta "Fogon del Menudo" (Full Text)
        fogon_label = tk.Label(
            self, 
            text="Fogon del Menudo", 
            font=f["inter_italic_24"], 
            fg='#000000', 
            bg='#FAA18F'
        )
        # Ajustamos y y height para evitar recorte (Corrección)
        fogon_label.place(x=1119, y=140, width=212, height=35) 
        fogon_label.lift()

        # --- Botones Principales ---
        button_width = 462
        button_height = 50
        button_x = 456
        bg_color = '#F87C63'
        
        # Helper para crear botones
        def create_menu_button(text, y_pos, command_func):
            btn = tk.Button(
                self,
                text=text,
                font=f["inter_italic_20"],
                bg=bg_color,
                fg='#000000',
                bd=1, relief="raised", 
                cursor="hand2",
                command=command_func
            )
            btn.place(x=button_x, y=y_pos, width=button_width, height=button_height)
            return btn
            
        # Función para navegar a la pantalla de Ventas
        def goto_ventas():
             self.controller.show_frame("VentasApp")

        # Funciones de prueba (usan messagebox)
        def gestionar_usuarios(): messagebox.showinfo("Acción", "Abriendo módulo: Gestionar usuarios")
        def inventario(): messagebox.showinfo("Acción", "Abriendo módulo: Inventario")
        def reporte(): messagebox.showinfo("Acción", "Abriendo módulo: Reporte")
        
        # Función para cerrar sesión (regresar al login)
        def logout():
            if messagebox.askyesno("Confirmar", "¿Estás seguro que deseas cerrar sesión?"):
                self.controller.show_frame("LoginApp")

        create_menu_button("Registrar venta", 297, goto_ventas) # Navega a la nueva pantalla
        create_menu_button("Gestionar usuarios", 425, gestionar_usuarios)
        create_menu_button("Inventario", 561, inventario)
        create_menu_button("Reporte", 697, reporte)

        # Botón de Cerrar Sesión
        logout_btn = tk.Button(
            self,
            text="Cerrar sesion",
            font=f["inter_italic_20"],
            bg=bg_color,
            fg='#000000',
            bd=1, relief="raised", cursor="hand2",
            command=logout
        )
        logout_btn.place(x=574, y=887, width=227, height=52)


# --- CLASE VENTAS (VentasApp) ---

class VentasApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#FAA18F', width=1440, height=1024)

        self.productos_disponibles = [
            (1, "Menudo chico", 85.00, 80),
            (2, "Menudo grande", 110.00, 42),
            (3, "Burro de chicharron", 45.00, 31),
            (4, "Taco de asada", 25.00, 55),
            (5, "Refresco coca-cola 600ml", 22.00, 78),
            (6, "Refresco manzanita 600ml", 22.00, 50),
            (7, "Gordita", 22.00, 117),
        ]
        self.ticket_items = {} # {id_producto: {nombre: str, cantidad: int, precio: float}}
        self.total_amount = 0.0
        self.total_var = tk.StringVar(value="$0.00")

        self.create_widgets()
        self.populate_productos_table()

    def create_widgets(self):
        f = self.controller.fonts

        # --- Barra Superior (similar a CajeroApp, pero sin el logo, solo botón de regreso) ---
        header_frame = tk.Frame(self, bg='#013D5B', height=164)
        header_frame.place(x=0, y=0, width=1440, height=164)
        
        # Botón Regresar (similar a Rectangle 25)
        btn_regresar = tk.Button(
            self,
            text="Regresar",
            font=f["inter_italic_20"],
            bg='#F87C63',
            fg='#000000',
            bd=1, relief="raised", cursor="hand2",
            command=lambda: self.controller.show_frame("CajeroApp") # Regresa al menú
        )
        # Posición basada en el diseño: x=66.24, y=52.64, width=227, height=52
        btn_regresar.place(x=66, y=53, width=227, height=52) 
        
        # --- Título de la Pantalla "Ventas" ---
        title_label = tk.Label(
            self,
            text="Ventas",
            font=f["inter_bold_48"],
            fg='#013D5B',
            bg='#FAA18F',
            bd=1, relief="solid"
        )
        title_label.place(x=448, y=53)

        # --- Panel de Productos Disponibles (Izquierda) ---
        frame_productos_header = tk.Frame(self, bg='#701705', bd=0)
        frame_productos_header.place(x=36, y=279, width=618, height=30)
        
        # Encabezados de tabla de Productos (ID, Nombre, Precio, Stock)
        tk.Label(frame_productos_header, text="ID", font=f["inter_normal_24"], bg='#701705', fg='white').place(relx=0.05, rely=0.5, anchor="w")
        tk.Label(frame_productos_header, text="Nombre", font=f["inter_normal_24"], bg='#701705', fg='white').place(relx=0.2, rely=0.5, anchor="w")
        tk.Label(frame_productos_header, text="Precio", font=f["inter_normal_24"], bg='#701705', fg='white').place(relx=0.6, rely=0.5, anchor="w")
        tk.Label(frame_productos_header, text="Stock", font=f["inter_normal_24"], bg='#701705', fg='white').place(relx=0.85, rely=0.5, anchor="w")

        # Tabla de Productos (Treeview)
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=f["inter_normal_24"], background="#FFFFFF", fieldbackground="#FFFFFF", foreground="black")
        style.configure("Treeview.Heading", font=f["inter_normal_24"])

        self.tree_productos = ttk.Treeview(self, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=10)
        
        # Configuración de columnas (basada en tu diseño de anchos relativos)
        self.tree_productos.column("#1", width=50, anchor="center")
        self.tree_productos.column("#2", width=250, anchor="w")
        self.tree_productos.column("#3", width=120, anchor="center")
        self.tree_productos.column("#4", width=80, anchor="center")

        # Configuración de headings (texto en blanco porque ya los mostramos arriba)
        self.tree_productos.heading("ID", text="")
        self.tree_productos.heading("Nombre", text="")
        self.tree_productos.heading("Precio", text="")
        self.tree_productos.heading("Stock", text="")
        
        self.tree_productos.place(x=36, y=309, width=618, height=270)
        self.tree_productos.bind('<ButtonRelease-1>', self.on_select_producto)

        # --- Panel de Ticket de Venta (Derecha) ---
        frame_ticket_header = tk.Frame(self, bg='#701705', bd=0)
        frame_ticket_header.place(x=792, y=279, width=618, height=30)
        
        # Encabezados de tabla de Ticket (Producto, Cantidad, Subtotal)
        tk.Label(frame_ticket_header, text="Producto", font=f["inter_normal_24"], bg='#701705', fg='white').place(relx=0.15, rely=0.5, anchor="w")
        tk.Label(frame_ticket_header, text="Cantidad", font=f["inter_normal_24"], bg='#701705', fg='white').place(relx=0.55, rely=0.5, anchor="w")
        tk.Label(frame_ticket_header, text="Subtotal", font=f["inter_normal_24"], bg='#701705', fg='white').place(relx=0.8, rely=0.5, anchor="w")

        # Tabla de Ticket (Treeview)
        self.tree_ticket = ttk.Treeview(self, columns=("Producto", "Cantidad", "Subtotal"), show="headings", height=10)
        
        self.tree_ticket.column("#1", width=250, anchor="w")
        self.tree_ticket.column("#2", width=120, anchor="center")
        self.tree_ticket.column("#3", width=120, anchor="center")

        self.tree_ticket.heading("Producto", text="")
        self.tree_ticket.heading("Cantidad", text="")
        self.tree_ticket.heading("Subtotal", text="")
        
        self.tree_ticket.place(x=792, y=309, width=618, height=270)
        
        # --- Controles de Cantidad y Botones ---
        
        # Etiqueta "cantidad:"
        tk.Label(
            self, text="cantidad:", font=f["inter_italic_32"], fg='#000000', bg='#FAA18F'
        ).place(x=649, y=597) 

        # Campo de entrada de cantidad (Rectangle y ej. 1)
        self.entry_cantidad = tk.Entry(
            self, 
            width=10, 
            bg='#D9D9D9', 
            font=f["inter_normal_24"], 
            justify='center',
            relief="flat", # Simula el fondo
            bd=1
        )
        self.entry_cantidad.insert(0, "1") # Valor inicial 1
        self.entry_cantidad.place(x=619, y=634, width=266, height=44)

        # Botones de Acción (Rectangle 26, 27, 28)
        self.create_action_button("agregar al ticket", 705, self.agregar_al_ticket)
        self.create_action_button("Eliminar del ticket", 783, self.eliminar_del_ticket)
        self.create_action_button("Finalizar venta", 850, self.finalizar_venta)

        # --- Total ---
        tk.Label(
            self, 
            text="TOTAL:", 
            font=f["inter_italic_32"], 
            fg='#000000', 
            bg='#FAA18F'
        ).place(x=500, y=940) 
        
        # Etiqueta de Subtotal ($0.00)
        self.label_total = tk.Label(
            self, 
            textvariable=self.total_var, 
            font=f["inter_64_italic"], 
            fg='#000000', 
            bg='#FAA18F',
            anchor='e', # Alineación derecha dentro del widget
            justify='right'
        )
        self.label_total.place(x=670, y=930, width=300, height=80)
        
        # Variables de estado
        self.producto_seleccionado_id = None
        self.producto_seleccionado_nombre = None
        self.producto_seleccionado_precio = None


    def create_action_button(self, text, y_pos, command_func):
        """Helper para crear botones de acción con el estilo de tu diseño."""
        btn = tk.Button(
            self,
            text=text,
            font=self.controller.fonts["inter_italic_24"],
            bg='#F87C63',
            fg='#FFFFFF',
            bd=1, relief="raised", 
            cursor="hand2",
            command=command_func
        )
        # Ajustamos el ancho y el alto a los 267x50px del diseño
        btn.place(x=619, y=y_pos, width=267, height=50) 
        return btn

    def populate_productos_table(self):
        """Rellena la tabla de productos disponibles."""
        self.tree_productos.delete(*self.tree_productos.get_children())
        for id, nombre, precio, stock in self.productos_disponibles:
            # Insertamos el ID como tag (como string para consistencia)
            # values: (ID visible vacío, nombre, precio formateado, stock)
            self.tree_productos.insert("", "end", tags=(str(id),), values=(id, nombre, f"${precio:.2f}", stock))

    def on_select_producto(self, event):
        """Captura el producto seleccionado en la tabla."""
        selected_item = self.tree_productos.focus()
        if selected_item:
            tags = self.tree_productos.item(selected_item, 'tags')
            if not tags:
                self.producto_seleccionado_id = None
                return
            item_tag = tags[0]
            try:
                item_id = int(item_tag)
            except ValueError:
                self.producto_seleccionado_id = None
                return

            producto = next((p for p in self.productos_disponibles if p[0] == item_id), None)
            
            if producto:
                self.producto_seleccionado_id = producto[0]
                self.producto_seleccionado_nombre = producto[1]
                self.producto_seleccionado_precio = producto[2]
                self.entry_cantidad.delete(0, tk.END)
                self.entry_cantidad.insert(0, "1") # Resetea la cantidad a 1
                messagebox.showinfo("Selección", f"Seleccionado: {self.producto_seleccionado_nombre}")
            else:
                self.producto_seleccionado_id = None
                
    def calcular_total(self):
        """Calcula y actualiza el total del ticket."""
        current_total = 0.0
        for item in self.ticket_items.values():
            current_total += item["cantidad"] * item["precio"]
        self.total_amount = current_total
        self.total_var.set(f"${self.total_amount:.2f}")

    def agregar_al_ticket(self):
        """Agrega el producto seleccionado al ticket de venta."""
        if not self.producto_seleccionado_id:
            messagebox.showerror("Error", "Por favor, selecciona un producto primero.")
            return

        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        p_id = self.producto_seleccionado_id
        nombre = self.producto_seleccionado_nombre
        precio = self.producto_seleccionado_precio
        subtotal = cantidad * precio
        
        tag_str = str(p_id)
        if p_id in self.ticket_items:
            # Si ya existe, actualiza la cantidad
            self.ticket_items[p_id]["cantidad"] += cantidad
            nuevo_subtotal = self.ticket_items[p_id]["cantidad"] * precio
            
            # Encuentra y actualiza el item en el Treeview del ticket
            for item in self.tree_ticket.get_children():
                tags = self.tree_ticket.item(item, "tags")
                if tags and tags[0] == tag_str:
                    self.tree_ticket.item(item, values=(nombre, self.ticket_items[p_id]["cantidad"], f"${nuevo_subtotal:.2f}"))
                    break
        else:
            # Si es nuevo, agrégalo
            self.ticket_items[p_id] = {"nombre": nombre, "cantidad": cantidad, "precio": precio}
            self.tree_ticket.insert("", "end", tags=(tag_str,), values=(nombre, cantidad, f"${subtotal:.2f}"))

        self.calcular_total()
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")
        self.producto_seleccionado_id = None # Deseleccionar

    def eliminar_del_ticket(self):
        """Elimina la cantidad del producto seleccionado del ticket de venta."""
        selected_item = self.tree_ticket.focus()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un item del ticket para eliminar.")
            return
        
        tags = self.tree_ticket.item(selected_item, "tags")
        if not tags:
            messagebox.showerror("Error", "No se pudo obtener el item seleccionado.")
            return
        tag_str = tags[0]
        try:
            p_id = int(tag_str)
        except ValueError:
            messagebox.showerror("Error", "ID de item inválido.")
            return
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar '{self.ticket_items[p_id]['nombre']}' del ticket?"):
            # Eliminar del diccionario y del treeview
            del self.ticket_items[p_id]
            self.tree_ticket.delete(selected_item)
            self.calcular_total()
        
    def finalizar_venta(self):
        """Procesa la venta y resetea el ticket."""
        if not self.ticket_items:
            messagebox.showerror("Error", "El ticket está vacío. Agrega productos para finalizar la venta.")
            return

        total_venta = self.total_amount
        
        # Lógica de venta simulada
        messagebox.showinfo("Venta Finalizada", 
                            f"Venta registrada con éxito!\nTotal a pagar: ${total_venta:.2f}")

        # Resetear
        self.ticket_items = {}
        self.tree_ticket.delete(*self.tree_ticket.get_children())
        self.total_amount = 0.0
        self.total_var.set("$0.00")
        self.producto_seleccionado_id = None


# --- Bloque de Ejecución Principal ---

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
