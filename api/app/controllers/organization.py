from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.user import User
from app.models.orgnanizations_users import OrganizationsUsers
from app.schemas.organization_schemas import OrganizationCreate, OrganizationRead, OrganizationReadWithUsers


class OrganizationController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_organization(self, organization_data: OrganizationCreate) -> Organization:
        organization = Organization(**organization_data.dict())
        self.db_session.add(organization)
        self.db_session.commit()
        self.db_session.refresh(organization)
        return organization

    def get_organizations(self) -> List[OrganizationRead]:
        organizations = self.db_session.query(Organization).all()
        return [OrganizationRead.from_orm(org) for org in organizations]

    def get_organization(self, organization_id: UUID) -> OrganizationReadWithUsers:
        organization = self.db_session.query(Organization).filter(Organization.uid == organization_id).first()
        if organization:
            return OrganizationReadWithUsers.from_orm(organization)
        return None

    def add_user_to_organization(self, organization_id: UUID, user_id: UUID) -> None:
        organization_user = OrganizationsUsers(organization_id=organization_id, user_id=user_id)
        self.db_session.add(organization_user)
        self.db_session.commit()
