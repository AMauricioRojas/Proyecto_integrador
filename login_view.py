# login_view.py
import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image 
from ventas_view import VentasVentana
from menu_admin_view import MenuAdmin
from login_controller import LoginController

class LoginVentana(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Fogón EMD")
        self.geometry("450x600")
        self.resizable(False, False)
        
        # --- SALSEO: Fondo Cálido (Crema) ---
        self.configure(fg_color="#FFF6F3") 

        self.controller = LoginController()
        if not self.controller.is_db_connected():
            self.destroy()
            return
            
        # --- TARJETA CENTRAL (Blanca) ---
        frame_card = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_color="#FFCCBC", border_width=1)
        frame_card.pack(pady=40, padx=30, fill="both", expand=True)

        # Logo
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
            imagen_pil = Image.open(ruta_logo)
            self.logo_img = ctk.CTkImage(light_image=imagen_pil, dark_image=imagen_pil, size=(150, 150))
            ctk.CTkLabel(frame_card, image=self.logo_img, text="").pack(pady=(30, 10))
        except:
            ctk.CTkLabel(frame_card, text="🔥", font=("Arial", 60)).pack(pady=20)

        # Títulos
        ctk.CTkLabel(frame_card, text="Bienvenido", font=("Arial", 24, "bold"), text_color="#D35400").pack(pady=5)
        ctk.CTkLabel(frame_card, text="Inicia sesión para continuar", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        # Campos
        self.usuario_entry = ctk.CTkEntry(frame_card, placeholder_text="Usuario", height=45, 
                                          fg_color="#FAFAFA", border_color="#E67E22", text_color="black")
        self.usuario_entry.pack(fill="x", padx=30, pady=(0, 15))
        self.usuario_entry.insert(0, "admin") 

        self.pass_entry = ctk.CTkEntry(frame_card, placeholder_text="Contraseña", show="*", height=45,
                                       fg_color="#FAFAFA", border_color="#E67E22", text_color="black")
        self.pass_entry.pack(fill="x", padx=30, pady=(0, 20))
        self.pass_entry.insert(0, "admin123") 

        # Botón Salseado
        ctk.CTkButton(frame_card, text="INGRESAR", command=self.validar_login_vista, height=45, 
                      font=("Arial", 14, "bold"), fg_color="#D35400", hover_color="#A04000", corner_radius=25).pack(padx=30, pady=10, fill="x")
        
        self.bind('<Return>', self.validar_login_vista) 
        ctk.CTkLabel(self, text="Fogón EMD System © 2025", font=("Arial", 10), text_color="gray").pack(side="bottom", pady=10)

    def validar_login_vista(self, event=None):
        usuario = self.usuario_entry.get().strip()
        password = self.pass_entry.get().strip()
        autenticado, rol, id_usuario = self.controller.validar_login(usuario, password)

        if autenticado:
            if rol == "admin":
                self.withdraw() 
                MenuAdmin(self, id_usuario)
            elif rol == "cajero":
                self.withdraw()
                VentasVentana(self, id_usuario)
            else:
                messagebox.showwarning("Error", f"Rol desconocido: {rol}")