import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Parâmetros de conexão
dbname = 'Parte-3'
user = 'WaynerYtallo'
password = 'WaynerYtallo'
host = 'database-faculdade.cdqauergwnin.us-east-1.rds.amazonaws.com'
port = '5432'
schema = 'mydb'

# Função para conectar ao banco de dados
def connect():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    return conn

@app.route('/autores', methods=['POST'])
def criar_autor():
    conn = connect()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("INSERT INTO autor (nome, quantidade_livros, data_nascimento, melhor_livro) VALUES (%s, %s, %s, %s)",
                (data['nome'], data['quantidade_livros'], data['data_nascimento'], data['melhor_livro']))
    conn.close()
    return jsonify({'mensagem': 'Autor criado com sucesso!'})

@app.route('/autores/<int:id>', methods=['GET'])
def obter_autor(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM autor WHERE id = %s", (id,))
    autor = cur.fetchone()
    conn.close()
    if autor:
        return jsonify({'id': autor[0],
                        'nome': autor[1],
                        'quantidade_livros': autor[2],
                        'data_nascimento': autor[3].strftime('%Y-%m-%d'),
                        'melhor_livro': autor[4]})
    else:
        return jsonify({'mensagem': 'Autor não encontrado!'}), 404

@app.route('/autores/<int:id>', methods=['PUT'])
def atualizar_autor(id):
    conn = connect()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("UPDATE autor SET nome = %s, quantidade_livros = %s, data_nascimento = %s, melhor_livro = %s WHERE id = %s",
                (data['nome'], data['quantidade_livros'], data['data_nascimento'], data['melhor_livro'], id))
    conn.close()
    return jsonify({'mensagem': 'Autor atualizado com sucesso!'})

@app.route('/autores/<int:id>', methods=['DELETE'])
def deletar_autor(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM autor WHERE id = %s", (id,))
    conn.close()
    return jsonify({'mensagem': 'Autor deletado com sucesso!'})

@app.route('/livros', methods=['POST'])
def criar_livro():
    conn = connect()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("INSERT INTO livro (isbn, ranking, idioma, publicacao, quantidade_paginas, tipo_capa, mc_avaliacoes, editora_cnpj) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (data['isbn'], data['ranking'], data['idioma'], data['publicacao'], data['quantidade_paginas'], data['tipo_capa'], data['mc_avaliacoes'], data['editora_cnpj']))
    conn.close()
    return jsonify({'mensagem': 'Livro criado com sucesso!'})

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM livro WHERE id = %s", (id,))
    livro = cur.fetchone()
    conn.close()
    if livro:
        return jsonify({'id': livro[0],
                        'isbn': livro[1],
                        'ranking': livro[2],
                        'idioma': livro[3],
                        'publicacao': livro[4].strftime('%Y-%m-%d %H:%M:%S'),
                        'quantidade_paginas': livro[5],
                        'tipo_capa': livro[6],
                        'mc_avaliacoes': livro[7],
                        'editora_cnpj': livro[8]})
    else:
        return jsonify({'mensagem': 'Livro não encontrado!'}), 404

@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    conn = connect()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("UPDATE livro SET isbn = %s, ranking = %s, idioma = %s, publicacao = %s, quantidade_paginas = %s, tipo_capa = %s, mc_avaliacoes = %s, editora_cnpj = %s WHERE id = %s",
                (data['isbn'], data['ranking'], data['idioma'], data['publicacao'], data['quantidade_paginas'], data['tipo_capa'], data['mc_avaliacoes'], data['editora_cnpj'], id))
    conn.close()
    return jsonify({'mensagem': 'Livro atualizado com sucesso!'})

@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM livro WHERE id = %s", (id,))
    conn.close()
    return jsonify({'mensagem': 'Livro deletado com sucesso!'})

@app.route('/autor_has_livro', methods=['POST'])
def adicionar_relacao_autor_livro():
    conn = connect()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("INSERT INTO autor_has_livro (autor_id, livro_isbn) VALUES (%s, %s)",
                (data['autor_id'], data['livro_isbn']))
    conn.close()
    return jsonify({'mensagem': 'Relação autor-livro adicionada com sucesso!'})

@app.route('/autor_has_livro/<int:autor_id>/<int:livro_isbn>', methods=['DELETE'])
def remover_relacao_autor_livro(autor_id, livro_isbn):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM autor_has_livro WHERE autor_id = %s AND livro_isbn = %s", (autor_id, livro_isbn))
    conn.close()
    return jsonify({'mensagem': 'Relação autor-livro removida com sucesso!'})

@app.route('/autor_has_livro/<int:autor_id>', methods=['GET'])
def listar_livros_autor(autor_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM livro INNER JOIN autor_has_livro ON livro.isbn = autor_has_livro.livro_isbn WHERE autor_has_livro.autor_id = %s", (autor_id,))
    livros = cur.fetchall()
    conn.close()
    if livros:
        response = []
        for livro in livros:
            response.append({'id': livro[0],
                             'isbn': livro[1],
                             'ranking': livro[2],
                             'idioma': livro[3],
                             'publicacao': livro[4].strftime('%Y-%m-%d %H:%M:%S'),
                             'quantidade_paginas': livro[5],
                             'tipo_capa': livro[6],
                             'mc_avaliacoes': livro[7],
                             'editora_cnpj': livro[8]})
        return jsonify(response)
    else:
        return jsonify({'mensagem': 'Nenhum livro encontrado para este autor!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
