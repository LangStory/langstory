from datetime import datetime
from typing import Optional, Union, List
from uuid import UUID
from pydantic import Field, model_validator

from app.models.message import EventType
from app.schemas.tool_call_schemas import ToolCallCreate, ToolCallRead
from app.schemas.base_schema import (
    BaseSchema,
    id_regex_pattern,
    id_example,
    id_description,
)


class ChatCreate(BaseSchema):
    name: str = Field(
        ...,
        description="The name of the chat",
        max_length=255,
        examples=["Customer Onboarding Chat"],
    )
    description: Optional[str] = Field(
        None,
        description="A description of the chat",
        max_length=255,
        examples=["A chat for discussing the project"],
    )
    project_id: str = Field(
        ...,
        pattern=id_regex_pattern("project"),
        examples=id_example("project"),
        description=id_description("project"),
    )


class ChatRead(BaseSchema):
    id: str = Field(
        ...,
        pattern=id_regex_pattern("chat"),
        examples=id_example("chat"),
        description=id_description("chat"),
    )
    name: str
    description: Optional[str] = None
    project_id: str = Field(
        ...,
        pattern=id_regex_pattern("project"),
        examples=id_example("project"),
        description=id_description("project"),
        validation_alias="project_id",
    )


class ChatUpdate(BaseSchema):
    name: Optional[str] = Field(
        None,
        description="The name of the chat",
        max_length=255,
        examples=["Customer Onboarding Chat"],
    )
    description: Optional[str] = Field(
        None,
        description="A description of the chat",
        max_length=255,
        examples=["A chat for discussing the project"],
    )


class MessageCreate(BaseSchema):
    type: EventType
    content: str
    timestamp: datetime
    thread_id: Optional[str] = Field(
        None,
        pattern=id_regex_pattern("thread"),
        examples=id_example("thread"),
        description=id_description("thread"),
    )

    # user
    name: Optional[str] = Field(
        None, description="The name of the user", max_length=255, examples=["John Doe"]
    )
    persona_id: Optional[str] = Field(
        None,
        pattern=id_regex_pattern("persona"),
        examples=id_example("persona"),
        description=id_description("persona"),
    )

    # TODO: fast followup here, be able to edit the tool calls as related objects on the message directly.

    # assistant
    tool_calls_requested: Optional[List[Optional[ToolCallCreate]]] = Field(
        None, description="The tool calls requested by the assistant"
    )

    # tool
    tool_call_response: Optional[ToolCallCreate] = Field(
        None,
        description="The tool call associated with the response from executing the tool call",
    )

    @model_validator(mode="before")
    def check_event_type_params(cls, values):
        try:
            vtype = values["type"]
        except (KeyError, TypeError):
            return values
        try:
            if vtype == EventType.tool_message:
                assert (
                    values.get("tool_call_response", None) is not None
                ), "tool_call_response is required for tool_message events"
                assert (
                    values.get("tool_calls_requested", None) is None
                ), "tool_calls_requested is not allowed for tool_message events"
            elif not vtype == EventType.assistant_message:
                assert (
                    values.get("tool_calls_requested", None) is None
                ), "tool_calls_requested is not allowed for non-assistant_message events"
            return values
        except AssertionError as e:
            raise ValueError(e)


class MessageRead(MessageCreate):
    id: str = Field(
        ...,
        pattern=id_regex_pattern("message"),
        examples=id_example("message"),
        description=id_description("message"),
    )
    chat_id: str = Field(
        ...,
        pattern=id_regex_pattern("chat"),
        examples=id_example("chat"),
        description=id_description("chat"),
        validation_alias="chat_id",
    )

    # assistant
    tool_calls_requested: Optional[List[Optional[Union[ToolCallRead, str]]]] = Field(
        None, description="The tool calls requested by the assistant"
    )

    # tool
    tool_call_response: Optional[Union[ToolCallRead, str]] = Field(
        None,
        description="The tool call associated with the response from executing the tool call",
    )
