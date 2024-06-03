from typing import Optional, List, Literal, Union, Any
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base
from app.models.project import Project
from app.models._mixins import ProjectMixin


class Tool(ProjectMixin, Base):
    """The callable function as presented to the LLM"""

    __tablename__ = "tool"

    name: Mapped[str] = mapped_column(String, doc="The name of the tool to be called")
    json_schema: Mapped[dict] = mapped_column(
        JSONB,
        doc="The jsonschema for the tool",
    )
    description: Mapped[Optional[str]] = mapped_column(
        String, doc="A displayable description of the tool"
    )

    project: Mapped["Project"] = relationship("Project", back_populates="tools")

    @classmethod
    def apply_access_predicate(
        cls,
        query: "Select",
        actor: Union["ScopedUser", "User"],
        access: List[Literal["read", "write", "admin"]],
    ) -> "Select":
        """applies a WHERE clause restricting results to the given actor and access level"""
        del access  # not used by default, will be used for more complex access control
        # by default, just check for matching organizations
        org_uid = getattr(
            actor, "_organization_uid", getattr(actor.organization, "uid", None)
        )
        if not org_uid:
            raise ValueError("object %s has no organization accessor", actor)
        return query.join(Project).where(Project._organization_uid == org_uid)

    @classmethod
    def related_lookup(cls, value: Any):
        """When searching a related field that targets a model class, this is the default sql constructor for that search.
        Note: the ilike values need to be managed during lookup build
        Example: for a user, if we wanted to look up first_name, last_name, username, and full name in that order, the override on User would be:
        return (
            cls.first_name.ilike(value)
            | cls.last_name.ilike(value)
            | cls.username.ilike(value)
            | (cls.first_name + " " + cls.last_name).ilike(value)
        )
        """
        # look for similar function names
        return cls.name.ilike(f"%{value}%")
