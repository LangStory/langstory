from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from uuid import UUID
from datetime import datetime
from sqlmodel import Field, Relationship
from humps import depascalize

from app.models.base import Base
if TYPE_CHECKING:
    from app.models.tool_call import ToolCall
    from app.models.persona import Persona

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

class Event(Base):

    name: str = Field(..., description="The name of the event")
    description: Optional[str] = Field(default=None, description="A description of the event")
    journey_id: UUID = Field(..., foreign_key="journey.uid", description="The ID of the journey this event belongs to")
    timestamp: datetime = Field(..., description="The timestamp of the event")

    @property
    def event_type(self) ->  EventType:
        raw = depascalize(self.__class__.__name__)
        return EventType(raw)

class Message(Event):
    """Classic OAI message, with some additional metadata."""
    role: MessageRole = Field(..., description="The role of the message")
    content: str = Field(..., description="The content of the message")

class SystemMessage(Message, table=True):
    role: MessageRole = Field(MessageRole.system,  description="The role of the message")

class UserMessage(Message, table=True):
    role: MessageRole = Field(MessageRole.user, description="The role of the message")

    # relationships
    persona_id: Optional[UUID] = Field(default=None, foreign_key="persona.uid", description="The optional persona ID for user messages")
    persona: Optional["Persona"] = Relationship(back_populates="user_messages")

    @property
    def name(self)-> str:
        if self.persona:
            return self.persona.name
        return "Anonymous"

class AssistantMessage(Message, table=True):

    role: MessageRole = Field(MessageRole.assistant, description="The role of the message")
    tool_calls: List["ToolCall"] = Relationship(back_populates="assistant_message")

class ToolMessage(Message, table=True):

    role: MessageRole = Field(MessageRole.tool, description="The role of the message")
    tool_call_request_id: Optional[UUID] = Field(default=None, foreign_key="toolcall.request_id", description="The tool call request ID if a tool call initiated this response")

class ExternalEvent(Event, table=True):
    """Stimuli that can trigger or impact a journey"""

    name: str = Field(..., description="The name of the external event")
    description: Optional[str] = Field(default=None, description="A description of the external event")