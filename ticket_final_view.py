# ticket_final_view.py
import customtkinter as ctk
from datetime import datetime
from ticket_pdf import generar_ticket_pdf
from tkinter import messagebox

class TicketFinalVentana(ctk.CTkToplevel):
    def __init__(self, parent, id_venta, productos, total, metodo_pago):
        super().__init__(parent)
        self.title(f"Desglose Final - Venta #{id_venta}")
        self.geometry("500x600")
        self.resizable(False, False)
        self.id_venta = id_venta
        self.productos = productos
        self.total = total
        self.metodo_pago = metodo_pago

        # === ENCABEZADO ===
        ctk.CTkLabel(self, text="Fogón EMD POS", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Durango, México", font=("Arial", 14)).pack()

        ctk.CTkLabel(self, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", font=("Arial", 12)).pack(pady=5)
        ctk.CTkLabel(self, text=f"ID Venta: {id_venta}", font=("Arial", 12)).pack()

        # === LÍNEA SEPARADORA ===
        ctk.CTkLabel(self, text="----------------------------------------------", font=("Consolas", 12)).pack(pady=5)

        # === TABLA DE PRODUCTOS ===
        texto_productos = "Producto              Cant   Precio   Subtotal\n"
        texto_productos += "----------------------------------------------\n"
        for nombre, cantidad, precio, subtotal in productos:
            texto_productos += f"{nombre[:15]:15} {cantidad:<5} ${precio:<7.2f} ${subtotal:<7.2f}\n"

        self.textbox = ctk.CTkTextbox(self, width=460, height=300)
        self.textbox.pack(padx=10, pady=10)
        self.textbox.insert("1.0", texto_productos)
        self.textbox.configure(state="disabled")

        # === TOTAL Y MÉTODO DE PAGO ===
        ctk.CTkLabel(self, text="----------------------------------------------", font=("Consolas", 12)).pack(pady=5)
        ctk.CTkLabel(self, text=f"Método de pago: {metodo_pago}", font=("Arial", 14, "bold")).pack(pady=2)
        ctk.CTkLabel(self, text=f"TOTAL: ${total:.2f}", font=("Arial", 18, "bold")).pack(pady=10)

        # === BOTONES ===
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=15)

        ctk.CTkButton(frame_botones, text="💾 Guardar Ticket PDF", command=self.guardar_pdf).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botones, text="❌ Cerrar", command=self.destroy).grid(row=0, column=1, padx=10)

    def guardar_pdf(self):
        """Genera el ticket PDF usando ticket_pdf.py"""
        try:
            generar_ticket_pdf(
                id_venta=self.id_venta,
                productos=self.productos,
                total=self.total,
                nombre_cliente="Cliente General"
            )
            messagebox.showinfo("Éxito", f"Ticket PDF guardado correctamente (venta #{self.id_venta}).")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el ticket:\n{e}")
