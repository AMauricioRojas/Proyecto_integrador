# ticket_simple_view.py
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
import win32print # Librería para imprimir en Windows
import sys # Para detectar el OS

class TicketSimpleVentana(ctk.CTkToplevel):
    def __init__(self, parent, id_venta, productos, total, metodo_pago):
        super().__init__(parent)
        self.title(f"Ticket - Venta #{id_venta}")
        self.geometry("450x600")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()

        # === Preparamos el texto del ticket ===
        # Lo guardamos en self para poder usarlo en la función de imprimir
        self.texto_ticket = "\n"
        self.texto_ticket += "   🔥 FOGÓN EMD POS 🔥\n"
        self.texto_ticket += "     Durango, México\n"
        self.texto_ticket += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        self.texto_ticket += f"Venta ID: {id_venta}\n"
        self.texto_ticket += "----------------------------------------\n"
        self.texto_ticket += f"{'Producto':<20}{'Cant':<5}{'P.Unit':<10}{'Subtotal':>10}\n"
        self.texto_ticket += "----------------------------------------\n"

        # (nombre, cantidad, precio, subtotal)
        for nombre, cantidad, precio_unit, subtotal in productos:
            nombre_corto = nombre[:19]
            cant_str = str(cantidad)
            precio_str = f"${precio_unit:,.2f}"
            sub_str = f"${subtotal:,.2f}"
            
            self.texto_ticket += f"{nombre_corto:<20}{cant_str:<5}{precio_str:<10}{sub_str:>10}\n"

        self.texto_ticket += "----------------------------------------\n"
        self.texto_ticket += f"Método de pago: {metodo_pago}\n"
        self.texto_ticket += "\n"
        self.texto_ticket += f"            TOTAL: ${total:,.2f}\n"
        self.texto_ticket += "\n"
        self.texto_ticket += "      ¡Gracias por su compra!\n"
        

        # === Mostramos el texto en un Textbox ===
        textbox = ctk.CTkTextbox(self, font=("Consolas", 12), wrap="none")
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        textbox.insert("1.0", self.texto_ticket)
        textbox.configure(state="disabled")

        # === Frame para los nuevos botones ===
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=10, padx=10, fill="x")
        
        # Distribuimos los botones
        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(frame_botones, text="🖨️ Imprimir", command=self.imprimir_ticket, height=40).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(frame_botones, text="Cerrar", command=self.destroy, height=40, fg_color="gray").grid(row=0, column=1, padx=5, sticky="ew")

    def imprimir_ticket(self):
        """
        Función para enviar el texto crudo a la impresora.
        AHORA ESTÁ SIMULADO.
        """
        
        # --- SIMULACIÓN (ESTO ES LO QUE VERÁS AHORA) ---
        messagebox.showinfo(
            "Impresión (Simulación)",
            "Enviando a la impresora de tickets...\n\n(Esto es una simulación. El código real está comentado en 'ticket_simple_view.py')"
        )
        return
        
        # --- CÓDIGO REAL (PARA EL FUTURO, CUANDO TENGAS IMPRESORA) ---
        # 1. Borra el 'return' y el messagebox de arriba.
        # 2. Descomenta todo lo de abajo.
        # 3. Cambia "Nombre_De_Tu_Impresora_De_Tickets" por el nombre real de la impresora
        #    (ej. "EPSON TM-T20II" o el nombre que aparezca en Windows).
        
        # if sys.platform != "win32":
        #     messagebox.showerror("Error", "La impresión directa solo está soportada en Windows.")
        #     return

        # printer_name = "Nombre_De_Tu_Impresora_De_Tickets"
        
        # try:
        #     # Abrir la impresora
        #     hPrinter = win32print.OpenPrinter(printer_name)
        #     try:
        #         # Iniciar un documento de impresión
        #         hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket Fogón EMD", None, "RAW"))
        #         try:
        #             win32print.StartPagePrinter(hJob)
        #             # Escribir el texto crudo (bytes) en la impresora
        #             win32print.WritePrinter(hJob, self.texto_ticket.encode('utf-8'))
        #             win32print.EndPagePrinter(hJob)
        #         finally:
        #             win32print.EndDocPrinter(hJob)
        #     finally:
        #         win32print.ClosePrinter(hPrinter)
            
        #     messagebox.showinfo("Éxito", "Ticket enviado a la impresora.")
            
        # except Exception as e:
        #     messagebox.showerror("Error de Impresión", f"No se pudo imprimir:\n{e}\n\nVerifica que la impresora '{printer_name}' esté conectada y el nombre sea correcto.")