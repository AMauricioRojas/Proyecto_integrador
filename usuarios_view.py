# usuarios_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from db import conectar

class UsuariosVentana(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Usuarios - Fogón EMD")
        self.geometry("900x500")
        self.resizable(False, False)
        
        # Modal
        self.transient(parent)
        self.grab_set()

        # Conectar a la base de datos
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()

        # Título
        ctk.CTkLabel(self, text="🧑‍💻 Gestión de Usuarios", font=("Arial", 22, "bold")).pack(pady=20)

        # Tabla de usuarios
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Usuario", "Rol"), show="headings", height=15)
        self.tabla.pack(padx=20, pady=10, fill="x")

        # Configurar columnas
        columnas = [("ID", 50), ("Nombre", 200), ("Usuario", 150), ("Rol", 100)]
        for col, ancho in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        # Botones de acciones
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=10)

        ctk.CTkButton(frame_botones, text="➕ Agregar", command=self.abrir_formulario_agregar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botones, text="✏️ Editar", command=self.abrir_formulario_editar).grid(row=0, column=1, padx=10)
        ctk.CTkButton(frame_botones, text="🗑️ Eliminar", command=self.eliminar_usuario, fg_color="red").grid(row=0, column=2, padx=10)
        ctk.CTkButton(frame_botones, text="🔄 Actualizar", command=self.mostrar_usuarios).grid(row=0, column=3, padx=10)

        self.mostrar_usuarios()

    def mostrar_usuarios(self):
        """Carga los usuarios desde la base de datos"""
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        try:
            self.cursor.execute("SELECT id_usuario, nombre, usuario, rol FROM usuarios")
            for user in self.cursor.fetchall():
                self.tabla.insert("", "end", values=user)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios:\n{e}", parent=self)

    def abrir_formulario_agregar(self):
        FormularioUsuario(self, modo="agregar", conexion=self.conexion, callback=self.mostrar_usuarios)

    def abrir_formulario_editar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un usuario para editar.", parent=self)
            return
        datos = self.tabla.item(seleccionado)["values"]
        FormularioUsuario(self, modo="editar", conexion=self.conexion, datos=datos, callback=self.mostrar_usuarios)

    def eliminar_usuario(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un usuario para eliminar.", parent=self)
            return
        
        datos = self.tabla.item(seleccionado)["values"]
        id_usuario = datos[0]
        nombre_usuario = datos[1]
        
        # Evitar que se elimine el admin principal (ID 1)
        if id_usuario == 1:
            messagebox.showerror("Error", "No se puede eliminar al administrador principal.", parent=self)
            return

        if messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar a '{nombre_usuario}'?", parent=self):
            try:
                self.cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
                self.conexion.commit()
                self.mostrar_usuarios()
                messagebox.showinfo("Eliminado", "Usuario eliminado correctamente.", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el usuario:\n{e}", parent=self)


class FormularioUsuario(ctk.CTkToplevel):
    def __init__(self, parent, modo, conexion, callback, datos=None):
        super().__init__(parent)
        self.title("Formulario de Usuario")
        self.geometry("400x450")
        
        self.modo = modo
        self.conexion = conexion
        self.callback = callback
        self.cursor = self.conexion.cursor()
        
        # Modal
        self.transient(parent)
        self.grab_set()

        titulo = "Agregar Usuario" if modo == "agregar" else "Editar Usuario"
        ctk.CTkLabel(self, text=titulo, font=("Arial", 18, "bold")).pack(pady=20)

        # Campos
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
            self.rol.set("cajero") # Por defecto

        texto_boton = "Guardar Cambios" if modo == "editar" else "Agregar Usuario"
        ctk.CTkButton(self, text=texto_boton, command=self.guardar, height=40).pack(pady=20)

    def guardar(self):
        nombre = self.nombre.get().strip()
        usuario = self.usuario.get().strip()
        contrasena = self.contrasena.get().strip()
        rol = self.rol.get()

        if not nombre or not usuario:
            messagebox.showwarning("Campos vacíos", "El Nombre y el Usuario son obligatorios.", parent=self)
            return

        try:
            if self.modo == "agregar":
                if not contrasena:
                    messagebox.showwarning("Campos vacíos", "La Contraseña es obligatoria para usuarios nuevos.", parent=self)
                    return
                self.cursor.execute(
                    "INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES (%s, %s, %s, %s)",
                    (nombre, usuario, contrasena, rol)
                )
            else: # Modo "editar"
                if contrasena: # Si el usuario escribió una nueva contraseña
                    self.cursor.execute(
                        "UPDATE usuarios SET nombre=%s, usuario=%s, contrasena=%s, rol=%s WHERE id_usuario=%s",
                        (nombre, usuario, contrasena, rol, self.id_usuario)
                    )
                else: # Si dejó la contraseña en blanco, no la actualizamos
                    self.cursor.execute(
                        "UPDATE usuarios SET nombre=%s, usuario=%s, rol=%s WHERE id_usuario=%s",
                        (nombre, usuario, rol, self.id_usuario)
                    )

            self.conexion.commit()
            messagebox.showinfo("Éxito", "Usuario guardado correctamente.", parent=self)
            self.callback() # Actualiza la tabla en la ventana anterior
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario:\n{e}", parent=self)