from typing import Optional
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import String
from sqlmodel import Field, Column, Relationship

from app.models.base import AuditedBase
from app.models.organization import Organization


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
    fkey_organization_uid: UUID = Field(
        ...,
        foreign_key="organization.uid",
        description="The ID of the organization that owns this project",
    )

    @property
    def organization_id(self) -> str:
        if uid := self.fkey_organization_uid:
            return f"organization-{uid}"
        return None

    @organization_id.setter
    def organization_id(self, value:str) -> None:
        self.fkey_organization_uid = Organization.to_uid(value)

    # relationships
    organization: Organization = Relationship(join_column="fkey_organization_uid" back_populates="projects")

