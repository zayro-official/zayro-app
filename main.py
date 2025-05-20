import os
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PLACE_ID = os.getenv("GOOGLE_PLACE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class Review(BaseModel):
    author_name: str
    rating: int
    text: str
    reply_text: str = ""

stored_replies = {}
mode = {"value": "ai"}  # "ai" または "manual"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, lang: str = "en"):
    reviews = await fetch_google_reviews()
    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": reviews,
        "lang": lang,
        "mode": mode["value"]
    })

@app.post("/set_mode")
async def set_mode(request: Request, mode_value: str = Form(...)):
    mode["value"] = mode_value
    return RedirectResponse(url="/", status_code=303)

@app.post("/reply")
async def reply_to_review(
    request: Request,
    author_name: str = Form(...),
    review_text: str = Form(...),
    lang: str = Form(...),
    reply_text: str = Form("")
):
    if mode["value"] == "manual":
        stored_replies[author_name] = reply_text
    else:
        try:
            prompt = f"Respond to the following customer review in a friendly and professional tone:\n\nReview: {review_text}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            reply = response.choices[0].message.content.strip()
            stored_replies[author_name] = reply
        except Exception as e:
            stored_replies[author_name] = f"(AI返信エラー: {str(e)})"

    return RedirectResponse(url=f"/?lang={lang}", status_code=303)

async def fetch_google_reviews():
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=review&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    google_reviews = data.get("result", {}).get("reviews", [])

    reviews = []
    for r in google_reviews:
        author_name = r.get("author_name")
        rating = r.get("rating", 0)
        text = r.get("text", "")
        reply_text = stored_replies.get(author_name, "")
        reviews.append(Review(
            author_name=author_name,
            rating=rating,
            text=text,
            reply_text=reply_text
        ))
    return reviews
