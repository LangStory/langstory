from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base
from app.models.tool import Tool
from app.models.event import AssistantMessage

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
    _tool_uid: UUID = Field(
        ..., foreign_key="tool.uid", description="The ID of the tool being called"
    )
    _assistant_message_uid: UUID = Field(
        ...,
        foreign_key="assistantmessage.uid",
        description="The assistant message associated with this tool call",
    )

    @property
    def tool_id(self) -> str:
        if uid := self._tool_uid:
            return f"tool-{uid}"
        return None

    @tool_id.setter
    def tool_id(self, value:str) -> None:
        self._tool_uid = Tool.to_uid(value)

    @property
    def assistant_message_id(self) -> str:
        if uid := self._assistant_message_uid:
            return f"assistantmessage-{uid}"
        return None

    @assistant_message_id.setter
    def assistant_message_id(self, value:str) -> None:
        self._assistant_message_uid = AssistantMessage.to_uid(value)

    # relationships
    assistant_message: AssistantMessage = Relationship(join_column="_assistant_message_uid", back_populates="tool_calls")
    tool: Tool = Relationship(join_column="_tool_uid", back_populates="tool_calls")