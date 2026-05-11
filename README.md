# Banking AI Agent
## Student information:
- Student ID: 23120089
- Full name: Đỗ Quốc Thịnh
- Class: 23_22
- Subject: Project 3, Applications of Natural Language Processing in Industry
- Assitance Teacher: Mr Lê Đức Khoan
- Lecturer: Dr Nguyễn Hồng Bửu Long
## Objective

A simple AI agentic workflow for customer support in the banking domain.  
The system receives a customer message, identifies the intent, retrieves relevant policy, generates a draft response, validates it, and decides whether to send the reply, ask for more information, or escalate to a human agent.

## Workflow

```
Customer Message
      │
      ▼
Intent Detection Node  (call fine-tuned model from Lab 2)
      │
      ▼
Priority Assessment Node  (include Low, Medium and High)
      │
      ▼
Policy Retrieval Node  (lookup from policies.py)
      │
      ▼
Response Drafting Node  (call LLM gpt-oss:20b via Ollama)
      │
      ▼
Validation Node  (length / confidence / error checks)
      │
      ▼
Router / Escalation Node
      │
   ┌──┴──────────────┐
send_reply       escalate / ask_more_info
```

## Project Structure

```
banking-agentic/
├── Ollama_Pinggy.ipynb
├── README.md
├── requirements.txt
├── run.py
├── .gitignore
├── app/
│   ├── app.py
|   ├── frontend.py
│   ├── core/
│   │   ├── settings.py
│   │   └── schemas.py
│   ├── data/
│   │   └── policies.py
│   ├── clients/
│   │   ├── base.py
│   │   └── ollama_client.py
│   ├── nodes/
│   │   ├── intent_node.py
|   |   ├── intent_service_pb2.py
|   |   ├── intent_service_pb2_grpc.py
│   │   ├── priority_node.py
│   │   ├── policy_node.py
│   │   ├── draft_node.py
│   │   ├── validation_node.py
│   │   └── router_node.py
│   └── agent/
│       └── orchestrator.py
└── examples/
|    └── sample_requests.json
|
└── intent-service/
   |   ├── intent_service.ipynb
   |   ├── intent_service.proto
   │   ├── requirements.txt
   │   └── server.py
   └── model/
       └── drivelink.txt
└── proto/
      ├── intent_service_pb2.py
      ├── intent_service_pb2_grpc.py
      ├── intent_service.proto
      └── test.py
```

Because the saved model file ``adapter_model.safetensors`` is too large, I uploaded it to GG Drive and provide a public link in ``drivelink.txt`` for downloading it.

## How to run
### Step 1: Prepare
- Clone the repository
```bash
git clone https://github.com/QUOCTHINH05/nlp-banking-agentic.git
cd banking-agentic
```

- Create a virtual environment (venv)
```bash
python -m venv .venv
.venv\Scripts\activate
```

- Install dependencies 
```bash
pip install -r requirements.txt
```

### Step 2: Run the Intent Service
Here, I suggest running on Collab and then we use Pinggy to provides a public URL for a service running on localhost. The files I use are all in folder ``intent-service``.
- Firstly, upload the file ``intent_service.ipynb`` to Collab. Note that to choose the **T4 GPU** as accelerator.
- Then run the 1st cell to install denpendencies
- Then run the 2nd cell to create the file ``server.py``
- Then upload the file ``intent_service.proto`` on the same folder of ``server.py`` (usually on \content)
- Then run the 3rd cell to execute the ``intent_service.proto``, we can see 2 python files will be automatically created (``intent_service_pb2.py`` and ``intent_service_pb2_grpc.py``)
```bash
!python -m grpc_tools.protoc -I. \
--python_out=. \
--grpc_python_out=. \
intent_service.proto
```
- Then go to Google Drive, ``drive/MyDrive``, and upload the folder ``model`` to this place to save my banking intent classification model from Lab 2.
- Then, run the 4th cell to mount to Drive.
- Finally, run the last cell to run the ``server.py``, and here our server for intent node is ready to listen to client's request.
- Lastly, we need to run this command in terminal of Collab to get the Pinggy link, Pinggy will provide a public URL for a service running on localhost.
```bash
# Open tunnel TCP through Pinggy (use prefix tcp@)
ssh -o "StrictHostKeyChecking=no" -p 443 -R0:localhost:50051 tcp@a.pinggy.io
```
- Copy the link after ``tcp://``, and then replace the old link with this new link on the `INTENT_SERVICE_URL` in the file ``settings.py``
- We can test whether the intent service is running or not by running the file `test.py` on `intent-service/proto/test.py`

### Step 3: Run the LLM ``gpt-oss:20b``
I suggest that running this LLM on another Google Collab account, with accelerator **T4 GPU**
- Firstly, upload the file `Ollama_Pinggy.ipynb`. 
- This file has 4 cells, run cell 1 and 2 to pull the model ``gpt-oss:20b``
- Cell 3 is an instruction to get the Pinggy link. Run this in the terminal of Collab
```bash
ssh -p 443 -R0:localhost:11434 qr@a.pinggy.io
```
- After that, we will see a http link, copy this link and paste to the link on cell 4th. Note that the link url on cell 4th must have the end point **/api/chat**. Cell 4th is to test the model.
- We also have to use this Pinggy link to paste to the ``OLLAMA_BASE_URL`` of file ``settings.py``

### Step 4: Run the application
Now everything is well-prepared. 
- First, we start the entry point for running the application on ``run.py``. Open a new terminal in VSCode, navigate to folder ``banking-agentic``, then run:
```bash
cd banking-agentic
python run.py
```
- The server will be started on port 8000 on localhost: ``http://localhost:8000/run-agent``
- Then open another terminal in VSCode and start the client on file ``frontend.py``

```bash
cd banking-agentic/app
streamlit run frontend.py
```
- The user interface will appear localhost on port 8501 : ``http://localhost:8501``
- Now we can use this **Banking AI Chatbot** to ask it anything you want about domain banking.


## Video Demo

[DemoVideo](https://drive.google.com/file/d/1-EHg8N0rTD6H4JZ8nvFsNwjslPHae_AR/view?usp=drive_link)
