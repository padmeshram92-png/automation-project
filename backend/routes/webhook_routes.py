from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.services.trigger_service import trigger_webhook, get_automation_status, start_automation_engine, stop_automation_engine
from backend.utils.logger import log_info, log_error

router = APIRouter()

@router.post("/trigger/{workflow_id}")
async def trigger_workflow_webhook(workflow_id: str, data: dict = None):
    """
    Webhook endpoint to trigger a workflow
    External services can call this to trigger workflows automatically
    """
    try:
        log_info(f"🪝 Webhook received for workflow: {workflow_id}")

        # Trigger the workflow
        trigger_webhook(workflow_id, data)

        return {
            "status": "success",
            "message": f"Workflow {workflow_id} triggered",
            "data": data
        }

    except Exception as e:
        log_error(f"Error triggering webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_webhook_status():
    """Get automation engine status"""
    try:
        status = get_automation_status()
        return {
            "automation_status": status,
            "webhook_endpoints": [
                f"/api/webhook/trigger/{{workflow_id}}"
            ]
        }
    except Exception as e:
        log_error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start")
async def start_automation(background_tasks: BackgroundTasks):
    """Start the automation engine"""
    try:
        background_tasks.add_task(start_automation_engine)
        return {"status": "success", "message": "Automation engine starting..."}
    except Exception as e:
        log_error(f"Error starting automation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_automation():
    """Stop the automation engine"""
    try:
        stop_automation_engine()
        return {"status": "success", "message": "Automation engine stopped"}
    except Exception as e:
        log_error(f"Error stopping automation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
