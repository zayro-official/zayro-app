from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PLACE_ID = os.getenv("PLACE_ID")

@app.get("/reviews", response_class=HTMLResponse)
async def get_reviews(request: Request, lang: str = "en"):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])

    # 最新順に並び替え
    sorted_reviews = sorted(reviews, key=lambda x: x.get("time", 0), reverse=True)

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": sorted_reviews,
        "lang": lang
    })
