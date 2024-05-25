from typing import Optional, TYPE_CHECKING
from uuid import UUID
from pydantic import HttpUrl
from sqlmodel import Field, Column, String, Relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event import UserMessage


class Persona(Base, table=True):
    name: str = Field(..., description="The name of the persona")
    description: Optional[str] = Field(
        default=None, description="A description of the persona"
    )
    project_id: UUID = Field(
        ...,
        foreign_key="project.uid",
        description="The ID of the project this persona belongs to",
    )
    avatar_url: Optional[HttpUrl] = Field(
        None, description="The URL of the persona's avatar", sa_column=Column(String)
    )
    user_messages: list["UserMessage"] = Relationship(back_populates="persona")
