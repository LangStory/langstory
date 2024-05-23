from typing import Optional
from pydantic import Field

from app.schemas.base_schema import BaseSchema


class JWTBase(BaseSchema):
    token: str = Field(..., description="The actual JWT token")


class JWTResponse(JWTBase):
    data: Optional[dict] = Field(
        default={},
        description="The data stored in the JWT token, readable by the client",
    )
