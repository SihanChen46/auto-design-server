from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from data_types import ComponentReq, WorkflowReq, SequenceDiagramReq, SequenceDiagramResp, ImplementReq, ImplementResp
from components.handlers import ComponentHandler, WorkflowHandler, SequenceDiagramHandler, ImplementHandler

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow any method
    allow_headers=["*"],  # Allow any headers
)

component_handler = ComponentHandler()
workflow_handler = WorkflowHandler()
sequence_diagram_handler = SequenceDiagramHandler()
implement_handler = ImplementHandler()


@app.post("/new_component")
async def generate(req: ComponentReq) -> StreamingResponse:
    """generate new components"""
    resp = component_handler.handle(req)
    return resp


@app.post("/new_workflow")
async def generate(req: WorkflowReq) -> StreamingResponse:
    """generate new workflow"""
    resp = workflow_handler.handle(req)
    return resp


@app.post("/new_sequence_diagram")
def generate(req: SequenceDiagramReq) -> SequenceDiagramResp:
    """generate new sequenceDiagram"""
    resp = sequence_diagram_handler.handle(req)
    return resp


@app.post("/implement")
def generate(req: ImplementReq) -> ImplementResp:
    """generate implementation"""
    resp = implement_handler.handle(req)
    return resp
