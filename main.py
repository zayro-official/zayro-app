import os
import requests
from fastapi import FastAPI

app = FastAPI()

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
        {
            "author": r.get("author_name", ""),
            "rating": r.get("rating", 0),
            "comment": r.get("text", ""),
        }
        for r in reviews
    ]

    return {
        "status": "ok",
        "source": "google",
        "review_count": len(simplified_reviews),
        "reviews": simplified_reviews,
    }
