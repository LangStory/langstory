from uuid import UUID
from sqlmodel import Field
from app.models.base import Base
from app.models.user import User
from app.models.organization import Organization


class OrganizationsUsers(Base, table=True):
    _organization_uid: UUID = Field(..., foreign_key="organization.uid")
    _user_uid: UUID = Field(..., foreign_key="user.uid")


    @property
    def user_id(self) -> str:
        if uid := self._user_uid:
            return f"user-{uid}"
        return None

    @user_id.setter
    def user_id(self, value:str) -> None:
        self._user_uid = User.to_uid(value)

    @property
    def organization_id(self) -> str:
        if uid := self._organization_uid:
            return f"organization-{uid}"
        return None

    @organization_id.setter
    def organization_id(self, value:str) -> None:
        self._organization_uid = Organization.to_uid(value)
