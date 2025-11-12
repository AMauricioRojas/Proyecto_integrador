# db.py
import mysql.connector
from mysql.connector import Error

def conectar():
    """Conecta con la base de datos EMD_POS"""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',         
            password='',          
            database='EMD_POS'
        )
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos EMD_POS")
            return conexion
    except Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None
