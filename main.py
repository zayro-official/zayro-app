import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_PLACE_ID = os.getenv("GOOGLE_PLACE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 10000))

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def fetch_reviews():
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={GOOGLE_PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])
    return reviews

def generate_reply(review_text, lang="ja"):
    try:
        prompt = f"以下のレビューに対して、レストランのオーナーとして丁寧な返信を書いてください（日本語）：\n\n「{review_text}」"
        if lang == "en":
            prompt = f"As a restaurant owner, write a kind reply to the following review:\n\n\"{review_text}\""

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"(AI返信エラー: {str(e)})"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, lang: str = "ja", mode: str = "auto"):
    reviews = fetch_reviews()
    seen = set()
    filtered_reviews = []

    for review in reviews:
        review_id = review.get("author_name") + str(review.get("time"))
        if review_id not in seen:
            seen.add(review_id)
            filtered_reviews.append(review)

    enriched_reviews = []
    for review in filtered_reviews:
        reply = ""
        if mode == "auto":
            reply = generate_reply(review.get("text", ""), lang)
        enriched_reviews.append({
            "author_name": review.get("author_name"),
            "rating": int(review.get("rating", 0)),
            "text": review.get("text"),
            "reply": reply
        })

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": enriched_reviews,
        "lang": lang,
        "mode": mode
    })
