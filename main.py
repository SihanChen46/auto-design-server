from fastapi import FastAPI
from data_types import Message, DiagramClick
from components.handlers import MessageHandler, DiagramHandler
from components.session import SessionManager

app = FastAPI()
session_manager = SessionManager()
message_handler = MessageHandler(session_manager)
diagram_handler = DiagramHandler(session_manager)


@app.post("/chat")
def chat(message: Message):
    """handle new user messages"""
    resp_message = message_handler.handle(message)
    return resp_message


@app.post("/diagram")
def chat(diagram_click: DiagramClick):
    """handle new user messages"""
    resp_diagram = diagram_handler.handle(diagram_click)
    return resp_diagram
