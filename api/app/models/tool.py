from typing import Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base
from app.models.mixins import ProjectMixin

if TYPE_CHECKING:
    from app.models.project import Project


class Tool(ProjectMixin, Base):
    """The callable function as presented to the LLM"""
    __tablename__ = "tool"

    name: Mapped[str] = mapped_column(String, doc="The name of the tool to be called")
    json_schema: Mapped[dict] = mapped_column(
        JSONB,
        doc="The jsonschema for the tool",
    )
    description: Mapped[Optional[str]] = mapped_column(String, doc="A displayable description of the tool")

    project:Mapped["Project"] = relationship("Project", back_populates="tools")