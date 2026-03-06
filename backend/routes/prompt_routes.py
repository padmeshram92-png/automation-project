from fastapi import APIRouter, HTTPException
from backend.models.workflow_model import PromptRequest, PromptResponse, Workflow
from backend.models.workflow_parser import generate_workflow
from backend.utils.logger import log_info, log_error

router = APIRouter()


@router.post("/generate-workflow", response_model=PromptResponse)
def generate_workflow_from_prompt(request: PromptRequest):
    """
    Generate a workflow from a natural language prompt
    
    Args:
        request: PromptRequest containing the user's prompt
        
    Returns:
        PromptResponse with generated workflow
    """
    try:
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        log_info(f"Generating workflow from prompt: {request.prompt[:100]}")
        
        # Generate workflow using parser
        workflow = generate_workflow(request.prompt)
        
        log_info(f"Workflow generated successfully: {workflow.name}")
        
        return PromptResponse(
            prompt=request.prompt,
            workflow=workflow
        )
    
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error generating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating workflow: {str(e)}")

