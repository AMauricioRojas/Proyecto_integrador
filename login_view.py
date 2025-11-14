# login_view.py
import customtkinter as ctk
from tkinter import messagebox
# Ya no importamos 'conectar' desde aquí
from ventas_view import VentasVentana
from menu_admin_view import MenuAdmin
# --- IMPORTAMOS EL NUEVO CONTROLADOR ---
from login_controller import LoginController

class LoginVentana(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Fogón EMD")
        self.geometry("400x400")
        self.resizable(False, False)

        # --- CREAMOS LA INSTANCIA DEL CONTROLADOR ---
        self.controller = LoginController()

        # Si el controlador no pudo conectarse a la BD, cerramos la app
        if not self.controller.is_db_connected():
            self.destroy()
            return
            
        # --- DIBUJO DE LA VISTA (sin cambios) ---
        ctk.CTkLabel(self, text="🔥 Fogón EMD", font=("Arial", 26, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Inicia sesión", font=("Arial", 18)).pack(pady=5)

        ctk.CTkLabel(self, text="Usuario:").pack(pady=5)
        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Ej. admin")
        self.usuario_entry.pack(pady=5)
        self.usuario_entry.insert(0, "admin") # Pre-llenado para pruebas

        ctk.CTkLabel(self, text="Contraseña:").pack(pady=5)
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="••••••", show="*")
        self.pass_entry.pack(pady=5)
        self.pass_entry.insert(0, "admin123") # Pre-llenado para pruebas

        ctk.CTkButton(self, text="Iniciar Sesión", command=self.validar_login_vista).pack(pady=20)
        self.bind('<Return>', self.validar_login_vista) # Bind Enter
        ctk.CTkLabel(self, text="Fogón EMD © 2025", font=("Arial", 10)).pack(side="bottom", pady=10)

    # ==========================================================
    # === FUNCIÓN "TONTA" DE LA VISTA ===
    # ==========================================================
    def validar_login_vista(self, event=None):
        """
        Función "tonta" de la vista.
        1. Recoge datos.
        2. Los pasa al controlador.
        3. Actúa según la respuesta.
        """
        # 1. Recoge datos de la vista
        usuario = self.usuario_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        # 2. Pasa los datos al controlador y espera una respuesta
        autenticado, rol, id_usuario = self.controller.validar_login(usuario, password)

        # 3. Actúa según la respuesta del controlador
        if autenticado:
            if rol == "admin":
                self.withdraw()  # Oculta la ventana de login
                MenuAdmin(self, id_usuario)
            elif rol == "cajero":
                self.withdraw()
                VentasVentana(self, id_usuario)
            else:
                messagebox.showwarning("Error", f"Rol desconocido: {rol}")
