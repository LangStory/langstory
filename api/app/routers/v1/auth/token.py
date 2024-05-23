from typing import TYPE_CHECKING, Generator, Annotated
from fastapi import APIRouter, Depends

from app.schemas.jtw_schema import JWTBase, JWTResponse
from app.routers.utilities import get_db_session

from app.controllers.auth import JWTTokenFlow

router = APIRouter(prefix="/token", tags=["auth"])


@router.post("/refresh")
def refresh(
    token: JWTBase,
    db_session: Annotated["Generator", Depends(get_db_session)],
):
    """use a refresh token to get a new JWT"""
    #flow = JWTTokenFlow(db_session)
    # return flow.get_auth_token(token.token)
