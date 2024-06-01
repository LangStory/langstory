from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base
from app.models.tool import Tool

if TYPE_CHECKING:
    from app.models.event import AssistantMessage


class ToolCall(Base, table=True):
    """A called instance of a tool"""

    request_id: str = Field(
        description="a unique identifier to link calls to responses",
    )
    arguments: dict = Field(
        default_factory=dict,
        description="The arguments to be passed to the tool",
        sa_type=JSONB,
    )

    # relationship
    fkey_tool_uid: UUID = Field(
        ..., foreign_key="tool.uid", description="The ID of the tool being called"
    )
    fkey_assistant_message_uid: UUID = Field(
        ...,
        foreign_key="assistantmessage.uid",
        description="The assistant message associated with this tool call",
    )

    @property
    def tool_id(self) -> str:
        if uid := self.fkey_tool_uid:
            return f"tool-{uid}"
        return None

    @tool_id.setter
    def tool_id(self, value:str) -> None:
        self.fkey_tool_uid = Tool.to_uid(value)

    @property
    def assistant_message_id(self) -> str:
        if uid := self.fkey_assistant_message_uid:
            return f"assistantmessage-{uid}"
        return None

    @assistant_message_id.setter
    def assistant_message_id(self, value:str) -> None:
        self.fkey_assistant_message_uid = Base.to_uid(value, prefix="assistantmessage")

    # relationships
    assistant_message: "AssistantMessage" = Relationship(sa_relationship_kwargs={"primaryjoin": "ToolCall.fkey_assistant_message_uid == AssistantMessage.uid"})
    tool: Tool = Relationship(sa_relationship_kwargs={"primaryjoin":"ToolCall.fkey_tool_uid == Tool.uid"})