# 🚀 FastAPI + Flask Starter Project

This repository provides a base setup for a backend combining **FastAPI** and **Flask** — ideal for teams experimenting or integrating both frameworks.

---

## 📂 Project Structure

backend/
├── fastapi/ # FastAPI service
└── flask/ # Flask service

yaml
Copy code

---

## 🧰 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<YOUR_USERNAME>/fastapi-flask-starter.git
cd fastapi-flask-starter
2. Create a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure environment variables
Duplicate example.env and rename it to .env, then fill in your values.

5. Run FastAPI
bash
Copy code
uvicorn Fast-api.main:app --reload
6. Run Flask
bash
Copy code
python Flask/app.py 