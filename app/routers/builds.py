import json

from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated, Optional

from app.models.build import Build
from app.routers.armas import carregar_armas
from app.routers.armaduras import carregar_armaduras
from app.routers.kinsects import carregar_kinsects
from app.routers.talismas import carregar_talismas
from app.routers.decoracoes import carregar_decoracoes


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def resolver_nome(lista, id_):
    if not id_:
        return None
    return next((item.nome for item in lista if str(item.id) == str(id_)), None)

@router.get("/arma-modal", response_class=HTMLResponse)
def arma_modal(request: Request):
    return templates.TemplateResponse("_arma_modal.html", {"request": request})

@router.get("/armas-modal-lista", response_class=HTMLResponse)
def listar_armas_modal(request: Request, busca: str = "", tipo: str = ""):
    with open("app/data/armas.json", encoding="utf-8") as f:
        armas = json.load(f)

    if tipo:
        armas = [a for a in armas if a["tipo"] == tipo]
    if busca:
        armas = [a for a in armas if busca.lower() in a["nome"].lower()]

    return templates.TemplateResponse(
        "_lista_armas_modal.html",
        {"request": request, "armas": armas}
    )

@router.get("/kinsect-select")
def kinsect_select(request: Request, arma_id: Optional[str] = None):
    armas = carregar_armas()
    arma = next((a for a in armas if str(a.id) == str(arma_id)), None)

    if not arma or arma.tipo != "glaive_insetos":
        return templates.TemplateResponse(
            request=request,
            name="_kinsect_vazio.html",
            context={},
        )

    return templates.TemplateResponse(
        request=request,
        name="_kinsect_select.html",
        context={"kinsects": carregar_kinsects()},
    )

@router.get("/decoracoes-select/{campo}/{item_id}")
def decoracoes_select(request: Request, campo: str, item_id: Optional[str] = None):
    origem = {
        "arma": carregar_armas(),
        "cabeca": carregar_armaduras(),
        "peito": carregar_armaduras(),
        "bracos": carregar_armaduras(),
        "cintura": carregar_armaduras(),
        "pernas": carregar_armaduras(),
    }

    itens = origem.get(campo)
    item = next((i for i in itens if str(i.id) == str(item_id)), None) if itens else None

    if not item or not item.slots:
        return templates.TemplateResponse(
            request=request,
            name="_decoracoes_select_vazio.html",
            context={"campo": campo},
        )

    return templates.TemplateResponse(
        request=request,
        name="_decoracoes_select.html",
        context={
            "campo": campo,
            "slots": item.slots,
            "decoracoes": carregar_decoracoes(),
        },
    )


@router.post("/build")
def montar_build(
    request: Request,
    arma_id: Annotated[str | None, Form()] = None,
    kinsect_id: Annotated[str | None, Form()] = None,
    cabeca_id: Annotated[str | None, Form()] = None,
    peito_id: Annotated[str | None, Form()] = None,
    bracos_id: Annotated[str | None, Form()] = None,
    cintura_id: Annotated[str | None, Form()] = None,
    pernas_id: Annotated[str | None, Form()] = None,
    talisma_id: Annotated[str | None, Form()] = None
):
    build = Build(
        arma_id=arma_id,
        kinsect_id=kinsect_id,
        cabeca_id=cabeca_id,
        peito_id=peito_id,
        bracos_id=bracos_id,
        cintura_id=cintura_id,
        pernas_id=pernas_id,
        talisma_id=talisma_id
    )
    armas = carregar_armas()
    kinsects = carregar_kinsects()
    todas_armaduras = carregar_armaduras()
    talismas = carregar_talismas()

    context = {
        "build": build,
        "arma_nome": resolver_nome(armas, build.arma_id),
        "kinsect_nome": resolver_nome(kinsects, build.kinsect_id),
        "cabeca_nome": resolver_nome(todas_armaduras, build.cabeca_id),
        "peito_nome": resolver_nome(todas_armaduras, build.peito_id),
        "bracos_nome": resolver_nome(todas_armaduras, build.bracos_id),
        "cintura_nome": resolver_nome(todas_armaduras, build.cintura_id),
        "pernas_nome": resolver_nome(todas_armaduras, build.pernas_id),
        "talisma_nome": resolver_nome(talismas, build.talisma_id),
    }

    return templates.TemplateResponse(
        request=request,
        name="_build_resumo.html",
        context=context
    )