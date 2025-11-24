# generar_assets.py
from PIL import Image, ImageDraw
import os

# Asegurar que existe la carpeta assets
if not os.path.exists("assets"):
    os.makedirs("assets")

def crear_icono(nombre, color_fondo, simbolo, color_simbolo="white"):
    """Crea un icono cuadrado con un diseño simple"""
    size = (100, 100)
    img = Image.new('RGBA', size, (0, 0, 0, 0)) # Transparente
    draw = ImageDraw.Draw(img)
    
    # Círculo de fondo
    draw.ellipse([5, 5, 95, 95], fill=color_fondo)
    
    # Dibujamos algo simple representativo (Rectángulos o lineas)
    if simbolo == "venta": # Carrito
        draw.rectangle([30, 40, 70, 60], fill=color_simbolo)
        draw.ellipse([35, 65, 45, 75], fill=color_simbolo)
        draw.ellipse([60, 65, 70, 75], fill=color_simbolo)
    elif simbolo == "caja": # Inventario
        draw.rectangle([25, 35, 75, 75], fill=color_simbolo)
        draw.line([25, 35, 50, 55, 75, 35], fill="black", width=2)
    elif simbolo == "user": # Usuario
        draw.ellipse([35, 20, 65, 50], fill=color_simbolo)
        draw.pieslice([20, 55, 80, 115], 180, 360, fill=color_simbolo)
    elif simbolo == "chart": # Reporte
        draw.rectangle([30, 50, 40, 75], fill=color_simbolo)
        draw.rectangle([45, 35, 55, 75], fill=color_simbolo)
        draw.rectangle([60, 20, 70, 75], fill=color_simbolo)
    elif simbolo == "exit": # Salir
        draw.polygon([(40, 30), (70, 50), (40, 70)], fill=color_simbolo)
        draw.rectangle([20, 45, 40, 55], fill=color_simbolo)
    elif simbolo == "pdf": # PDF
        draw.rectangle([30, 20, 70, 80], fill="white")
        draw.text((35, 40), "PDF", fill="red")
    
    img.save(f"assets/{nombre}.png")
    print(f"Generado: assets/{nombre}.png")

# Colores de la paleta Fogón (Ladrillo, Naranja, Café)
c_ladrillo = "#D35400"
c_naranja = "#E67E22"
c_azul = "#2980B9"
c_rojo = "#C0392B"
c_verde = "#27AE60"

# Generamos los iconos
crear_icono("icon_ventas", c_naranja, "venta")
crear_icono("icon_inventario", c_azul, "caja")
crear_icono("icon_usuarios", c_ladrillo, "user")
crear_icono("icon_reportes", c_verde, "chart")
crear_icono("icon_salir", c_rojo, "exit")
crear_icono("icon_pdf", "red", "pdf")

print("¡Íconos listos! Revisa tu carpeta assets.")