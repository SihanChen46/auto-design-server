from data_types.common import Id
from pydantic import BaseModel


class WorkflowReq(BaseModel):
    sessionId: Id
    requirement: str
    components: str


class WorkflowResp(BaseModel):
    sessionId: Id
    workflow: str
