# 🚀 FastAPI + Flask Starter Project

This repository provides a base setup for a backend combining **FastAPI** and **Flask** — ideal for teams experimenting or integrating both frameworks.

---

## 📂 Project Structure

Backend/
├── fastapi_app/ # FastAPI service
└── flask_app/ # Flask service


---

## 🧰 Setup Instructions

### 1. Clone the repository

git clone https://github.com/ranimbenali/Mosaic-hire.git
cd fastapi-flask-starter
2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies

pip install -r /Backend/requirements.txt
4. Configure environment variables
Duplicate example.env and rename it to .env, then fill in your values.

5. Run FastAPI

Copy code
uvicorn Backend/Fast-api.main:app --reload
6. Run Flask

python Backend/Flask/app.py 