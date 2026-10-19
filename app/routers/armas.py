import json
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.models.arma import Arma

router = APIRouter(prefix="/armas", tags=["armas"])
templates = Jinja2Templates(directory="app/templates")

DATA_PATH = Path("app/data/armas.json")


@lru_cache
def carregar_armas() -> list[Arma]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)
    return [Arma(**item) for item in dados]

TIPOS_ARMAS = {
     "grande_espada": "Grande Espada",
    "espada_e_escudo": "Espada e Escudo",
    "laminas_duplas": "Lâminas Duplas",
    "espada_longa": "Espada Longa",
    "martelo": "Martelo",
    "lanca": "Lança",
    "lanca_arma": "Lança-arma",
    "corneta_de_caca": "Corneta de Caça",
    "lamina_carregada": "Lâmina Dínamo",
    "machado_espada": "Transmachado",
    "glaive_insetos": "Glaive Inseto",
    "arco": "Arco",
    "fuzil_leve": "Fuzilarco Leve",
    "fuzil_pesado": "Fuzilarco Pesado",
}

ELEMENTOS = {
    "fire": "Fogo",
    "water": "Água",
    "ice": "Gelo",
    "thunder": "Raio",
    "dragon": "Dragão",
    "poison": "Veneno",
    "sleep": "Sono",
    "paralysis": "Paralisia",
    "blast": "Explosão",
    "nenhum": "Sem elemento",
}

@router.get("/modal")
def modal_armas(request: Request):
    armas = carregar_armas()

    return templates.TemplateResponse(
        request=request,
        name="_lista_armas_modal.html",
        context={
            "armas": armas,
            "tipos_armas": TIPOS_ARMAS,
            "elementos": ELEMENTOS,
        },
    )

@router.get("/modal/lista")
def lista_armas_modal(
    request: Request,
    tipo: str,
    elemento: str = "todos",
):
    armas = carregar_armas()

    armas_filtradas = [
        arma for arma in armas
        if arma.tipo == tipo
        and (
            elemento == "todos"
            or (
                elemento == "nenhum"
                and not arma.elementos
            )
            or any(
                e.tipo == elemento
                for e in (arma.elementos or [])
            )
        )
    ]

    return templates.TemplateResponse(
        request=request,
        name="_lista_armas_filtradas.html",
        context={
            "armas": armas_filtradas,
            "tipo": tipo,
            "elemento": elemento,
        },
    )