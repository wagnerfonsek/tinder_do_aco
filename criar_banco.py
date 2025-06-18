import sqlite3

# Conectar ao banco (ele será criado se ainda não existir)
conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

# Criar a tabela de usuários
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

# Fechar conexão
conexao.commit()
conexao.close()

print("Banco de dados e tabela criados com sucesso!")
