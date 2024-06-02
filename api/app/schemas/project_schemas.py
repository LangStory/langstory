from typing import Optional

from pydantic import HttpUrl

from app.schemas.base_schema import BaseSchema


class ProjectCreate(BaseSchema):
    name: str
    avatar_url: Optional[HttpUrl] = None
    description: Optional[str] = None


class ProjectRead(BaseSchema):
    id: str
    name: str
    avatar_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    organization_id: str
