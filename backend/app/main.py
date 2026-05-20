# app/main.py
from fastapi import FastAPI
from app.core.schemas import AgentRequest, AgentResponse
from app.agent.orchestrator import BankingOrchestrator

app = FastAPI()
orchestrator = BankingOrchestrator()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/config")
def get_config():
    return {"config": "some_config_value"}

@app.post("/run-agent")
async def run_agent_endpoint(request: AgentRequest):
    result = orchestrator.run(request.message)
    
    final_message = result.reply if result.reply else f" {result.escalation_reason}"
    
    return {
        "response": final_message, 
        "intent": result.trace.get("intent", {}).get("intent"),
        "confidence": result.trace.get("intent", {}).get("confidence"),
        "reason": result.trace.get("intent", {}).get("reason"),
        "action": result.trace.get("routing", {}).get("action"),
    }