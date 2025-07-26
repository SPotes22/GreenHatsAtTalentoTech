from flask import Flask, request, render_template, session, redirect , flash
import chatbot_core as chat_core
import mysql.connector
from datetime import datetime
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'super-secret-key1'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configuración BD
'''
# db test
db_config = {
    'host': 'bvjqxiivyol038q4cjkr-mysql.services.clever-cloud.com',
    'user': 'uqhw6kmlznvlaoz1',
    'password': 'w2shabcQnnoUWLZO0Luy',
    'database': 'bvjqxiivyol038q4cjkr',
 'port' : '3306',
}'''
# Variables desde entorno
db_config = {
    'host': os.environ.get('MYSQL_ADDON_HOST', 'tu-host'),
    'user': os.environ.get('MYSQL_ADDON_USER', 'tu-user'),
    'password': os.environ.get('MYSQL_ADDON_PASSWORD', 'tu-password'),
    'database': os.environ.get('MYSQL_ADDON_DB', 'tu-bd'),
    'port': int(os.environ.get('MYSQL_ADDON_PORT', 3306))
}
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Conectado a la base de datos:", cursor.fetchone())
except mysql.connector.Error as err:
    print("Error de conexión a MySQL:", err)
# Crear conexión
def get_db():
    return mysql.connector.connect(**db_config)

# Crear o recuperar el usuario actual de sesión
def get_or_create_user():
    if 'user_id' not in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, rol) VALUES (%s, %s)", ('Invitado', 'usuario'))
        conn.commit()
        session['user_id'] = cursor.lastrowid
        cursor.close()
        conn.close()
    return session['user_id']

# Ruta principal protegida
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session.pop('conversation_id', None)
            return redirect('/')

        # Verificar si las credenciales son correctas
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session.pop('conversation_id', None)  # nueva conversación
            return redirect('/')
        else:
            flash('Credenciales incorrectas')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash de la contraseña
        password_hash = generate_password_hash(password)

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Verificar si ya existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('Ya existe una cuenta con este correo.')
            return render_template('signup.html')

        # Insertar nuevo usuario
        cursor.execute("""
            INSERT INTO usuarios (nombre, rol, email, password)
            VALUES (%s, 'usuario', %s, %s)
        """, (nombre, email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()

        session['user_id'] = user_id
        session.pop('conversation_id', None)
        return redirect('/')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



# Chat con historial
@app.route('/chat/', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect('/login')
    # Conectar a la base de datos
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    user_id = get_or_create_user()

    # Verificar conversación activa
    if 'conversation_id' not in session:
        cursor.execute("""
            INSERT INTO conversaciones (id_usuario) VALUES (%s)
        """, (user_id,))
        conn.commit()
        session['conversation_id'] = cursor.lastrowid

    conversation_id = session['conversation_id']
    response = ''

    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            # Guardar pregunta
            cursor.execute("""
                INSERT INTO mensajes (id_usuario, id_conversacion, rol, contenido)
                VALUES (%s, %s, 'user', %s)
            """, (user_id, conversation_id, question))
            conn.commit()

            # Obtener respuesta
            start_time = datetime.now()
            '''
            # v1.0
            response_v1 = chat_core.predecir_intencion(question, temp=0.7, verbose=0.34)
            # v2.0
            response = consultar_php_backend(question)
            duration = (datetime.now() - start_time).microseconds // 1000
            '''
            # Generar ambas respuestas
            respuesta_modelo = chat_core.predecir_intencion(question, temp=0.7, verbose=0.34)
            respuesta_api = consultar_php_backend(question)

            # Combinar ambas
            response = f"🧠 Model: {respuesta_modelo}\n🌐 API: {respuesta_api}"
            # Guardar respuesta
            cursor.execute("""
                INSERT INTO mensajes (id_usuario, id_conversacion, rol, contenido, tiempo_respuesta_ms)
                VALUES (%s, %s, 'bot', %s, %s)
            """, (user_id, conversation_id, response, duration))
            conn.commit()

    # Cargar últimos 30 mensajes de la conversación
    cursor.execute("""
        SELECT rol, contenido FROM mensajes
        WHERE id_conversacion = %s
        ORDER BY enviado_en ASC
        LIMIT 30
    """, (conversation_id,))
    mensajes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('chat_hist.html', messages=mensajes, response=response)

@app.route('/nueva_conversacion')
def nueva_conversacion():
    session.pop('conversation_id', None)
    return redirect('/chat/')

def consultar_php_backend(pregunta):
    try:
        php_backend_url = 'https://greenhats-backend.onrender.com'  # <-- cambia según ruta real
        payload = {'pregunta': pregunta}

        response = requests.post(php_backend_url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('respuesta', 'Lo siento, no pude obtener respuesta.')
        else:
            return f"Error en el backend PHP (status {response.status_code})"
    except Exception as e:
        return f"Error de conexión al backend PHP: {str(e)}"

# Integracion de Api externa
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    pregunta = data.get('pregunta')

    if not pregunta:
        return {'error': 'Falta la pregunta'}, 400

    respuesta = consultar_php_backend(pregunta)
    return {'respuesta': respuesta}


@app.route('/renderoso')
def home():
    return '¡Hola! Soy el chatbot de Inge Lean.'

# Para healthz en Render
@app.route('/healthz')
def healthz():
    return 'OK', 200


# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
