import json
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.models.talisma import Talisma

router = APIRouter(prefix="/talismas", tags=["talismas"])
templates = Jinja2Templates(directory="app/templates")

DATA_PATH = Path("app/data/talismas.json")


@lru_cache
def carregar_talismas() -> list[Talisma]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)
    return [Talisma(**item) for item in dados]


@router.get("")
def listar_talismas(request: Request):
    talismas = carregar_talismas()
    return templates.TemplateResponse(
        request=request, 
        name="_lista_talismas.html",
        context={"talismas": talismas}
    )