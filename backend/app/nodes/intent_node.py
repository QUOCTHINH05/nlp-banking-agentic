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

Known intents: activate_my_card, age_limit, card_arrival, change_pin, exchange_rate, lost_or_stolen_card, passcode_forgotten, request_refund, terminate_account, transfer_timing, dispute_transaction, check_balance, update_contact_info, apply_for_credit_line, cancel_subscription, report_suspicious_activity, request_overdraft_protection, check_transaction_history, apply_for_new_card, update_beneficiary

Confidence Guidelines:
- 0.9-1.0: Message clearly matches one intent with no ambiguity
- 0.7-0.9: Message matches intent well with minor ambiguity
- 0.5-0.7: Message could match multiple intents
- 0.3-0.5: Message is vague or unclear
- 0.0-0.3: Message does not match any known intent

Rules:
- Always respond with valid JSON.
- If the intent is unclear or not in the known list, use "unknown".
- Confidence should reflect how certain you are (0.0-1.0) based on the guidelines above.
- Keep reason brief and explain your confidence level."""


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
            
            # Debug: Print raw response
            print(f"[IntentNode] Raw Ollama response: {response_text}")
            
            # Check for LLM errors
            if "[LLM ERROR]" in response_text:
                print(f"[IntentNode] Ollama error: {response_text}")
                return IntentResult(
                    intent="unknown",
                    confidence=0.0,
                    reason=f"Ollama service error: {response_text[:50]}"
                )
            
            # Parse JSON response
            import json
            response_obj = json.loads(response_text)
            
            intent = response_obj.get("intent", "unknown")
            confidence = float(response_obj.get("confidence", 0.0))
            reason = response_obj.get("reason", "Failed to parse")
            
            print(f"[IntentNode] Parsed - Intent: {intent}, Confidence: {confidence:.2%}, Reason: {reason}")
            
            return IntentResult(
                intent=intent,
                confidence=confidence,
                reason=reason
            )
        except Exception as e:
            print(f"Error detecting intent: {e}")
            return IntentResult(
                intent="unknown",
                confidence=0.0,
                reason=f"Detection error: {str(e)}"
            )