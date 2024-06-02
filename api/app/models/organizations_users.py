from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import UserMixin, OrganizationMixin

class OrganizationsUsers(UserMixin, OrganizationMixin, Base):
    """associates users with organizations"""
    __tablename__ = "organizations_users"