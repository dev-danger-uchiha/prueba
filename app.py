import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_qa_key"

# Conexión a la base de datos (apunta a Render en producción)
def get_db_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost/testdb')
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Creación de tabla inicial
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            futbolista_favorito VARCHAR(100)
        )
    ''')
    conn.commit()
    try:
        cur.execute('ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS futbolista_favorito VARCHAR(100);')
        conn.commit()
    except Exception:
        conn.rollback()
    cur.close()
    conn.close()

with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=('GET', 'POST'))
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        futbolista_favorito = request.form['futbolista_favorito']
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO usuarios (nombre, email, futbolista_favorito) VALUES (%s, %s, %s)', (nombre, email, futbolista_favorito))
            conn.commit()
            flash('¡Fichaje exitoso! Usuario registrado', 'success')
        except Exception as e:
            conn.rollback()
            flash('Error: El correo ya está fichado o la base de datos falló.', 'error')
        finally:
            cur.close()
            conn.close()
            return redirect(url_for('registro'))
            
    # Lógica de consulta embebida en la página de registro
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios ORDER BY id DESC LIMIT 5')
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('registro.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)