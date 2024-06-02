from typing import Optional, TYPE_CHECKING
from pydantic import HttpUrl
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import OrganizationMixin

if TYPE_CHECKING:
    from app.models.organization import Organization



class Persona(Base, OrganizationMixin):
    __tablename__ = "persona"

    name: Mapped[str] = mapped_column(nullable=False, doc="The name of the persona")
    description: Mapped[Optional[str]] = mapped_column(default=None, doc="A description of the persona")
    avatar_url: Mapped[Optional[HttpUrl]] = mapped_column(String, default=None, doc="The URL of the persona's avatar")

    organization: "Organization" = relationship("Organization", back_populates="personas")