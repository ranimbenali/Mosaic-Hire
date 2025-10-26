from fastapi import FastAPI

app = FastAPI(title="FastAPI Example")

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}
