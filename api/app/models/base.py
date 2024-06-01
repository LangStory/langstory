from typing import Optional, TYPE_CHECKING, Type, Self, List, Literal, Union, Any
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
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
            cls, db_session: "Session",
            identifier: Union[str, UUID], **kwargs
    ) -> Type[Self]:
        del kwargs
        identifier = cls.to_uid(identifier)
        if found := db_session.get(cls, identifier):
            return found
        raise NoResultFound(f"{cls.__name__} with id {identifier} not found")

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
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

    @classmethod
    def to_uid(cls, identifier: Union[str, UUID], prefix: Optional[str] = None) -> UUID:
        """takes any possible format of a classes ID and returns the UUID
        Args:
            identifier (Union[str, UUID]): the flexible identifier to convert
            prefix (Optional[str], optional): makes it possible to set the class name and avoid circular imports
        """
        try:
            # a valid ID for the class was passed, or the uid was passed as a string
            uid = UUID(identifier.split(f"{cls.__name__.lower()}-")[-1])
        except AttributeError:
            # a UUID was passed
            uid = identifier
        except ValueError as e:
            raise ValueError(f"{identifier} is not a valid id for {cls.__name__}") from e
        return uid

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
        return query.where(cls.organization_id == org_uid)

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
        return str(cls.uid) == str(value)


class AuditedBase(Base):
    __abstract__ = True

    fkey_creator_uid: Optional[UUID] = Field(
        default=None,
        foreign_key="user.uid",
        description="The ID of the user that owns this entity",
    )
    fkey_last_updater_uid: Optional[UUID] = Field(
        default=None,
        foreign_key="user.uid",
        description="The ID of the user that last updated this entity",
    )

    @property
    def creator_id(self) -> Optional[str]:
        if uid := self.fkey_creator_uid:
            return f"user-{uid}"
        return None

    @creator_id.setter
    def creator_id(self, value: Union[str, UUID, "User", "ScopedUser"]) -> None:
        try:
            uid = getattr(value, "user", value).uid
        except AttributeError:
            uid = self.to_uid(value)
        self.fkey_creator_uid = uid

    @property
    def updater_id(self) -> Optional[str]:
        return f"user-{self.fkey_last_updater_uid}"

    @updater_id.setter
    def updater_id(self, value: Union[str, UUID, "User", "ScopedUser"]) -> None:
        try:
            uid = getattr(value, "user", value).uid
        except AttributeError:
            uid = self.to_uid(value)
        self.fkey_last_updater_uid = uid
