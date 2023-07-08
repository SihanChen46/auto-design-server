from data_types.common import Id, Timestamp
from enum import Enum
from pydantic import BaseModel


# class MessageStatus(str, Enum):
#     LOADING = "LOADING"
#     DONE = "DONE"
#     FAILED = "FAILED"


class CreatorRole(str, Enum):
    User = "User"
    Admin = "Admin"
    Assistant = "Assistant"


class MessageReq(BaseModel):
    # As Req only
    checkpointId: Id
    content: str
    creatorRole: CreatorRole
    createTimestamp: Timestamp


class MessageResp(BaseModel):
    # As Resp only
    content: str
    creatorRole: CreatorRole
    createTimestamp: Timestamp


class Message(BaseModel):
    # Actually save to DB
    msgId: Id
    creatorRole: CreatorRole
    content: str
    createTimestamp: Timestamp
