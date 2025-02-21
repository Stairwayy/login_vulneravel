# 🚀 Flask Vulnerable Login Page

Este repositório contém uma aplicação web de login desenvolvida em **Python** utilizando **Flask** e **SQLite**. O objetivo deste projeto é demonstrar vulnerabilidades comuns em autenticação para fins educacionais, como **SQL Injection**, **CSRF (Cross-Site Request Forgery)** e **XSS (Cross-Site Scripting)**.

⚠ **Atenção:** Este código possui vulnerabilidades intencionais.

---

## 📌 Funcionalidades
- 📌 Página de login vulnerável a **SQL Injection**
- 📌 Página de alteração de senha vulnerável a **CSRF**
- 📌 Página vulnerável a **XSS (Cross-Site Scripting)**
- 📌 Banco de dados SQLite para armazenar usuários
- 📌 Implementação básica com Flask

---

## 🚀 Tecnologias Utilizadas
- **Python** (Flask, SQLite3)
- **HTML/CSS** (para os formulários de login e alteração de senha)

---

## ⚠️ Vulnerabilidades Demonstradas

### 🔥 1. SQL Injection
A aplicação permite injeção de SQL na consulta de login.

#### 🔴 Código vulnerável
```py
query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{password}'"
cursor.execute(query)
```

#### ✅ Código corrigido
```py
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (user, password))
```
📌 Por que isso impede SQL Injection?
Os valores user e password são tratados como parâmetros, não como parte do SQL, evitando manipulação da consulta.

### 🔥 2. CSRF (Cross-Site Request Forgery)
A página de alteração de senha **não** possui proteção contra CSRF, permitindo que um atacante altere a senha do usuário sem seu consentimento.
Precisamos de tokens CSRF para garantir que a requisição vem do próprio site.

#### ✅ Passo 1: Instalar a biblioteca Flask-WTF
```
pip install flask-wtf
```
#### ✅ Passo 2: Criar um SECRET_KEY no app.py
Adicione esta linha no início do app.py:
```py
app.config['SECRET_KEY'] = 'chave_super_secreta'
```
#### ✅ Passo 3: Modificar o formulário para incluir um token CSRF
Atualizar a função change_password():
```py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)  # Ativando proteção CSRF

class ChangePasswordForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    new_password = PasswordField("Nova Senha", validators=[DataRequired()])
    submit = SubmitField("Alterar Senha")
   
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        new_password = form.new_password.data

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        conn.close()

        return "Senha alterada com sucesso!"

    return render_template("change_password.html", form=form)

```
### 🔥 3. XSS (Cross-Site Scripting)
A aplicação não sanitiza corretamente as entradas do usuário, permitindo ataques de **XSS**.

#### 🔴 Código vulnerável
```
return f"<h1>Bem-vindo, {username}!</h1>"
```

#### ✅ Código corrigido

```
from markupsafe import escape

return f"<h1>Bem-vindo, {escape(username)}!</h1>"
```
📌 Por que isso impede XSS?
escape() converte caracteres especiais (< > " ' &) em entidades HTML seguras.


---

