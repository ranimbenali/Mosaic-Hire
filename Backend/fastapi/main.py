import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Backend.fastapi.analyser import extract_text, CVAnalyzerGroq

app = FastAPI(title="Mosaic Hire API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser l'analyseur une fois
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
KB_FOLDER = os.getenv("KB_FOLDER", "knowledge_base")

analyzer = CVAnalyzerGroq(api_key=GROQ_API_KEY, serpapi_key=SERPAPI_API_KEY, kb_folder=KB_FOLDER)

@app.get("/")
def home():
    return {"message": "Bienvenue sur Mosaic Hire API 🚀"}

@app.post("/analyze")
async def analyze_cv(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Fichier manquant")

    content = await file.read()
    text = extract_text(content, file.filename)
    if not text:
        return {"result": "❌ Impossible d'extraire le texte du fichier. Vérifie le format."}

    result = analyzer.analyze(text)
    return {"result": result}
