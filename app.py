from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Função para conectar ao banco
def conectar_banco():
    db_path = os.path.join(os.path.dirname(__file__), 'banco.db')
    conn = sqlite3.connect(db_path)
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for('perfil', username=usuario))
        else:
            return "Login inválido! Tente novamente."

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
            cursor.execute('''
                INSERT INTO usuarios (nome, idade, genero, celular, senha, objetivo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, idade, genero, celular, senha, objetivo))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            app.logger.error('Erro no cadastro: %s', e, exc_info=True)
            return 'Erro interno ao cadastrar. Verifique logs.', 500
    return render_template('cadastro.html')

@app.route('/boas_vindas')
def boas_vindas():
    nome = request.args.get('nome', 'Usuário')
    return render_template('boas_vindas.html', nome=nome)

# Rota de perfil
@app.route('/perfil/<username>')
def perfil(username):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, idade, objetivo FROM usuarios WHERE nome = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        usuario = {
            'nome': resultado[0],
            'idade': resultado[1],
            'objetivo': resultado[2]
        }
        return render_template('perfil.html', **usuario)

    return f"Usuário {username} não encontrado."
@app.route('/login')
def login():
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
