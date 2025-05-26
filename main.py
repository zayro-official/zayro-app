from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/reviews", response_class=HTMLResponse)
async def read_reviews(request: Request):
    reviews = [
        {"Customer Name": "Emily Chen", "Review ID": "R001", "Review Date": "2025-05-20"},
        {"Customer Name": "Jake Turner", "Review ID": "R002", "Review Date": "2025-06-14"},
        {"Customer Name": "Sophia Martinez", "Review ID": "R003", "Review Date": "2025-05-21"},
    ]
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews})

@app.post("/generate")
async def generate_reply(request: Request):
    data = await request.json()
    review = data.get("review", "")
    reply = f"Thank you for your review! ({review})"
    return JSONResponse(content={"reply": reply})
