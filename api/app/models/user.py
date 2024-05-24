from typing import Optional
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import String
from sqlmodel import Field, Column, Relationship

from app.models.base import Base
from app.models.organization import Organization
from app.models.orgnanizations_users import OrganizationsUsers


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
    password: Optional[str] = Field(default=None, description="The user's password")

    # relationships
    organizations: list["Organization"] = Relationship(
        link_model=OrganizationsUsers, sa_relationship_kwargs={"lazy": "joined"}
    )

    @classmethod
    def read(
        cls,
        db_session,
        id_: Optional[str] = None,
        uid: Optional[UUID] = None,
        email_address: Optional[str] = None,
    ):
        if id_:
            try:
                uid = UUID(id_.split("user-")[1])
            except (IndexError, ValueError) as e:
                raise ValueError("id_ must be a valid user id")
        if uid:
            return super().read(db_session, uid=uid)
        if not email_address:
            raise ValueError("id_, uid or email_address is required")
        with db_session as session:
            return session.query(cls).filter(cls.email_address == email_address).one()
