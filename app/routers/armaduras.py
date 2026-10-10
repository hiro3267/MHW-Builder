import json
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

from app.models.armadura import Armadura

router = APIRouter(prefix="/armaduras", tags=["armaduras"])
templates = Jinja2Templates(directory="app/templates")

DATA_PATH = Path("app/data/armaduras.json")


@lru_cache
def carregar_armaduras() -> list[Armadura]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)

    return [Armadura(**item) for item in dados]


@router.get("")
def listar_armaduras(request: Request):
    armaduras = carregar_armaduras()

    return templates.TemplateResponse(
        request=request,
        name="_lista_armaduras.html",
        context={"armaduras": armaduras},
    )


@router.get("/modal")
def modal_armaduras(request: Request, campo: str):
    campos_validos = {
        "cabeca",
        "peito",
        "bracos",
        "cintura",
        "pernas",
    }

    if campo not in campos_validos:
        raise HTTPException(
            status_code=400,
            detail="Peça de armadura inválida",
        )

    armaduras = carregar_armaduras()

    return templates.TemplateResponse(
        request=request,
        name="_lista_armaduras_modal.html",
        context={
            "request": request,
            "armaduras": armaduras,
            "campo": campo,
        },
    )