from typing import TYPE_CHECKING, Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.routers.utilities import get_db_session

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

router = APIRouter(prefix="/username-password", tags=["auth"])

@router.get("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: "Session" = Depends(get_db_session),
):
    """use standard U/P to exchange for a JWT"""
    raise NotImplementedError