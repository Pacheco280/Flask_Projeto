from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criar banco de dados e tabela
def init_db():
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    mensagem = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        
        with sqlite3.connect("usuarios.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
            user = cursor.fetchone()
        
        if user:
            return redirect(url_for("sucesso"))
        else:
            mensagem = "Login incorreto. Tente novamente."
    
    return render_template("login.html", mensagem=mensagem)

@app.route("/sucesso")
def sucesso():
    return "Login realizado com sucesso!"

@app.route("/register", methods=["GET", "POST"])
def register():
    mensagem = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        
        with sqlite3.connect("usuarios.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
                conn.commit()
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                mensagem = "Usuário já cadastrado. Tente outro."
    
    return render_template("register.html", mensagem=mensagem)

if __name__ == "__main__":
    app.run(debug=True)
