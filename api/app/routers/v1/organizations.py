from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.controllers.organization import OrganizationController

from app.routers.utilities import get_db_session
from app.schemas.organization_schemas import OrganizationCreate, OrganizationRead, OrganizationReadWithUsers

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/", response_model=OrganizationRead)
def create_organization(organization_data: OrganizationCreate, db: Session = Depends(get_db_session)):
    controller = OrganizationController(db)
    organization = controller.create_organization(organization_data)
    return organization


@router.get("/", response_model=List[OrganizationRead])
def get_organizations(db: Session = Depends(get_db_session)):
    controller = OrganizationController(db)
    organizations = controller.get_organizations()
    return organizations


@router.get("/{organization_id}", response_model=OrganizationReadWithUsers)
def get_organization(organization_id: UUID, db: Session = Depends(get_db_session)):
    controller = OrganizationController(db)
    organization = controller.get_organization(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.post("/{organization_id}/users/{user_id}")
def add_user_to_organization(organization_id: UUID, user_id: UUID, db: Session = Depends(get_db_session)):
    controller = OrganizationController(db)
    controller.add_user_to_organization(organization_id, user_id)
    return {"message": "User added to organization"}
