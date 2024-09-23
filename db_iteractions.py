#Para quem ja esta mais acostumado com devweb, este seria equivalente à nosso Repository File.
#Por simplicidade estarei evitando estes nomes técnicos, sirva de referencia para quem quiser ir mais a fundo
from mysql.connector import Error
from dotenv import load_dotenv
import mysql.connector
from typing import *
import os

################################################################################################################
###################### Conexão ao db e rota morta, para ver se estamos conectando ##############################
################################################################################################################

load_dotenv('.cred')
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  
    'user': os.getenv('DB_USER'),  
    'password': os.getenv('DB_PASSWORD'),  
    'database': os.getenv('DB_NAME', 'db_biblioteca'),  
    'port': int(os.getenv('DB_PORT', 3306)),  
    'ssl_ca': os.getenv('SSL_CA_PATH')  
}

def connect_db():
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        return None
    
################ Código Auxiliares #########################

#IMPORTANTE: Note que utilizo varios f strings no código. NUNCA faça isso em uma situação real, pois isso cria sistemas vulneraveis a SQL Injection
#Sempre dê prioridade à utilizar % commands ou seu próprio verificador de injections

#Pega todos da tabela fornecida
def get_all(cursor : object, table : str) -> Dict:
    sql = f"SELECT * FROM {table}"
    cursor.execute(sql)
    return cursor.fetchall()

def get_single_by_id(cursor : object, table : str, id : int) -> Dict:
    sql = f"SELECT * FROM {table} WHERE id = %s"
    cursor.execute(sql, (id,))
    return cursor.fetchone()

#Adiciona usuario na tabela de usuarios
def add_user(cursor : object, name : str, cpf : str, age : int) -> int:
    sql = "INSERT INTO tbl_usuarios (nome, cpf, idade) VALUES (%s, %s, %s)" 
    cursor.execute(sql, (name, cpf, age))
    return cursor.lastrowid

def add_book(cursor : object, name : str, author : str, isbn : str) -> int:
    sql = "INSERT INTO tbl_livros (titulo, autor, isbn) VALUES (%s, %s, %s)"  
    cursor.execute(sql, (name, author, isbn))
    return cursor.lastrowid

def add_rent(cursor : object, usuario_id : int, livro_id : int) -> int:
    sql = "INSERT INTO tbl_emprestimos (usuario_id, livro_id) VALUES (%s, %s)"
    cursor.execute(sql, (usuario_id, livro_id))
    return cursor.lastrowid

def delete_by_id(cursor : object, table : str, id : int) -> None:
    sql = f"DELETE FROM {table} WHERE id = %s"
    cursor.execute(sql, (id,))

def edit_table_by_id(cursor : object, table : str, field : str, new_value : any, id : int) -> None:
    #IMPORTANTE: Utilizo um for para editar uma coluna por vez da tabela. Faço isso pela **FACILIDADE** em entender, compactar e re-utilizar o código
    #Fazer multiplas edições ao mesmo tempo SEMPRE é mais eficiente em um cenario real
    sql = f"UPDATE {table} SET {field} = %s WHERE id = %s" 
    cursor.execute(sql, (new_value, id))

