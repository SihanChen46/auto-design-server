from data_types.common import Id
from pydantic import BaseModel


class ImplementReq(BaseModel):
    checkpointId: Id
    programmingLanguage: str


class ImplementResp(BaseModel):
    checkpointId: Id
    content: dict
