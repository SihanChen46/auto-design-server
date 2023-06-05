from typing import Literal
from data_types.common import Id, Timestamp
from enum import Enum
from pydantic import BaseModel

DiagramStatus = Literal["LOADING", "DONE", "FAILED"]


class Diagram(BaseModel):
    diagramId: Id
    conversationId: str
    diagramCode: str
    status: DiagramStatus


class DiagramClick(BaseModel):
    conversationId: str
