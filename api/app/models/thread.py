from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.message import Message


class Thread(Base, table=True):
    name: str = Field(..., description="The name of the organization")
    messages: list["Message"] = Relationship(
        back_populates="thread", sa_relationship_kwargs={"lazy": "selectin"}
    )
