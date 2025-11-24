# venta_controller.py
from db import conectar
from tkinter import messagebox
from datetime import datetime

class VentaController:

    def __init__(self):
        self.conexion = conectar()
        if self.conexion:
            # Usamos cursor normal (tuplas) para máxima compatibilidad
            self.cursor = self.conexion.cursor()
        else:
            # Si falla la conexión, avisamos y dejamos el cursor en None
            messagebox.showerror("Error Crítico", "No se pudo conectar a la base de datos.")
            self.cursor = None

    def get_productos_para_venta(self):
        """Obtiene todos los productos que tienen stock > 0."""
        if not self.cursor:
            return []
            
        try:
            # Seleccionamos ordenados por índice: 0=id, 1=nombre, 2=precio, 3=stock
            self.cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE stock > 0")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos:\n{e}")
            return []

    def finalizar_venta(self, items_ticket, total, metodo_pago, id_usuario):
        """
        Procesa la venta completa.
        items_ticket viene como: (id_producto, nombre, cantidad, subtotal)
        """
        if not self.cursor:
            return False, None, None

        if not items_ticket:
            messagebox.showwarning("Vacío", "No hay productos en el ticket.")
            return False, None, None

        try:
            # 1. Insertar la venta principal
            sql_venta = "INSERT INTO ventas (fecha, total, metodo_pago, id_usuario) VALUES (%s, %s, %s, %s)"
            datos_venta = (datetime.now(), total, metodo_pago, id_usuario)
            
            self.cursor.execute(sql_venta, datos_venta)
            id_venta = self.cursor.lastrowid

            # 2. Insertar detalle y actualizar stock
            sql_detalle = "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) VALUES (%s, %s, %s, %s)"
            sql_update_stock = "UPDATE productos SET stock = stock - %s WHERE id_producto = %s"

            productos_para_ticket = []

            for id_prod, nombre, cantidad, subtotal in items_ticket:
                # Insertar detalle
                self.cursor.execute(sql_detalle, (id_venta, id_prod, cantidad, subtotal))
                
                # Actualizar stock
                self.cursor.execute(sql_update_stock, (cantidad, id_prod))

                # Preparar datos para el ticket simple
                precio_unitario = 0
                if cantidad > 0:
                    precio_unitario = subtotal / cantidad
                productos_para_ticket.append((nombre, cantidad, precio_unitario, subtotal))

            self.conexion.commit()
            return True, id_venta, productos_para_ticket

        except Exception as e:
            self.conexion.rollback()
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")
            return False, None, None