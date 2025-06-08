from fastapi import FastAPI
from pydantic import BaseModel
from kernel_message_engine import process_message
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageInput(BaseModel):
    content: str

@app.post("/api/message")
def handle_message(message: MessageInput):
    response = process_message(message.content)
    return {"response": response}
