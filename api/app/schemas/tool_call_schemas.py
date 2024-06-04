from datetime import datetime
from typing import Optional, Union, Dict
from uuid import UUID, uuid4
from pydantic import Field, field_validator

from app.schemas.base_schema import (
    BaseSchema,
    id_regex_pattern,
    id_example,
    id_description,
)


class ToolCallCreate(BaseSchema):

    tool_id: str = Field(
        ...,
        pattern=id_regex_pattern("tool"),
        description="The id of the tool being called",
        examples=id_example("tool"),
    )
    request_id: Optional[str] = Field(
        default_factory=uuid4, description="The ID of the request, generated by the LLM"
    )
    parameters: Optional[Dict[str, Union[str, int, float, bool]]] = Field(
        None, description="The parameters for the tool call"
    )
    assistant_message_id: Optional[str] = Field(
        None,
        pattern=id_regex_pattern("assistantmessage"),
        examples=id_example("assistantmessage"),
        description="Optional only because it can be used in compound creates for the assistant message",
    )


class ToolCallRead(BaseSchema):

    id: str = Field(
        ...,
        pattern=id_regex_pattern("toolcall"),
        examples=id_example("toolcall"),
        description=id_description("toolcall"),
    )
    tool_id: str = Field(
        ...,
        pattern=id_regex_pattern("tool"),
        description="The id of the tool being called",
        examples=id_example("tool"),
    )
    request_id: Optional[str] = Field(
        default_factory=uuid4, description="The ID of the request, generated by the LLM"
    )
    parameters: Optional[Dict[str, Union[str, int, float, bool]]] = Field(
        None, description="The parameters for the tool call"
    )
    assistant_message_id: str = Field(
        ...,
        pattern=id_regex_pattern("assistantmessage"),
        examples=id_example("assistantmessage"),
        description=id_description("assistantmessage"),
    )
