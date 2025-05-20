import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import openai

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 環境変数からキー読み込み
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_PLACE_ID = os.getenv("GOOGLE_PLACE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Googleレビュー取得
def get_google_reviews():
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={GOOGLE_PLACE_ID}&fields=review&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])
    sorted_reviews = sorted(reviews, key=lambda x: x.get("time", 0), reverse=True)
    return sorted_reviews

# AI返信生成（OpenAI）
def generate_reply(text, lang="ja"):
    prompt_ja = f"以下のカスタマーレビューに対して、寿司レストランの店長として親しみやすく丁寧な返信を日本語で書いてください。\n\nレビュー:「{text}」"
    prompt_en = f"As the owner of a sushi restaurant, write a friendly and professional reply to the following review in English:\n\nReview: \"{text}\""

    prompt = prompt_ja if lang == "ja" else prompt_en

    try:
        result = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return result.choices[0].message["content"].strip()
    except Exception as e:
        return f"(返信生成エラー: {str(e)})"

@app.get("/reviews", response_class=HTMLResponse)
async def show_reviews(request: Request):
    lang = request.query_params.get("lang", "en")
    reviews = get_google_reviews()

    for review in reviews:
        reply = generate_reply(review.get("text", ""), lang=lang)
        review["reply"] = reply
        review["stars"] = "★" * int(review.get("rating", 0))

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": reviews,
        "lang": lang,
    })
