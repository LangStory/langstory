from typing import Optional
from sqlmodel import Field, Column
from sqlalchemy import String
from pydantic import HttpUrl

from app.models.base import Base

class User(Base, table=True):

    email_address: str = Field(..., description="The unique email address of the user", sa_column=Column(String, unique=True))
    first_name: Optional[str] = Field(default=None, description="The first name of the user")
    last_name: Optional[str] = Field(default=None, description="The last name of the user")
    avatar_url: Optional[HttpUrl] = Field(default=None, description="The URL of the user's avatar", sa_column=Column(String))
