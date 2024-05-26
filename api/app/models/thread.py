from sqlmodel import Field, Relationship

from app.models.base import Base
from app.models.event import Message


class Thread(Base, table=True):
    name: str = Field(..., description="The name of the organization")
    messages: list[Message] = Relationship(
        link_model=OrganizationsUsers, sa_relationship_kwargs={"lazy": "joined"}
    )
