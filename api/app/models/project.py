from typing import Optional
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import String
from sqlmodel import Field, Column

from app.models.base import AuditedBase


class Project(AuditedBase, table=True):
    name: str = Field(..., description="The name of the project")
    avatar_url: Optional[HttpUrl] = Field(
        default=None,
        description="The URL of the project's avatar",
        sa_column=Column(String),
    )
    description: Optional[str] = Field(
        default=None, description="A description of the project"
    )
    organization_id: UUID = Field(
        ...,
        foreign_key="organization.uid",
        description="The ID of the organization that owns this project",
    )
