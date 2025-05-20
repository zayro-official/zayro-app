import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_PLACE_ID = os.getenv("GOOGLE_PLACE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Googleレビュー取得関数（返信も含めて）
def get_google_reviews():
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={GOOGLE_PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])
    return sorted(reviews, key=lambda x: x.get("time", 0), reverse=True)

# AIによる返信生成（返信がない場合のみ）
def generate_ai_reply(text, lang="ja"):
    prompt = {
        "ja": f"以下のレビューに対して、寿司レストランのオーナーとして丁寧で親しみやすい返信を書いてください：\n\n{text}",
        "en": f"Write a friendly and professional reply to the following sushi restaurant review:\n\n{text}"
    }

    try:
        result = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt[lang]}],
            temperature=0.7,
            max_tokens=150
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        return f"(AI返信エラー: {str(e)})"

# レビュー表示
@app.get("/reviews", response_class=HTMLResponse)
async def show_reviews(request: Request):
    lang = request.query_params.get("lang", "en")
    reviews = get_google_reviews()

    for review in reviews:
        review["stars"] = "★" * int(review.get("rating", 0))

        # 既にオーナー返信があるか？
        if "author_response" in review:
            review["reply"] = review["author_response"]
            review["replied_by"] = "manual"
        else:
            review["reply"] = generate_ai_reply(review.get("text", ""), lang)
            review["replied_by"] = "ai"

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": reviews,
        "lang": lang,
    })

# Render動作確認用ルート
@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h2>ZAYRO is running. Go to <a href='/reviews?lang=ja'>/reviews</a></h2>"
