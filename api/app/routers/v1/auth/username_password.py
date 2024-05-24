from typing import TYPE_CHECKING, Annotated, Generator, Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.jtw_schema import JWTBase, JWTResponse
from app.routers.utilities import get_db_session
from app.schemas.user_schemas import NewUser
from app.controllers.auth import JWTTokenFlow, CreateUserFlow, AuthenticateUsernamePasswordFlow

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

router = APIRouter(prefix="/username-password", tags=["auth"])


@router.post("/sign-up")
async def sign_up(
    new_user: NewUser,
    db_session: Annotated["Generator", Depends(get_db_session)],
) -> Optional[JWTResponse]:
    """register a new user"""
    raise NotImplementedError


@router.get("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated["Generator", Depends(get_db_session)],
)-> Optional[JWTResponse]:
    """use standard U/P to exchange for a refresh JWT"""
    user = AuthenticateUsernamePasswordFlow(db_session).authenticate(email_address=form_data.username, password=form_data.password)
    return JWTTokenFlow(db_session).get_refresh_token(user)