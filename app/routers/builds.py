import json

from typing import Annotated, Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.models.build import Build
from app.routers.armas import carregar_armas
from app.routers.armaduras import carregar_armaduras
from app.routers.kinsects import carregar_kinsects
from app.routers.talismas import carregar_talismas
from app.routers.decoracoes import carregar_decoracoes
from app.routers.skills import carregar_niveis_maximos
from app.services.builds_service import (
    salvar_build,
    listar_builds,
    obter_build,
)


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def resolver_nome(lista, id_):
    if not id_:
        return None

    return next(
        (item.nome for item in lista if str(item.id) == str(id_)),
        None,
    )


def validar_decoracoes(item, decoracoes_ids, decoracoes):
    slots = [slot for slot in item.slots if slot > 0] if item else []

    for indice, decoracao_id in enumerate(decoracoes_ids):
        if not decoracao_id:
            continue

        if item is None:
            return "Selecione um equipamento antes de adicionar decorações."

        decoracao = next(
            (d for d in decoracoes if str(d.id) == str(decoracao_id)),
            None,
        )

        if decoracao is None:
            return "Uma das decorações selecionadas não existe."

        if indice >= len(slots):
            return "Há mais decorações selecionadas do que slots disponíveis."

        if decoracao.tamanho > slots[indice]:
            return (
                f"A decoração {decoracao.nome} não cabe no slot "
                f"de nível {slots[indice]}."
            )

    return None


# --------------------------------------------------
# Modais e seletores
# --------------------------------------------------

@router.get("/arma-modal", response_class=HTMLResponse)
def arma_modal(request: Request):
    return templates.TemplateResponse(
        "_arma_modal.html",
        {"request": request},
    )


@router.get("/armas-modal-lista", response_class=HTMLResponse)
def listar_armas_modal(
    request: Request,
    busca: str = "",
    tipo: str = "",
):
    with open("app/data/armas.json", encoding="utf-8") as f:
        armas = json.load(f)

    if tipo:
        armas = [a for a in armas if a["tipo"] == tipo]

    if busca:
        armas = [
            a for a in armas
            if busca.lower() in a["nome"].lower()
        ]

    return templates.TemplateResponse(
        "_lista_armas_modal.html",
        {"request": request, "armas": armas},
    )


@router.get("/kinsect-select")
def kinsect_select(
    request: Request,
    arma_id: Optional[str] = None,
):
    armas = carregar_armas()
    arma = next(
        (a for a in armas if str(a.id) == str(arma_id)),
        None,
    )

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
def decoracoes_select(
    request: Request,
    campo: str,
    item_id: Optional[str] = None,
):
    origem = {
        "arma": carregar_armas(),
        "cabeca": carregar_armaduras(),
        "peito": carregar_armaduras(),
        "bracos": carregar_armaduras(),
        "cintura": carregar_armaduras(),
        "pernas": carregar_armaduras(),
    }

    itens = origem.get(campo)

    item = (
        next(
            (i for i in itens if str(i.id) == str(item_id)),
            None,
        )
        if itens
        else None
    )

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


# --------------------------------------------------
# Minhas builds: rotas específicas primeiro
# --------------------------------------------------

@router.get(
    "/minhas-builds/salvar-modal",
    response_class=HTMLResponse,
)
def modal_salvar_build(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="_salvar_build_modal.html",
        context={},
    )


@router.get("/minhas-builds/api/{build_id}")
def obter_build_salva(build_id: int):
    registro = obter_build(build_id)

    if registro is None:
        return JSONResponse(
            {"erro": "Build não encontrada."},
            status_code=404,
        )

    return {
        "id": registro["id"],
        "nome": registro["nome"],
        "dados": registro["dados"].model_dump(),
    }


@router.get("/minhas-builds/{build_id}")
def carregar_build_salva(build_id: int):
    registro = obter_build(build_id)

    if registro is None:
        return JSONResponse(
            {"erro": "Build não encontrada."},
            status_code=404,
        )

    return {
        "id": registro["id"],
        "nome": registro["nome"],
        "dados": registro["dados"].model_dump(),
    }


