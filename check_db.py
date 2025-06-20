import sqlite3

conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

# Verifica se a tabela 'usuarios' existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios';")
exists = cursor.fetchone()
if exists:
    print("Tabela 'usuarios' já existe.")
    # Opcional: mostra estrutura
    cursor.execute("PRAGMA table_info(usuarios);")
    cols = cursor.fetchall()
    print("Estrutura da tabela 'usuarios':")
    for col in cols:
        # col = (cid, name, type, notnull, dflt_value, pk)
        print(f"  - {col[1]} ({col[2]}) notnull={col[3]} pk={col[5]}")
else:
    print("Tabela 'usuarios' NÃO existe. Vamos criar agora.")
    cursor.execute('''
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        genero TEXT NOT NULL,
        celular TEXT NOT NULL,
        senha TEXT NOT NULL,
        objetivo TEXT NOT NULL
    )
    ''')
    conn.commit()
    print("Tabela 'usuarios' criada com sucesso.")

conn.close()
