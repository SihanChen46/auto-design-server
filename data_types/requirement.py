from data_types.common import Id
from pydantic import BaseModel


class Requirement(BaseModel):
    sessionId: Id
    content: str


class RequirementResp(BaseModel):
    sessionId: Id
    components: str
    workflow: str
    sequenceDiagramCode: str
