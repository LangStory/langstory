from typing import Optional, Union, List, Literal, TYPE_CHECKING
from uuid import UUID
from sqlalchemy import select
from sqlmodel import Field, Session, Relationship

from app.models.base import AuditedBase
from app.models.event import Message

if TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select
    from app.schemas.user_schemas import ScopedUser
    from app.schemas.user_schemas import User
    from app.models.project import Project

class Chat(AuditedBase, table=True):
    name: str = Field(..., description="The name of the chat")
    description: Optional[str] = Field(
        default=None, description="A description of the chat"
    )
    project_id: UUID = Field(
        ...,
        foreign_key="project.uid",
        description="The ID of the project this chat belongs to",
    )
    project: "Project" = Relationship()
    messages: List["Message"] = Relationship(back_populates="chat", sa_relationship_kwargs={"lazy":"dynamic"})

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
        return query.where(cls.project.organization_id == org_uid)