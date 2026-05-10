import grpc
import intent_service_pb2
import intent_service_pb2_grpc

def test_call():
    target = "jhjcb-8-228-11-225.run.pinggy-free.link:46219" 

    channel = grpc.insecure_channel(target)
    stub = intent_service_pb2_grpc.IntentServiceStub(channel)
    
    print(f"Đang gửi tin nhắn thử nghiệm tới: {target}...")
    try:
        response = stub.IntentRecognizer(intent_service_pb2.IntentRequest(
            message="I lost my card and I want to report it"
        ))
        print("--- KẾT QUẢ TỪ COLAB ---")
        print(f"Intent dự đoán: {response.intent}")
        print(f"Độ tin cậy: {response.confidence}")
        print(f"Lý do: {response.reason}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

if __name__ == "__main__":
    test_call()