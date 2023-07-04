from data_types.common import Id
from pydantic import BaseModel


class SequenceDiagramReq(BaseModel):
    sessionId: Id


class SequenceDiagramResp(BaseModel):
    sessionId: Id
    sequenceDiagramCode: str
