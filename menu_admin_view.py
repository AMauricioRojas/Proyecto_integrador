# menu_admin_view.py
import customtkinter as ctk
from tkinter import messagebox
from db import conectar
from ventas_view import VentasVentana
from inventario_view import InventarioVentana
from usuarios_view import UsuariosVentana
# --- IMPORTAMOS EL NUEVO MÓDULO DE REPORTES ---
from reportes_view import ReportesVentana


class MenuAdmin(ctk.CTkToplevel):
    def __init__(self, parent, id_usuario):
        super().__init__(parent)
        self.title("Panel de Administración - Fogón EMD")
        self.geometry("600x450") # Un poco más alto para el nuevo botón
        self.resizable(False, False)
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()
        
        self.login_window = parent
        # --- GUARDAMOS EL ID DEL ADMIN LOGUEADO ---
        self.id_usuario = id_usuario

        ctk.CTkLabel(self, text="🧑‍💼 Panel del Administrador", font=("Arial", 24, "bold")).pack(pady=20)

        # Botones principales
        
        # --- ACTUALIZADO: Pasamos el self.id_usuario a VentasVentana ---
        ctk.CTkButton(self, text="🛒 Abrir Módulo de Ventas", width=250, height=40,command=lambda: VentasVentana(self, self.id_usuario)).pack(pady=10)
        
        ctk.CTkButton(self, text="📦 Gestionar Inventario", width=250, height=40,command=lambda: InventarioVentana(self)).pack(pady=10)
        
        ctk.CTkButton(self, text="🧑‍💻 Gestionar Usuarios", width=250, height=40,command=lambda: UsuariosVentana(self)).pack(pady=10)
        
        # --- NUEVO BOTÓN DE REPORTES (CORREGIDO) ---
        ctk.CTkButton(self, text="📊 Reporte de Ventas", width=250, height=40,command=lambda: ReportesVentana(self)).pack(pady=10)

        ctk.CTkButton(self, text="🚪 Cerrar Sesión", width=250, height=40, fg_color="red",command=self.cerrar_sesion).pack(pady=20, side="bottom")

    def cerrar_sesion(self):
        """Cierra sesión y vuelve al login"""
        self.destroy()
        self.login_window.deiconify()