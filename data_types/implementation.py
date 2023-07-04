from data_types.common import Id
from pydantic import BaseModel


class ImplementReq(BaseModel):
    sessionId: Id
    programmingLanguage: str


class ImplementResp(BaseModel):
    sessionId: Id
    status: str
