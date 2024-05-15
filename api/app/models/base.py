from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from humps import depascalize, camelize

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

