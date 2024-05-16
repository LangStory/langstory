from fastapi import APIRouter
from app.models.organization import Organization

router = APIRouter(prefix="/organizations", tags=["admin"])

@router.get("/")
async def list_organizations(
    # TODO: need a "get_admin_user" dependency injection here
    # TODO: start with pagination for all lists right out of the gate please!
):
    return "orgs will go here!"