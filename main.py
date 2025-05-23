@app.get("/reviews", response_class=HTMLResponse)
async def read_reviews(request: Request):
    try:
        response = supabase.table("zayro_reviews").select("*").execute()
        reviews = response.data
    except Exception as e:
        print("Supabase接続エラー:", e)
        reviews = []

    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "reviews": reviews
    })
