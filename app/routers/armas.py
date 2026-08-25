import json
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.models.arma import Arma

router = APIRouter(prefix="/armas", tags=["armas"])
templates = Jinja2Templates(directory="app/templates")

DATA_PATH = Path("app/data/armas.json")


def carregar_armas() -> list[Arma]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)
    return [Arma(**item) for item in dados]

@router.get("")
def listar_armas(request: Request):
    armas = carregar_armas()
    return templates.TemplateResponse(
        request=request,
        name="_lista_armas.html",
        context={"armas": armas},
    )