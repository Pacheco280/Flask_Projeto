from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
            return redirect(url_for("dashboard"))
        else:
            mensagem = "Login incorreto. Tente novamente."
    
    return render_template("login.html", mensagem=mensagem)

@app.route("/dashboard")
def dashboard():
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
    return render_template("dashboard.html", usuarios=usuarios)

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

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        user = cursor.fetchone()
    
    if request.method == "POST":
        novo_usuario = request.form["usuario"]
        nova_senha = request.form["senha"]
        with sqlite3.connect("usuarios.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET usuario = ?, senha = ? WHERE id = ?", (novo_usuario, nova_senha, id))
            conn.commit()
        return redirect(url_for("dashboard"))
    
    return render_template("edit.html", user=user)

@app.route("/delete/<int:id>")
def delete(id):
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)

