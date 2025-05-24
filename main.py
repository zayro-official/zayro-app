from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
import os

app = FastAPI()

# Supabase接続
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# テンプレート設定
templates = Jinja2Templates(directory="templates")

@app.get("/reviews", response_class=HTMLResponse)
async def read_reviews(request: Request):
    try:
        response = supabase.table("zayro_reviews").select("*").execute()
        reviews = response.data if response.data else []
    except Exception as e:
        reviews = []
        print(f"Supabase error: {e}")
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews})
