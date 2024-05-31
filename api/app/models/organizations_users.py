from uuid import UUID
from sqlmodel import Field
from app.models.base import Base


class OrganizationsUsers(Base, table=True):
    fkey_organization_uid: UUID = Field(..., foreign_key="organization.uid")
    fkey_user_uid: UUID = Field(..., foreign_key="user.uid")


    @property
    def user_id(self) -> str:
        if uid := self.fkey_user_uid:
            return f"user-{uid}"
        return None

    @user_id.setter
    def user_id(self, value:str) -> None:
        self.fkey_user_uid = Base.to_uid(value, prefix="user")

    @property
    def organization_id(self) -> str:
        if uid := self.fkey_organization_uid:
            return f"organization-{uid}"
        return None

    @organization_id.setter
    def organization_id(self, value:str) -> None:
        self.fkey_organization_uid = Base.to_uid(value, prefix="organization")
