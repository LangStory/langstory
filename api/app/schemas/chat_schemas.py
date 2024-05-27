from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.event import MessageRole
from app.schemas.base_schema import BaseSchema


class ChatBase(BaseSchema):
    class Config:
        from_attributes = True


class ChatCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    project_id: UUID


class ChatRead(BaseSchema):
    id: UUID
    name: str
    description: Optional[str] = None
    project_id: UUID


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
