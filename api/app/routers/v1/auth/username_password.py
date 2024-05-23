from typing import TYPE_CHECKING, Annotated, Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schemas import NewUser
from app.schemas.jtw_schema import JWTBase, JWTResponse
from app.routers.utilities import get_db_session

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from uuid import UUID

router = APIRouter(prefix="/username-password", tags=["auth"])


@router.post("/register")
async def register(
    new_user: Annotated["NewUser", Depends()],
    db_session: "Session" = Depends(get_db_session),
):
    """register a new user"""
    raise NotImplementedError


@router.get("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: "Session" = Depends(get_db_session),
):
    """use standard U/P to exchange for a JWT"""
    raise NotImplementedError


@router.get("/refresh", response_model=JWTResponse)
async def refresh(
    token: JWTBase,
    db_session: "Session" = Depends(get_db_session),
):
    """use a refresh token to get a new JWT"""
