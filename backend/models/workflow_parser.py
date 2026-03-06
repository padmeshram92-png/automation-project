"""
Workflow parser utilities - converts prompts to workflow configurations
"""
from backend.models.workflow_model import Workflow, TriggerConfig, AIStepConfig, ActionConfig


def rule_based_parser(prompt: str) -> dict:
    """Parse prompt using rule-based system"""
    prompt_lower = prompt.lower()
    
    # Detect trigger
    if "email" in prompt_lower:
        trigger = "new_email"
    elif "order" in prompt_lower:
        trigger = "new_order"
    else:
        trigger = "manual_trigger"
    
    # Detect AI step
    if "classify" in prompt_lower:
        ai_step = "classify_text"
    elif "summarize" in prompt_lower:
        ai_step = "summarize_text"
    else:
        ai_step = "basic_processing"
    
    # Detect action
    if "reply" in prompt_lower or "send email" in prompt_lower:
        action = "send_email"
    elif "api" in prompt_lower:
        action = "call_api"
    elif "save" in prompt_lower:
        action = "save_database"
    else:
        action = "log_data"
    
    return {
        "trigger": trigger,
        "ai_step": ai_step,
        "action": action
    }


def call_llm(prompt: str):
    """Call LLM to generate workflow (placeholder for real LLM integration)"""
    try:
        # Example LLM response - replace with actual OpenAI/Gemini API
        if "email" in prompt.lower():
            return {
                "trigger": "new_email",
                "ai_step": "summarize_text",
                "action": "send_email"
            }
    except Exception as e:
        print(f"LLM Error: {e}")
    
    return None


def generate_workflow(prompt: str) -> Workflow:
    """
    Generate workflow from natural language prompt
    Uses hybrid approach: LLM first, fallback to rule parser
    """
    # Step 1: Try LLM
    workflow_dict = call_llm(prompt)
    
    if workflow_dict:
        print("Using LLM-generated workflow")
    else:
        # Step 2: Fallback to rule parser
        print("Using rule-based workflow")
        workflow_dict = rule_based_parser(prompt)
    
    # Convert to Pydantic model
    workflow = Workflow(
        name=prompt[:50],  # Use first 50 chars as name
        prompt=prompt,
        trigger=TriggerConfig(type=workflow_dict["trigger"]),
        ai_step=AIStepConfig(type=workflow_dict["ai_step"]),
        action=ActionConfig(type=workflow_dict["action"])
    )
    
    return workflow
