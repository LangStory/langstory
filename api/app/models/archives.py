from datetime import datetime
from uuid import UUID

from sqlalchemy import Integer, UUID as SQLUUID, BOOLEAN
from sqlalchemy.dialects.postgresql import JSONB, TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AbsoluteBase


class Archives(AbsoluteBase):
    """Reflection of table created manually by migration"""

    __tablename__ = "archives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    table_name: Mapped[str] = mapped_column(TEXT, nullable=False)
    record_type: Mapped[str] = mapped_column(TEXT, nullable=False)
    record_id: Mapped[UUID] = mapped_column(SQLUUID, nullable=False)
    operation: Mapped[str] = mapped_column(TEXT, nullable=False)
    old_values: Mapped[dict] = mapped_column(JSONB, nullable=True)
    new_values: Mapped[dict] = mapped_column(JSONB, nullable=True)
    most_recent: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=True)
    recorded_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
