import requests
import logging
from app.core.settings import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip('/')
        logger.info(f"Ollama client initialized with URL: {self.base_url}")

    def chat(self, system: str, user: str): 
        prompt = f"System: {system}\nUser: {user}"
        result = self.generate(model=settings.RESPONSE_MODEL, prompt=prompt)
        return result.get("response", "[LLM ERROR] No response generated")
    
    def generate(self, model: str, prompt: str, system: str = None, stream: bool = False):
        url = f"{self.base_url}/api/generate"
        payload = {"model": model, "prompt": prompt, "system": system, "stream": stream}
    
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "ngrok-skip-browser-warning": "true",
            "X-Pinggy-No-Screen": "true" 
        }

        try:
            logger.info(f"Calling Ollama API: {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=180)
            logger.info(f"Ollama API response status: {response.status_code}")
            
            # Kiểm tra nếu request thành công (200 OK)
            if response.status_code != 200:
                error_msg = f"API Error {response.status_code}: {response.text[:200]}"
                logger.error(error_msg)
                return {"response": f"[LLM ERROR] {error_msg}"}

            # Thử parse JSON, nếu lỗi thì in ra nội dung nhận được để debug
            try:
                return response.json()
            except Exception as e:
                error_msg = f"Failed to parse JSON: {str(e)}"
                logger.error(error_msg)
                logger.error(f"Response text: {response.text[:500]}")
                return {"response": f"[LLM ERROR] {error_msg}"}

        except requests.exceptions.Timeout:
            error_msg = f"Timeout: Ollama API did not respond within 180 seconds"
            logger.error(error_msg)
            return {"response": f"[LLM ERROR] {error_msg}"}
        
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection Error: Cannot reach Ollama at {self.base_url}. Check if Ollama is running and URL is correct."
            logger.error(error_msg)
            logger.error(f"Original error: {str(e)}")
            return {"response": f"[LLM ERROR] {error_msg}"}
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Request Error: {str(e)}"
            logger.error(error_msg)
            return {"response": f"[LLM ERROR] {error_msg}"}
            raise