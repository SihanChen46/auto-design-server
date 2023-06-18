from fastapi import FastAPI
from data_types import Message, DiagramClick, Requirement, RequirementResp
from components.handlers import MessageHandler, DiagramHandler, RequirementHandler
from components.session import SessionManager

app = FastAPI()
# session_manager = SessionManager()
requirement_handler = RequirementHandler()
# message_handler = MessageHandler(session_manager)
# diagram_handler = DiagramHandler(session_manager)


# @app.post("/chat")
# def chat(message: Message):
#     """handle new user messages"""
#     resp_message = message_handler.handle(message)
#     return resp_message

@app.post("/handle_requirement")
def chat(requirement: Requirement) -> RequirementResp:
    """handle new user requirement and generate design"""
    resp = requirement_handler.handle(requirement)
    return resp


# @app.post("/update_sequence_diagram")
# def chat(diagram_click: DiagramClick):
#     """handle new user messages"""
#     resp_diagram = diagram_handler.handle(diagram_click)
#     return resp_diagram

# @app.post("/update_class_diagram")
# def chat(diagram_click: DiagramClick):
#     """handle new user messages"""
#     resp_diagram = diagram_handler.handle(diagram_click)
#     return resp_diagram

# @app.post("/update_components")
# def chat(diagram_click: DiagramClick):
#     """handle new user messages"""
#     resp_diagram = diagram_handler.handle(diagram_click)
#     return resp_diagram
