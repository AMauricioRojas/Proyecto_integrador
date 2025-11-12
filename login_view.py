# login_view.py
import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from ventas_view import VentasVentana
from menu_admin_view import MenuAdmin

# Configuración de la app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class LoginVentana(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Fogón EMD")
        self.geometry("400x400")
        self.resizable(False, False)

        self.conexion = conectar()
        if not self.conexion:
            messagebox.showerror("Error DB", "No se pudo conectar a la base de datos.")
            self.destroy()
            return
            
        self.cursor = self.conexion.cursor()

        # Título
        ctk.CTkLabel(self, text="🔥 Fogón EMD", font=("Arial", 26, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Inicia sesión", font=("Arial", 18)).pack(pady=5)

        # Usuario
        ctk.CTkLabel(self, text="Usuario:").pack(pady=5)
        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Ej. admin")
        self.usuario_entry.pack(pady=5)
        self.usuario_entry.insert(0, "admin") # Pre-llenado para pruebas

        # Contraseña
        ctk.CTkLabel(self, text="Contraseña:").pack(pady=5)
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="••••••", show="*")
        self.pass_entry.pack(pady=5)
        self.pass_entry.insert(0, "admin123") # Pre-llenado para pruebas

        # Botón de login
        ctk.CTkButton(self, text="Iniciar Sesión", command=self.validar_login).pack(pady=20)
        
        # Bind "Enter" key to login
        self.bind('<Return>', self.validar_login)

        # Pie
        ctk.CTkLabel(self, text="Fogón EMD © 2025", font=("Arial", 10)).pack(side="bottom", pady=10)

    # ==========================================================
    def validar_login(self, event=None):
        """Valida usuario y contraseña"""
        usuario = self.usuario_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
            return
        
        try:
            # --- CORREGIDO ---
            # Usa 'contrasena' para que coincida con tu base de datos
            self.cursor.execute("SELECT id_usuario, rol FROM usuarios WHERE usuario=%s AND contrasena=%s", (usuario, password))
            datos = self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error de Consulta", f"No se pudo verificar el usuario: {e}")
            return

        if not datos:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            return

        id_usuario, rol = datos

        # Si es admin, abre panel completo
        if rol == "admin":
            self.withdraw()  # Oculta la ventana de login
            MenuAdmin(self, id_usuario)

        # Si es cajero, abre solo la ventana de ventas
        elif rol == "cajero":
            self.withdraw()
            # --- CORREGIDO ---
            # Ahora pasa el id_usuario, igual que el admin
            VentasVentana(self, id_usuario)

        else:
            messagebox.showwarning("Error", f"Rol desconocido: {rol}")

# --- PUNTO DE INICIO ---
if __name__ == "__main__":
    app = LoginVentana()
    app.mainloop()