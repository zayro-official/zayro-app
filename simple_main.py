from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ZAYRO backend is live."}

@app.get("/reviews/google")
def get_google_reviews():
    # 環境変数からキーを取得（仮のtest値対応）
    api_key = os.getenv("GOOGLE_API_KEY", "no_key_set")
    place_id = os.getenv("GOOGLE_PLACE_ID", "no_place_id")

    # 仮データを返す（本物のAPI実装は後で）
    return {
        "status": "ok",
        "source": "google",
        "api_key": api_key,
        "place_id": place_id,
        "reviews": [
            {"author": "Taro", "rating": 5, "comment": "最高の寿司でした！"},
            {"author": "Lisa", "rating": 4, "comment": "雰囲気が良いです。"}
        ]
    }

