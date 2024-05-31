from typing import Optional, Union, List, Literal, TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship

from app.models.base import AuditedBase
from app.models.project import Project


if TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select
    from app.schemas.user_schemas import ScopedUser
    from app.schemas.user_schemas import User


class Chat(AuditedBase, table=True):
    name: str = Field(..., description="The name of the chat")
    description: Optional[str] = Field(
        default=None, description="A description of the chat"
    )
    fkey_project_uid: UUID = Field(
        ...,
        foreign_key="project.uid",
        description="The ID of the project this chat belongs to",
    )

    @property
    def project_id(self) -> str:
        if uid := self.fkey_project_uid:
            return f"project-{uid}"
        return None

    @project_id.setter
    def project_id(self, value:str) -> None:
        self.fkey_project_uid = Project.to_uid(value)


    # relationships
    project: "Project" = Relationship(join_column="fkey_project_uid", back_populates="chats")




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
