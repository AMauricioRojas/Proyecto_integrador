# usuario_controller.py
from db import conectar
from tkinter import messagebox

class UsuarioController:
    
    def __init__(self):
        # Creamos una conexión única para este controlador
        try:
            self.conexion = conectar()
            self.cursor = self.conexion.cursor()
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{e}")

    def get_all_usuarios(self):
        """Obtiene todos los usuarios de la base de datos."""
        try:
            self.cursor.execute("SELECT id_usuario, nombre, usuario, rol FROM usuarios")
            return self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error de Consulta", f"No se pudieron cargar los usuarios:\n{e}")
            return []

    def delete_usuario(self, id_usuario, nombre_usuario):
        """Elimina un usuario, con lógica de validación."""
        if id_usuario == 1:
            messagebox.showerror("Error", "No se puede eliminar al administrador principal.")
            return False

        if messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar a '{nombre_usuario}'?"):
            try:
                self.cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
                self.conexion.commit()
                messagebox.showinfo("Eliminado", "Usuario eliminado correctamente.")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el usuario:\n{e}")
                return False
        return False

    def add_usuario(self, nombre, usuario, contrasena, rol):
        """Agrega un nuevo usuario."""
        if not nombre or not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "El Nombre, Usuario y Contraseña son obligatorios.")
            return False
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES (%s, %s, %s, %s)",
                (nombre, usuario, contrasena, rol)
            )
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario:\n{e}")
            return False

    def update_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        """Actualiza un usuario existente."""
        if not nombre or not usuario:
            messagebox.showwarning("Campos vacíos", "El Nombre y el Usuario son obligatorios.")
            return False
        try:
            if contrasena: # Si el usuario escribió una nueva contraseña
                self.cursor.execute(
                    "UPDATE usuarios SET nombre=%s, usuario=%s, contrasena=%s, rol=%s WHERE id_usuario=%s",
                    (nombre, usuario, contrasena, rol, id_usuario)
                )
            else: # Si dejó la contraseña en blanco, no la actualizamos
                self.cursor.execute(
                    "UPDATE usuarios SET nombre=%s, usuario=%s, rol=%s WHERE id_usuario=%s",
                    (nombre, usuario, rol, id_usuario)
                )
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario:\n{e}")
            return False