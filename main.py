from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reviews", response_class=HTMLResponse)
async def read_reviews(request: Request):
    replies = ["Thank you!", "We appreciate your feedback!", "Hope to see you again!"]
    return templates.TemplateResponse("reviews.html", {
        "request": request,
        "replies": replies
    })
