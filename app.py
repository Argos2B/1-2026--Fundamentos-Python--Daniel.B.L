import os
import sqlite3
import secrets
import hashlib
import shutil
from datetime import datetime, timedelta, timezone
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from google import genai
from google.genai import types

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(BASE_DIR, "SQL")
DB_PATH = os.path.join(SQL_DIR, "pharmatech.sqlite3")
LEGACY_DB_PATH = os.path.join(BASE_DIR, "pharmatech.sqlite3")
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

app = Flask(__name__)
CORS(app)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip() or "gemini-2.0-flash"
API_KEY_ENV_NAMES = ("GEMINI_API_KEY", "GOOGLE_API_KEY")


def get_api_key():
    for name in API_KEY_ENV_NAMES:
        value = os.getenv(name, "").strip()
        if value and value not in {"TU_API_KEY", "TU_API_KEY_AQUI", "YOUR_API_KEY_HERE"}:
            return value
    return ""


def api_key_status():
    key = get_api_key()
    if not key:
        return {"configured": False, "masked": ""}
    masked = f"{key[:4]}...{key[-4:]}" if len(key) >= 8 else "****"
    return {"configured": True, "masked": masked}


def utc_now():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.isoformat()


def hash_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def prepare_sql_storage():
    os.makedirs(SQL_DIR, exist_ok=True)
    if os.path.exists(LEGACY_DB_PATH) and not os.path.exists(DB_PATH):
        shutil.copy2(LEGACY_DB_PATH, DB_PATH)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                recovery_token_hash TEXT,
                recovery_expires_at TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        admin = conn.execute("SELECT id FROM users WHERE username = ?", ("admin",)).fetchone()
        if not admin:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                ("admin", "admin@pharmatech.local", hash_text("12345"), iso(utc_now()))
            )


def public_user(row):
    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
    }


def create_session(conn, user_id):
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sessions (user_id, token_hash, expires_at, created_at) VALUES (?, ?, ?, ?)",
        (user_id, hash_text(token), iso(utc_now() + timedelta(days=7)), iso(utc_now()))
    )
    return token


def current_user(conn):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token_hash = hash_text(auth.removeprefix("Bearer ").strip())
    row = conn.execute(
        """
        SELECT users.id, users.username, users.email
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.token_hash = ? AND sessions.expires_at > ?
        """,
        (token_hash, iso(utc_now()))
    ).fetchone()
    return row

# System prompt: el asistente se comporta como IA de PharmaTech
SYSTEM_PROMPT = """Eres el asistente virtual de PharmaTech NeuroScience Division, una empresa farmacÃ©utica de investigaciÃ³n neurolÃ³gica avanzada.

CATÃLOGO DE PRODUCTOS:
1. Neurovexis-9 (â‚¡15,000) - Modulador sinÃ¡ptico experimental para estabilizar impulsos neuronales
2. Synaptrol-XR (â‚¡22,500) - Compuesto neuroadaptativo para regeneraciÃ³n neuronal artificial
3. Cerebrix Delta (â‚¡18,000) - Neuroestimulante de precisiÃ³n para interfaces neuronales avanzadas

SERVICIOS:
- NeurocirugÃ­a Avanzada: Sistemas de apoyo neuroquÃ­mico para procedimientos cerebrales complejos
- Sinapsis Artificial: InvestigaciÃ³n de conexiones neuronales experimentales
- BioingenierÃ­a Cognitiva: SimulaciÃ³n neuronal y estabilizaciÃ³n neuroelÃ©ctrica

MÃ‰TODOS DE PAGO:
- SINPE MÃ³vil: 8888-8888
- Transferencia Bancaria: Banco Nacional, Cuenta 123456789
- Tarjeta de crÃ©dito

Tu funciÃ³n es:
- Responder preguntas especÃ­ficas sobre productos: caracterÃ­sticas, precios, usos
- Explicar los servicios disponibles
- Ayudar con informaciÃ³n de pagos y envÃ­os
- Responder de forma profesional, concisa y cientÃ­fica pero accesible
- Si preguntan algo fuera de PharmaTech, redirige amablemente pero mantÃ©n el contexto

Proporciona respuestas claras, Ãºtiles y siempre en contexto con la empresa."""


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)


