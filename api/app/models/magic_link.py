from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditedBase
from app.models.mixins import UserMixin

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.models.user import User


def ten_minutes():
    return datetime.now(timezone.utc) + timedelta(minutes=10)


class MagicLink(AuditedBase, UserMixin):
    __tablename__ = "magic_link"

    token_hash: Mapped[str] = mapped_column(nullable=False, doc="The token to verify against")
    expiration: Mapped[datetime] = mapped_column(default=ten_minutes, doc="The expiration date of the magic link")

    # relationships
    user: Mapped["User"] = relationship("User", primaryjoin="MagicLink._user_uid == User.uid")

    @property
    def is_expired(self) -> bool:
        return self.expiration.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)

    @classmethod
    def clear_for_user(cls, db_session: "Session", user_uid: UUID):
        db_session.query(cls).filter(cls._user_uid == user_uid).delete()
        db_session.commit()

    @classmethod
    def read(cls, db_session: "Session", identifier: str) -> Optional["MagicLink"]:
        # look up by user_id, not the magic link id
        user_uid = User.to_uid(identifier)
        return db_session.query(cls).where(cls._user_uid == user_uid).one_or_none()
