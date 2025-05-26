from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class Review(BaseModel):
    review: str

@app.post("/generate")
async def generate_reply(data: Review):
    # 仮の返信ロジック（必要に応じて後で改善）
    return JSONResponse(content={"reply": f"Thank you for your review: {data.review}"}
