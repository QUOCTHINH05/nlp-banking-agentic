from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    def chat(self, system: str, user: str) -> str:
        """Send a chat prompt and return the model's text response."""
        ...
