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
            email VARCHAR(100) UNIQUE NOT NULL
        )
    ''')
    conn.commit()
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
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO usuarios (nombre, email) VALUES (%s, %s)', (nombre, email))
            conn.commit()
            flash('Usuario registrado exitosamente', 'success')
        except Exception as e:
            conn.rollback()
            flash('Error: El correo ya existe o la base de datos falló.', 'error')
        finally:
            cur.close()
            conn.close()
        
        # El return va AFUERA del bloque try/except/finally
        return redirect(url_for('registro'))
            
    # Lógica de consulta (solo se ejecuta si el método es GET)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios ORDER BY id DESC LIMIT 5')
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('registro.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
