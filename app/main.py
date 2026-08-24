from fastapi import FastAPI

app = FastAPI(title="MHW Build Planner")

@app.get("/health")
def health_check():
    return {"Status": "OK"}