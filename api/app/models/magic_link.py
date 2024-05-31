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
    fkey_user_uid: UUID = Field(
        ..., foreign_key="user.uid", description="The user this magic link is for"
    )

    @property
    def user_id(self) -> str:
        if uid := self.fkey_user_uid:
            return f"user-{uid}"
        return None

    @user_id.setter
    def user_id(self, value:str) -> None:
        self.fkey_user_uid = User.to_uid(value)


    # relationships
    user: "User" = Relationship(sa_relationship_kwargs={"lazy": "joined", "primaryjoin": "User.uid == MagicLink.fkey_user_uid"})

    @property
    def is_expired(self) -> bool:
        return self.expiration.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)

    @classmethod
    def clear_for_user(cls, db_session: "Session", user_uid: UUID):
        db_session.query(cls).filter(cls.fkey_user_uid == user_uid).delete()
        db_session.commit()

    @classmethod
    def read(cls, db_session: "Session", identifier: str) -> Optional["MagicLink"]:
        # look up by user_id, not the magic link id
        user_uid = User.to_uid(identifier)
        return db_session.query(cls).where(cls.fkey_user_uid == user_uid).one_or_none()
