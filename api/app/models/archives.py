from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, UUID as SQLUUID, BOOLEAN
from sqlalchemy.dialects.postgresql import JSONB, TEXT, TIMESTAMP
from uuid import UUID
from sqlmodel import SQLModel, Field

from app.models.base import Base

class Archives(SQLModel, table=True):
    """Reflection of table created manually by migration"""

    __tablename__ = "archives"

    id: int = Field(primary_key=True, sa_type=Integer)
    table_name: str = Field(..., nullable=False, sa_type=TEXT)
    record_type: str = Field(..., nullable=False, sa_type=TEXT)
    record_id: UUID = Field(..., nullable=False, sa_type=SQLUUID)
    operation: str = Field(nullable=False, sa_type=TEXT)
    old_values: Optional[dict] = Field(nullable=True, sa_type=JSONB)
    new_values: Optional[dict] = Field(nullable=True, sa_type=JSONB)
    most_recent: Optional[bool] = Field(nullable=False, default=True, sa_type=BOOLEAN)
    recorded_at: datetime = Field(..., nullable=False, sa_type=TIMESTAMP)