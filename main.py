from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"message": "ZAYRO backend is live."}

@app.get("/reviews/google")
def get_google_reviews():
    api_key = os.getenv("GOOGLE_API_KEY", "no_key_set")
    place_id = os.getenv("GOOGLE_PLACE_ID", "no_place_id")
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}&fields=reviews&key={api_key}"
    )
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])
    simplified_reviews = [
        {"author": r.get("author_name"), "rating": r.get("rating"), "comment": r.get("text")}
        for r in reviews
    ]
    return {
        "status": "ok",
        "source": "google",
        "review_count": len(simplified_reviews),
        "reviews": simplified_reviews
    }

# 追加：HTML表示版のレビュー一覧
@app.get("/reviews", response_class=None)
def show_reviews(request: Request):
    api_key = os.getenv("GOOGLE_API_KEY", "no_key_set")
    place_id = os.getenv("GOOGLE_PLACE_ID", "no_place_id")
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}&fields=reviews&key={api_key}"
    )
    response = requests.get(url)
    data = response.json()
    reviews = data.get("result", {}).get("reviews", [])
    simplified_reviews = [
        {"author": r.get("author_name"), "rating": r.get("rating"), "comment": r.get("text")}
        for r in reviews
    ]
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": simplified_reviews})
