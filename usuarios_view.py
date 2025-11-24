# usuarios_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from usuario_controller import UsuarioController

class UsuariosVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Usuarios - Fogón EMD")
        self.geometry("900x550")
        self.resizable(False, False)
        
        # --- SALSEO: Fondo Crema ---
        self.configure(fg_color="#FFF6F3")

        self.parent = parent 
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.controller = UsuarioController()

        # HEADER
        frame_top = ctk.CTkFrame(self, height=80, fg_color="white", corner_radius=0)
        frame_top.pack(fill="x", side="top")

        frame_tit = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_tit.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(frame_tit, text="🧑‍💻 Gestión de Usuarios", font=("Arial", 22, "bold"), text_color="#D35400").pack(anchor="w")
        ctk.CTkLabel(frame_tit, text="Control de personal y accesos", font=("Arial", 12), text_color="gray").pack(anchor="w")

        ctk.CTkButton(frame_top, text="🔙 Volver", fg_color="transparent", border_width=1, border_color="#555", text_color="#555", hover_color="#EEE", width=100,
                      command=self.on_closing).pack(side="right", padx=20)

        # CUERPO
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Usuario", "Rol"), show="headings", height=15)
        self.tabla.pack(padx=20, pady=20, fill="both", expand=True)

        columnas = [("ID", 50), ("Nombre", 250), ("Usuario", 150), ("Rol", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        # Botones
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=20)

        btn_config = [
            ("➕ Nuevo Usuario", self.abrir_formulario_agregar, "#27AE60", "#1E8449"),
            ("✏️ Editar", self.abrir_formulario_editar, "#F39C12", "#D68910"),
            ("🗑️ Eliminar", self.eliminar_usuario, "#C0392B", "#922B21"),
        ]

        for txt, cmd, color, hover in btn_config:
             ctk.CTkButton(frame_botones, text=txt, command=cmd, fg_color=color, hover_color=hover, width=140, height=40, font=("Arial", 13, "bold")).pack(side="left", padx=10)

        self.mostrar_usuarios()

    def on_closing(self):
        self.parent.deiconify() 
        self.destroy() 

    def mostrar_usuarios(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        usuarios = self.controller.get_all_usuarios()
        for user in usuarios:
            self.tabla.insert("", "end", values=user)

    def abrir_formulario_agregar(self):
        FormularioUsuario(self, "agregar", self.controller, self.mostrar_usuarios)

    def abrir_formulario_editar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un usuario para editar.", parent=self)
            return
        datos = self.tabla.item(seleccionado)["values"]
        FormularioUsuario(self, "editar", self.controller, self.mostrar_usuarios, datos)

    def eliminar_usuario(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un usuario para eliminar.", parent=self)
            return
        datos = self.tabla.item(seleccionado)["values"]
        id_usuario = datos[0]
        nombre_usuario = datos[1]
        if self.controller.delete_usuario(id_usuario, nombre_usuario):
            self.mostrar_usuarios()

class FormularioUsuario(ctk.CTkToplevel):
    def __init__(self, parent, modo, controller, callback, datos=None):
        super().__init__(parent)
        self.title("Formulario de Usuario")
        self.geometry("400x480")
        self.configure(fg_color="#FFF6F3") # Fondo Crema
        
        self.modo = modo
        self.controller = controller 
        self.callback = callback
        self.transient(parent)
        self.grab_set()

        titulo = "Agregar Usuario" if modo == "agregar" else "Editar Usuario"
        ctk.CTkLabel(self, text=titulo, font=("Arial", 20, "bold"), text_color="#D35400").pack(pady=20)

        frame_campos = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame_campos.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(frame_campos, text="Nombre Completo:", text_color="gray").pack(pady=(10,0))
        self.nombre = ctk.CTkEntry(frame_campos, width=250, border_color="#D35400")
        self.nombre.pack(pady=5)
        
        ctk.CTkLabel(frame_campos, text="Usuario (login):", text_color="gray").pack()
        self.usuario = ctk.CTkEntry(frame_campos, width=250, border_color="#D35400")
        self.usuario.pack(pady=5)

        ctk.CTkLabel(frame_campos, text="Contraseña:", text_color="gray").pack()
        placeholder_pass = "Nueva contraseña" if modo == "editar" else "Contraseña"
        self.contrasena = ctk.CTkEntry(frame_campos, placeholder_text=placeholder_pass, show="*", width=250, border_color="#D35400")
        self.contrasena.pack(pady=5)
        if modo == "editar":
             ctk.CTkLabel(frame_campos, text="(Dejar en blanco para no cambiarla)", font=("Arial", 10), text_color="gray").pack()

        ctk.CTkLabel(frame_campos, text="Rol:", text_color="gray").pack()
        self.rol = ctk.CTkComboBox(frame_campos, values=["admin", "cajero"], width=250, border_color="#D35400", button_color="#D35400", button_hover_color="#A04000")
        self.rol.pack(pady=10)

        if datos:
            self.id_usuario = datos[0]
            self.nombre.insert(0, datos[1])
            self.usuario.insert(0, datos[2])
            self.rol.set(datos[3])
        else:
            self.rol.set("cajero")

        texto_boton = "💾 Guardar" if modo == "editar" else "➕ Crear Usuario"
        ctk.CTkButton(self, text=texto_boton, command=self.guardar, height=40, 
                      fg_color="#D35400", hover_color="#A04000", font=("Arial", 14, "bold")).pack(pady=20)
        
        # --- TECLA ENTER PARA GUARDAR ---
        self.bind('<Return>', lambda event: self.guardar())

    def guardar(self):
        nombre = self.nombre.get().strip()
        usuario = self.usuario.get().strip()
        contrasena = self.contrasena.get().strip()
        rol = self.rol.get()
        exito = False
        if self.modo == "agregar":
            exito = self.controller.add_usuario(nombre, usuario, contrasena, rol)
        else:
            exito = self.controller.update_usuario(self.id_usuario, nombre, usuario, contrasena, rol)
        if exito:
            self.callback() 
            self.destroy()