"""
Router / Escalation Node.
Final decision: send reply | ask for more info | escalate to human.
"""
from backend.app.core.schemas import RouterResult


class RouterNode:
    def run(
        self,
        priority: str,
        valid: bool,
        missing_info: str | None,
        suggested_action: str,
    ) -> RouterResult:

        if not valid:
            return RouterResult(
                action="escalate",
                reason="Validation failed; escalating to human agent.",
            )

        if priority == "high":
            return RouterResult(
                action="escalate",
                reason="High-priority issue requires human review.",
            )

        if missing_info:
            return RouterResult(
                action="ask_more_info",
                reason=f"Missing required information: {missing_info}.",
            )

        return RouterResult(action="send_reply", reason="Response is valid and complete.")
