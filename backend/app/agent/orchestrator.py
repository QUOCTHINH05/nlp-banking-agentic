"""
Orchestrator — main agentic pipeline controller.
Calls all nodes in order and collects intermediate trace.
"""
from app.nodes.intent_node import IntentNode
from app.nodes.priority_node import PriorityNode
from app.nodes.policy_node import PolicyNode
from app.nodes.draft_node import DraftNode
from app.nodes.validation_node import ValidationNode
from app.nodes.router_node import RouterNode
from app.core.schemas import AgentResponse


class BankingOrchestrator:
    def __init__(self):
        self.intent_node = IntentNode()
        self.priority_node = PriorityNode()
        self.policy_node = PolicyNode()
        self.draft_node = DraftNode()
        self.validation_node = ValidationNode()
        self.router_node = RouterNode()

    def run(self, message: str) -> AgentResponse:
        trace = {}

        # 1. Intent Detection
        intent_result = self.intent_node.run(message)
        trace["intent"] = intent_result.model_dump()

        # 2. Priority Assessment
        priority_result = self.priority_node.run(message, intent_result.intent)
        trace["priority"] = priority_result.model_dump()

        # 3. Policy Retrieval
        policy_result = self.policy_node.run(intent_result.intent)
        trace["policy"] = policy_result.model_dump()

        # 4. Response Drafting
        draft_result = self.draft_node.run(
            message=message,
            intent=intent_result.intent,
            priority=priority_result.priority,
            policy=policy_result.policy,
        )
        trace["draft"] = draft_result.model_dump()

        # 5. Validation
        validation_result = self.validation_node.run(
            draft=draft_result.draft,
            confidence=intent_result.confidence,
            missing_info=draft_result.missing_info,
        )
        trace["validation"] = validation_result.model_dump()

        # 6. Routing / Escalation
        router_result = self.router_node.run(
            priority=priority_result.priority,
            valid=validation_result.valid,
            missing_info=draft_result.missing_info,
            suggested_action=draft_result.suggested_action,
        )
        trace["routing"] = router_result.model_dump()
        
        # Build final response based on router action
        if router_result.action == "escalate":
            reply = None
            escalation_reason = router_result.reason
        else:
            reply = draft_result.draft
            escalation_reason = None

        return AgentResponse(
            action=router_result.action,
            reply=reply,
            escalation_reason=escalation_reason,
            trace=trace,
        )
