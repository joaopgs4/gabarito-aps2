from flask import Flask, request
from mysql.connector import Error

from db_iteractions import *
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def index():
    return {"mensagem": "Sucesso"}, 200

################################################################################################################
########################################### Código à baixo #####################################################
################################################################################################################


# Aviso: Todos os returns são realiados em forma de dicionario, pois o FRAMEWORK do Flask (e a maioria dos framworks python, como FastAPI e Sanic)
# São capazes de identificar que um retorno em dicionario é para ser convertido em JSON, assim não precisamos do Jsonify.
#E NTENDA por que podemos ignorar esta função, por que ela existe e por que ela é util em certos casos ou outras linguagens


############# Rotas de Usuario #############

@app.route("/usuarios", methods=["POST, GET"]) #Podemos dividir em multiplas funções, mas prefiro dividir por rotas
def users_root():
    #Conexão na DB
    conn = connect_db()
    if conn.is_connected():
        cursor = conn.cursor()
    else:
        return {"Erro": "Cursor não conectado"}, 500
    
    try:
        #Rota de Get
        if request.method == "GET":
            users = get_all(cursor, "tbl_usuarios")
            user_list = []
            for user in users:
                #Usamos um for para formatar o retorno, já que a função é bem ampla e queremos manter qualidade de visualização. 
                #Poderiamos retornar direto o json do cursor sem formatação tambem (como vocês vão ver em códigos reais de produção)
                user_list.append({'ID: ': user[0], 'Nome: ': user[1], 'CPF: ': user[2], 'Idade: ': user[3]}) 
            return {"Usuarios: ": user_list}, 200

        #Rota de Post
        if request.method == "POST":
            data = request.json
            mandatory_fields = ['nome', 'cpf']
            if not all(field in data for field in mandatory_fields):
                return {"Erro: ": "Campos obrigatórios pendentes"}, 400
            new_user_id = add_user(cursor, data['nome'], data['cpf'], data['idade'])  
            conn.commit()
            return {"Sucesso: ": f"Usuario de id {new_user_id} criado com sucesso"}, 201
            
        #Rotas invalidas
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Error as e:
        return {"Erro: ": e}, 500
        
    finally:
        cursor.close()
        conn.close()


@app.route("/usuarios/<int:id>", methods=["GET", "PUT", "DELETE"])
def user_by_id(id : int):
    conn = connect_db()
    if conn.is_connected():
        cursor = conn.cursor()
    else:
        return {"Erro": "Cursor não conectado"}, 500
    
    try:
        user = get_single_by_id(cursor, "tbl_usuarios", id)

        if not user:
            {"Erro: ": f"Usuario de ID {id} inexistente"}, 400
        
        if request.method == "GET":
            return {"Usuario: ": user}, 200

        if request.method == "PUT":
            data = request.json
            for field in user:
                edit_table_by_id(cursor, "tbl_usuarios", field, data[field])
            conn.commit()
            return {"Sucesso: ": f"Usuario de ID {id} editado com sucesso"}, 200

        if request.method == "DELETE":
            delete_by_id(cursor, "tbl_usuarios", id)
            conn.commit()
            return {"Sucesso: ": f"Usuario de ID {id} deletado com sucesso"}, 200
                
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Error as e:
        return {"Erro: ": e}, 500
    
    finally:
        cursor.close()
        conn.close()
        


############# Rotas de Livros #############
@app.route("/livros", methods=["POST, GET"]) #Podemos dividir em multiplas funções, mas prefiro dividir por rotas
def livros_root():
    #Conexão na DB
    conn = connect_db()
    if conn.is_connected():
        cursor = conn.cursor()
    else:
        return {"Erro": "Cursor não conectado"}, 500
    
    try:
        #Rota de Get
        if request.method == "GET":
            books = get_all(cursor, "tbl_livros")
            book_list = []
            for book in books:
                book_list.append({'ID: ': book[0], 'Titulo: ': book[1], 'Autor: ': book[2], 'ISBN: ': book[3]}) 
            return {"Livros: ": book_list}, 200

        #Rota de Post
        if request.method == "POST":
            data = request.json
            mandatory_fields = ['titulo', 'autor', 'isbn']
            if not all(field in data for field in mandatory_fields):
                return {"Erro: ": "Campos obrigatórios pendentes"}, 400
            new_book_id = add_book(cursor, data['titulo'], data['autor'], data['isbn'])
            conn.commit()
            return {"Sucesso: ": f"Livro de id {new_book_id} criado com sucesso"}, 201
            
        #Rotas invalidas
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Error as e:
        return {"Erro: ": e}, 500
        
    finally:
        cursor.close()
        conn.close()


