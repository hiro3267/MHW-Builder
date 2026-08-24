from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI(title="MHW Build Planner")

templates = Jinja2Templates(directory="app/templates")

@app.get("/health")
def health_check():
    return {"Status": "OK"}

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"titulo": "MHW Build Planner"}
    )