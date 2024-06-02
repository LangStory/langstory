from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


from app.models.base import Base
from app.models._mixins import ChatMixin

if TYPE_CHECKING:
    from app.models.message import Message


class Thread(ChatMixin, Base):
    __tablename__ = "thread"

    name: Mapped[str] = mapped_column(
        String, nullable=False, doc="The name of the thread"
    )

    # relationships
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="thread", lazy="selectin"
    )
