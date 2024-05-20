from typing import Optional, Union, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict
from sqlalchemy import DateTime, func, select
from sqlalchemy.orm import Mapped, mapped_column
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

    uid: UUID = Field(default=uuid4, primary_key=True)
    created_at: datetime = Field(default=None, sa_column=mapped_column(DateTime(), server_default=func.now(), nullable=True))
    updated_at: datetime = Field(default=None, sa_column=mapped_column(DateTime(), onupdate=func.now(), nullable=True))


    @property
    def __prefix__(self) -> str:
        return depascalize(self.__class__.__name__)

    @property
    def id(self) -> Optional[str]:
        return f"{self.__prefix__}-{self.uid}"

    def find(cls, db_session:"Session", lookup=dict) -> "Base":
        """gets a single existing object or raises, based on filter criteria
        Args: 
            kwargs: the filter and values
        Raises:
            - NoResultFound, MultipleResultsFound if not one
        """
        with db_session as session:
            query = session(cls)
            for k,v in lookup:
                key = getattr(cls, k)
                query = query.where(key==v)
            return session.one(query)
            
            