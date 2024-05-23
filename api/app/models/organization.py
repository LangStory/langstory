from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Column, Relationship
from sqlalchemy import String
from pydantic import HttpUrl

from app.models.base import Base
from app.models.orgnanizations_users import OrganizationsUsers

if TYPE_CHECKING:
    from app.models.user import User


class Organization(Base, table=True):
    name: str = Field(..., description="The name of the organization")
    email_domain: Optional[str] = Field(None, description="If set, all users with this email domain will be granted access to this organization")
    avatar_url: Optional[HttpUrl] = Field(None, description="The URL of the organization's avatar", sa_column=Column(String))
    users: list["User"] = Relationship(back_populates="users", link_model=OrganizationsUsers)
