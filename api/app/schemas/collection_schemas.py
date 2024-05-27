from typing import Union, Literal, Type
from pydantic import Field, ConfigDict

from app.models.base import Base
from app.schemas.base_schema import BaseSchema
from app.schemas.user_schemas import ScopedUser
from app.schemas.user_schemas import User

class CollectionRequest(BaseSchema):
    # TODO: define __get_pydantic_core_schema__ on ScopedUser to remove this
    model_config = ConfigDict(arbitrary_types_allowed=True)

    actor: Union[ScopedUser, User] = Field(description="The User acting on the request")
    per_page: int = Field(default=10, description="Number of items per page")
    page: int = Field(default=0, description="The current page number (0 indexed)")
    order_dir: Literal["asc", "desc"] = Field(default="asc", description="The order direction")
    order_by: str = Field(default=None, description="The field to order by")
    query: str = Field(default=None, description="The power-query formatted search query to filter the collection")

class CollectionResponse(BaseSchema):
    pages: int = Field(description="The total number of pages in the collection")
    per_page: int = Field(description="Number of items per page")
    page: int = Field(description="The current page number (0 indexed)")
    items: list[Type[Base]] = Field(description="The items in the collection")