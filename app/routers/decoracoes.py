import json
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.models.decoracao import Decoracao

router = APIRouter(prefix="/decoracoes", tags=["decoracoes"])
templates = Jinja2Templates(directory="app/templates")

DATA_PATH = Path("app/data/decoracoes.json")

@lru_cache
def carregar_decoracoes() -> list[Decoracao]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)
    return [Decoracao(**item) for item in dados]


@router.get("")
def listar_decoracoes(request: Request):
    decoracoes = carregar_decoracoes()
    return templates.TemplateResponse(
        request=request, name="_lista_decoracoes.html", context={"decoracoes": decoracoes}
    )