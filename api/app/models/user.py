from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Column, Relationship
from sqlalchemy import String
from pydantic import HttpUrl

from app.models.base import Base
from app.models.orgnanizations_users import OrganizationsUsers

if TYPE_CHECKING:
    from app.models.organization import Organization


class User(Base, table=True):
    email_address: str = Field(..., description="The unique email address of the user", sa_column=Column(String, unique=True))
    first_name: Optional[str] = Field(default=None, description="The first name of the user")
    last_name: Optional[str] = Field(default=None, description="The last name of the user")
    avatar_url: Optional[HttpUrl] = Field(default=None, description="The URL of the user's avatar", sa_column=Column(String))
    organizations: list["Organization"] = Relationship(back_populates="users", link_model=OrganizationsUsers)

    @classmethod
    def read(cls, db_session, uid: Optional[UUID] = None, email_address: Optional[User] = None):
        if uid:
            return super().read(db_session, uid=uid)
        if not email_address:
            raise ValueError("uid or email_address is required")
        with db_session as session:
            return session.query(cls).filter(cls.email_address == email_address).one()
