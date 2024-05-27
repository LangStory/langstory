from typing import Optional, TYPE_CHECKING, Type, Self, List, Literal, Union
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict
from sqlalchemy import func
from uuid import UUID, uuid4
from humps import depascalize, camelize

if TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select
    from sqlalchemy.orm import Session
    from app.schemas.user_schemas import ScopedUser
    from app.schemas.user_schemas import User


class Base(SQLModel):
    __abstract__ = True

    __order_by_default__ = "created_at"

    model_config = ConfigDict(
        alias_generator=camelize,
        extra="forbid",
    )

    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default=datetime.now(),
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        default=datetime.now(),
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
    deleted: bool = Field(default=False, exclude=True)

    @property
    def __prefix__(self) -> str:
        return depascalize(self.__class__.__name__)

    @property
    def id(self) -> Optional[str]:
        return f"{self.__prefix__}-{self.uid}"

    @classmethod
    def list(cls, db_session: "Session") -> list[Type["Base"]]:
        with db_session as session:
            return session.query(cls).all()

    @classmethod
    def read(
        cls, db_session: "Session", uid: Optional[UUID] = None, **kwargs
    ) -> Type[Self]:
        del kwargs
        if uid is None:
            raise ValueError("uid is required")
        with db_session as session:
            return session.query(cls).where(cls.uid == uid).one()

    def create(self, db_session: "Session") -> Type[Self]:
        with db_session as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

    def delete(self, db_session: "Session") -> Type[Self]:
        self.deleted = True
        return self.update(db_session)

    def update(self, db_session: "Session") -> Type[Self]:
        with db_session as session:
            session.commit()
            session.refresh(self)
            return self

    @classmethod
    def id_to_uid(cls, id: str) -> UUID:
        try:
            return UUID(id.split(f"{cls.__name__.lower()}-")[-1])
        except (ValueError, IndexError):
            raise ValueError(f"Invalid ID: {id}")

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
        org = getattr(
            actor, "organization_id", getattr(actor.organization, "uid", None)
        )
        if not org:
            raise ValueError("object %s has no organization accessor", actor)
        return query.where(cls.organization_id == actor.organization_id)

    @classmethod
    def related_lookup(cls, value: str):
        """When searching a related field that targets a model class, this is the default sql constructor for that search.
        Note: the ilike values need to be managed during lookup build
        Example: for a user, we want to look up first_name, last_name, username, and full name in that order. so override on User would be:
        return (
            cls.first_name.ilike(value)
            | cls.last_name.ilike(value)
            | cls.username.ilike(value)
            | (cls.first_name + " " + cls.last_name).ilike(value)
        )
        """
        return cls.uid == value


class AuditedBase(Base):
    __abstract__ = True
    created_by: Optional[UUID] = Field(
        default=None,
        foreign_key="user.uid",
        description="The ID of the user that owns this entity",
    )
    last_updated_by: Optional[UUID] = Field(
        default=None,
        foreign_key="user.uid",
        description="The ID of the user that last updated this entity",
    )
