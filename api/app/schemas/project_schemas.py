# app/dependencies.py
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class ProjectCreate(BaseModel):
    name: str
    avatar_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    organization_id: UUID


class ProjectRead(BaseModel):
    id: UUID
    name: str
    avatar_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    organization_id: UUID

    class Config:
        orm_mode = True
