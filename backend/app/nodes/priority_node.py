class PriorityNode:
    def __init__(self):
        self.priority_map = {
            "lost_or_stolen_card": "High",
            "activate_my_card": "Medium",
            "change_pin": "High",
            "transfer_timing": "Medium",
            "exchange_rate": "Low",
            "age_limit": "Low",
            "card_arrival": "Medium",
            "passcode_forgotten": "High",
            "request_refund": "High",
            "terminate_account": "High"
        }

    def run(self, message: str, intent: str): 
        priority = self.priority_map.get(intent, "Medium")
        print(f"[PriorityNode] Intent: {intent} -> Priority: {priority}")
        from app.core.schemas import PriorityResult
        return PriorityResult(priority=priority.lower(), reason="Mapped from intent")