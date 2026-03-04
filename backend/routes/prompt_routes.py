from fastapi import APIRouter
from services.ai_service import generate_workflow

router = APIRouter()

@router.post("/generate-workflow")
def generate_workflow_from_prompt(prompt: str):

    workflow = generate_workflow(prompt)

    return {
        "prompt": prompt,
        "workflow": workflow
    }
