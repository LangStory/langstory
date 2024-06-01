from typing import Optional, Union
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import String
from sqlmodel import Field, Column, Relationship

from app.models.base import Base
from app.models.organization import Organization
from app.models.organizations_users import OrganizationsUsers


class User(Base, table=True):
    email_address: str = Field(
        ...,
        description="The unique email address of the user",
        sa_column=Column(String, unique=True),
    )
    first_name: Optional[str] = Field(
        default=None, description="The first name of the user"
    )
    last_name: Optional[str] = Field(
        default=None, description="The last name of the user"
    )
    avatar_url: Optional[HttpUrl] = Field(
        default=None,
        description="The URL of the user's avatar",
        sa_column=Column(String),
    )
    password: Optional[str] = Field(
        default=None, description="The user's password", exclude=True
    )

    # relationships
    organizations: list["Organization"] = Relationship(
        link_model=OrganizationsUsers, sa_relationship_kwargs={"lazy": "joined"}
    )

    @classmethod
    def read(
            cls,
            db_session,
            identifier: Union[str, UUID] = None,
    ):
        # email address lookup
        if "@" in identifier:
            return db_session.query(cls).filter(cls.email_address == identifier).one()
        return super().read(db_session, identifier)
