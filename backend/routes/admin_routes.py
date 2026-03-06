from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.services.api_key_manager import set_api_key, get_api_key, delete_api_key, list_api_keys
from backend.services.workflow_scheduler import get_scheduler
from backend.models.workflow_model import Workflow
from backend.database.db import get_db_connection
from backend.utils.logger import log_info, log_error

# Router uses no prefix; prefix is added when included in app.py
router = APIRouter(prefix="", tags=["admin"])


class APIKeyRequest(BaseModel):
    key_name: str
    key_value: str


class APIKeyResponse(BaseModel):
    key_name: str
    status: str


class WorkflowScheduleRequest(BaseModel):
    workflow_id: str
    schedule_type: str  # "interval", "cron", "once"
    interval_seconds: Optional[int] = None
    cron_expression: Optional[str] = None
    run_at: Optional[str] = None  # ISO datetime string


class IntegrationConfigRequest(BaseModel):
    integration_type: str  # "email", "api"
    config: dict


@router.post("/api-keys", response_model=APIKeyResponse)
async def set_api_key_endpoint(request: APIKeyRequest):
    """
    Set an API key for integrations
    """
    try:
        set_api_key(request.key_name, request.key_value)
        log_info(f"API key set: {request.key_name}")
        return APIKeyResponse(key_name=request.key_name, status="success")
    except Exception as e:
        log_error(f"Error setting API key: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api-keys")
async def list_api_keys_endpoint():
    """
    List all stored API key names (values are hidden)
    """
    try:
        keys = list_api_keys()
        return {"api_keys": keys, "count": len(keys)}
    except Exception as e:
        log_error(f"Error listing API keys: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api-keys/{key_name}")
async def delete_api_key_endpoint(key_name: str):
    """
    Delete an API key
    """
    try:
        delete_api_key(key_name)
        log_info(f"API key deleted: {key_name}")
        return {"message": f"API key '{key_name}' deleted successfully"}
    except Exception as e:
        log_error(f"Error deleting API key: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/{workflow_id}/schedule")
async def schedule_workflow(workflow_id: str, request: WorkflowScheduleRequest):
    """
    Schedule a workflow for automatic execution
    """
    try:
        scheduler = get_scheduler()

        if request.schedule_type == "interval":
            if not request.interval_seconds:
                raise HTTPException(status_code=400, detail="interval_seconds required for interval scheduling")
            scheduler.add_workflow(workflow_id, "interval", interval_seconds=request.interval_seconds)

        elif request.schedule_type == "cron":
            if not request.cron_expression:
                raise HTTPException(status_code=400, detail="cron_expression required for cron scheduling")
            scheduler.add_workflow(workflow_id, "cron", cron_expression=request.cron_expression)

        elif request.schedule_type == "once":
            if not request.run_at:
                raise HTTPException(status_code=400, detail="run_at required for one-time scheduling")
            scheduler.add_workflow(workflow_id, "once", run_at=request.run_at)

        else:
            raise HTTPException(status_code=400, detail="Invalid schedule_type. Use 'interval', 'cron', or 'once'")

        log_info(f"Workflow {workflow_id} scheduled: {request.schedule_type}")
        return {"message": f"Workflow {workflow_id} scheduled successfully"}

    except Exception as e:
        log_error(f"Error scheduling workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/workflows/{workflow_id}/schedule")
async def unschedule_workflow(workflow_id: str):
    """
    Remove a workflow from automatic scheduling
    """
    try:
        scheduler = get_scheduler()
        scheduler.remove_workflow(workflow_id)
        log_info(f"Workflow {workflow_id} unscheduled")
        return {"message": f"Workflow {workflow_id} removed from schedule"}
    except Exception as e:
        log_error(f"Error unscheduling workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/scheduled")
async def list_scheduled_workflows():
    """
    List all scheduled workflows
    """
    try:
        scheduler = get_scheduler()
        scheduled = scheduler.list_scheduled_workflows()
        return {"scheduled_workflows": scheduled}
    except Exception as e:
        log_error(f"Error listing scheduled workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/integrations/configure")
async def configure_integration(request: IntegrationConfigRequest):
    """
    Configure integrations (email, API services)
    """
    try:
        if request.integration_type == "email":
            from backend.integrations.email_integration import configure_email_integration

            sender_email = request.config.get("sender_email")
            password = request.config.get("password")
            smtp_server = request.config.get("smtp_server", "smtp.gmail.com")
            port = request.config.get("port", 587)

            if not sender_email or not password:
                raise HTTPException(status_code=400, detail="sender_email and password required for email integration")

            configure_email_integration(sender_email, password, smtp_server, port)

        elif request.integration_type == "api":
            from backend.integrations.api_connector import configure_api_integration

            api_name = request.config.get("api_name")
            api_key = request.config.get("api_key")
            base_url = request.config.get("base_url")

            if not api_name or not api_key:
                raise HTTPException(status_code=400, detail="api_name and api_key required for API integration")

            configure_api_integration(api_name, api_key, base_url)

        else:
            raise HTTPException(status_code=400, detail="Invalid integration_type. Use 'email' or 'api'")

        log_info(f"Integration configured: {request.integration_type}")
        return {"message": f"{request.integration_type} integration configured successfully"}

    except Exception as e:
        log_error(f"Error configuring integration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/integrations/test")
async def test_integration(integration_type: str, test_data: dict = None):
    """
    Test integration configuration
    """
    try:
        if integration_type == "email":
            from backend.integrations.email_integration import test_email_integration

            test_email = test_data.get("test_email") if test_data else None
            if not test_email:
                raise HTTPException(status_code=400, detail="test_email required for email integration test")

            result = test_email_integration(test_email)
            return {"test_result": result}

        elif integration_type == "api":
            from backend.integrations.api_connector import test_api_integration

            api_name = test_data.get("api_name") if test_data else None
            test_url = test_data.get("test_url") if test_data else None

            if not api_name:
                raise HTTPException(status_code=400, detail="api_name required for API integration test")

            result = test_api_integration(api_name, test_url)
            return {"test_result": result}

        else:
            raise HTTPException(status_code=400, detail="Invalid integration_type. Use 'email' or 'api'")

    except Exception as e:
        log_error(f"Error testing integration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/status")
async def get_system_status():
    """
    Get system status and statistics
    """
    try:
        conn = get_db_connection()
        workflow_count = 0

        if conn:
            cursor = conn.cursor()
            # Get workflow count
            cursor.execute("SELECT COUNT(*) FROM workflows")
            workflow_count = cursor.fetchone()[0]
            conn.close()
            db_status = "connected"
        else:
            db_status = "disconnected"

        # Get scheduled workflows
        scheduler = get_scheduler()
        scheduled_count = len(scheduler.list_active_workflows())

        # Get API keys count
        api_keys_count = len(list_api_keys())

        return {
            "status": "healthy",
            "database": db_status,
            "workflows": {
                "total": workflow_count,
                "scheduled": scheduled_count
            },
            "integrations": {
                "api_keys_configured": api_keys_count
            }
        }

    except Exception as e:
        log_error(f"Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))