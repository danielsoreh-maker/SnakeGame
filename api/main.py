"""The Big O-Block serveris: REST API rezultātiem un mājaslapa ar Jinja veidnēm."""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from api.db import get_connection

# Server
app = FastAPI()

# BASE_DIR ir mape, kurā atrodas šis fails (api/). Tā serveris vienmēr atrod
# savas mapes, neatkarīgi no tā, no kuras vietas to palaiž.
BASE_DIR = Path(__file__).parent

# Visu, ko pārlūks prasa adresē /static/..., ņem no mapes api/static (CSS).
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Jinja veidnes 
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class Score(BaseModel):
    """Dati, ko serveris pieņem, saglabājot rezultātu (validācija).
    Ja dati neatbilst, FastAPI pats atbild ar 422 un nekas netiek ierakstīts.
    """

    player: str = Field(min_length=1, max_length=20)  # vārds: 1 līdz 20 zīmes
    score: int = Field(ge=0)  # punkti: 0 vai vairāk 

# REST API (spēle runā ar serveri šeit)

# 1. endpoint: POST /scores - saglabā rezultātu
@app.post("/scores", status_code=201)  # 201 = "izveidots"
def add_score(item: Score):
    # "with" saglabā izmaiņas datubāzē, kad bloks beidzas.
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO scores (player, score) VALUES (?, ?)",# ? ir drošas vietas vērtībām (nekad neliek vērtības SQL tekstā ar f-string,jo tā var uzlauzt datubāzi).
            (item.player, item.score))
    return item


# 2. endpoint: GET /scores/top - 5 labākie rezultāti
@app.get("/scores/top")
def top():
    """Atdod 5 labākos rezultātus no lielākā uz mazāko."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT player, score FROM scores "
            "ORDER BY score DESC LIMIT 5").fetchall()
    return [{"player": p, "score": s} for p, s in rows]

# Mājaslapa (HTML lapas, ko atdod serveris)

@app.get("/", response_class=HTMLResponse)  # atbilde ir HTML, nevis JSON
def leaderboard_page(request: Request):
    return templates.TemplateResponse(
        request, "leaderboard.html", {"rows": top()[:5]})   # {"rows": ...} nodod sarakstu veidnei, kur tas ir {% for row in rows %}.top()[:5] paņem pirmos 5 no tā paša saraksta, ko atdod /scores/top.


# Lapa: /rules - spēles noteikumi
@app.get("/rules", response_class=HTMLResponse)
def rules_page(request: Request):
    return templates.TemplateResponse(request, "rules.html")


# Lapa: /players/{name} - spēlētāja profils
@app.get("/players/{name}", response_class=HTMLResponse)
def player_page(request: Request, name: str):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT score FROM scores WHERE player = ? " # Tikai šī spēlētāja rezultāti, labākie pirmie.
            "ORDER BY score DESC", (name,)).fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Spēlētājs nav atrasts")     # Ja nav neviena rezultāta, tāda spēlētāja nav: atbilde 404.
    results = [row[0] for row in rows]
    return templates.TemplateResponse(
        request, "player.html",
        {"name": name,
         "games": len(results),  # cik spēles nospēlētas
         "best": results[0],  # saraksts ir sakārtots, tātad pirmais ir labākais
         "results": results})
# 3. endpoint: GET /players/{name}/stats - spēlētāja statistika
@app.get("/players/{name}/stats")
def player_stats(name: str):
    with get_connection() as conn:
        games, best = conn.execute(
            "SELECT COUNT(*), MAX(score) FROM scores WHERE player = ?",        # COUNT(*) = cik rindu, MAX(score) = lielākais skaitlis
            (name,)).fetchone()
    if games == 0:
        raise HTTPException(status_code=404, detail="Spēlētājs nav atrasts")
    return {"player": name, "games": games, "best": best}