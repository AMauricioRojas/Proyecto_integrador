# inventario_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from inventario_controller import InventarioController

class InventarioVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inventario - Fogón EMD")
        self.geometry("1100x650")
        self.resizable(False, False)
        
        # --- SALSEO: Fondo Crema ---
        self.configure(fg_color="#FFF6F3")

        self.parent = parent 
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.controller = InventarioController()
        self.lista_productos_completa = [] 

        # HEADER (Blanco)
        frame_top = ctk.CTkFrame(self, height=80, fg_color="white", corner_radius=0)
        frame_top.pack(fill="x", side="top")

        # Título
        frame_tit = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_tit.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(frame_tit, text="📦 Gestión de Inventario", font=("Arial", 22, "bold"), text_color="#D35400").pack(anchor="w")
        ctk.CTkLabel(frame_tit, text="Control de Stock y Precios", font=("Arial", 12), text_color="gray").pack(anchor="w")

        # Buscador
        frame_bus = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_bus.pack(side="left", fill="x", expand=True, padx=20)
        ctk.CTkLabel(frame_bus, text="Buscar:", text_color="gray").pack(anchor="w")
        self.entry_busqueda = ctk.CTkEntry(frame_bus, placeholder_text="Nombre del producto...", height=35, border_color="#D35400")
        self.entry_busqueda.pack(fill="x")
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_productos)

        # Botón Volver
        ctk.CTkButton(frame_top, text="🔙 Volver", fg_color="transparent", border_width=1, border_color="#555", text_color="#555", hover_color="#EEE", width=100,
                      command=self.on_closing).pack(side="right", padx=20)

        # CUERPO
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Categoría", "Precio", "Stock"), show="headings", height=18)
        self.tabla.pack(padx=20, pady=10, fill="both", expand=True)

        columnas = [("ID", 50), ("Nombre", 250), ("Categoría", 150), ("Precio", 100), ("Stock", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        # Botones de Acción
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=20)

        # Colores actualizados a la paleta Fogón / Semáforo
        btn_config = [
            ("➕ Agregar Nuevo", self.abrir_formulario_agregar, "#27AE60", "#1E8449"), # Verde
            ("✏️ Editar", self.abrir_formulario_editar, "#F39C12", "#D68910"),       # Naranja/Amarillo
            ("🗑️ Eliminar", self.eliminar_producto, "#C0392B", "#922B21"),           # Rojo
            ("🔄 Actualizar", self.mostrar_productos, "#2980B9", "#21618C")           # Azul
        ]

        for txt, cmd, color, hover in btn_config:
             ctk.CTkButton(frame_botones, text=txt, command=cmd, fg_color=color, hover_color=hover, width=140, height=40, font=("Arial", 13, "bold")).pack(side="left", padx=10)

        self.mostrar_productos()

    def on_closing(self):
        self.parent.deiconify() 
        self.destroy() 

    def mostrar_productos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        datos = self.controller.get_all_productos()
        self.lista_productos_completa = datos 
        self.actualizar_tabla(datos)

    def actualizar_tabla(self, lista):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for prod in lista:
            self.tabla.insert("", "end", values=(prod[0], prod[1], prod[2], f"${prod[3]}", prod[4]))

    def filtrar_productos(self, event=None):
        texto = self.entry_busqueda.get().lower()
        if not texto:
            self.actualizar_tabla(self.lista_productos_completa)
        else:
            filtrada = [p for p in self.lista_productos_completa if texto in str(p[1]).lower()]
            self.actualizar_tabla(filtrada)

    def abrir_formulario_agregar(self):
        VentanaProducto(self, "agregar", self.controller, self.mostrar_productos)

    def abrir_formulario_editar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para editar.", parent=self)
            return
        datos = self.tabla.item(seleccionado)["values"]
        precio_limpio = str(datos[3]).replace("$", "")
        datos_limpios = (datos[0], datos[1], datos[2], precio_limpio, datos[4])
        VentanaProducto(self, "editar", self.controller, self.mostrar_productos, datos_limpios)

    def eliminar_producto(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar.", parent=self)
            return
        datos = self.tabla.item(seleccionado)["values"]
        id_prod = datos[0]
        nombre_prod = datos[1]
        if self.controller.delete_producto(id_prod, nombre_prod):
            self.mostrar_productos()

class VentanaProducto(ctk.CTkToplevel):
    def __init__(self, parent, modo, controller, callback, producto=None):
        super().__init__(parent)
        self.title("Producto")
        self.geometry("400x500")
        self.configure(fg_color="#FFF6F3") # Fondo Crema
        
        self.modo = modo
        self.controller = controller 
        self.callback = callback
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text="Detalles del Producto", font=("Arial", 20, "bold"), text_color="#D35400").pack(pady=20)

        frame_campos = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_campos.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(frame_campos, text="Nombre:", text_color="gray").pack(pady=(10,0))
        self.nombre = ctk.CTkEntry(frame_campos, width=250, border_color="#D35400")
        self.nombre.pack(pady=5)
        
        ctk.CTkLabel(frame_campos, text="Categoría:", text_color="gray").pack()
        self.categoria = ctk.CTkEntry(frame_campos, width=250, border_color="#D35400")
        self.categoria.pack(pady=5)
        
        ctk.CTkLabel(frame_campos, text="Precio:", text_color="gray").pack()
        self.precio = ctk.CTkEntry(frame_campos, width=250, border_color="#D35400")
        self.precio.pack(pady=5)
        
        ctk.CTkLabel(frame_campos, text="Stock Inicial:", text_color="gray").pack()
        self.stock = ctk.CTkEntry(frame_campos, width=250, border_color="#D35400")
        self.stock.pack(pady=5)

        if producto:
            self.id_producto = producto[0]
            self.nombre.insert(0, producto[1])
            self.categoria.insert(0, producto[2])
            self.precio.insert(0, str(producto[3])) 
            self.stock.insert(0, str(producto[4])) 

        texto_boton = "💾 Guardar Cambios" if modo == "editar" else "➕ Agregar Producto"
        
        # Botón Guardar (Naranja)
        ctk.CTkButton(self, text=texto_boton, command=self.guardar, height=40, 
                      fg_color="#D35400", hover_color="#A04000", font=("Arial", 14, "bold")).pack(pady=20)
        
        # --- TECLA ENTER PARA GUARDAR ---
        self.bind('<Return>', lambda event: self.guardar())

    def guardar(self):
        nombre = self.nombre.get()
        categoria = self.categoria.get()
        precio = self.precio.get()
        stock = self.stock.get()
        exito = False
        if self.modo == "agregar":
            exito = self.controller.add_producto(nombre, categoria, precio, stock)
        else:
            exito = self.controller.update_producto(self.id_producto, nombre, categoria, precio, stock)
        if exito:
            self.callback() 
            self.destroy()