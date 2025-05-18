from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ZAYRO backend is working!"}

@app.get("/hello")
def hello():
    return {"message": "こんにちは、ZAYROです！"}
