from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID
from pydantic import Field, model_validator, AliasChoices
from pydantic.json_schema import SkipJsonSchema

from app.models.message import EventType
from app.schemas.tool_call_schemas import ToolCallCreate, ToolCallRead
from app.schemas.base_schema import (
    BaseSchema,
    id_regex_pattern,
    id_example,
    id_description,
)


class ToolCreate(BaseSchema):
    name: str = Field(
        ...,
        description="The name of the tool",
        max_length=255,
        examples=["order_flight"],
    )
    description: Optional[str] = Field(
        None,
        description="A description of the tool",
        max_length=255,
        examples=["places a user's order for flight"],
    )
    project_id: str = Field(
        ...,
        pattern=id_regex_pattern("project"),
        examples=id_example("project"),
        description=id_description("project"),
        validation_alias=AliasChoices("project_id", "projectId", ),
    )
    json_schema: dict = Field(
        default_factory=lambda: {},
        description="The full OAI compatible JSON schema for the tool",
    )


class ToolRead(ToolCreate):
    id: str = Field(
        ...,
        pattern=id_regex_pattern("tool"),
        examples=id_example("tool"),
        description=id_description("tool"),
    )


class ToolUpdate(ToolRead):
    # optional to allow router to assemble from url
    id: Optional[str] = Field(
        None,
        pattern=id_regex_pattern("tool"),
        examples=id_example("tool"),
        description=id_description("tool"),
    )
    name: Optional[str] = Field(
        None,
        description="The name of the tool",
        max_length=255,
        examples=["order_flight"],
    )
    json_schema: Optional[dict] = Field(
        None,
        description="The full OAI compatible JSON schema for the tool",
    )
    project_id: SkipJsonSchema[str] = Field(default=None, read_only=True)
