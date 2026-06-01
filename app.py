import os
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("GEMINI_API_KEY")

# System prompt: el asistente se comporta como IA de PharmaTech
SYSTEM_PROMPT = """Eres el asistente virtual de PharmaTech NeuroScience Division, una empresa farmacéutica de investigación neurológica avanzada.

Tu función es:
- Responder preguntas sobre los productos neurofarmacológicos del catálogo: Neurovexis-9, Synaptrol-XR y Cerebrix Delta.
- Informar sobre los servicios: Neurocirugía Avanzada, Sinapsis Artificial y Bioingeniería Cognitiva.
- Ayudar con preguntas generales sobre la empresa, pagos (SINPE, tarjeta, transferencia) y soporte.
- Responder siempre de forma profesional, concisa y con un tono científico pero accesible.
- Si alguien pregunta algo fuera del contexto de PharmaTech, redirige amablemente la conversación.

Recuerda: eres parte de un proyecto académico / demo, así que puedes responder preguntas generales de manera educativa también."""


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)


@app.route('/preguntar', methods=['POST'])
def preguntar():
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({'respuesta': '❌ No se recibió ningún dato en la solicitud.'}), 400

    pregunta = data.get('pregunta', '').strip()

    if not pregunta:
        return jsonify({'respuesta': '❌ La pregunta está vacía.'}), 400

    if not api_key:
        return jsonify({
            'respuesta': '⚠️ API Key no configurada. Verifica el archivo <strong>.env</strong> y que contenga <code>GEMINI_API_KEY</code>.'
        }), 500

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=pregunta,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=1024,
            )
        )

        respuesta_texto = response.text
        return jsonify({'respuesta': respuesta_texto})

    except Exception as e:
        error_str = str(e)
        print(f"[PharmaTech IA Error] {error_str}")

        if 'API_KEY_INVALID' in error_str or 'API key not valid' in error_str:
            return jsonify({'respuesta': '❌ La API Key de Gemini no es válida. Verifica el archivo .env'})
        elif 'quota' in error_str.lower():
            return jsonify({'respuesta': '⚠️ Se alcanzó el límite de cuota de la API. Intenta en unos minutos.'})
        elif 'network' in error_str.lower() or 'connection' in error_str.lower():
            return jsonify({'respuesta': '🌐 Error de conexión con el servidor de IA. Verifica tu internet.'})
        else:
            return jsonify({'respuesta': f'❌ Error inesperado: {error_str}'})


if __name__ == '__main__':
    print("=" * 50)
    print("  PharmaTech IA Backend - Iniciando...")
    print(f"  API Key cargada: {'[OK] Si' if api_key else '[ERROR] NO (revisar .env)'}")
    print("  Servidor: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