@app.route('/preguntar', methods=['POST'])
def preguntar():
    data = request.get_json(silent=True) or {}

    if not data or 'pregunta' not in data:
        return jsonify({'respuesta': 'No se recibio ningun dato en la solicitud.'}), 400

    pregunta = data.get('pregunta', '').strip()

    if not pregunta:
        return jsonify({'respuesta': 'La pregunta esta vacia.'}), 400

    api_key = get_api_key()
    if not api_key:
        return jsonify({
            'respuesta': (
                'Modo local activo: falta configurar <code>GEMINI_API_KEY</code> en el archivo '
                '<strong>.env</strong>. Mientras tanto puedo responder informacion basica de PharmaTech: '
                'productos Neurovexis-9, Synaptrol-XR, Cerebrix Delta, servicios neurologicos y metodos de pago.'
            ),
            'modo': 'local_sin_api_key'
        }), 200

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=pregunta,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.5,
                top_p=0.85,
                max_output_tokens=400,
            )
        )

        respuesta_texto = (response.text or '').strip()
        if not respuesta_texto:
            respuesta_texto = 'Disculpa, no pude generar una respuesta. Intenta reformular tu pregunta.'
        return jsonify({'respuesta': respuesta_texto}), 200

    except Exception as e:
        error_str = str(e)
        error_lower = error_str.lower()
        print(f'[PharmaTech IA Error] {error_str}')

        if 'invalid_argument' in error_lower or 'api key not valid' in error_lower or 'api_key_invalid' in error_lower:
            return jsonify({'respuesta': 'La API Key de Gemini no es valida. Revisa GEMINI_API_KEY en el archivo .env.'}), 400
        if 'quota' in error_lower or 'rate limit' in error_lower:
            return jsonify({'respuesta': 'Se alcanzo el limite de cuota de Gemini. Intenta en unos minutos.'}), 429
        if 'connection' in error_lower or 'timeout' in error_lower:
            return jsonify({'respuesta': 'Error de conexion con Gemini. Verifica internet e intenta de nuevo.'}), 503

        print(f'Error completo: {error_str}')
        return jsonify({'respuesta': f'Error de Gemini: {error_str[:200]}'}), 500


@app.route('/api/status', methods=['GET'])
def status():
    key_status = api_key_status()
    return jsonify({
        'ok': True,
        'database': DB_PATH,
        'databaseReady': os.path.exists(DB_PATH),
        'sqlFolder': SQL_DIR,
        'geminiModel': GEMINI_MODEL,
        'apiKeyConfigured': key_status['configured'],
        'apiKey': key_status['masked'],
    })


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if len(username) < 3 or "@" not in email or len(password) < 5:
        return jsonify({"error": "Use usuario de 3+ caracteres, email valido y clave de 5+ caracteres."}), 400

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (username, email, hash_text(password), iso(utc_now()))
            )
            user = conn.execute("SELECT id, username, email FROM users WHERE username = ?", (username,)).fetchone()
            token = create_session(conn, user["id"])
            return jsonify({"message": "Usuario creado correctamente.", "token": token, "user": public_user(user)})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Ese usuario o email ya existe."}), 409


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    with get_db() as conn:
        user = conn.execute(
            "SELECT id, username, email, password_hash FROM users WHERE username = ? OR email = ?",
            (username, username.lower())
        ).fetchone()
        if not user or user["password_hash"] != hash_text(password):
            return jsonify({"error": "Usuario o clave incorrectos."}), 401
        token = create_session(conn, user["id"])
        return jsonify({"message": "Inicio de sesion correcto.", "token": token, "user": public_user(user)})


@app.route('/api/me', methods=['GET'])
def me():
    with get_db() as conn:
        user = current_user(conn)
        if not user:
            return jsonify({"error": "Sesion no valida."}), 401
        return jsonify({"user": public_user(user)})


@app.route('/api/logout', methods=['POST'])
def logout():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        with get_db() as conn:
            conn.execute("DELETE FROM sessions WHERE token_hash = ?", (hash_text(auth.removeprefix("Bearer ").strip()),))
    return jsonify({"message": "Sesion cerrada."})


@app.route('/api/recovery/request', methods=['POST'])
def request_recovery():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    if "@" not in email:
        return jsonify({"error": "Ingrese un email valido."}), 400

    token = secrets.token_urlsafe(8)
    with get_db() as conn:
        user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if user:
            conn.execute(
                "UPDATE users SET recovery_token_hash = ?, recovery_expires_at = ? WHERE id = ?",
                (hash_text(token), iso(utc_now() + timedelta(minutes=30)), user["id"])
            )
        return jsonify({
            "message": "Si el email existe, se genero un codigo de recuperacion valido por 30 minutos.",
            "recoveryToken": token if user else None
        })


@app.route('/api/recovery/reset', methods=['POST'])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    token = (data.get("token") or "").strip()
    new_password = data.get("newPassword") or ""

    if "@" not in email or not token or len(new_password) < 5:
        return jsonify({"error": "Email, codigo y clave nueva de 5+ caracteres son obligatorios."}), 400

    with get_db() as conn:
        user = conn.execute(
            """
            SELECT id FROM users
            WHERE email = ? AND recovery_token_hash = ? AND recovery_expires_at > ?
            """,
            (email, hash_text(token), iso(utc_now()))
        ).fetchone()
        if not user:
            return jsonify({"error": "Codigo invalido o vencido."}), 400
        conn.execute(
            """
            UPDATE users
            SET password_hash = ?, recovery_token_hash = NULL, recovery_expires_at = NULL
            WHERE id = ?
            """,
            (hash_text(new_password), user["id"])
        )
        conn.execute("DELETE FROM sessions WHERE user_id = ?", (user["id"],))
        return jsonify({"message": "Clave actualizada correctamente. Inicie sesion de nuevo."})


prepare_sql_storage()
init_db()


if __name__ == '__main__':
    key_status = api_key_status()
    print("=" * 50)
    print("  PharmaTech IA Backend - Iniciando...")
    print(f"  SQL: {DB_PATH}")
    print(f"  API Key cargada: {'[OK] Si ' + key_status['masked'] if key_status['configured'] else '[INFO] NO (modo local)'}")
    print(f"  Modelo Gemini: {GEMINI_MODEL}")
    print("  Servidor: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
