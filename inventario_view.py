# inventario_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from db import conectar

class InventarioVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inventario - Fogón EMD")
        self.geometry("900x500")
        self.resizable(False, False)

        # Conectar a la base de datos
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()

        # Título
        ctk.CTkLabel(self, text="📦 Inventario de Productos", font=("Arial", 22, "bold")).pack(pady=20)

        # Tabla de productos
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Categoría", "Precio", "Stock"), show="headings", height=15)
        self.tabla.pack(padx=20, pady=10)

        # Configurar columnas
        columnas = [("ID", 50), ("Nombre", 200), ("Categoría", 120), ("Precio", 100), ("Stock", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        # Botones de acciones
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="➕ Agregar", command=self.agregar_producto).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botones, text="✏️ Editar", command=self.editar_producto).grid(row=0, column=1, padx=10)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", command=self.eliminar_producto).grid(row=0, column=2, padx=10)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar", command=self.mostrar_productos).grid(row=0, column=3, padx=10)

        self.mostrar_productos()

    def mostrar_productos(self):
        """Carga los productos desde la base de datos"""
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        try:
            self.cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos")
            for prod in self.cursor.fetchall():
                self.tabla.insert("", "end", values=prod)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos:\n{e}")

    def agregar_producto(self):
        VentanaProducto(self, modo="agregar", conexion=self.conexion, callback=self.mostrar_productos)

    def editar_producto(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para editar.")
            return
        datos = self.tabla.item(seleccionado)["values"]
        VentanaProducto(self, modo="editar", conexion=self.conexion, producto=datos, callback=self.mostrar_productos)

    def eliminar_producto(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")
            return
        datos = self.tabla.item(seleccionado)["values"]
        id_prod = datos[0]

        if messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar '{datos[1]}'?"):
            try:
                self.cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_prod,))
                self.conexion.commit()
                self.mostrar_productos()
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")

class VentanaProducto(ctk.CTkToplevel):
    def __init__(self, parent, modo, conexion, callback, producto=None):
        super().__init__(parent)
        self.title("Producto")
        self.geometry("400x400")
        self.modo = modo
        self.conexion = conexion
        self.callback = callback
        self.cursor = self.conexion.cursor()

        ctk.CTkLabel(self, text="Formulario de Producto", font=("Arial", 18, "bold")).pack(pady=20)

        # Campos
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre del producto")
        self.nombre.pack(pady=10)
        self.categoria = ctk.CTkEntry(self, placeholder_text="Categoría")
        self.categoria.pack(pady=10)
        self.precio = ctk.CTkEntry(self, placeholder_text="Precio")
        self.precio.pack(pady=10)
        self.stock = ctk.CTkEntry(self, placeholder_text="Stock")
        self.stock.pack(pady=10)

        if producto:
            self.id_producto = producto[0]
            self.nombre.insert(0, producto[1])
            self.categoria.insert(0, producto[2])
            self.precio.insert(0, producto[3])
            self.stock.insert(0, producto[4])

        texto_boton = "Guardar Cambios" if modo == "editar" else "Agregar Producto"
        ctk.CTkButton(self, text=texto_boton, command=self.guardar).pack(pady=20)

    def guardar(self):
        nombre = self.nombre.get()
        categoria = self.categoria.get()
        precio = self.precio.get()
        stock = self.stock.get()

        if not nombre or not precio or not stock:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return

        try:
            if self.modo == "agregar":
                self.cursor.execute(
                    "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
                    (nombre, categoria, precio, stock)
                )
            else:
                self.cursor.execute(
                    "UPDATE productos SET nombre=%s, categoria=%s, precio=%s, stock=%s WHERE id_producto=%s",
                    (nombre, categoria, precio, stock, self.id_producto)
                )

            self.conexion.commit()
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            self.callback()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{e}")
