"""
Response Drafting Node.
Calls Ollama to generate a customer-facing reply grounded in the retrieved policy.
"""
from app.clients.ollama_client import OllamaClient
from app.core.settings import settings
from app.core.schemas import DraftResult

SYSTEM_PROMPT = """You are a helpful banking customer support agent.
Draft a polite, concise reply to the customer based on:
- Their message
- The detected intent and priority
- The relevant bank policy

Rules:
- Be empathetic and professional.
- Do NOT invent information beyond the policy.
- If critical information is missing (e.g. transaction ID), note it.
- End with a clear next step for the customer.
- Keep the reply under 120 words."""


class DraftNode:
    def __init__(self, client: OllamaClient = None):
        self.client = client or OllamaClient(base_url=settings.OLLAMA_BASE_URL)

    def run(self, message: str, intent: str, priority: str, policy: str) -> DraftResult:
        user_prompt = (
            f"Customer message: {message}\n"
            f"Intent: {intent} | Priority: {priority}\n"
            f"Policy: {policy}\n\n"
            "Draft a reply:"
        )
        
        try:
            draft = self.client.chat(system=SYSTEM_PROMPT, user=user_prompt)
        except Exception as e:
            print(f"[DraftNode] Error calling Ollama: {e}")
            draft = f"[LLM ERROR] Failed to draft response: {str(e)[:100]}"

        missing = None
        if intent == "transfer_failure" and "reference" not in message.lower():
            missing = "transaction reference number"
        elif intent == "refund_request" and "transaction" not in message.lower():
            missing = "transaction details / dispute form"

        suggested = "escalate" if priority == "high" else "send_reply"
        return DraftResult(draft=draft, missing_info=missing, suggested_action=suggested)
