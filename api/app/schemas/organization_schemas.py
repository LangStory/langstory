from typing import Optional, List

from pydantic import HttpUrl

from app.schemas.base_schema import BaseSchema

class OrganizationBase(BaseSchema):
    class Config:
        from_attributes = True

class OrganizationCreate(OrganizationBase):
    name: str
    email_domain: Optional[HttpUrl] = None
    avatar_url: Optional[HttpUrl] = None

class OrganizationRead(OrganizationBase):
    id: str
    name: str
    email_domain: Optional[str] = None
    avatar_url: Optional[str] = None

class OrganizationReadWithUsers(OrganizationRead):
    users: List
