from fastapi import APIRouter, HTTPException
from backend.models.workflow_model import Workflow, WorkflowResponse
from backend.services.automation_engine import run_workflow
from backend.utils.logger import log_info, log_error

router = APIRouter()

# Temporary in-memory storage for workflows
workflow_store = []


@router.post("/create", response_model=WorkflowResponse)
def create_workflow(workflow: Workflow):
    """
    Create a new workflow
    
    Args:
        workflow: Workflow object
        
    Returns:
        Confirmation with workflow details
    """
    try:
        workflow.id = str(len(workflow_store) + 1)
        workflow_store.append(workflow)
        
        log_info(f"Workflow created: {workflow.name}")
        
        return WorkflowResponse(
            message="Workflow created successfully",
            workflow=workflow
        )
    except Exception as e:
        log_error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating workflow: {str(e)}")


@router.get("/list")
def list_workflows():
    """
    Get all workflows
    
    Returns:
        List of all workflows
    """
    try:
        log_info(f"Retrieving {len(workflow_store)} workflows")
        return {
            "count": len(workflow_store),
            "workflows": workflow_store
        }
    except Exception as e:
        log_error(f"Error listing workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run")
def run(workflow: Workflow):
    """
    Execute a workflow
    
    Args:
        workflow: Workflow to execute
        
    Returns:
        Result of workflow execution
    """
    try:
        log_info(f"Executing workflow: {workflow.name}")
        
        result = run_workflow(workflow)
        
        return {
            "message": "Workflow executed",
            "result": result
        }
    except Exception as e:
        log_error(f"Error running workflow: {str(e)}")
        return {
            "message": "Error executing workflow",
            "error": str(e)
        }


@router.get("/{workflow_id}")
def get_workflow(workflow_id: str):
    """
    Get a specific workflow by ID
    
    Args:
        workflow_id: Workflow ID
        
    Returns:
        Workflow details
    """
    try:
        for workflow in workflow_store:
            if workflow.id == workflow_id:
                return workflow
        
        raise HTTPException(status_code=404, detail="Workflow not found")
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error retrieving workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

