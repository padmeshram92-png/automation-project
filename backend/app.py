from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.workflow_routes import router as workflow_router
from backend.routes.prompt_routes import router as prompt_router
from backend.routes.webhook_routes import router as webhook_router
from backend.routes.admin_routes import router as admin_router

from backend.utils.logger import log_info, log_error
from backend.services.trigger_service import start_automation_engine
from backend.services.workflow_scheduler import get_scheduler

app = FastAPI(
    title="Automation API",
    description="Workflow Automation API with Automatic Triggers and Admin Controls",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router, prefix="/api/workflow", tags=["Workflows"])
app.include_router(prompt_router, prefix="/api/prompt", tags=["Prompts"])
app.include_router(webhook_router, prefix="/api/webhook", tags=["Webhooks"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
def home():
    return {
        "message": "Automation API running",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    log_info("Application startup")

    try:
        start_automation_engine()
        log_info("Automation engine started")
    except Exception as e:
        log_error(f"Automation engine error: {e}")

    try:
        scheduler = get_scheduler()
        scheduler.start_scheduler()
        log_info("Scheduler started")
    except Exception as e:
        log_error(f"Scheduler error: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    log_info("Application shutdown")

    try:
        scheduler = get_scheduler()
        scheduler.stop_scheduler()
        log_info("Scheduler stopped")
    except Exception as e:
        log_error(f"Shutdown error: {e}")