from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as SQLUUID
from uuid import UUID

from app.models.base import AuditedBase
from app.models._mixins import ToolMixin

if TYPE_CHECKING:
    from app.models.message import Message
    from app.models.tool import Tool


class ToolCall(AuditedBase, ToolMixin):
    """A called instance of a tool"""

    __tablename__ = "tool_call"

    request_id: Mapped[str] = mapped_column(
        String, nullable=False, doc="a unique identifier to link calls to responses"
    )
    arguments: Mapped[dict] = mapped_column(
        JSONB, default=lambda: {}, doc="The arguments to be passed to the tool"
    )

    # relationship keys
    _assistant_message_uid: Mapped[UUID] = mapped_column(
        SQLUUID(),
        ForeignKey(
            "message.uid",
            name="fk_tool_call_assistant_message_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
        doc="The assistant message associated with this tool call",
    )
    _tool_message_uid: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(),
        ForeignKey(
            "message.uid",
            name="fk_tool_call_tool_message_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=True,
        doc="The tool message associated with this tool call",
    )

    # relationships
    assistant_message: Mapped["Message"] = relationship(
        "Message",
        foreign_keys=[_assistant_message_uid],
        back_populates="_assistant_message_tool_calls",
    )
    tool_message: Mapped["Message"] = relationship(
        "Message",
        foreign_keys=[_tool_message_uid],
        back_populates="_tool_message_tool_call",
    )
    tool: Mapped["Tool"] = relationship("Tool")

    @property
    def assistant_message_id(self) -> str:
        return f"message-{self._assistant_message_uid}"

    @assistant_message_id.setter
    def assistant_message_id(self, value: str) -> None:
        self._assistant_message_uid = Base.to_uid(value, prefix="message")
