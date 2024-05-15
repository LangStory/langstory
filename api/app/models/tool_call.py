from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event import AssistantMessage

class ToolCall(Base, table=True):
    """A called instance of a tool"""
    request_id: UUID = Field(default_factory=uuid4, description="a unique identifier to link calls to responses", unique=True)
    arguments: dict = Field(default_factory=dict, description="The arguments to be passed to the tool", sa_type=JSONB)

    # relationship
    tool_id: UUID = Field(..., foreign_key="tool.uid", description="The ID of the tool being called")
    assistant_message_id: UUID = Field(..., foreign_key="assistantmessage.uid", description="The assistant message associated with this tool call")
    assistant_message: "AssistantMessage" = Relationship(back_populates="tool_calls")