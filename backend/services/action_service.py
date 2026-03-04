from integrations.email_integration import send_email
from integrations.api_connector import call_api

def execute_action(action, data):

    if action == "send_email":
        send_email(
            to=data.get("to"),
            subject=data.get("subject"),
            message=data.get("message")
        )
        return "Email sent"

    elif action == "call_api":
        response = call_api(
            url=data.get("url"),
            payload=data.get("payload")
        )
        return response

    elif action == "log_data":
        print("Logging data:", data)
        return "Data logged"

    else:
        return "Unknown action"