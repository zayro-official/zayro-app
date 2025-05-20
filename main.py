from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PLACE_ID = os.getenv("PLACE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_ai_reply(review_text: str, lang: str = "en") -> str:
    prompt = {
        "en": f"Reply to the following customer review in a friendly and professional tone:\n\n{review_text}",
        "ja": f"以下のお客様レビューに対して、寿司店として丁寧かつ親しみやすい返信を日本語で書いてください：\n\n{review_text}"
    }
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful sushi restaurant manager."},
                {"role": "user", "content": prompt[lang]},
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "(返信生成エラー)"

@app.get("/reviews", response_class=HTMLResponse)
async def get_reviews(request: Request, lang: str = "en"):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])

    # 最新順に並び替え
    sorted_reviews = sorted(reviews, key=lambda x: x.get("time", 0), reverse=True)

    # AI返信を生成
    for review in sorted_reviews:
        review["ai_reply"] = generate_ai_reply(review["text"], lang)

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": sorted_reviews,
        "lang": lang
    })
