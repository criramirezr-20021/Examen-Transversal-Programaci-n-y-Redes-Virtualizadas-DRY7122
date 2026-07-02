import sqlite3
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def crear_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    usuario = "Cristobal Ramirez"
    password = "Duoc.2026"

    cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (usuario,))
    existe = cursor.fetchone()

    if existe is None:
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)",
            (usuario, password_hash)
        )

    conexion.commit()
    conexion.close()

@app.route("/")
def inicio():
    return """
    <h1>Login Examen DRY7122</h1>
    <form method="POST" action="/login">
        <label>Usuario:</label><br>
        <input type="text" name="usuario"><br><br>

        <label>Contraseña:</label><br>
        <input type="password" name="password"><br><br>

        <button type="submit">Ingresar</button>
    </form>
    """

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    password = request.form["password"]

    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (usuario,))
    resultado = cursor.fetchone()

    conexion.close()

    if resultado and check_password_hash(resultado[0], password):
        return "<h2>Acceso permitido</h2>"
    else:
        return "<h2>Usuario o contraseña incorrectos</h2>"

if __name__ == "__main__":
    crear_base_datos()
    app.run(host="0.0.0.0", port=7500)
