import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API keys
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_PLACE_ID = os.environ.get("GOOGLE_PLACE_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# 言語切替と返信モード切替
@app.get("/", response_class=HTMLResponse)
async def read_reviews(request: Request, lang: str = "ja", mode: str = "ai"):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={GOOGLE_PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])
    replies = []

    if mode == "ai":
        for review in reviews:
            try:
                content = review["text"]
                res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a friendly sushi restaurant owner replying to customer reviews."},
                        {"role": "user", "content": f"Review: {content}\nReply:"}
                    ]
                )
                reply = res.choices[0].message.content.strip()
            except Exception as e:
                reply = f"(AI返信エラー: {str(e)})"
            replies.append(reply)
    else:
        replies = [""] * len(reviews)

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": reviews,
        "replies": replies,
        "lang": lang,
        "mode": mode
    })
