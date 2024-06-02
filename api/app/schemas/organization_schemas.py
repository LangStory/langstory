from typing import Optional, List

from pydantic import HttpUrl, Field

from app.schemas.base_schema import (
    BaseSchema,
    id_example,
    id_regex_pattern,
    id_description,
)


class OrganizationBase(BaseSchema):
    class Config:
        from_attributes = True


class OrganizationCreate(OrganizationBase):
    name: str
    email_domain: Optional[HttpUrl] = None
    avatar_url: Optional[HttpUrl] = None


class OrganizationRead(OrganizationBase):
    id: str = Field(
        ...,
        example=id_example("organization"),
        pattern=id_regex_pattern("organization"),
        description=id_description("organization"),
    )
    name: str
    email_domain: Optional[str] = None
    avatar_url: Optional[str] = None


class OrganizationReadWithUsers(OrganizationRead):
    users: List
