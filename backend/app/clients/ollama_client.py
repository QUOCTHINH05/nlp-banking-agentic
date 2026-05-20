import requests
import logging
from backend.app.core.settings import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip('/')


    def chat(self, system: str, user: str): 
        prompt = f"System: {system}\nUser: {user}"
        return self.generate(model=settings.RESPONSE_MODEL, prompt=prompt).get("response", "")
    
    def generate(self, model: str, prompt: str, system: str = None, stream: bool = False):
        url = f"{self.base_url}/api/generate"
        payload = {"model": model, "prompt": prompt, "system": system, "stream": stream}
    
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            # Header quan trọng để bỏ qua trang cảnh báo của Pinggy/Ngrok
            "ngrok-skip-browser-warning": "true",
            "X-Pinggy-No-Screen": "true" 
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=180)
            
            # Kiểm tra nếu request thành công (200 OK)
            if response.status_code != 200:
                print(f"API Error {response.status_code}: {response.text}")
                return {"response": "[LLM ERROR] Server returned non-200 status."}

            # Thử parse JSON, nếu lỗi thì in ra nội dung nhận được để debug
            try:
                return response.json()
            except Exception:
                print("Lỗi: Server không trả về JSON. Nội dung nhận được là:")
                print(response.text[:500]) # In 500 ký tự đầu để xem có phải trang HTML không
                return {"response": "[LLM ERROR] Invalid JSON received from server."}

        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {e}")
            raise