from typing import Optional, Union, List, Literal, TYPE_CHECKING
from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditedBase
from app.models.mixins import ProjectMixin
from app.models.project import Project

if TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select
    from app.schemas.user_schemas import ScopedUser
    from app.schemas.user_schemas import User
    from app.models.message import Message


class Chat(AuditedBase, ProjectMixin):
    __tablename__ = "chat"

    name: Mapped[str] = mapped_column(TEXT(), nullable=False, doc="The name of the chat")
    description: Mapped[Optional[str]] = mapped_column(TEXT(), default=None, doc="A description of the chat")


    # relationships
    project: Mapped["Project"] = relationship("Project", back_populates="chats")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="chat", lazy="dynamic")

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
            actor, "organization_id", getattr(actor.organization, "uid", None)
        )
        if not org_uid:
            raise ValueError("object %s has no organization accessor", actor)
        return query.join(Project).where(Project.organization_id == org_uid)
