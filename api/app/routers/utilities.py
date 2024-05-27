from typing import Generator, Optional, TYPE_CHECKING, Annotated
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.settings import settings
from app.schemas.user_schemas import ScopedUser

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _create_engine(database: Optional[str] = None) -> Engine:
    database = database or settings.db_name
    return create_engine(
        URL.create(
            drivername="postgresql",
            host=settings.db_host,
            port=settings.db_port,
            username=settings.db_user,
            password=settings.db_password,
            database=database,
        )
    )


def get_db_session() -> Generator:
    bound_session = sessionmaker(bind=_create_engine())
    with bound_session() as session:
        yield session


def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/token/refresh"))]
) -> "ScopedUser":
    """decode the user from the JWT"""
    return ScopedUser.from_jwt(token)
