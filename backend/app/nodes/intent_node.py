import grpc
from backend.app.nodes import intent_service_pb2 
from backend.app.nodes import intent_service_pb2_grpc 
from backend.app.core.settings import settings
from backend.app.core.schemas import IntentResult

class IntentNode:
    def __init__(self):
        self.channel = grpc.insecure_channel(settings.INTENT_SERVICE_URL)
        self.stub = intent_service_pb2_grpc.IntentServiceStub(self.channel)

    def run(self, message: str):
        """
        Gửi message tới model server và nhận intent dự đoán
        """
        try:
            request = intent_service_pb2.IntentRequest(message=message)
            response = self.stub.IntentRecognizer(request)
            return IntentResult(
            intent=response.intent,
            confidence=response.confidence,
            reason=response.reason
        )
        except Exception as e:
            print(f"Error calling Intent Service: {e}")
            return IntentResult(
                intent="unknown",
                confidence=0.0,
                reason="Service error"
            )