from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import Optional, List
from app.schemas.user_schemas import ScopedUser


class OrganizationCreate(BaseModel):
    name: str
    email_domain: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None


class OrganizationRead(BaseModel):
    id: UUID
    name: str
    email_domain: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

    class Config:
        orm_mode = True


class OrganizationReadWithUsers(OrganizationRead):
    users: List[ScopedUser]
