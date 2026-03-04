from fastapi import FastAPI
from routes.workflow import router as workflow_router
from routes.prompt_routes import router as prompt_router

app = FastAPI()

app.include_router(workflow_router, prefix="/workflow")
app.include_router(prompt_router, prefix="/prompt")

@app.get("/")
def home():
    return {"message": "Automation API running"}
