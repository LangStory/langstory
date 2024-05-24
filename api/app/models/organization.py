from typing import Optional, TYPE_CHECKING, Generator
from sqlmodel import Field, Column, Relationship
from sqlalchemy import String
from pydantic import HttpUrl

from app.models.base import Base
from app.models.orgnanizations_users import OrganizationsUsers

if TYPE_CHECKING:
    from app.models.user import User
    from sqlalchemy.orm import Session



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


    @classmethod
    def default(cls, db_session:"Generator[Session, None, None]"):
        return db_session.query(cls).first()