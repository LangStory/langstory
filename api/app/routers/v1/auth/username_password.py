from typing import Annotated, Generator, Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.jtw_schema import JWTResponse
from app.routers.utilities import get_db_session
from app.schemas.user_schemas import NewUser
from app.controllers.auth import JWTTokenFlow, AuthenticateUsernamePasswordFlow
from app.controllers.user import CreateNewUserFlow
from app.controllers.magic_link import MagicLinkFlow


router = APIRouter(prefix="/auth/username-password", tags=["auth"])


@router.post("/sign-up")
async def sign_up(
    new_user: NewUser,
    db_session: Annotated["Generator", Depends(get_db_session)],
) -> Optional[JWTResponse]:
    """register a new user"""
    user = CreateNewUserFlow(db_session).create_user_with_username_password(new_user)
    return JWTTokenFlow(db_session).get_refresh_token(user)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated["Generator", Depends(get_db_session)],
) -> Optional[JWTResponse]:
    """use standard U/P to exchange for a refresh JWT"""
    user = AuthenticateUsernamePasswordFlow(db_session).authenticate(email_address=form_data.username, password=form_data.password)
    return JWTTokenFlow(db_session).get_refresh_token(user)

@router.get("/get-magic-link")
async def get_magic_link(
    email_address: str,
    db_session: Annotated["Generator", Depends(get_db_session)],
):
    """send a magic link to the user"""
    MagicLinkFlow(db_session).send_magic_link(email_address)
