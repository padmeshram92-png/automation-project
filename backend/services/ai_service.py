def generate_workflow(prompt: str):

    prompt = prompt.lower()

    workflow = {
        "trigger": None,
        "ai_step": None,
        "action": None
    }

    # Detect trigger
    if "email" in prompt:
        workflow["trigger"] = "new_email"

    elif "order" in prompt:
        workflow["trigger"] = "new_order"

    else:
        workflow["trigger"] = "manual_trigger"

    # Detect AI step
    if "classify" in prompt:
        workflow["ai_step"] = "classify_text"

    elif "summarize" in prompt:
        workflow["ai_step"] = "summarize_text"

    else:
        workflow["ai_step"] = "basic_processing"

    # Detect action
    if "reply" in prompt or "send email" in prompt:
        workflow["action"] = "send_email"

    elif "api" in prompt:
        workflow["action"] = "call_api"

    elif "save" in prompt:
        workflow["action"] = "save_database"

    else:
        workflow["action"] = "log_data"

    return workflow
