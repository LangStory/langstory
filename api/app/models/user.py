from typing import Optional, Union, List, Literal, TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from pydantic import HttpUrl
from app.models.base import Base

from app.models.base import Base
from app.models.organization import Organization
from app.models.organizations_users import OrganizationsUsers

if TYPE_CHECKING:
    from sqlalchemy.orm import Select
    from app.schemas.user_schemas import ScopedUser

class User(Base):
    __tablename__ = "user"

    email_address: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, doc="The unique email address of the user"
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String, default=None, doc="The first name of the user"
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String, default=None, doc="The last name of the user"
    )
    avatar_url: Mapped[Optional[HttpUrl]] = mapped_column(
        String, default=None, doc="The URL of the user's avatar"
    )
    password: Mapped[Optional[str]] = mapped_column(
        String, default=None, doc="The user's password"
    )

    # relationships
    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", secondary="organizations_users", back_populates="users"
    )

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
        query = query.join(OrganizationsUsers).where(OrganizationsUsers._organization_uid == org_uid)
        return query