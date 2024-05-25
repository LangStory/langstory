from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import Optional, List
from app.schemas.user_schemas import NewUser


class OrganizationCreate(BaseModel):
    name: str
    email_domain: Optional[HttpUrl] = None
    avatar_url: Optional[HttpUrl] = None

    class Config:
        orm_mode = True


class OrganizationRead(BaseModel):
    id: UUID
    name: str
    email_domain: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        orm_mode = True


class OrganizationReadWithUsers(OrganizationRead):
    users: List[NewUser]
