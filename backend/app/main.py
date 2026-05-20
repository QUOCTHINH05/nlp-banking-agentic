# app/main.py
from fastapi import FastAPI
from backend.app.core.schemas import AgentRequest, AgentResponse
from backend.app.agent.orchestrator import BankingOrchestrator

app = FastAPI()
orchestrator = BankingOrchestrator()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: AgentRequest):
    result = orchestrator.run(request.message)
    
    final_message = result.reply if result.reply else f" {result.escalation_reason}"
    
    return {
        "response": final_message, 
        "intent": result.trace.get("intent", {}).get("intent")
    }