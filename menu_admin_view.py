# menu_admin_view.py
import customtkinter as ctk
import os
from PIL import Image
from ventas_view import VentasVentana
from inventario_view import InventarioVentana
from usuarios_view import UsuariosVentana
from reportes_view import ReportesVentana

class MenuAdmin(ctk.CTkToplevel):
    def __init__(self, parent, id_usuario):
        super().__init__(parent)
        self.title("Panel de Administración - Fogón EMD")
        self.geometry("900x600")
        self.resizable(False, False)
        self.login_window = parent
        self.id_usuario = id_usuario

        # --- SALSEO: Fondo general ---
        self.configure(fg_color="#FFF6F3")

        # --- LAYOUT: Dos Columnas ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. BARRA LATERAL (Izquierda) - Color Ladrillo Oscuro
        frame_sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#A04000")
        frame_sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo o Título en Sidebar
        ctk.CTkLabel(frame_sidebar, text="FOGÓN\nEMD", font=("Arial", 28, "bold"), text_color="white").pack(pady=(40, 20))
        ctk.CTkLabel(frame_sidebar, text="Modo Admin", font=("Arial", 14), text_color="#FFCCBC").pack(pady=(0, 40))

        # Botón Salir en Sidebar
        try:
            path = os.path.join(os.path.dirname(__file__), "assets", "icon_salir.png")
            icon_salir = ctk.CTkImage(Image.open(path), size=(20, 20))
        except: icon_salir = None
        
        ctk.CTkButton(frame_sidebar, text="Cerrar Sesión", image=icon_salir, compound="left", 
                      fg_color="transparent", border_width=1, border_color="white", hover_color="#873600",
                      command=self.cerrar_sesion).pack(side="bottom", pady=40, padx=20, fill="x")

        # 2. CONTENIDO PRINCIPAL (Derecha)
        frame_main = ctk.CTkFrame(self, fg_color="transparent")
        frame_main.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

        ctk.CTkLabel(frame_main, text="¿Qué deseas gestionar hoy?", font=("Arial", 24, "bold"), text_color="#5D4037").pack(anchor="w", pady=(0, 30))

        # Grid de botones
        frame_grid = ctk.CTkFrame(frame_main, fg_color="transparent")
        frame_grid.pack(fill="both", expand=True)

        # Cargamos iconos
        self.icons = {}
        for n in ["ventas", "inventario", "usuarios", "reportes"]:
            try:
                path = os.path.join(os.path.dirname(__file__), "assets", f"icon_{n}.png")
                self.icons[n] = ctk.CTkImage(Image.open(path), size=(60, 60))
            except: self.icons[n] = None

        # Botones Estilizados (Tarjetas)
        self.crear_tarjeta(frame_grid, "Ventas", "Caja y Tickets", self.icons["ventas"], 0, 0, self.abrir_modulo_ventas)
        self.crear_tarjeta(frame_grid, "Inventario", "Productos y Stock", self.icons["inventario"], 0, 1, self.abrir_modulo_inventario)
        self.crear_tarjeta(frame_grid, "Usuarios", "Personal y Roles", self.icons["usuarios"], 1, 0, self.abrir_modulo_usuarios)
        self.crear_tarjeta(frame_grid, "Reportes", "Estadísticas y PDF", self.icons["reportes"], 1, 1, self.abrir_modulo_reportes)

    def crear_tarjeta(self, parent, titulo, subtitulo, icono, fila, col, comando):
        # Creamos un botón que parezca una tarjeta grande
        btn = ctk.CTkButton(parent, text=f"\n{titulo}\n\n{subtitulo}", image=icono, compound="top",
                            width=200, height=180, font=("Arial", 18, "bold"),
                            fg_color="white", text_color="#D35400", hover_color="#FDEBD0",
                            border_width=0, corner_radius=15,
                            # Sombra sutil simulada con el color de fondo del botón
                            command=comando)
        btn.grid(row=fila, column=col, padx=15, pady=15, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(fila, weight=1)

    def abrir_modulo_ventas(self):
        self.withdraw()
        VentasVentana(self, self.id_usuario)

    def abrir_modulo_inventario(self):
        self.withdraw()
        InventarioVentana(self)

    def abrir_modulo_usuarios(self):
        self.withdraw()
        UsuariosVentana(self)

    def abrir_modulo_reportes(self):
        self.withdraw()
        ReportesVentana(self)

    def cerrar_sesion(self):
        self.destroy()
        self.login_window.deiconify()