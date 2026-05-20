class PriorityNode:
    def __init__(self):
        self.priority_map = {
            "lost_or_stolen_card": "High",
            "activate_my_card": "Medium",
            "change_pin": "Medium",
            "transfer_timing": "Medium",
            "exchange_rate": "Low",
            "age_limit": "Low",
            "card_arrival": "Medium",
            "passcode_forgotten": "Medium",
            "request_refund": "High",
            "terminate_account": "High",
            "dispute_transaction": "High",
            "check_balance": "Low",
            "update_contact_info": "Low",
            "apply_for_credit_line": "Medium",
            "cancel_subscription": "Medium",
            "report_suspicious_activity": "High",
            "request_overdraft_protection": "Medium",
            "check_transaction_history": "Low",
            "apply_for_new_card": "Medium",
            "update_beneficiary": "Medium"
        }

    def run(self, message: str, intent: str): 
        priority = self.priority_map.get(intent, "Medium")
        print(f"[PriorityNode] Intent: {intent} -> Priority: {priority}")
        from app.core.schemas import PriorityResult
        return PriorityResult(priority=priority.lower(), reason="Mapped from intent")