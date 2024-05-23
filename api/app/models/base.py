from typing import Optional, TYPE_CHECKING, Type, Self
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict
from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column
from uuid import UUID, uuid4
from humps import depascalize, camelize

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class Base(SQLModel):
    __abstract__ = True
    model_config = ConfigDict(
        alias_generator=camelize,
        extra="forbid",
    )

    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
    deleted: bool = Field(default=False)

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
    def read(cls, db_session: "Session", uid: Optional[UUID] = None, **kwargs) -> Type[Self]:
        del kwargs
        if uid is None:
            raise ValueError("uid is required")
        with db_session as session:
            return session.query(cls).where(cls.uid==uid).one()

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
