# inventario_controller.py
from db import conectar
from tkinter import messagebox

class InventarioController:

    def __init__(self):
        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor()
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{e}")

    def get_all_productos(self):
        """Obtiene todos los productos de la base de datos."""
        try:
            self.cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos:\n{e}")
            return []

    def delete_producto(self, id_prod, nombre_prod):
        """Elimina un producto de la base de datos."""
        if messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar '{nombre_prod}'?"):
            try:
                self.cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_prod,))
                self.conexion.commit()
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")
                return False
        return False

    def add_producto(self, nombre, categoria, precio, stock):
        """Agrega un nuevo producto."""
        if not nombre or not precio or not stock:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return False
        try:
            self.cursor.execute(
                "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
                (nombre, categoria, precio, stock)
            )
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{e}")
            return False

    def update_producto(self, id_producto, nombre, categoria, precio, stock):
        """Actualiza un producto existente."""
        if not nombre or not precio or not stock:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return False
        try:
            self.cursor.execute(
                "UPDATE productos SET nombre=%s, categoria=%s, precio=%s, stock=%s WHERE id_producto=%s",
                (nombre, categoria, precio, stock, id_producto)
            )
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto:\n{e}")
            return False