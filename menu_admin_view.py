# menu_admin_view.py
import customtkinter as ctk
from ventas_view import VentasVentana
from inventario_view import InventarioVentana
from usuarios_view import UsuariosVentana
from reportes_view import ReportesVentana


class MenuAdmin(ctk.CTkToplevel):
    def __init__(self, parent, id_usuario):
        super().__init__(parent)
        self.title("Panel de Administración - Fogón EMD")
        self.geometry("600x450")
        self.resizable(False, False)
        
        self.login_window = parent
        self.id_usuario = id_usuario

        ctk.CTkLabel(self, text="🧑‍💼 Panel del Administrador", font=("Arial", 24, "bold")).pack(pady=20)

        # Botones principales (AHORA LLAMAN A FUNCIONES)
        ctk.CTkButton(self, text="🛒 Abrir Módulo de Ventas", width=250, height=40, 
                      command=self.abrir_modulo_ventas).pack(pady=10)
                      
        ctk.CTkButton(self, text="📦 Gestionar Inventario", width=250, height=40, 
                      command=self.abrir_modulo_inventario).pack(pady=10)
                      
        ctk.CTkButton(self, text="🧑‍💻 Gestionar Usuarios", width=250, height=40, 
                      command=self.abrir_modulo_usuarios).pack(pady=10)
                      
        ctk.CTkButton(self, text="📊 Reporte de Ventas", width=250, height=40, 
                      command=self.abrir_modulo_reportes).pack(pady=10)

        ctk.CTkButton(self, text="🚪 Cerrar Sesión", width=250, height=40, fg_color="red", 
                      command=self.cerrar_sesion).pack(pady=20, side="bottom")

    # --- NUEVAS FUNCIONES DE APERTURA ---

    def abrir_modulo_ventas(self):
        self.withdraw() # Oculta este menú
        VentasVentana(self, self.id_usuario) # Abre la ventana hija

    def abrir_modulo_inventario(self):
        self.withdraw() # Oculta este menú
        InventarioVentana(self) # Abre la ventana hija

    def abrir_modulo_usuarios(self):
        self.withdraw() # Oculta este menú
        UsuariosVentana(self) # Abre la ventana hija

    def abrir_modulo_reportes(self):
        self.withdraw() # Oculta este menú
        ReportesVentana(self) # Abre la ventana hija

    # --- FUNCIÓN DE CIERRE DE SESIÓN ---
    
    def cerrar_sesion(self):
        """Cierra sesión y vuelve al login"""
        self.destroy()
        self.login_window.deiconify() # Muestra la ventana de login