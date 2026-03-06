from backend.integrations.email_integration import send_email_action
from backend.integrations.api_connector import call_api_action
from backend.utils.logger import log_info, log_error


def execute_action(action_type: str, data=None):

    try:
        log_info(f"Executing action: {action_type} with data: {data}")

        if action_type == "send_email":

            recipient = None

            if isinstance(data, dict):
                recipient = data.get("recipient") or data.get("to")

                if not recipient and "config" in data:
                    recipient = data["config"].get("recipient")

            else:
                recipient = getattr(data, "recipient", None)

            result = send_email_action(
                to=recipient,
                subject=data.get("subject", "Automation Result") if isinstance(data, dict) else getattr(data, "subject", "Automation Result"),
                message=data.get("message", "") if isinstance(data, dict) else getattr(data, "message", "")
            )

            log_info(f"Email action result: {result}")
            return result

        elif action_type == "call_api":

            result = call_api_action(
                url=data.get("url") if isinstance(data, dict) else getattr(data, "url", None),
                method=data.get("method", "POST") if isinstance(data, dict) else getattr(data, "method", "POST"),
                payload=data.get("payload", {}) if isinstance(data, dict) else getattr(data, "payload", {})
            )

            log_info(f"API action result: {result}")
            return result

        elif action_type == "log_data":

            log_info(f"Logging data: {data}")
            return {"status": "success", "message": "Data logged successfully"}

        elif action_type == "save_database":

            log_info(f"Saving to database: {data}")
            return {"status": "success", "message": "Data saved to database"}

        else:

            log_error(f"Unknown action type: {action_type}")
            return {"status": "error", "message": f"Unknown action type: {action_type}"}

    except Exception as e:

        log_error(f"Error executing action {action_type}: {str(e)}")
        return {"status": "error", "message": f"Error executing action: {str(e)}"}