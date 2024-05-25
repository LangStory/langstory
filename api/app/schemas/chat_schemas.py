from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.models.event import MessageRole
from app.schemas.base_schema import BaseSchema


class ChatCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    project_id: UUID


class ChatRead(BaseSchema):
    id: UUID
    name: str
    description: Optional[str] = None
    project_id: UUID

    class Config:
        orm_mode = True


class MessageCreate(BaseSchema):
    role: MessageRole
    content: str
    timestamp: datetime


class MessageRead(BaseSchema):
    id: UUID
    role: MessageRole
    content: str
    timestamp: datetime
    chat_id: UUID

    class Config:
        orm_mode = True
