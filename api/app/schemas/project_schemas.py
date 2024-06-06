from typing import Optional, List

from pydantic import HttpUrl

from app.schemas.base_schema import BaseSchema
from app.schemas.tool_schemas import ToolRead


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
    tools: List[ToolRead]
