from typing import TYPE_CHECKING, List, Any, Union, Literal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


from app.models.base import Base
from app.models._mixins import ChatMixin
from app.models.chat import Chat
from app.models.project import Project

if TYPE_CHECKING:
    from app.models.message import Message
    from sqlalchemy.sql.selectable import Select
    from app.schemas.user_schemas import ScopedUser
    from app.schemas.user_schemas import User


class Thread(ChatMixin, Base):
    __tablename__ = "thread"

    name: Mapped[str] = mapped_column(
        String, nullable=False, doc="The name of the thread"
    )

    # relationships
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="thread", lazy="selectin"
    )

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
        return (
            query.join(Chat).join(Project).where(Project._organization_uid == org_uid)
        )

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
        return cls.name.ilike(f"%{value}%")