@app.route("/livros/<int:id>", methods=["GET", "PUT", "DELETE"])
def livros_by_id(id : int):
    conn = connect_db()
    if conn.is_connected():
        cursor = conn.cursor()
    else:
        return {"Erro": "Cursor não conectado"}, 500
    
    try:
        book = get_single_by_id(cursor, "tbl_livros", id)

        if not book:
            {"Erro: ": f"Usuario de ID {id} inexistente"}, 400
        
        if request.method == "GET":
            return {"Livro: ": book}, 200

        if request.method == "PUT":
            data = request.json
            for field in book:
                edit_table_by_id(cursor, "tbl_livros", field, data[field])
            conn.commit()
            return {"Sucesso: ": f"Livro de ID {id} editado com sucesso"}, 200

        if request.method == "DELETE":
            delete_by_id(cursor, "tbl_livros", id)
            conn.commit()
            return {"Sucesso: ": f"Livro de ID {id} deletado com sucesso"}, 200
                
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Error as e:
        return {"Erro: ": e}, 500
    
    finally:
        cursor.close()
        conn.close()

############# Rotas de Empréstimos #############
@app.route("/emprestimos", methods=["POST, GET"]) #Podemos dividir em multiplas funções, mas prefiro dividir por rotas
def emprestimos_root():
    #Conexão na DB
    conn = connect_db()
    if conn.is_connected():
        cursor = conn.cursor()
    else:
        return {"Erro": "Cursor não conectado"}, 500
    
    try:
        #Rota de Get
        if request.method == "GET":
            rents = get_all(cursor, "tbl_emprestimos")
            rent_list = []
            for rent in rents:
                rent_list.append({'ID: ': rent[0], 'id_usuario: ': rent[1], 'id_livro: ': rent[2]}) 
            return {"Emprestimos: ": rent_list}, 200

        #Rota de Post
        if request.method == "POST":
            data = request.json
            mandatory_fields = ['id_usuario', 'id_livro']
            if not all(field in data for field in mandatory_fields):
                return {"Erro: ": "Campos obrigatórios pendentes"}, 400
            user = get_single_by_id(cursor, "tbl_usuarios", data['id_usuario'])
            book = get_single_by_id(cursor, "tbl_usuarios", data['id_usuario'])
            if not user or not book:
                return {"Erro: ": "Usuario ou livro inexistentes"}, 400
            
            new_rent_id = add_rent(cursor, data['id_usuario'], data['id_livro'])
            conn.commit()
            return {"Sucesso: ": f"Empréstimo de id {new_rent_id} criado com sucesso"}, 201
            
        #Rotas invalidas
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Error as e:
        return {"Erro: ": e}, 500
        
    finally:
        cursor.close()
        conn.close()


@app.route("/emprestimos/<int:id>", methods=["GET", "DELETE"]) #Não precisamos editar emprestimo
def emprestimos_by_id(id : int):
    conn = connect_db()
    if conn.is_connected():
        cursor = conn.cursor()
    else:
        return {"Erro": "Cursor não conectado"}, 500
    
    try:
        rent = get_single_by_id(cursor, "tbl_emprestimos", id)

        if not rent:
            {"Erro: ": f"Empréstimo de ID {id} inexistente"}, 400
        
        if request.method == "GET":
            return {"Empréstimo: ": rent}, 200

        if request.method == "DELETE":
            delete_by_id(cursor, "tbl_emprestimos", id)
            conn.commit()
            return {"Sucesso: ": f"Empréstimo de ID {id} deletado com sucesso"}, 200
                
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Error as e:
        return {"Erro: ": e}, 500
    
    finally:
        cursor.close()
        conn.close()


# Run em modo debug, não edite abaixo


if __name__ == '__main__':
    app.run(debug=True)