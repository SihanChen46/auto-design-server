from typing import Literal
from data_types.common import Id, Timestamp
from enum import Enum
from pydantic import BaseModel


MessageStatus = Literal["LOADING", "DONE", "FAILED"]


class CreatorRole(str, Enum):
    User = "user"
    Admin = "admin"
    Moderator = "moderator"


class Message(BaseModel):
    id: Id
    conversationId: str
    creatorId: Id
    creatorRole: CreatorRole
    createdAt: Timestamp
    content: str
    status: MessageStatus
