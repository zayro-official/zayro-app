from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 環境変数の読み込み
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPIアプリの初期化
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ルートパス
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# /reviews 表示
@app.get("/reviews", response_class=HTMLResponse)
async def read_reviews(request: Request):
    try:
        response = supabase.table("zayro_reviews").select("*").execute()
        reviews = response.data
        print("取得データ:", reviews)
    except Exception as e:
        print("Supabase接続エラー:", e)
        reviews = []

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": reviews
    })
