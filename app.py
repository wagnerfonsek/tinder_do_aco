from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco
def conectar_banco():
    return sqlite3.connect('banco.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        genero = request.form["genero"]
        celular = request.form["celular"]
        senha = request.form["senha"]
        objetivo = request.form["objetivo"]

        conn = conectar_banco()
        cursor = conn.cursor()

        # Inserindo no banco
        cursor.execute("""
            INSERT INTO usuarios (nome, idade, genero, celular, senha, objetivo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, idade, genero, celular, senha, objetivo))

        conn.commit()
        conn.close()

        return redirect(url_for('boas_vindas', nome=nome))

    return render_template("cadastro.html")

@app.route('/boas_vindas')
def boas_vindas():
    nome = request.args.get('nome', 'Usuário')
    return render_template('boas_vindas.html', nome=nome)

@app.route('/perfil/<username>')
def perfil(username):
    # Exemplo de usuário fictício, depois você pode puxar do banco
    usuario = {
        'nome': 'vinicius(gatinho)',
        'idade': 37,
        'bio': 'Sou mecânico e amante do meu chefe!',
        'objetivo': 'sair do arame',
        'foto': 'perfil1.jpg'  # Corrigido o nome da imagem
    }
    return render_template('perfil.html', **usuario)

if __name__ == '__main__':
    app.run(debug=True)
