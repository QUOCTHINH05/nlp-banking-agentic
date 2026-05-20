from app.data.policies import POLICIES, DEFAULT_POLICY
from app.core.schemas import PolicyResult

class PolicyNode:
    def __init__(self):
        self.policies = POLICIES
        self.default_policy = DEFAULT_POLICY

    def run(self, intent: str) -> PolicyResult:
        policy = self.policies.get(intent, self.default_policy)
        return PolicyResult(policy=policy, found=(intent in self.policies))