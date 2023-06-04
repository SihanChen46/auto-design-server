from typing import Union

from fastapi import FastAPI
from data_types import Message
from components.message_handler import MessageHandler

app = FastAPI()
message_handler = MessageHandler()


@app.post("/chat")
def chat(message: Message):
    '''handle new user messages'''
    resp_message = message_handler.handle(message)
    return resp_message


# @app.get("/chat")
# def chat():
#     '''fetch chat hisotry of the current conversation'''
#     pass
