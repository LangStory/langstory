from pydantic import BaseModel, ConfigDict
from humps import camelize


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        extra="forbid",
        from_attributes=True,
        # TODO: implement __get_pydantic_core_schema__ on ScopedUser to remove this
        arbitrary_types_allowed=True
    )
