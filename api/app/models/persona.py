from typing import Optional
from uuid import UUID
from pydantic import HttpUrl
from sqlmodel import Field, Column, String

from app.models.base import Base

class Persona(Base, table=True):

    name: str = Field(..., description="The name of the persona")
    description: Optional[str] = Field(default=None, description="A description of the persona")
    project_id: UUID = Field(..., foreign_key="project.uid", description="The ID of the project this persona belongs to")
    avatar_url: Optional[HttpUrl] = Field(None, description="The URL of the persona's avatar", sa_column=Column(String))