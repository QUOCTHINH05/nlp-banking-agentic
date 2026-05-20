import grpc
from .intent_grpc import intent_service_pb2, intent_service_pb2_grpc

def detect_intent(message: str, host: str = "intent-service:50051"):
    channel = grpc.insecure_channel(host)
    stub = intent_service_pb2_grpc.IntentServiceStub(channel)
    response = stub.DetectIntent(intent_service_pb2.IntentRequest(message=message))
    return response.intent, response.confidence