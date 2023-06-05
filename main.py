from fastapi import FastAPI
from data_types import Message

app = FastAPI()


@app.post("/handle_message")
def handle_chat(message: Message):
    rspContent = message.dict()["content"]
    return {"respContent": rspContent}
