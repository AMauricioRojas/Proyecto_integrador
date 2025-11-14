# login_controller.py
from db import conectar
from tkinter import messagebox

class LoginController:
    
    def __init__(self):
        try:
            self.conexion = conectar()
            if self.conexion:
                self.cursor = self.conexion.cursor()
            else:
                # Si la conexión falla aquí, la app no puede iniciar
                messagebox.showerror("Error Crítico de Conexión", "No se pudo conectar a la base de datos. La aplicación se cerrará.")
                self.cursor = None
        except Exception as e:
            messagebox.showerror("Error Crítico", f"Error al iniciar el controlador de login:\n{e}")
            self.cursor = None

    def is_db_connected(self):
        """Revisa si la conexión a la BD fue exitosa."""
        return self.cursor is not None

    def validar_login(self, usuario, password):
        """
        Valida las credenciales contra la BD.
        Retorna (True/False, rol, id_usuario)
        """
        if not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
            return (False, None, None)
        
        try:
            self.cursor.execute("SELECT id_usuario, rol FROM usuarios WHERE usuario=%s AND contrasena=%s", (usuario, password))
            datos = self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error de Consulta", f"No se pudo verificar el usuario: {e}")
            return (False, None, None)

        if not datos:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            return (False, None, None)

        # Si encontramos datos, 'datos' es una tupla (id_usuario, rol)
        id_usuario = datos[0]
        rol = datos[1]
        
        return (True, rol, id_usuario)