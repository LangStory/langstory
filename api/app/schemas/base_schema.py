from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from humps import camelize


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        extra="forbid",
        from_attributes=True,
        # TODO: implement __get_pydantic_core_schema__ on ScopedUser to remove this
        arbitrary_types_allowed=True,
    )

    @property
    def uid(self) -> "UUID":
        """reverse of the id property on the models :vomit:"""
        if not hasattr(self, "id") or not self.id:
            raise ValueError("cannot infer uid, id property not found")
        return UUID(self.id.split("-",-1)[-1])

def id_regex_pattern(prefix: str):
    """generates the regex pattern for a given id"""
    return (
        r"^" + prefix + r"-"  # prefix string
        r"[a-fA-F0-9]{8}-"  # 8 hexadecimal characters
        r"[a-fA-F0-9]{4}-"  # 4 hexadecimal characters
        r"[a-fA-F0-9]{4}-"  # 4 hexadecimal characters
        r"[a-fA-F0-9]{4}-"  # 4 hexadecimal characters
        r"[a-fA-F0-9]{12}$"  # 12 hexadecimal characters
    )

def id_example(prefix: str):
    """generates an example id for a given prefix"""
    return [prefix + "-123e4567-e89b-12d3-a456-426614174000"]

def id_description(prefix: str):
    """generates a factory function for a given prefix"""
    return f"The human-friendly ID of the {prefix.capitalize()}"