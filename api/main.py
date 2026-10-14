from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from api.db import get_connection

app = FastAPI()

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class Score(BaseModel):
    player: str = Field(min_length=1, max_length=20)
    score: int = Field(ge=0)


@app.post("/scores", status_code=201)
def add_score(item: Score):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO scores (player, score) VALUES (?, ?)",
            (item.player, item.score))
    return item


@app.get("/scores/top")
def top():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT player, score FROM scores "
            "ORDER BY score DESC LIMIT 10").fetchall()
    return [{"player": p, "score": s} for p, s in rows]


@app.get("/", response_class=HTMLResponse)
def leaderboard_page(request: Request):
    return templates.TemplateResponse(
        request, "leaderboard.html", {"rows": top()[:5]})


@app.get("/rules", response_class=HTMLResponse)
def rules_page(request: Request):
    return templates.TemplateResponse(request, "rules.html")