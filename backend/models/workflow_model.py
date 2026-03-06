from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TriggerConfig(BaseModel):
    """Trigger configuration for workflow"""
    type: str = Field(..., description="Trigger type: email, order, manual, webhook")
    conditions: Optional[dict] = Field(default=None, description="Additional conditions")


class AIStepConfig(BaseModel):
    """AI Processing step configuration"""
    type: str = Field(..., description="AI step type: classify, summarize, process")
    model: Optional[str] = Field(default="gpt-3.5-turbo", description="AI model to use")
    settings: Optional[dict] = Field(default=None, description="Model settings")


class ActionConfig(BaseModel):
    """Action configuration for workflow"""
    type: str = Field(..., description="Action type: email, api, database, log")
    config: Optional[dict] = Field(default=None, description="Action-specific configuration")


class Workflow(BaseModel):
    """Workflow model for automation"""
    id: Optional[str] = Field(default=None, description="Workflow ID")
    name: str = Field(..., description="Workflow name")
    prompt: str = Field(..., description="User prompt that triggered workflow")
    trigger: TriggerConfig = Field(..., description="Trigger configuration")
    ai_step: AIStepConfig = Field(..., description="AI processing step")
    action: ActionConfig = Field(..., description="Action to execute")
    status: str = Field(default="active", description="Workflow status: active, inactive, paused")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Email Classifier",
                "prompt": "Classify incoming emails and send summary",
                "trigger": {
                    "type": "new_email",
                    "conditions": {}
                },
                "ai_step": {
                    "type": "classify_text",
                    "model": "gpt-3.5-turbo"
                },
                "action": {
                    "type": "send_email",
                    "config": {"recipient": "admin@example.com"}
                }
            }
        }


class WorkflowResponse(BaseModel):
    """Response model for workflow operations"""
    message: str
    workflow: Optional[Workflow] = None
    data: Optional[dict] = None


class PromptRequest(BaseModel):
    """Request model for prompt generation"""
    prompt: str = Field(..., description="Natural language prompt")
    
    
class PromptResponse(BaseModel):
    """Response model for generated workflow from prompt"""
    prompt: str
    workflow: Workflow