from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


from app.models.base import Base
from app.models.mixins import ChatMixin

if TYPE_CHECKING:
    from app.models.message import Message

class Thread(Base, ChatMixin):
    __tablename__ = "thread"

    name: Mapped[str] = mapped_column(String, nullable=False, doc="The name of the thread")

    # relationships
    messages: list["Message"] = relationship("Message", back_populates="thread", lazy="selectin")
