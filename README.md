# 🧑‍💼 Mosaic Hire — AI-Powered CV Analyzer

## Project Overview

**Mosaic Hire** is an AI-powered HR tool that **analyzes a candidate's CV** and generates a **personalized career and training report**.
It combines **document extraction (with OCR)**, a **web-based RAG** layer and a **Large Language Model (LLaMA 3.3 70B via Groq)** to give concrete, actionable recommendations.

For each CV, the report includes:

- 🔍 **Profile analysis**
- 🎯 **Goals and aspirations**
- 💪 **Strengths**
- ⚠️ **Critical weaknesses**
- 🏆 **Recommended certifications** (with official links)
- 📚 **Priority courses** (with official links)
- 🚀 **Tailored action plan**

---

## ⚙️ How It Works

```
CV upload (PDF / DOCX / image / text)
        │
        ▼
Text extraction ── PyPDF2 · python-docx · Tesseract OCR (fallback for scanned PDFs & images)
        │
        ▼
Web RAG ── SerpAPI retrieves relevant courses, certifications and guides
        │
        ▼
LLM analysis ── LLaMA 3.3 70B (Groq) generates the structured report
        │
        ▼
Safe HTML rendering ── displayed in the React frontend
```

- **Multi-format support**: PDF, DOCX, PNG/JPG and plain text
- **OCR fallback** when a PDF contains little or no extractable text
- **Self-check**: if certifications or courses are missing from the answer, a second LLM call completes them
- **Secure output**: Markdown is escaped and converted to safe HTML with clickable links

---

## 🔧 Tech Stack

| Layer | Technologies |
|:--|:--|
| **AI / LLM** | Groq API, LLaMA 3.3 70B, RAG, SerpAPI |
| **Document processing** | PyPDF2, python-docx, pdf2image, Pytesseract (OCR), Pillow |
| **Backend** | FastAPI, Uvicorn, Flask |
| **Frontend** | React 19, React Router, Vite |

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+, Node.js
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Poppler](https://poppler.freedesktop.org/) installed
- API keys: **Groq** and **SerpAPI**

### Backend
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r Backend/requirements.txt google-search-results
```

Create a `.env` file at the project root:
```env
GROQ_API_KEY=your_groq_key
SERPAPI_API_KEY=your_serpapi_key
```

Run the API (from the project root):
```bash
uvicorn Backend.fastapi.main:app --reload      # http://127.0.0.1:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                                     # http://localhost:5173
```

---

## 📡 API

| Method | Endpoint | Description |
|:--|:--|:--|
| `GET` | `/` | Health check |
| `POST` | `/analyze` | Upload a CV (`file`) and get the HTML analysis report |

---

## 📁 Project Structure

```
HR-Project/
├── Backend/
│   ├── fastapi/
│   │   ├── main.py        # FastAPI app & /analyze endpoint
│   │   ├── analyser.py    # Text extraction, RAG, Groq CV analyzer
│   │   └── rag_utils.py   # Web RAG with SerpAPI
│   ├── Flask/
│   │   └── app.py         # Flask version of the API
│   └── requirements.txt
└── frontend/              # React + Vite interface
    └── src/pages/
        ├── Home.jsx
        └── Analyze.jsx    # CV upload & report display
```

---

## 👩‍💻 Author

**Ranim Benali** — [GitHub](https://github.com/ranimbenali) · [LinkedIn](https://www.linkedin.com/in/benaliranim/)
