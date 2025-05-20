import os
import openai
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_PLACE_ID = os.getenv("GOOGLE_PLACE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 10000))

openai.api_key = OPENAI_API_KEY

@app.get("/reviews", response_class=HTMLResponse)
async def get_reviews(request: Request, lang: str = "en", mode: str = "auto"):
    AUTO_REPLY_MODE = mode == "auto"

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={GOOGLE_PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    reviews = data.get("result", {}).get("reviews", [])

    review_data = []
    for review in reviews:
        reply = None

        if AUTO_REPLY_MODE:
            try:
                prompt = f"お客様からのレビュー:\n{review['text']}\n\nこのレビューに対して、感謝の気持ちを伝える丁寧で自然な返信文を日本語で作成してください。"
                res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "あなたは一流の寿司店の丁寧な店長です。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                )
                reply = res.choices[0].message.content.strip()
            except Exception as e:
                reply = f"(AI返信エラー: {e})"

        review_data.append({
            "author_name": review.get("author_name"),
            "rating": review.get("rating"),
            "text": review.get("text"),
            "reply": reply,
        })

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": review_data,
        "lang": lang,
        "mode": mode
    })
