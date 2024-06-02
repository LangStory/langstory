from typing import Optional, TYPE_CHECKING, List, Union, Literal
from datetime import datetime
from enum import Enum
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditedBase
from app.models._mixins import ChatMixin, ThreadMixin
from app.models.project import Project
from app.models.chat import Chat

if TYPE_CHECKING:
    from app.models.persona import Persona
    from app.models.thread import Thread
    from app.models.tool_call import ToolCall
    from app.models.user import User
    from app.schemas.user_schemas import ScopedUser
    from sqlalchemy import Select


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


class Message(AuditedBase, ChatMixin, ThreadMixin):
    __tablename__ = "message"

    type: Mapped[EventType] = mapped_column(nullable=False, doc="The type of message")
    display_name: Mapped[Optional[str]] = mapped_column(
        default=None,
        doc="The assignable name of the message sender. DO NOT ACCESS DIRECTLY - use the name property to correctly access the name value",
    )
    content: Mapped[str] = mapped_column(
        nullable=False, doc="The content of the message"
    )
    timestamp: Mapped[datetime] = mapped_column(
        nullable=False,
        doc="The timestamp of the event in the chat. This is used as the chat index and controls the order in which chat messages are displayed.",
    )

    # overload thread mixin to make it optional
    _thread_uid: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(), ForeignKey("thread.uid"), nullable=True
    )

    @property
    def role(self) -> MessageRole:
        match self.type:
            case EventType.user_message:
                return MessageRole.user
            case EventType.assistant_message:
                return MessageRole.assistant
            case EventType.tool_message:
                return MessageRole.tool
            case self.type if self.type in (
                EventType.system_message,
                EventType.external_event,
            ):
                return MessageRole.system

    # relationships
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    thread: Mapped[Optional["Thread"]] = relationship(
        "Thread", back_populates="messages"
    )

    # =========================
    # USER MESSAGES PROPS
    # =========================
    _user_message_persona_uid: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(),
        ForeignKey("persona.uid"),
        nullable=True,
        doc="The ID of the persona this message belongs to (if any); only valid for user messages",
    )
    _user_message_persona: Mapped[Optional["Persona"]] = relationship(
        "Persona", primaryjoin="Message._user_message_persona_uid==Persona.uid"
    )

    @property
    def persona_id(self) -> Optional[str]:
        if not self.type == EventType.user_message:
            raise ValueError("persona_id is only valid for user messages")
        if uid := self._user_message_persona_uid:
            return f"persona-{uid}"
        return None

    @persona_id.setter
    def persona_id(self, value: str) -> None:
        if not self.type == EventType.user_message:
            raise ValueError("persona_id is only valid for user messages")
        self._user_message_persona_uid = AuditedBase.to_uid(value, prefix="persona")

    @property
    def persona(self) -> Optional["Persona"]:
        if not self.type == EventType.user_message:
            raise ValueError("persona is only accessible for user messages")
        return self._user_message_persona

    @persona.setter
    def persona(self, value: "Persona") -> None:
        if not self.type == EventType.user_message:
            raise ValueError("persona is only accessible for user messages")
        self._user_message_persona = value

    # =========================
    # ASSISTANT MESSAGES PROPS
    # =========================
    _assistant_message_tool_calls: Mapped[Optional[List["ToolCall"]]] = relationship(
        back_populates="assistant_message",
        foreign_keys="ToolCall._assistant_message_uid",
    )

    @property
    def tool_calls_requested(self) -> Optional[List["ToolCall"]]:
        if not self.type == EventType.tool_message:
            raise ValueError(
                "tool calls requested are only accessible for assistant messages"
            )
        return self._assistant_message_tool_calls

    @tool_calls_requested.setter
    def tool_calls_requested(self, value: List["ToolCall"]) -> None:
        if not self.type == EventType.assistant_message:
            raise ValueError(
                "tool calls requested are only accessible for assistant messages"
            )
        self._assistant_message_tool_calls = value

    # =========================
    # TOOL MESSAGES PROPS
    # =========================
    _tool_message_tool_call: Mapped["ToolCall"] = relationship(
        "ToolCall",
        back_populates="tool_message",
        foreign_keys="ToolCall._tool_message_uid",
    )

    @property
    def tool_call_response(self) -> "ToolCall":
        if not self.type == EventType.tool_message:
            raise ValueError("tool call response is only accessible for tool messages")
        return self._tool_message_tool_call

    @tool_call_response.setter
    def tool_call_response(self, value: "ToolCall") -> None:
        if not self.type == EventType.tool_message:
            raise ValueError("tool call response is only accessible for tool messages")
        self._tool_message_tool_call = value

    # =========================
    # GENERAL MESSAGES PROPS
    # =========================
    @property
    def name(self) -> Optional[str]:
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

    @name.setter
    def name(self, value: str) -> None:
        self.display_name = value

    @classmethod
    def apply_access_predicate(
        cls,
        query: "Select",
        actor: Union["ScopedUser", "User"],
        access: List[Literal["read", "write", "admin"]],
    ) -> "Select":
        """applies a WHERE clause restricting results to the given actor and access level"""
        del access  # not used by default, will be used for more complex access control
        org_uid = getattr(
            actor, "_organization_uid", getattr(actor.organization, "uid", None)
        )
        if not org_uid:
            raise ValueError("object %s has no organization accessor", actor)
        # TODO: access roles on chats goes here!
        return (
            query.join(Chat)
            .join(Project)
            .where(Project._organization_uid == org_uid)
        )
