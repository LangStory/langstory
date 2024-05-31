from typing import Optional
from uuid import UUID
from sqlmodel import Field, Column
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base
from app.models.project import Project


class Tool(Base, table=True):
    """The callable function as presented to the LLM"""

    name: str = Field(..., description="The name of the tool to be called")
    json_schema: dict = Field(
        default_factory=dict,
        description="The jsonschema for the tool",
        sa_column=Column(JSONB),
    )
    description: Optional[str] = Field(
        default=None, description="A displayable description of the tool"
    )
    fkey_project_uid: UUID = Field(
        ...,
        foreign_key="project.uid",
        description="The ID of the project this tool belongs to",
    )

    @property
    def project_id(self) -> str:
        if uid := self.fkey_project_uid:
            return f"project-{uid}"
        return None

    @project_id.setter
    def project_id(self, value:str) -> None:
        self.fkey_project_uid = Project.to_uid(value)