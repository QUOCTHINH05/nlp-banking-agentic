import os
class Settings:
    def __init__(self):
        self.OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://erajd-34-19-121-41.run.pinggy-free.link")
        self.RESPONSE_MODEL: str = os.getenv("RESPONSE_MODEL", "gpt-oss:20b")
        self.INTENT_SERVICE_URL: str = os.getenv("INTENT_SERVICE_URL", "roasr-35-237-251-53.run.pinggy-free.link:43749")

settings = Settings()