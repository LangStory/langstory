from uuid import UUID

from sqlmodel import Field

from app.models.base import Base


class OrganizationsUsers(Base, table=True):
    organization_id: UUID = Field(..., foreign_key='organization.id')
    user_id: UUID = Field(..., foreign_key='user.id')
