from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from pydantic import Field, field_validator

from app.models.event import MessageRole
from app.schemas.base_schema import BaseSchema, id_regex_pattern, id_example, id_description



class ChatCreate(BaseSchema):
    name: str = Field(..., description="The name of the chat", max_length=255, examples=["Customer Onboarding Chat"])
    description: Optional[str] = Field(None, description="A description of the chat", max_length=255, examples=["A chat for discussing the project"])
    project_id: str = Field(..., pattern=id_regex_pattern("project"), examples=id_example("project"), description=id_description("project"))


class ChatRead(BaseSchema):
    id: str = Field(..., pattern=id_regex_pattern("chat"), examples=id_example("chat"), description=id_description("chat"))
    name: str
    description: Optional[str] = None
    project_id: str = Field(..., pattern=id_regex_pattern("project"), examples=id_example("project"), description=id_description("project"), validation_alias="project_id")

    @field_validator("project_id", mode="before")
    def project_id_validator(cls, value: Union[UUID,str]) -> str:
        """TODO: there is a broken pattern here that we need to do this"""
        if isinstance(value, UUID):
            return f"project-{value}"
        return value

class MessageCreate(BaseSchema):
    role: MessageRole
    content: str
    timestamp: datetime


class MessageRead(BaseSchema):
    id: str = Field(..., pattern=id_regex_pattern("message"), examples=id_example("message"), description=id_description("message"))
    role: MessageRole
    content: str
    timestamp: datetime
    chat_id: str = Field(..., pattern=id_regex_pattern("chat"), examples=id_example("chat"), description=id_description("chat"))
