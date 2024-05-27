from typing import Annotated, Generator, Optional
from fastapi import APIRouter, Depends

from app.routers.utilities import get_db_session
from app.schemas.user_schemas import UpdateUser
from app.controllers.user import UpdateUserFlow
from app.schemas.user_schemas import ScopedUser, PydanticScopedUser
from app.routers.utilities import get_current_user, get_db_session


router = APIRouter(prefix="/me", tags=["user"])


@router.put("")
@router.patch("")
async def update_self(
    updates: UpdateUser,
    db_session: Annotated["Generator", Depends(get_db_session)],
    actor: ScopedUser = Depends(get_current_user),
) -> Optional[PydanticScopedUser]:
    """update a user's own profile"""
    controller = UpdateUserFlow(db_session)
    return controller.update_user(actor, updates)
