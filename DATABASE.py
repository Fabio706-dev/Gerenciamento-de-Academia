import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import Error  

load_dotenv()

passeword = os.getenv("password")
def conecta():
    try: 
         conn = psycopg2.connect(
          host="localhost",
          database="trabalho",
          user="postgres",
          password=passeword,
          port="5432")
         
         print("Conexão com o banco de dados realizada com sucesso!")
         
         return conn
     
     
    except Error as e:
        print(f"ocorreu um erro ao tentar se conectar ao banco de dados: {e}")
    
def encerra_conexao(conn):
    if conn:
        conn.close()
        print("Conexão com o banco de dados encerrada!")


def executar(conn, sql, params=()):
    """INSERT, UPDATE, DELETE e CREATE: executa e salva (commit)."""
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()


def consultar(conn, sql, params=()):
    """SELECT: devolve uma lista de linhas (cada linha é uma tupla)."""
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        cursor.close()