from typing import Optional, TYPE_CHECKING
from uuid import UUID
from pydantic import HttpUrl
from sqlmodel import Field, Column, String, Relationship

from app.models.base import Base
from app.models.organization import Organization



class Persona(Base, table=True):
    name: str = Field(..., description="The name of the persona")
    description: Optional[str] = Field(
        default=None, description="A description of the persona"
    )
    _organizataion_uid: UUID = Field(
        ...,
        foreign_key="organization.uid",
        description="The ID of the organization this persona belongs to",
    )

    avatar_url: Optional[HttpUrl] = Field(
        None, description="The URL of the persona's avatar", sa_column=Column(String)
    )

    @property
    def organization_id(self) -> str:
        if uid := self._organization_uid:
            return f"organization-{uid}"
        return None

    @organization_id.setter
    def organization_id(self, value:str) -> None:
        self._organization_uid = Organization.to_uid(value)

    # relationships
    organization: "Organization" = Relationship(join_column="_organization_uid", back_populates="personas")