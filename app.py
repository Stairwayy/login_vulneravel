from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    # Função para criar e retornar uma conexão com o banco de dados
    conn = sqlite3.connect("usuarios.db")
    return conn

# Rota criada para a página de login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        # Criando conexão com o banco dentro da função
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta INSEGURA (SQL Injection)
        query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        if result:
            return render_template("home.html", username=user)
        else:
            return "Login falhou! Verifique suas credenciais."

    return render_template("login.html")

#Rota Change Password
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"UPDATE users SET password = '{new_password}' WHERE username = '{username}'")
        conn.commit()
        conn.close()

        return"Senha alterada com sucesso!"
    
    return '''
        <form method="post">
            Usuário: <input type="text" name="username"><br>
            Nova senha: <input type="password" name="new_password"><br>
            <button type="submit">Alterar Senha</button>
        </form>
    '''
if __name__ == "__main__":
    app.run(debug=True)
