from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import NoResultFound, MultipleResultsFound

from fastapi import APIRouter, Depends

from app.http_errors import not_found

if TYPE_CHECKING:
    from sqlalchemy import Session

router = APIRouter(prefix="/users", tags=["users"])


def get_logged_in_user():
    return None
