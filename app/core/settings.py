import os
class Settings:
    def __init__(self):
        self.OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://aykre-34-12-209-200.run.pinggy-free.link")
        self.RESPONSE_MODEL: str = os.getenv("RESPONSE_MODEL", "gpt-oss:20b")
        self.INTENT_SERVICE_URL: str = os.getenv("INTENT_SERVICE_URL", "jhjcb-8-228-11-225.run.pinggy-free.link:46219")

settings = Settings()