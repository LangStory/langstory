from typing import Union, Literal, Type, Optional, List
from pydantic import Field
from app.models.base import Base
from app.schemas.base_schema import BaseSchema
from app.schemas.user_schemas import ScopedUser
from app.models.user import User


class CollectionRequest(BaseSchema):
    actor: Union[ScopedUser, User] = Field(
        description="The User acting on the request",
    )
    per_page: Optional[int] = Field(default=10, description="Number of items per page")
    page: Optional[int] = Field(
        default=1, description="The current page number (1 indexed)"
    )
    order_dir: Optional[Literal["asc", "desc"]] = Field(
        default="asc", description="The order direction"
    )
    order_by: Optional[str] = Field(default=None, description="The field to order by")
    query: Optional[str] = Field(
        default=None,
        description="The power-query formatted search query to filter the collection",
    )


class CollectionResponse(BaseSchema):
    pages: int = Field(description="The total number of pages in the collection")
    items: List = Field(description="The items in the collection")
    page: int = Field(description="The current page number")
