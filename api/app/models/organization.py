from typing import Optional, TYPE_CHECKING, Generator, List

from pydantic import HttpUrl
from sqlalchemy import String
from sqlmodel import Field, Column, Relationship

from app.models.base import Base
from app.settings import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.models.project import Project


class Organization(Base, table=True):
    name: str = Field(..., description="The name of the organization")
    email_domain: Optional[str] = Field(
        None,
        description="If set, all users with this email domain will be granted access to this organization",
    )
    avatar_url: Optional[HttpUrl] = Field(
        None,
        description="The URL of the organization's avatar",
        sa_column=Column(String),
    )

    # relationships
    projects: List["Project"] = Relationship(back_populates="organization", sa_relationship_kwargs={"lazy":"dynamic"})

    @classmethod
    def default(cls, db_session: "Generator[Session, None, None]"):
        if org := db_session.query(cls).first():
            return org
        return Organization(name=settings.organization_name).create(db_session)