from typing import Optional
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from app.schemas.base_schema import (
    BaseSchema,
    id_regex_pattern,
    id_example,
    id_description,
)

class ThreadCreate(BaseSchema):
    name: str = Field(
        ...,
        description="The name of the thread",
        max_length=255,
        examples=["variant 2"],
    )
    chat_id: str = Field(
        ...,
        pattern=id_regex_pattern("chat"),
        examples=id_example("chat"),
        description=id_description("chat"),
    )
    message_ids: Optional[list[str]] = Field(
        [],
        description="The ids of the messages in the thread",
        examples=[id_example('message')],
    )

class ThreadRead(ThreadCreate):
    id: str = Field(
        ...,
        pattern=id_regex_pattern("thread"),
        examples=id_example("thread"),
        description=id_description("thread"),
    )


class ThreadUpdate(ThreadRead):
    # optional to allow router to assemble from url
    id: Optional[str] = Field(
        None,
        pattern=id_regex_pattern("thread"),
        examples=id_example("thread"),
        description=id_description("thread"),
    )
    name: Optional[str] = Field(
        None,
        description="The name of the thread",
        max_length=255,
        examples=["order_flight"],
    )
    chat_id: SkipJsonSchema[str] = Field(
        None,
        pattern=id_regex_pattern("chat"),
        examples=id_example("chat"),
        description=id_description("chat"),
        exclude=True,
    )
