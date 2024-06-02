from typing import Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import HttpUrl

from app.models.base import AuditedBase
from app.models.mixins import OrganizationMixin

if TYPE_CHECKING:
    from app.models.chat import Chat
    from app.models.organization import Organization

class Project(AuditedBase, OrganizationMixin):
    __tablename__ = "project"

    name: Mapped[str] = mapped_column(String, nullable=False, doc="The name of the project")
    avatar_url: Mapped[Optional[HttpUrl]] = mapped_column(String, default=None, doc="The URL of the project's avatar")
    description: Mapped[Optional[str]] = mapped_column(String, default=None, doc="A description of the project")

    # relationships
    organization: "Organization" = relationship("Organization", back_populates="projects")
    chats: list["Chat"] = relationship("Chat", back_populates="project")

