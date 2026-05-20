"""
Validation Node.
Checks whether the generated draft response is acceptable before sending.
"""
from backend.app.core.schemas import ValidationResult


MIN_DRAFT_LENGTH = 30
MIN_CONFIDENCE = 0.4


class ValidationNode:
    def run(self, draft: str, confidence: float, missing_info: str | None) -> ValidationResult:
        issues = []

        if len(draft.strip()) < MIN_DRAFT_LENGTH:
            issues.append("Draft response is too short.")

        if confidence < MIN_CONFIDENCE:
            issues.append(f"Intent confidence too low ({confidence:.2f}); response may be inaccurate.")

        if "[LLM ERROR]" in draft:
            issues.append("LLM returned an error; draft is invalid.")

        if issues:
            return ValidationResult(valid=False, issues=" | ".join(issues))
        return ValidationResult(valid=True)
