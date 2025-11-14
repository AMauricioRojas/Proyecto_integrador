# venta_controller.py
from db import conectar
from tkinter import messagebox
from datetime import datetime

class VentaController:

    def __init__(self):
        try:
            self.conexion = conectar()
            # Usamos dictionary=True para poder acceder a las columnas por nombre
            self.cursor = self.conexion.cursor(dictionary=True)
            self.cursor_simple = self.conexion.cursor() # Para operaciones sin dictionary
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{e}")

    def get_productos_para_venta(self):
        """Obtiene todos los productos que tienen stock > 0."""
        try:
            # Usamos el cursor con dictionary
            self.cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE stock > 0")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos:\n{e}")
            return []

    def finalizar_venta(self, items_ticket, total, metodo_pago, id_usuario):
        """
        Procesa la venta completa.
        Esto es una TRANSACCIÓN: o todo funciona, o nada se guarda.
        """
        if not items_ticket:
            messagebox.showwarning("Vacío", "No hay productos en el ticket.")
            return False, None, None

        try:
            # 1. Insertar la venta principal
            sql_venta = "INSERT INTO ventas (fecha, total, metodo_pago, id_usuario) VALUES (%s, %s, %s, %s)"
            datos_venta = (datetime.now(), total, metodo_pago, id_usuario)
            
            self.cursor_simple.execute(sql_venta, datos_venta)
            id_venta = self.cursor_simple.lastrowid # Obtenemos el ID de la venta que acabamos de crear

            # 2. Insertar cada producto en detalle_venta y actualizar stock
            sql_detalle = "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) VALUES (%s, %s, %s, %s)"
            sql_update_stock = "UPDATE productos SET stock = stock - %s WHERE id_producto = %s"

            productos_para_ticket = [] # Lista limpia para el ticket

            # items_ticket es: (id_producto, nombre, cantidad, subtotal)
            for id_prod, nombre, cantidad, subtotal in items_ticket:
                # Insertar en detalle_venta
                self.cursor_simple.execute(sql_detalle, (id_venta, id_prod, cantidad, subtotal))
                
                # Actualizar stock
                self.cursor_simple.execute(sql_update_stock, (cantidad, id_prod))

                # 3. Preparamos los datos para el ticket simple (calculando precio unitario)
                precio_unitario = 0
                if cantidad > 0:
                    precio_unitario = subtotal / cantidad
                productos_para_ticket.append((nombre, cantidad, precio_unitario, subtotal))

            # 4. Si todo salió bien, confirmamos los cambios en la BD
            self.conexion.commit()
            
            # Devolvemos éxito, el ID de la venta y los productos para el ticket
            return True, id_venta, productos_para_ticket

        except Exception as e:
            # 5. Si algo falló, revertimos TODOS los cambios
            self.conexion.rollback()
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")
            return False, None, None