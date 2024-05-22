from pydantic import BaseModel, ConfigDict
from humps import camelize


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        extra="forbid",
    )
