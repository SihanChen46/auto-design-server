from typing import Literal
from data_types.common import Id, Timestamp
from enum import Enum
from pydantic import BaseModel

MessageStatus = Literal['LOADING', 'DONE', 'FAILED']


class CreatorRole(str, Enum):
    User = "User"
    Admin = "Admin"
    Assistant = "Assistant"


class Message(BaseModel):
    msgId: Id
    conversationId: str
    creatorRole: CreatorRole
    content: str
    status: MessageStatus
