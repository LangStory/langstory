from datetime import datetime
from typing import Optional, TYPE_CHECKING, Type, Self, List, Literal, Union, Any
from uuid import UUID, uuid4

from humps import depascalize
from sqlalchemy import func, DateTime, text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

if TYPE_CHECKING:
    from sqlalchemy.sql.selectable import Select
    from sqlalchemy.orm import Session
    from app.schemas.user_schemas import ScopedUser
    from app.schemas.user_schemas import User


class AbsoluteBase(DeclarativeBase):
    pass


class Base(AbsoluteBase):
    __abstract__ = True

    __order_by_default__ = "created_at"

    uid: Mapped[UUID] = mapped_column(SQLUUID(), primary_key=True, default=uuid4)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    deleted: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))

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
        cls, db_session: "Session", identifier: Union[str, UUID], **kwargs
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
            prefix = prefix or cls.__name__.lower()
            uid = UUID(identifier.split(f"{prefix}-")[-1])
        except AttributeError:
            # a UUID was passed
            uid = identifier
        except ValueError as e:
            raise ValueError(
                f"{identifier} is not a valid id for {cls.__name__}"
            ) from e
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
            actor, "_organization_uid", getattr(actor.organization, "uid", None)
        )
        if not org_uid:
            raise ValueError("object %s has no organization accessor", actor)
        return query.where(cls._organization_uid == org_uid)

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

    _creator_uid: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(),
        ForeignKey("user.uid"),
        nullable=True,
        doc="The ID of the user that owns this entity",
    )
    _last_editor_uid: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(),
        ForeignKey("user.uid"),
        nullable=True,
        doc="The ID of the user that last updated this entity",
    )

    @property
    def creator_id(self) -> Optional[str]:
        if uid := self._creator_uid:
            return f"user-{uid}"
        return None

    @creator_id.setter
    def creator_id(self, value: Union[str, UUID, "User", "ScopedUser"]) -> None:
        try:
            uid = getattr(value, "user", value).uid
        except AttributeError:
            uid = self.to_uid(value, prefix="user")
        self._creator_uid = uid

    @property
    def editor_id(self) -> Optional[str]:
        return f"user-{self._last_editor_uid}"

    @editor_id.setter
    def editor_id(self, value: Union[str, UUID, "User", "ScopedUser"]) -> None:
        try:
            uid = getattr(value, "user", value).uid
        except AttributeError:
            uid = self.to_uid(value, prefix="user")
        self._last_editor_uid = uid
