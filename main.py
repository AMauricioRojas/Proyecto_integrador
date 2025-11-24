# main.py
import customtkinter as ctk
from login_view import LoginVentana
import os

if __name__ == "__main__":
    # Configuración visual
    ctk.set_appearance_mode("light")
    
    ctk.set_default_color_theme("dark-blue") 
    # ----------------------------------------------
    
    app = LoginVentana()
    app.mainloop()