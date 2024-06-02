from typing import Optional, TYPE_CHECKING, Generator, List

from pydantic import HttpUrl
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.settings import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.models.project import Project
    from app.models.persona import Persona
    from app.models.user import User

class Organization(Base):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String(), nullable=False, doc="The name of the organization")
    email_domain: Mapped[Optional[str]] = mapped_column(String(), doc="If set, all users with this email domain will be granted access to this organization")
    avatar_url: Mapped[Optional[HttpUrl]] = mapped_column(String(), doc="The URL of the organization's avatar")

    # relationships
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="organization", lazy="dynamic")
    personas: Mapped[List["Persona"]] = relationship("Persona", back_populates="organization", lazy="dynamic")

    users: Mapped[List["User"]] = relationship("User", secondary="organizations_users", lazy="selectin")

    @classmethod
    def default(cls, db_session: "Generator[Session, None, None]"):
        """manages the default org lookup"""
        if org := db_session.query(cls).first():
            return org
        return Organization(name=settings.organization_name).create(db_session)
