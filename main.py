from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_reply(request: Request):
    data = await request.json()
    review_text = data.get("review", "")
    return {"reply": f"Thanks for your feedback: {review_text}"}
