import os
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("GEMINI_API_KEY", "").strip()

# System prompt: el asistente se comporta como IA de PharmaTech
SYSTEM_PROMPT = """Eres el asistente virtual de PharmaTech NeuroScience Division, una empresa farmacéutica de investigación neurológica avanzada.

CATÁLOGO DE PRODUCTOS:
1. Neurovexis-9 (₡15,000) - Modulador sináptico experimental para estabilizar impulsos neuronales
2. Synaptrol-XR (₡22,500) - Compuesto neuroadaptativo para regeneración neuronal artificial
3. Cerebrix Delta (₡18,000) - Neuroestimulante de precisión para interfaces neuronales avanzadas

SERVICIOS:
- Neurocirugía Avanzada: Sistemas de apoyo neuroquímico para procedimientos cerebrales complejos
- Sinapsis Artificial: Investigación de conexiones neuronales experimentales
- Bioingeniería Cognitiva: Simulación neuronal y estabilización neuroeléctrica

MÉTODOS DE PAGO:
- SINPE Móvil: 8888-8888
- Transferencia Bancaria: Banco Nacional, Cuenta 123456789
- Tarjeta de crédito

Tu función es:
- Responder preguntas específicas sobre productos: características, precios, usos
- Explicar los servicios disponibles
- Ayudar con información de pagos y envíos
- Responder de forma profesional, concisa y científica pero accesible
- Si preguntan algo fuera de PharmaTech, redirige amablemente pero mantén el contexto

Proporciona respuestas claras, útiles y siempre en contexto con la empresa."""


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)


@app.route('/preguntar', methods=['POST'])
def preguntar():
    # Intenta múltiples formas de obtener los datos
    try:
        data = request.get_json()
    except:
        data = None
    
    if not data:
        try:
            import json
            data = json.loads(request.data.decode('utf-8'))
        except:
            data = None
    
    if not data or 'pregunta' not in data:
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
                temperature=0.5,
                top_p=0.85,
                max_output_tokens=400,
            )
        )

        respuesta_texto = response.text.strip()
        if not respuesta_texto:
            respuesta_texto = "Disculpa, no pude generar una respuesta. Intenta reformular tu pregunta."
        return jsonify({'respuesta': respuesta_texto}), 200

    except Exception as e:
        error_str = str(e)
        print(f"[PharmaTech IA Error] {error_str}")

        # Mensajes de error más específicos
        if 'INVALID_ARGUMENT' in error_str or 'API key not valid' in error_str.lower():
            return jsonify({'respuesta': '❌ La API Key de Gemini no es válida. Verifica el archivo .env'})
        elif 'quota' in error_str.lower() or 'rate limit' in error_str.lower():
            return jsonify({'respuesta': '⚠️ Se alcanzó el límite de cuota de la API. Intenta en unos minutos.'})
        elif 'connection' in error_str.lower() or 'timeout' in error_str.lower():
            return jsonify({'respuesta': '🌐 Error de conexión. Verifica tu internet.'})
        else:
            # Mostrar el error para debug
            print(f"Error completo: {error_str}")
            return jsonify({'respuesta': f'❌ Error: {error_str[:200]}'})


if __name__ == '__main__':
    print("=" * 50)
    print("  PharmaTech IA Backend - Iniciando...")
    print(f"  API Key cargada: {'[OK] Si' if api_key else '[ERROR] NO (revisar .env)'}")
    print("  Servidor: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
