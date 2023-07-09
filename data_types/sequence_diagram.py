from data_types.common import Id
from pydantic import BaseModel


class SequenceDiagramReq(BaseModel):
    checkpointId: Id


class SequenceDiagramResp(BaseModel):
    checkpointId: Id
    sequenceDiagramCode: str
