from typing import Optional, Union
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column
from pydantic import HttpUrl
from app.models.base import Base

from app.models.base import Base
from app.models.organization import Organization
from app.models.organizations_users import OrganizationsUsers

class User(Base):
    __tablename__ = "user"

    email_address: Mapped[str] = mapped_column(String, unique=True, nullable=False, doc="The unique email address of the user")
    first_name: Mapped[Optional[str]] = mapped_column(String, default=None, doc="The first name of the user")
    last_name: Mapped[Optional[str]] = mapped_column(String, default=None, doc="The last name of the user")
    avatar_url: Mapped[Optional[HttpUrl]] = mapped_column(String, default=None, doc="The URL of the user's avatar")
    password: Mapped[Optional[str]] = mapped_column(String, default=None, doc="The user's password")

    # relationships
    organizations: Mapped[list["Organization"]] = relationship("Organization", secondary="organizations_users", back_populates="users")

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
