# usuarios_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from usuario_controller import UsuarioController

class UsuariosVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Usuarios - Fogón EMD")
        self.geometry("900x500")
        self.resizable(False, False)
        
        self.parent = parent # Guardamos la referencia
        self.transient(parent)
        self.grab_set()

        # --- AÑADIMOS ESTA LÍNEA ---
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # -----------------------------

        self.controller = UsuarioController()

        # ... (El resto de tu código de __init__ no cambia) ...
        ctk.CTkLabel(self, text="🧑‍💻 Gestión de Usuarios", font=("Arial", 22, "bold")).pack(pady=20)
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Usuario", "Rol"), show="headings", height=15)
        self.tabla.pack(padx=20, pady=10, fill="x")
        columnas = [("ID", 50), ("Nombre", 200), ("Usuario", 150), ("Rol", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=10)
        ctk.CTkButton(frame_botones, text="➕ Agregar", command=self.abrir_formulario_agregar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botones, text="✏️ Editar", command=self.abrir_formulario_editar).grid(row=0, column=1, padx=10)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", command=self.eliminar_usuario, fg_color="red").grid(row=0, column=2, padx=10)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar", command=self.mostrar_usuarios).grid(row=0, column=3, padx=10)
        self.mostrar_usuarios()

    # --- AÑADIMOS ESTA NUEVA FUNCIÓN ---
    def on_closing(self):
        """Se ejecuta al presionar la 'X'."""
        self.parent.deiconify() # Le dice al menú admin que reaparezca
        self.destroy() # Se destruye a sí misma
    # -----------------------------------

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

# --- El resto del archivo (FormularioUsuario) no necesita cambios ---
class FormularioUsuario(ctk.CTkToplevel):
    def __init__(self, parent, modo, controller, callback, datos=None):
        super().__init__(parent)
        self.title("Formulario de Usuario")
        self.geometry("400x450")
        self.modo = modo
        self.controller = controller 
        self.callback = callback
        self.transient(parent)
        self.grab_set()
        titulo = "Agregar Usuario" if modo == "agregar" else "Editar Usuario"
        ctk.CTkLabel(self, text=titulo, font=("Arial", 18, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Nombre Completo:").pack()
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre Apellido", width=250)
        self.nombre.pack(pady=5)
        ctk.CTkLabel(self, text="Usuario (login):").pack()
        self.usuario = ctk.CTkEntry(self, placeholder_text="Ej. mcajero", width=250)
        self.usuario.pack(pady=5)
        ctk.CTkLabel(self, text="Contraseña:").pack()
        placeholder_pass = "Nueva contraseña" if modo == "editar" else "Contraseña"
        self.contrasena = ctk.CTkEntry(self, placeholder_text=placeholder_pass, show="*", width=250)
        self.contrasena.pack(pady=5)
        if modo == "editar":
             ctk.CTkLabel(self, text="(Dejar en blanco para no cambiarla)", font=("Arial", 10)).pack()
        ctk.CTkLabel(self, text="Rol:").pack()
        self.rol = ctk.CTkComboBox(self, values=["admin", "cajero"], width=250)
        self.rol.pack(pady=10)
        if datos:
            self.id_usuario = datos[0]
            self.nombre.insert(0, datos[1])
            self.usuario.insert(0, datos[2])
            self.rol.set(datos[3])
        else:
            self.rol.set("cajero")
        texto_boton = "Guardar Cambios" if modo == "editar" else "Agregar Usuario"
        ctk.CTkButton(self, text=texto_boton, command=self.guardar, height=40).pack(pady=20)

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