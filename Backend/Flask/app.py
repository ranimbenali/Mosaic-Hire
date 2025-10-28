import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import logging

# Import corrigé
from Backend.fastapi.analyser import extract_text, CVAnalyzerGroq

# === Configuration ===
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret")

# === Initialisation des clés ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
KB_FOLDER = os.getenv("KB_FOLDER", "knowledge_base")

# === Initialisation de l'analyseur ===
analyzer = CVAnalyzerGroq(api_key=GROQ_API_KEY, serpapi_key=SERPAPI_API_KEY, kb_folder=KB_FOLDER)


@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask + LLaMA/Groq!"})


@app.route("/analyze", methods=["POST"])
def analyze_cv():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files['file']
    file_content = file.read()
    filename = file.filename
    cv_text = extract_text(file_content, filename)
    if not cv_text:
        return jsonify({"result": "❌ Impossible d'extraire le texte du fichier."})

    result = analyzer.analyze(cv_text)
    return jsonify({"result": result})


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
