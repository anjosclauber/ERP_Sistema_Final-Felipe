# db.py
import mysql.connector
from mysql.connector import Error

def conectar():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.
    Ajuste as credenciais se necessário.
    """
    try:
        con = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="MAJu2022@",
            database="erp_sistema"
        )
        if con.is_connected():
            return con
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None
