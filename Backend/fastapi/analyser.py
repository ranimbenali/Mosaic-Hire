import logging
import re
import html
import io
from groq import Groq
from serpapi import GoogleSearch
from PIL import Image
import pytesseract
from docx import Document
from pdf2image import convert_from_bytes
import PyPDF2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MODEL_PRO = "llama-3.3-70b-versatile"

# ============================================================
# === EXTRACTION DU TEXTE (PDF / DOCX / IMAGE / TEXTE)
# ============================================================
def extract_text(file_bytes: bytes, filename: str) -> str:
    name = (filename or "").lower()
    logger.info("📄 extract_text: traitement de %s", filename)

    # --- PDF ---
    if name.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text_parts = [page.extract_text() for page in reader.pages if page.extract_text()]
            combined = "\n".join(text_parts).strip()
            if len(combined) < 50:  # OCR fallback
                images = convert_from_bytes(file_bytes)
                ocr_texts = [pytesseract.image_to_string(img) for img in images]
                combined = "\n".join([combined] + ocr_texts).strip()
            return combined
        except Exception as e:
            logger.exception("Erreur PDF: %s", e)
            return ""

    # --- DOCX ---
    if name.endswith(".docx"):
        try:
            doc = Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            logger.exception("Erreur DOCX: %s", e)
            return ""

    # --- IMAGE ---
    if name.endswith((".png", ".jpg", ".jpeg")):
        try:
            img = Image.open(io.BytesIO(file_bytes))
            return pytesseract.image_to_string(img)
        except Exception as e:
            logger.exception("Erreur image: %s", e)
            return ""

    # --- TEXTE BRUT ---
    try:
        return file_bytes.decode("utf-8")
    except:
        try:
            return file_bytes.decode("latin-1")
        except:
            return ""


# ============================================================
# === RAG Web (SerpAPI)
# ============================================================
class RAGKnowledgeBaseWeb:
    def __init__(self, serpapi_api_key: str, top_k: int = 5):
        self.serpapi_api_key = serpapi_api_key
        self.top_k = top_k

    def query(self, query_text, top_k=None):
        top_k = top_k or self.top_k
        results = []

        try:
            params = {
                "engine": "google",
                "q": query_text,
                "num": top_k,
                "api_key": self.serpapi_api_key
            }
            search = GoogleSearch(params)
            data = search.get_dict()
        except Exception as e:
            logger.exception("Erreur SerpAPI: %s", e)
            return ["⚠️ Aucun document pertinent trouvé via SerpAPI."]

        organic_results = data.get("organic_results", [])
        for item in organic_results[:top_k]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            if snippet:
                results.append(f"{title}\n{link}\n{snippet[:1000]}")

        if not results:
            results = ["⚠️ Aucun document pertinent trouvé via SerpAPI."]
        logger.info("SerpAPI query: trouvé %d documents", len(results))
        return results


# ============================================================
# === ANALYSEUR DE CV (GROQ)
# ============================================================
class CVAnalyzerGroq:
    def __init__(self, api_key: str = None, serpapi_key: str = None, kb_folder: str = None):
        self.client = None
        if api_key:
            try:
                self.client = Groq(api_key=api_key)
                logger.info("✅ Client Groq initialisé avec succès.")
            except Exception as e:
                logger.exception("❌ Impossible d'initialiser Groq: %s", e)

        self.model = MODEL_PRO
        self.kb_folder = kb_folder or "knowledge_base"
        self.rag = RAGKnowledgeBaseWeb(serpapi_api_key=serpapi_key, top_k=10)

    # ------------------------------------------------------------
    # Analyse principale
    # ------------------------------------------------------------
    def analyze(self, cv_text: str) -> str:
        cv_text = (cv_text or "").strip()
        if len(cv_text) < 80:
            return "❌ Texte insuffisant pour une analyse fiable."

        # 1️⃣ Récupérer du contexte web via SerpAPI
        try:
            context_docs = self.rag.query(cv_text, top_k=10)
        except Exception:
            context_docs = ["⚠️ Aucun document pertinent trouvé via SerpAPI."]
        context = "\n\n".join(context_docs)

        # 2️⃣ Construire le prompt principal
        prompt = f"""
Tu es un expert RH et conseiller en formation. Analyse ce CV :

{cv_text}

Contexte utile provenant du web (exemples de cours / certifications / guides) :
{context}

Réponds en Markdown et fournis :
🔍 ANALYSE DU PROFIL
🎯 OBJECTIFS ET ASPIRATIONS
💪 POINTS FORTS
⚠️ FAIBLESSES CRITIQUES
🏆 CERTIFICATIONS RECOMMANDÉES (NOM EXACT + LIEN OFFICIEL, au moins 3)
📚 COURS PRIORITAIRES (NOM EXACT + LIEN OFFICIEL, au moins 3)
🚀 PLAN D'ACTION SUR MESURE (étapes concrètes)
"""

        if self.client is None:
            return "❌ Client Groq non initialisé."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert RH avec accès à une base de connaissances web."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=6000
            )

            raw_content = getattr(response.choices[0].message, "content", None)
            if raw_content is None:
                raw_content = str(response)

            logger.info("Longueur réponse brute: %d caractères", len(raw_content))
            content = raw_content or ""

            # Vérifie si les sections finales sont présentes
            result_html = self.markdown_to_html_safe(content)
            if "certifications recommand" not in content.lower() or "cours prioritaires" not in content.lower():
                logger.warning("Réponse incomplète détectée. Nouvelle tentative pour certifications/cours...")
                result_html += self.generate_courses_certifications(cv_text)

            return result_html

        except Exception as e:
            logger.exception("Erreur Groq: %s", e)
            return f"❌ Erreur Groq: {e}"

    # ------------------------------------------------------------
    # Génération des cours et certifications
    # ------------------------------------------------------------
    def generate_courses_certifications(self, cv_text: str) -> str:
        prompt_courses = f"""
Liste 5 certifications officielles et 5 cours en ligne adaptés pour ce profil :

{cv_text}

Pour chaque élément :
- Nom exact
- Lien officiel
- Courte description
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert RH et conseiller en formation."},
                    {"role": "user", "content": prompt_courses}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            raw_content = getattr(response.choices[0].message, "content", None)
            if raw_content is None:
                raw_content = str(response)
            return self.markdown_to_html_safe(raw_content)
        except Exception as e:
            logger.exception("Erreur Groq (courses/certifications): %s", e)
            return f"<div>❌ Erreur Groq (courses/certifications): {e}</div>"

    # ------------------------------------------------------------
    # Conversion Markdown -> HTML sûr
    # ------------------------------------------------------------
    def markdown_to_html_safe(self, md_text: str) -> str:
        if not md_text:
            return "<div></div>"

        escaped = html.escape(md_text)
        url_pattern = re.compile(r'(https?://[^\s\)\]\"]+)')

        def _anchor(m):
            url = m.group(0)
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'

        safe_with_links = url_pattern.sub(_anchor, escaped)
        return f"<div style='white-space:pre-wrap;font-family:Arial,Helvetica,sans-serif'>{safe_with_links}</div>"
