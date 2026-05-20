from pydantic import BaseModel
from typing import Optional


# --- Request / Response ---

class AgentRequest(BaseModel):
    message: str

class AgentResponse(BaseModel):
    action: str          # "send_reply" | "ask_more_info" | "escalate"
    reply: Optional[str] = None
    escalation_reason: Optional[str] = None
    trace: dict          # intermediate node outputs


# --- Node output schemas ---

class IntentResult(BaseModel):
    intent: str
    confidence: float
    reason: str

class PriorityResult(BaseModel):
    priority: str        # "low" | "medium" | "high"
    reason: str

class PolicyResult(BaseModel):
    policy: str
    found: bool

class DraftResult(BaseModel):
    draft: str
    missing_info: Optional[str] = None
    suggested_action: str

class ValidationResult(BaseModel):
    valid: bool
    issues: Optional[str] = None

class RouterResult(BaseModel):
    action: str
    reason: str
