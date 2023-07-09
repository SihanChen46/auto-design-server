from data_types.common import Id
from pydantic import BaseModel


class ComponentReq(BaseModel):
    checkpointId: Id
    requirement: str


class ComponentResp(BaseModel):
    checkpointId: Id
    components: str
