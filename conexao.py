import mysql.connector
from tkinter import messagebox

def conectar():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",  # ajuste sua senha
            database="erp_sistema"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Erro de conexão", f"Não foi possível conectar ao banco:\n{e}")
        return None
