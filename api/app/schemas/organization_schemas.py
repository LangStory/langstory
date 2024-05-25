from typing import Optional, List

from pydantic import HttpUrl

from app.schemas.base_schema import BaseSchema


class OrganizationCreate(BaseSchema):
    name: str
    email_domain: Optional[HttpUrl] = None
    avatar_url: Optional[HttpUrl] = None

    class Config:
        orm_mode = True


class OrganizationRead(BaseSchema):
    id: str
    name: str
    email_domain: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        orm_mode = True


class OrganizationReadWithUsers(OrganizationRead):
    users: List
