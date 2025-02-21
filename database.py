import sqlite3
import os

def criar_banco():
    db_path = os.path.abspath("usuarios.db")
    print(f"Criando banco de dados em: {db_path}")

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Verificar se o usuário já existe antes de inserir
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe no banco de dados.")

    conn.commit()
    conn.close()
    return cursor

if __name__ == "__main__":
    cursor = criar_banco()
    print("Banco de dados configurado com sucesso!")
