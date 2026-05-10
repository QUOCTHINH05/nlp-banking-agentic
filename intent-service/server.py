import grpc
from concurrent import futures
import torch
from unsloth import FastLanguageModel
import intent_service_pb2
import intent_service_pb2_grpc

MODEL_PATH = "/content/drive/MyDrive/model"

INTENT_LABELS = [
    "activate_my_card", "age_limit", "card_arrival", "change_pin",
    "exchange_rate", "lost_or_stolen_card", "passcode_forgotten",
    "request_refund", "terminate_account", "transfer_timing"
]

class IntentServiceHandler(intent_service_pb2_grpc.IntentServiceServicer):
    def __init__(self):
        print("Loading Unsloth model and adapter...")
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name = MODEL_PATH,
            max_seq_length = 2048,
            load_in_4bit = True,
        )
        FastLanguageModel.for_inference(self.model)
        print("Model loaded successfully.")

    def IntentRecognizer(self, request, context):
        prompt = f"Customer message: {request.message}\nIntent:"

        inputs = self.tokenizer([prompt], return_tensors = "pt").to("cuda")

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens = 20)
            result = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

        print(f"Predicted intent: {result}")
        predicted_intent = "unknown"
        for label in INTENT_LABELS:
            if label in result.lower():
                predicted_intent = label
                break

        return intent_service_pb2.IntentResponse(
            intent=predicted_intent,
            confidence=1.0,
            reason="Prediction completed via Unsloth"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(IntentServiceHandler(), server)
    server.add_insecure_port('[::]:50051')
    print("Intent Service is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
