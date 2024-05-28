from typing import Optional, TYPE_CHECKING, List, Type

from sqlmodel import Field, Relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event import (
        UserMessage,
        AssistantMessage,
        ToolMessage,
        ExternalEvent,
        Event,
    )


def thread_relationship():
    return Relationship(
        back_populates="thread", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Thread(Base, table=True):
    name: str = Field(..., description="The name of the organization")

    # this is gross, but sqlmodel doesn't support polymorphic tables
    # NEVER USE THESE! Access via the messages property
    user_messages: Optional[List["UserMessage"]] = thread_relationship()
    assistant_messages: Optional[List["AssistantMessage"]] = thread_relationship()
    tool_messages: Optional[List["ToolMessage"]] = thread_relationship()
    external_events: Optional[List["ExternalEvent"]] = thread_relationship()

    @property
    def messages(self) -> List[Type["Event"]]:
        return (
            self.user_messages
            + self.assistant_messages
            + self.tool_messages
            + self.external_events
        )
