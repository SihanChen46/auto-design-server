from data_types.common import Id
from pydantic import BaseModel


class WorkflowReq(BaseModel):
    checkpointId: Id


class WorkflowResp(BaseModel):
    checkpointId: Id
    workflow: str
