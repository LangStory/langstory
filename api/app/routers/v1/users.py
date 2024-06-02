from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends

from app.schemas.collection_schemas import CollectionResponse, CollectionRequest
from app.routers.utilities import get_db_session, get_current_user
from app.controllers.user import UserController

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from app.schemas.user_schemas import ScopedUser

router = APIRouter(prefix="/users", tags=["user"])

@router.get("/", response_model=CollectionResponse)
def list_users(
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
    controller = UserController(db_session)
    return controller.list_for_actor(request)

