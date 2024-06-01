from typing import Optional, TYPE_CHECKING, List
from pydantic import Field
from datetime import datetime
from uuid import UUID
from enum import Enum
from sqlmodel import Relationship

from app.models.base import AuditedBase

if TYPE_CHECKING:
    from app.models.persona import Persona
    from app.models.thread import Thread

class EventType(str, Enum):
    system_message = "system_message"
    user_message = "user_message"
    assistant_message = "assistant_message"
    tool_message = "tool_message"
    external_event = "external_event"


class MessageRole(str, Enum):
    user = "user"
    system = "system"
    assistant = "assistant"
    tool = "tool"

class Message(AuditedBase):
    """All entries into a conversation are messages"""
    display_name: Optional[str] = Field(default=None, description="The assignable name of the message sender. DO NOT ACCESS DIRECTLY - use the name property to correctly access the name value")
    type: EventType = Field(..., description="The type of message")
    role: MessageRole = Field(..., description="The role of the message")

    timestamp: datetime = Field(
        ...,
        description="The timestamp of the event in the chat. This is used as the chat index and controls the order in which chat messages are displayed.",
    )
    fkey_thread_uid: Optional[UUID] = Field(
        default=None,
        foreign_key="thread.uid",
        description="The ID of the thread this event belongs to (if any)",
    )
    fkey_chat_uid: UUID = Field(foreign_key="chat.uid", description="The ID of the chat this message belongs to")
    content: str = Field(..., description="The content of the message")

    # user message props
    fkey_persona_uid: Optional[UUID] = Field(
        default=None,
        foreign_key="persona.uid",
        description="The ID of the persona this message belongs to (if any)",
    )
    persona: Optional["Persona"] = Relationship()

    # assistant message props
    tool_calls: List["ToolCall"] = Relationship(back_populates="assistant_message")


    @property
    def name(self) -> str:
        if self.display_name:
            return self.display_name
        match self.type:
            case EventType.system_message:
                return None
            case EventType.user_message:
                if self.persona:
                    return self.persona.name
                return "User"
            case EventType.assistant_message:
                return "Assistant"
            case _:
                return None
