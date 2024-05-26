from typing import Annotated, Generator, Optional
from fastapi import APIRouter, Depends

from app.routers.utilities import get_db_session
from app.controllers.magic_link import MagicLinkFlow
from app.controllers.auth import JWTTokenFlow
from app.http_errors import bad_request
from app.schemas.jtw_schema import JWTResponse

router = APIRouter(prefix="/auth/magic-link", tags=["auth"])


@router.get("")
async def get_magic_link(
    email_address: str,
    db_session: Annotated["Generator", Depends(get_db_session)],
):
    """send a magic link to the user"""
    try:
        MagicLinkFlow(db_session).send_magic_link(email_address)
    except NotImplementedError as e:
        bad_request(
            e=e,
            message="Email is not enabled on this server. Please update SMTP and try again.",
        )
    return {"message": "Magic link sent"}


@router.get("/login/{slug}")
async def login_with_magic_link(
    slug: str,
    db_session: Annotated["Generator", Depends(get_db_session)],
) -> Optional[JWTResponse]:
    """login with a magic link"""
    user = MagicLinkFlow(db_session).validate_magic_link(slug)
    return JWTTokenFlow(db_session).get_refresh_token(user)
