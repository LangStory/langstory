from typing import Optional
from uuid import UUID
from sqlmodel import Field

from app.models.base import Base


class Chat(Base, table=True):
    name: str = Field(..., description="The name of the chat")
    description: Optional[str] = Field(
        default=None, description="A description of the chat"
    )
    project_id: UUID = Field(
        ...,
        foreign_key="project.uid",
        description="The ID of the project this chat belongs to",
    )
