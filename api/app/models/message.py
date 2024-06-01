from typing import Optional, TYPE_CHECKING, List, Union, Literal
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import Field
from sqlmodel import Relationship

from app.models.base import AuditedBase
from app.models.project import Project

if TYPE_CHECKING:
    from app.models.persona import Persona
    from app.models.chat import Chat
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


class Message(AuditedBase, table=True):
    """All entries into a conversation are messages"""
    type: EventType = Field(..., description="The type of message")
    display_name: Optional[str] = Field(default=None, description="The assignable name of the message sender. DO NOT ACCESS DIRECTLY - use the name property to correctly access the name value")
    content: str = Field(..., description="The content of the message")
    timestamp: datetime = Field(
        ...,
        description="The timestamp of the event in the chat. This is used as the chat index and controls the order in which chat messages are displayed.",
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
            case self.type if self.type in (EventType.system_message, EventType.external_event,):
                return MessageRole.system

    # =========================
    # CHAT
    # =========================
    fkey_chat_uid: UUID = Field(foreign_key="chat.uid", description="The ID of the chat this message belongs to")

    @property
    def chat_id(self) -> str:
        return f"chat-{self.fkey_chat_uid}"

    @chat_id.setter
    def chat_id(self, value: str) -> None:
        self.fkey_chat_uid = AuditedBase.to_uid(value, prefix="chat")

    chat: "Chat" = Relationship(sa_relationship_kwargs={"primaryjoin": "Message.fkey_chat_uid==Chat.uid"}, back_populates="messages")

    fkey_thread_uid: Optional[UUID] = Field(
        default=None,
        foreign_key="thread.uid",
        description="The ID of the thread this event belongs to (if any)",
    )

    # =========================
    # THREAD
    # =========================
    @property
    def thread_id(self) -> Optional[str]:
        if uid := self.fkey_thread_uid:
            return f"thread-{uid}"
        return None

    @thread_id.setter
    def thread_id(self, value: str) -> None:
        self.fkey_thread_uid = AuditedBase.to_uid(value, prefix="thread")

    thread: Optional["Thread"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Message.fkey_thread_uid==Thread.uid"}, back_populates="messages")

    # =========================
    # USER MESSAGES PROPS
    # =========================
    private_user_message_fkey_persona_uid: Optional[UUID] = Field(
        default=None,
        foreign_key="persona.uid",
        description="The ID of the persona this message belongs to (if any); only valid for user messages",
    )
    private_user_message_persona: Optional["Persona"] = Relationship(sa_relationship_kwargs={"primaryjoin": "Message.private_user_message_fkey_persona_uid==Persona.uid"})

    @property
    def persona_id(self) -> Optional[str]:
        if not self.type == EventType.user_message:
            raise ValueError("persona_id is only valid for user messages")
        if uid := self.private_user_message_fkey_persona_uid:
            return f"persona-{uid}"
        return None

    @persona_id.setter
    def persona_id(self, value: str) -> None:
        if not self.type == EventType.user_message:
            raise ValueError("persona_id is only valid for user messages")
        self.private_user_message_fkey_persona_uid = AuditedBase.to_uid(value, prefix="persona")

    @property
    def persona(self) -> Optional["Persona"]:
        if not self.type == EventType.user_message:
            raise ValueError("persona is only accessible for user messages")
        return self.private_user_message_persona

    @persona.setter
    def persona(self, value: "Persona") -> None:
        if not self.type == EventType.user_message:
            raise ValueError("persona is only accessible for user messages")
        self.private_user_message_persona = value

    # =========================
    # ASSISTANT MESSAGES PROPS
    # =========================
    private_assistant_message_tool_calls: Optional[List["ToolCall"]] = Relationship(
        back_populates="assistant_message"
    )

    @property
    def tool_calls_requested(self) -> Optional[List["ToolCall"]]:
        if not self.type == EventType.tool_message:
            raise ValueError("tool calls requested are only accessible for assistant messages")
        return self.private_assistant_message_tool_calls

    @tool_calls_requested.setter
    def tool_calls_requested(self, value: List["ToolCall"]) -> None:
        if not self.type == EventType.assistant_message:
            raise ValueError("tool calls requested are only accessible for assistant messages")
        self.private_assistant_message_tool_calls = value

    # =========================
    # TOOL MESSAGES PROPS
    # =========================
    private_tool_message_fkey_tool_call_uid: UUID = Field(
        ...,
        foreign_key="tool_call.uid",
        description="The ID of the tool call this message belongs to (if any); only valid for tool messages",
    )

    private_tool_message_tool_call: "ToolCall" = Relationship(
        back_populates="tool_message"
    )

    @property
    def tool_call_response_id(self) -> str:
        if not self.type == EventType.tool_message:
            raise ValueError("tool call response id is only valid for tool messages")
        if uid := self.private_tool_message_fkey_tool_call_uid:
            return f"toolcall-{uid}"

    @tool_call_response_id.setter
    def tool_call_response_id(self, value: UUID) -> None:
        if not self.type == EventType.tool_message:
            raise ValueError("tool call response is only valid for tool messages")
        self.private_tool_message_fkey_tool_call_uid = AuditedBase.to_uid(value, prefix="toolcall")

    @property
    def tool_call_response(self) -> "ToolCall":
        if not self.type == EventType.tool_message:
            raise ValueError("tool call response is only accessible for tool messages")
        return self.private_tool_message_tool_call

    @tool_call_response.setter
    def tool_call_response(self, value: "ToolCall") -> None:
        if not self.type == EventType.tool_message:
            raise ValueError("tool call response is only accessible for tool messages")
        self.private_tool_message_tool_call = value

    # =========================
    # MESSAGES PROPS
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
            actor, "organization_id", getattr(actor.organization, "uid", None)
        )
        if not org_uid:
            raise ValueError("object %s has no organization accessor", actor)
        # TODO: access roles on chats goes here!
        return query.join(Chat).join(Project).where(Project.fkey_organization_uid == org_uid)
