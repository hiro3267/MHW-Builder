import json
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.models.kinsect import Kinsect

router = APIRouter(prefix="/kinsects", tags=["kinsects"])
templates = Jinja2Templates(directory="app/templates")

DATA_PATH = Path("app/data/kinsects.json")


def carregar_kinsects() -> list[Kinsect]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)
    return [Kinsect(**item) for item in dados]


@router.get("")
def listar_kinsects(request: Request):
    kinsects = carregar_kinsects()
    return templates.TemplateResponse(
        request=request, name="_lista_kinsects.html", context={"kinsects": kinsects}
    )