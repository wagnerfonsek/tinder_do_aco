from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Função para conectar ao banco
def conectar_banco():
    # Usa caminho absoluto para banco.db na mesma pasta do app
    db_path = os.path.join(os.path.dirname(__file__), 'banco.db')
    conn = sqlite3.connect(db_path)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            idade = request.form.get('idade')
            genero = request.form.get('genero')
            celular = request.form.get('celular')
            senha = request.form.get('senha')
            objetivo = request.form.get('objetivo')

            conn = conectar_banco()
            cursor = conn.cursor()
            # Garante criação da tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL,
                    genero TEXT NOT NULL,
                    celular TEXT NOT NULL,
                    senha TEXT NOT NULL,
                    objetivo TEXT NOT NULL
                )
            ''')
            # Insere o usuário
            cursor.execute('''
                INSERT INTO usuarios (nome, idade, genero, celular, senha, objetivo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, idade, genero, celular, senha, objetivo))
            conn.commit()
            conn.close()
            return redirect(url_for('boas_vindas', nome=nome))
        except Exception as e:
            app.logger.error('Erro no cadastro: %s', e, exc_info=True)
            return 'Erro interno ao cadastrar. Verifique logs.', 500
    return render_template('cadastro.html')

@app.route('/boas_vindas')
def boas_vindas():
    nome = request.args.get('nome', 'Usuário')
    return render_template('boas_vindas.html', nome=nome)

# Exemplo de rota perfil, descomente se necessário:
# @app.route('/perfil/<username>')
# def perfil(username):
#     conn = conectar_banco()
#     cursor = conn.cursor()
#     cursor.execute("SELECT nome, idade, objetivo FROM usuarios WHERE nome = ?", (username,))
#     resultado = cursor.fetchone()
#     conn.close()
#     if resultado:
#         usuario = {
#             'nome': resultado[0],
#             'idade': resultado[1],
#             'bio': f"{resultado[0]} tem {resultado[1]} anos e o objetivo é {resultado[2]}",
#             'objetivo': resultado[2],
#             'foto': 'perfil1.jpg'
#         }
#         return render_template('perfil.html', **usuario)
#     return f"Usuário {username} não encontrado."

if __name__ == '__main__':
    app.run(debug=True)
