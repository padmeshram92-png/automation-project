from backend.services.trigger_service import check_trigger
from backend.services.action_service import execute_action
from backend.utils.logger import log_info, log_error


def run_workflow(workflow):
    """
    Execute a complete workflow with trigger check and action execution
    """
    try:
        # Extract trigger and action from workflow
        trigger_type = workflow.trigger.type if hasattr(workflow, 'trigger') else workflow.get("trigger")
        action_type = workflow.action.type if hasattr(workflow, 'action') else workflow.get("action")
        
        log_info(f"Running workflow: {workflow.name if hasattr(workflow, 'name') else 'Unknown'}")
        
        # Check if trigger condition is met
        if check_trigger(trigger_type):
            log_info(f"Trigger '{trigger_type}' condition met")
            
            # Execute the associated action
            result = execute_action(action_type, workflow)
            log_info(f"Workflow executed successfully: {result}")
            
            return {
                "status": "success",
                "message": "Workflow executed successfully",
                "result": result
            }
        else:
            log_info(f"Trigger '{trigger_type}' condition not met")
            return {
                "status": "skipped",
                "message": "Trigger condition not met"
            }
    
    except Exception as e:
        log_error(f"Error running workflow: {str(e)}")
        return {
            "status": "error",
            "message": f"Error executing workflow: {str(e)}"
        }

