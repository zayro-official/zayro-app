import os
import openai
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_PLACE_ID = os.environ.get("GOOGLE_PLACE_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

AUTO_REPLY_MODE = True  # デフォルトは自動返信モード

@app.get("/", response_class=RedirectResponse)
async def root():
    return "/reviews"

@app.get("/reviews", response_class=HTMLResponse)
async def read_reviews(request: Request, lang: str = "en", mode: str = "auto"):
    global AUTO_REPLY_MODE
    AUTO_REPLY_MODE = (mode == "auto")

    google_reviews_url = (
        f"https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={GOOGLE_PLACE_ID}&fields=reviews&language={lang}&key={GOOGLE_API_KEY}"
    )
    response = requests.get(google_reviews_url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])

    review_data = []
    for review in reviews:
        reply = None
        if "original_language" in review:
            continue  # 翻訳レビューを除外

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
        "auto_mode": AUTO_REPLY_MODE,
    })
