from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlmodel import Field, Relationship

from app.models.base import Base

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.models.user import User


def ten_minutes():
    return datetime.now(timezone.utc) + timedelta(minutes=10)


class MagicLink(Base, table=True):
    token_hash: str = Field(..., description="The token to verify against")
    expiration: datetime = Field(
        default_factory=ten_minutes, description="The expiration date of the magic link"
    )
    user_uid: UUID = Field(
        ..., foreign_key="user.uid", description="The user this magic link is for"
    )

    # relationships
    user: "User" = Relationship(sa_relationship_kwargs={"lazy": "joined"})

    @property
    def is_expired(self) -> bool:
        return self.expiration.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)

    @classmethod
    def clear_for_user(cls, db_session: "Session", user_uid: UUID):
        db_session.query(cls).filter(cls.user_uid == user_uid).delete()
        db_session.commit()

    @classmethod
    def read(cls, db_session: "Session", user_uid: "UUID") -> Optional["MagicLink"]:
        return db_session.query(cls).where(cls.user_uid == user_uid).one()
