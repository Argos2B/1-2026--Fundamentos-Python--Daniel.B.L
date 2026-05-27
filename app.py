import os
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import google.generativeai as genai
load_dotenv()
app = Flask(__name__)
CORS(app)
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)
@app.route('/preguntar', methods=['POST'])
def preguntar():
    data = request.json
    pregunta = data.get('pregunta', '')
    try:
        if not api_key:
            return jsonify({'respuesta':'Configura tu GEMINI_API_KEY en el archivo .env'})
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(pregunta)
        return jsonify({'respuesta': response.text})
    except Exception as e:
        return jsonify({'respuesta': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
