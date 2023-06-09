from data_types.common import Id
from pydantic import BaseModel


class Requirement(BaseModel):
    checkpointId: Id
    content: str


class RequirementResp(BaseModel):
    checkpointId: Id
    components: str
    workflow: str
    sequenceDiagramCode: str
