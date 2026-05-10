import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Lệnh này sẽ tìm biến 'app' bên trong module 'app.app' và chạy server trên host
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)