from typing import Generator, Optional, TYPE_CHECKING, Annotated, Callable, Any, Type
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError

from app.settings import settings
from app.http_errors import auth_expired
from app.controllers.auth import JWTTokenFlow
from app.schemas.user_schemas import ScopedUser
from app.schemas.collection_schemas import CollectionRequest


if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.schemas.base_schema import BaseSchema


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
    token: Annotated[
        str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/username-password/dev-login"))
    ]
) -> "ScopedUser":
    """decode the user from the JWT"""
    try:
        decoded = JWTTokenFlow.decode_token(token)
        return ScopedUser.from_jwt(decoded)
    except ExpiredSignatureError as e:
        auth_expired(e=e)


def list_router_for_actor_factory(controller_model:Any) -> Callable:
    """since the list router is always the same, we can create a factory"""

    def list_collection(
        perPage: int = None,
        page: int = None,
        query: str = None,
        orderBy: str = None,
        orderDir: str = None,
        db_session: "Session" = Depends(get_db_session),
        actor: "ScopedUser" = Depends(get_current_user),
    ):
        query_args = {}
        # drop the None values
        for key in ["perPage", "page", "orderBy", "orderDir"]:
            if locals()[key] is not None:
                query_args[key] = locals()[key]
        request = CollectionRequest(actor=actor, **query_args)
        controller = controller_model(db_session)
        return controller.list_for_actor(request)

    return list_collection