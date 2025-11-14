# inventario_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
# --- IMPORTAMOS EL CONTROLADOR ---
from inventario_controller import InventarioController

class InventarioVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inventario - Fogón EMD")
        self.geometry("900x500")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()

        # --- CREAMOS LA INSTANCIA DEL CONTROLADOR ---
        self.controller = InventarioController()

        # Título
        ctk.CTkLabel(self, text="📦 Inventario de Productos", font=("Arial", 22, "bold")).pack(pady=20)

        # Tabla de productos
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Categoría", "Precio", "Stock"), show="headings", height=15)
        self.tabla.pack(padx=20, pady=10, fill="x")

        # Configurar columnas
        columnas = [("ID", 50), ("Nombre", 200), ("Categoría", 120), ("Precio", 100), ("Stock", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        # Botones de acciones
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="➕ Agregar", command=self.abrir_formulario_agregar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botones, text="✏️ Editar", command=self.abrir_formulario_editar).grid(row=0, column=1, padx=10)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", command=self.eliminar_producto, fg_color="red").grid(row=0, column=2, padx=10)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar", command=self.mostrar_productos).grid(row=0, column=3, padx=10)

        self.mostrar_productos()

    def mostrar_productos(self):
        """Pide los productos al controlador y los muestra."""
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        
        # La lógica de BD ahora está en el controlador
        productos = self.controller.get_all_productos()
        for prod in productos:
            self.tabla.insert("", "end", values=prod)

    def abrir_formulario_agregar(self):
        # Le pasamos el controlador al formulario
        VentanaProducto(self, "agregar", self.controller, self.mostrar_productos)

    def abrir_formulario_editar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para editar.", parent=self)
            return
        datos = self.tabla.item(seleccionado)["values"]
        # Le pasamos el controlador y los datos
        VentanaProducto(self, "editar", self.controller, self.mostrar_productos, datos)

    def eliminar_producto(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar.", parent=self)
            return
        
        datos = self.tabla.item(seleccionado)["values"]
        id_prod = datos[0]
        nombre_prod = datos[1]

        # La lógica de BD y validación ahora está en el controlador
        if self.controller.delete_producto(id_prod, nombre_prod):
            self.mostrar_productos() # Si se borró, actualizamos

class VentanaProducto(ctk.CTkToplevel):
    # Ahora el formulario recibe el controlador
    def __init__(self, parent, modo, controller, callback, producto=None):
        super().__init__(parent)
        self.title("Formulario de Producto")
        self.geometry("400x400")

        self.modo = modo
        self.controller = controller # Guardamos el controlador
        self.callback = callback
        
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text="Formulario de Producto", font=("Arial", 18, "bold")).pack(pady=20)

        # Campos
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre del producto", width=250)
        self.nombre.pack(pady=10)
        self.categoria = ctk.CTkEntry(self, placeholder_text="Categoría", width=250)
        self.categoria.pack(pady=10)
        self.precio = ctk.CTkEntry(self, placeholder_text="Precio (Ej. 85.00)", width=250)
        self.precio.pack(pady=10)
        self.stock = ctk.CTkEntry(self, placeholder_text="Stock (Ej. 50)", width=250)
        self.stock.pack(pady=10)

        if producto:
            self.id_producto = producto[0]
            self.nombre.insert(0, producto[1])
            self.categoria.insert(0, producto[2])
            self.precio.insert(0, str(producto[3])) # Aseguramos que sea string
            self.stock.insert(0, str(producto[4])) # Aseguramos que sea string

        texto_boton = "Guardar Cambios" if modo == "editar" else "Agregar Producto"
        ctk.CTkButton(self, text=texto_boton, command=self.guardar).pack(pady=20)

    def guardar(self):
        # 1. Recolectamos datos de la VISTA
        nombre = self.nombre.get()
        categoria = self.categoria.get()
        precio = self.precio.get()
        stock = self.stock.get()

        # 2. Enviamos los datos al CONTROLADOR
        exito = False
        if self.modo == "agregar":
            exito = self.controller.add_producto(nombre, categoria, precio, stock)
        else:
            exito = self.controller.update_producto(self.id_producto, nombre, categoria, precio, stock)
        
        # 3. Si el controlador dice que fue un éxito, cerramos
        if exito:
            self.callback() # Llama a mostrar_productos()
            self.destroy()