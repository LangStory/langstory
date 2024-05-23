from typing import Optional
from pydantic import Field
from app.schemas.base_schema import BaseSchema


class NewUser(BaseSchema):
    """when a new user is created"""

    email_address: str = Field(
        ..., description="the user's email address, must be unique once conformed"
    )
    display_name: str = Field(..., description="the user's display name")
    password: Optional[str] = Field(
        None, description="the user's password, required if not using SSO"
    )
