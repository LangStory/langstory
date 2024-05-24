from typing import Any, Optional, TYPE_CHECKING
from pydantic import Field
from app.schemas.base_schema import BaseSchema

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User


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