@router.get("/minhas-builds", response_class=HTMLResponse)
def minhas_builds(request: Request):
    builds_salvas = listar_builds()

    return templates.TemplateResponse(
        request=request,
        name="_minhas_builds.html",
        context={"builds_salvas": builds_salvas},
    )


@router.post(
    "/minhas-builds/salvar",
    response_class=HTMLResponse,
)
async def salvar_build_atual(request: Request):
    formulario = await request.form()

    nome = str(formulario.get("nome", "")).strip()

    if not nome:
        return HTMLResponse(
            "Informe um nome para a build.",
            status_code=400,
        )

    def obter_id(campo: str) -> str | None:
        valor = formulario.get(campo)
        return str(valor) if valor else None

    def obter_decoracoes(campo: str) -> list[str | None]:
        return [
            str(valor) if valor else None
            for valor in formulario.getlist(campo)
        ]

    build = Build(
        arma_id=obter_id("arma_id"),
        kinsect_id=obter_id("kinsect_id"),
        cabeca_id=obter_id("cabeca_id"),
        peito_id=obter_id("peito_id"),
        bracos_id=obter_id("bracos_id"),
        cintura_id=obter_id("cintura_id"),
        pernas_id=obter_id("pernas_id"),
        talisma_id=obter_id("talisma_id"),
        arma_decoracoes=obter_decoracoes("arma_decoracoes"),
        cabeca_decoracoes=obter_decoracoes("cabeca_decoracoes"),
        peito_decoracoes=obter_decoracoes("peito_decoracoes"),
        bracos_decoracoes=obter_decoracoes("bracos_decoracoes"),
        cintura_decoracoes=obter_decoracoes("cintura_decoracoes"),
        pernas_decoracoes=obter_decoracoes("pernas_decoracoes"),
    )

    salvar_build(nome, build)

    return templates.TemplateResponse(
        request=request,
        name="_minhas_builds.html",
        context={"builds_salvas": listar_builds()},
    )


# --------------------------------------------------
# Minhas builds: recuperar equipamentos por ID
# --------------------------------------------------

@router.get("/minhas-builds/equipamentos/{tipo}/{item_id}")
def obter_equipamento_salvo(tipo: str, item_id: str):
    fontes = {
        "arma": carregar_armas,
        "armadura": carregar_armaduras,
        "kinsect": carregar_kinsects,
        "talisma": carregar_talismas,
        "decoracao": carregar_decoracoes,
    }

    carregar = fontes.get(tipo)

    if carregar is None:
        return JSONResponse(
            {"erro": "Tipo de equipamento inválido."},
            status_code=400,
        )

    itens = carregar()

    item = next(
        (
            equipamento
            for equipamento in itens
            if str(equipamento.id) == str(item_id)
        ),
        None,
    )

    if item is None:
        return JSONResponse(
            {"erro": "Equipamento não encontrado."},
            status_code=404,
        )

    return item.model_dump(mode="json")

