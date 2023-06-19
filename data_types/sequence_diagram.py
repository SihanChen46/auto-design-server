from data_types.common import Id
from pydantic import BaseModel


class SequenceDiagramReq(BaseModel):
    sessionId: Id
    workflow: str


class SequenceDiagramResp(BaseModel):
    sessionId: Id
    sequenceDiagramCode: str
