from typing import Any, Optional, TYPE_CHECKING, Type
from uuid import UUID
from pydantic import Field

from app.schemas.base_schema import (
    BaseSchema,
    id_regex_pattern,
    id_example,
    id_description,
)
from app.schemas.organization_schemas import OrganizationRead
from app.models.user import User
from app.models.organization import Organization

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class NewUser(BaseSchema):
    """when a new user is created"""

    email_address: str = Field(
        ..., description="the user's email address, must be unique once conformed"
    )
    first_name: str = Field(..., description="the user's display name")
    last_name: str = Field(..., description="the user's display name")
    password: Optional[str] = Field(
        default=None, description="the user's password, required if not using SSO"
    )


class UpdateUser(NewUser):
    """when a user updates their own profile"""

    email_address: Optional[str] = Field(None, description="the user's email address")
    first_name: Optional[str] = Field(None, description="the user's display name")
    last_name: Optional[str] = Field(None, description="the user's display name")
    avatar_url: Optional[str] = Field(None, description="the user's avatar image URL")


class ReadUser(UpdateUser):
    id: str = Field(
        ...,
        example=id_example("user"),
        pattern=id_regex_pattern("user"),
        description=id_description("user"),
    )


class ScopedUser:
    """a user scoped to an organization"""

    user: "User"
    organization: Optional["Organization"] = None

    def __init__(self, user: "User", organization: Optional["Organization"] = None):
        self.user = user
        self.organization = organization

    def __getattr__(self, attr: str) -> Any:
        try:
            return self.__getattribute__(attr)
        except AttributeError as e:
            if hasattr(self.user, attr):
                return getattr(self.user, attr)
            raise e

    @classmethod
    def from_jwt(cls, decoded: dict) -> "ScopedUser":
        """create from a decoded auth JWT"""
        user_uid = UUID(decoded["sub"].split("user-")[1])
        org = None
        if decoded["org"]:
            org_uid = UUID(decoded["org"]["id"].split("organization-")[1])
            org = Organization(uid=org_uid, name=decoded["org"]["name"])
        return ScopedUser(
            user=User(
                uid=user_uid,
                email_address=decoded["user"]["email_address"],
                first_name=decoded["user"]["first_name"],
                last_name=decoded["user"]["last_name"],
                avatar_url=decoded["user"]["avatar_url"],
            ),
            organization=org,
        )

    def refresh(self, db_session: "Session") -> "ScopedUser":
        """refresh the user object from the database"""
        return ScopedUser(
            user=User.read(db_session, self.user.id),
            organization=Organization.read(db_session, self.organization.id),
        )

    def to_pydantic(self) -> Type["BaseSchema"]:
        """convert to a Pydantic model, no longer supports the graduated attr lookup"""
        return PydanticScopedUser(user=self.user, organization=self.organization)


class PydanticScopedUser(BaseSchema):
    """ScopedUser converted to a Pydantic model, no longer supports the graduated attr lookup"""

    user: ReadUser
    organization: Optional[OrganizationRead]
