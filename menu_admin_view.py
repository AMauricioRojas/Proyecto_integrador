# menu_admin_view.py
import customtkinter as ctk
# Ya no importa 'conectar' ni 'messagebox'
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
        
        # --- Conexión a BD y cursor ELIMINADOS (ya no son necesarios) ---
        
        self.login_window = parent
        self.id_usuario = id_usuario

        ctk.CTkLabel(self, text="🧑‍💼 Panel del Administrador", font=("Arial", 24, "bold")).pack(pady=20)

        # Botones principales
        ctk.CTkButton(self, text="🛒 Abrir Módulo de Ventas", width=250, height=40, 
                      command=lambda: VentasVentana(self, self.id_usuario)).pack(pady=10)
                      
        ctk.CTkButton(self, text="📦 Gestionar Inventario", width=250, height=40, 
                      command=lambda: InventarioVentana(self)).pack(pady=10)
                      
        ctk.CTkButton(self, text="🧑‍💻 Gestionar Usuarios", width=250, height=40, 
                      command=lambda: UsuariosVentana(self)).pack(pady=10)
                      
        ctk.CTkButton(self, text="📊 Reporte de Ventas", width=250, height=40, 
                      command=lambda: ReportesVentana(self)).pack(pady=10)

        ctk.CTkButton(self, text="🚪 Cerrar Sesión", width=250, height=40, fg_color="red", 
                      command=self.cerrar_sesion).pack(pady=20, side="bottom")

    def cerrar_sesion(self):
        """Cierra sesión y vuelve al login"""
        self.destroy()
        self.login_window.deiconify()