from data_types.common import Id
from pydantic import BaseModel


class ImproveReq(BaseModel):
    # As Req only
    checkpointId: Id


class ImproveResp(BaseModel):
    # As Resp only
    checkpointId: Id
    requirement: str
    components: str
    workflow: str
    sequenceDiagramCode: str
