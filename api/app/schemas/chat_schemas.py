from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.models.event import MessageRole


class ChatCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: UUID


class ChatRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    project_id: UUID

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime


class MessageRead(BaseModel):
    id: UUID
    role: MessageRole
    content: str
    timestamp: datetime
    chat_id: UUID

    class Config:
        orm_mode = True
