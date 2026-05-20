"""
Intent Detection Node.
Calls Ollama to detect customer intent from their message.
"""
from app.clients.ollama_client import OllamaClient
from app.core.settings import settings
from app.core.schemas import IntentResult
from app.data.policies import KNOWN_INTENTS

SYSTEM_PROMPT = """You are a banking intent classifier. Analyze the customer's message and detect their intent.

You MUST respond with ONLY a JSON object in this exact format:
{
  "intent": "<intent>",
  "confidence": <0.0-1.0>,
  "reason": "<brief explanation>"
}

Known intents: activate_my_card, age_limit, card_arrival, change_pin, exchange_rate, lost_or_stolen_card, passcode_forgotten, request_refund, terminate_account, transfer_timing

Rules:
- Always respond with valid JSON.
- If the intent is unclear or not in the known list, use "unknown".
- Confidence should reflect how certain you are (0.0-1.0).
- Keep reason brief."""


class IntentNode:
    def __init__(self, client: OllamaClient = None):
        self.client = client or OllamaClient(base_url=settings.OLLAMA_BASE_URL)

    def run(self, message: str) -> IntentResult:
        """
        Detect customer intent using Ollama LLM.
        """
        user_prompt = f"Customer message: {message}"
        
        try:
            response_text = self.client.chat(system=SYSTEM_PROMPT, user=user_prompt)
            
            # Parse JSON response
            import json
            response_obj = json.loads(response_text)
            
            return IntentResult(
                intent=response_obj.get("intent", "unknown"),
                confidence=float(response_obj.get("confidence", 0.0)),
                reason=response_obj.get("reason", "Failed to parse")
            )
        except Exception as e:
            print(f"Error detecting intent: {e}")
            return IntentResult(
                intent="unknown",
                confidence=0.0,
                reason=f"Detection error: {str(e)}"
            )