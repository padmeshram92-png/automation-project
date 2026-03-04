from fastapi import APIRouter
from models.workflow_model import Workflow
from services.automation_engine import run_workflow

router = APIRouter()

# Temporary in-memory storage
workflow_store = []

# Create workflow
@router.post("/create")
def create_workflow(workflow: Workflow):
    workflow_store.append(workflow)
    return {
        "message": "Workflow created successfully",
        "workflow": workflow
    }

# Get all workflows
@router.get("/list")
def list_workflows():
    return {
        "workflows": workflow_store
    }

# Run workflow
@router.post("/run")
def run(workflow: Workflow):

    result = run_workflow(workflow)

    return {
        "message": "Workflow executed",
        "result": result
    }
