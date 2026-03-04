from services.trigger_service import check_trigger
from services.action_service import execute_action

def run_workflow(workflow):

    trigger = workflow.get("trigger")
    action = workflow.get("action")

    if check_trigger(trigger):
        result = execute_action(action, workflow)
        return result

    return "Trigger condition not met"
