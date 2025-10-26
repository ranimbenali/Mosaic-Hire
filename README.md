# 🚀 FastAPI + Flask Starter Project

This repository provides a base setup for a backend combining **FastAPI** and **Flask** — ideal for teams experimenting with or integrating both frameworks.

---

## 📂 Project Structure

backend/
├── fastapi/ # FastAPI service
└── flask/ # Flask service



## 🧰 Setup Instructions

### 1. Clone the repository
yaml
Copy code

---
```bash
git clone https://github.com/ranimbenali/Mosaic-hire.git
cd Mosaic-hire
2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies

pip install -r /Backend/requirements.txt
4. Configure environment variables
Duplicate example.env and rename it to .env, then fill in your values.

5. Run FastAPI

uvicorn fastapi.main:app --reload
6. Run flask


python Flask/app.py 
