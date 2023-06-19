from data_types.common import Id
from pydantic import BaseModel


class ComponentReq(BaseModel):
    sessionId: Id
    requirement: str


class ComponentResp(BaseModel):
    sessionId: Id
    components: str
