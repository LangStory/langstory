from typing import Annotated, Generator
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.http_errors import not_found
from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization_schemas import OrganizationBase

router = APIRouter(prefix="/organizations", tags=["admin"])


def get_logged_in_user():
    return None


def get_db_session():
    return None


@router.get("/")
def list_organizations(
    # TODO: need a "get_admin_user" dependency injection here
    # TODO: start with pagination for all lists right out of the gate please!
):
    return "orgs will go here!"


@router.get("/{id}", response_model=OrganizationBase)
def read(
    uid: UUID,
    user: Annotated["User", Depends(get_logged_in_user)],
    db_session: Annotated["Generator", Depends(get_db_session)],
):
    try:
        org = user.organizations.filter(Organization.uid == uid).one()
        return OrganizationBase.model_validate(org)
    except (NoResultFound, MultipleResultsFound) as e:
        not_found(e=e)
