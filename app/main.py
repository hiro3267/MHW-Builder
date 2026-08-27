from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.models.build import Build

from app.routers import armas, armaduras, decoracoes, kinsects, talismas, builds
from app.routers.armas import carregar_armas
from app.routers.armaduras import carregar_armaduras
from app.routers.kinsects import carregar_kinsects
from app.routers.talismas import carregar_talismas

app = FastAPI(title="MHW Build Planner")

templates = Jinja2Templates(directory="app/templates")

app.include_router(armas.router)
app.include_router(armaduras.router)
app.include_router(decoracoes.router)
app.include_router(kinsects.router)
app.include_router(talismas.router)
app.include_router(builds.router)


@app.get("/health")
def health_check():
    return {"Status": "OK"}

@app.get("/ping")
def ping():
    return "HTMX is working!"

@app.get("/")
def index(request: Request):
    todas_armaduras = carregar_armaduras()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "titulo": "MHW Build Planner",
            "armas": carregar_armas(),
            "kinsects": carregar_kinsects(),
            "talismas": carregar_talismas(),
            "cabecas": [a for a in todas_armaduras if a.peca == "cabeca"],
            "peitos": [a for a in todas_armaduras if a.peca == "peito"],
            "bracos": [a for a in todas_armaduras if a.peca == "gloves"],
            "cinturas": [a for a in todas_armaduras if a.peca == "cintura"],
            "pernas": [a for a in todas_armaduras if a.peca == "perna"],
            "build": Build(),
        },
    )