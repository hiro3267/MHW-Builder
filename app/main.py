from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.routers import armas, armaduras, decoracoes, kinsects, talismas

app = FastAPI(title="MHW Build Planner")

templates = Jinja2Templates(directory="app/templates")

app.include_router(armas.router)
app.include_router(armaduras.router)
app.include_router(decoracoes.router)
app.include_router(kinsects.router)
app.include_router(talismas.router)


@app.get("/health")
def health_check():
    return {"Status": "OK"}

@app.get("/ping")
def ping():
    return "HTMX is working!"

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"titulo": "MHW Build Planner"}
    )