# --------------------------------------------------
# Montagem e cálculo da build
# --------------------------------------------------

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
    talisma_id: Annotated[str | None, Form()] = None,
    arma_decoracoes: Annotated[list[str] | None, Form()] = None,
    cabeca_decoracoes: Annotated[list[str] | None, Form()] = None,
    peito_decoracoes: Annotated[list[str] | None, Form()] = None,
    bracos_decoracoes: Annotated[list[str] | None, Form()] = None,
    cintura_decoracoes: Annotated[list[str] | None, Form()] = None,
    pernas_decoracoes: Annotated[list[str] | None, Form()] = None,
):
    build = Build(
        arma_id=arma_id,
        kinsect_id=kinsect_id,
        cabeca_id=cabeca_id,
        peito_id=peito_id,
        bracos_id=bracos_id,
        cintura_id=cintura_id,
        pernas_id=pernas_id,
        talisma_id=talisma_id,
        arma_decoracoes=arma_decoracoes or [],
        cabeca_decoracoes=cabeca_decoracoes or [],
        peito_decoracoes=peito_decoracoes or [],
        bracos_decoracoes=bracos_decoracoes or [],
        cintura_decoracoes=cintura_decoracoes or [],
        pernas_decoracoes=pernas_decoracoes or [],
    )

    armas = carregar_armas()
    kinsects = carregar_kinsects()
    todas_armaduras = carregar_armaduras()
    talismas = carregar_talismas()
    decoracoes = carregar_decoracoes()

    equipamentos_decoracoes = [
        (build.arma_id, build.arma_decoracoes, armas),
        (build.cabeca_id, build.cabeca_decoracoes, todas_armaduras),
        (build.peito_id, build.peito_decoracoes, todas_armaduras),
        (build.bracos_id, build.bracos_decoracoes, todas_armaduras),
        (build.cintura_id, build.cintura_decoracoes, todas_armaduras),
        (build.pernas_id, build.pernas_decoracoes, todas_armaduras),
    ]

    for equipamento_id, decoracoes_ids, equipamentos in equipamentos_decoracoes:
        equipamento = next(
            (
                item for item in equipamentos
                if str(item.id) == str(equipamento_id)
            ),
            None,
        )

        erro = validar_decoracoes(
            equipamento,
            decoracoes_ids,
            decoracoes,
        )

        if erro:
            return templates.TemplateResponse(
                request=request,
                name="_build_resumo.html",
                context={"erro": erro},
            )

    pecas_ids = [
        build.cabeca_id,
        build.peito_id,
        build.bracos_id,
        build.cintura_id,
        build.pernas_id,
    ]

    pecas = [
        armadura
        for id_ in pecas_ids
        if id_
        for armadura in todas_armaduras
        if str(armadura.id) == str(id_)
    ]

    defesa_total = sum(armadura.defesa for armadura in pecas)

    resistencias = {
        "fogo": sum(a.resistencia_fogo for a in pecas),
        "agua": sum(a.resistencia_agua for a in pecas),
        "trovao": sum(a.resistencia_trovao for a in pecas),
        "gelo": sum(a.resistencia_gelo for a in pecas),
        "dragao": sum(a.resistencia_dragao for a in pecas),
    }

    niveis_maximos = carregar_niveis_maximos()
    habilidades_totais = {}

    for armadura in pecas:
        for skill in armadura.skills:
            habilidades_totais[skill.nome] = (
                habilidades_totais.get(skill.nome, 0) + skill.nivel
            )

    talisma = next(
        (t for t in talismas if str(t.id) == str(build.talisma_id)),
        None,
    )

    if talisma:
        for skill in talisma.skills:
            habilidades_totais[skill.nome] = (
                habilidades_totais.get(skill.nome, 0) + skill.nivel
            )

    decoracoes_ids = (
        build.arma_decoracoes
        + build.cabeca_decoracoes
        + build.peito_decoracoes
        + build.bracos_decoracoes
        + build.cintura_decoracoes
        + build.pernas_decoracoes
    )

    for decoracao_id in decoracoes_ids:
        if not decoracao_id:
            continue

        decoracao = next(
            (d for d in decoracoes if str(d.id) == str(decoracao_id)),
            None,
        )

        if decoracao:
            for skill in decoracao.skills:
                habilidades_totais[skill.nome] = (
                    habilidades_totais.get(skill.nome, 0) + skill.nivel
                )

    habilidades = {}

    for nome, nivel in habilidades_totais.items():
        maximo = niveis_maximos.get(nome, nivel)
        habilidades[nome] = {
            "nivel": min(nivel, maximo),
            "maximo": maximo,
        }

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
        "defesa_total": defesa_total,
        "resistencias": resistencias,
        "habilidades": habilidades,
    }

    return templates.TemplateResponse(
        request=request,
        name="_build_resumo.html",
        context=context,
    )