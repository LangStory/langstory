from typing import Optional, Type, Self
from uuid import UUID
from sqlmodel import Field, Session

from app.models.base import Base
from app.models.event import Message


class Chat(Base, table=True):
    name: str = Field(..., description="The name of the chat")
    description: Optional[str] = Field(
        default=None, description="A description of the chat"
    )
    project_id: UUID = Field(
        ...,
        foreign_key="project.uid",
        description="The ID of the project this chat belongs to",
    )

    @classmethod
    def read(cls, db_session: Session, uid: Optional[UUID] = None, **kwargs):
        if not uid:
            raise ValueError("uid is required")
        chat = super().read(db_session, uid=uid)
        messages = db_session.query(Message).filter(Message.chat_id == uid).all()
        chat.messages = messages
        return chat
