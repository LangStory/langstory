from typing import Optional
from uuid import UUID
from sqlalchemy import UUID as SQLUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MalformedIdError(Exception):
    pass


def _relation_getter(instance: "Base", prop: str, prefix: str) -> Optional[str]:
    if not getattr(instance, prop):
        return None
    # TODO: should be able to get this from the Mapped typing, not sure how though
    # prefix = getattr(?, "prefix")
    formatted_prop = f"_{prop}_id"
    uuid_ = getattr(instance, formatted_prop)
    return f"{prefix}-{uuid_}"


def _relation_setter(instance: "Base", prop: str, prefix: str, value: str) -> None:
    formatted_prop = f"_{prop}_id"
    if not value:
        setattr(instance, formatted_prop, None)
        return
    try:
        found_prefix, id_ = value.split("_")
    except ValueError as e:
        raise MalformedIdError(f"{value} is not a valid ID.") from e
    assert (
        # TODO: should be able to get this from the Mapped typing, not sure how though
        # prefix = getattr(?, "prefix")
        found_prefix
        == prefix
    ), f"{found_prefix} is not a valid id prefix, expecting {prefix}"
    try:
        setattr(instance, formatted_prop, UUID(id_))
    except ValueError as e:
        raise MalformedIdError("Hash segment of {value} is not a valid UUID") from e


class OrganizationMixin(Base):
    """Mixin for models that belong to an organization."""

    __abstract__ = True

    _organization_id: Mapped[UUID] = mapped_column(
        SQLUUID(), ForeignKey("organization._id")
    )

    @property
    def organization_id(self) -> str:
        return _relation_getter(self, "organization", "org")

    @organization_id.setter
    def organization_id(self, value: str) -> None:
        return _relation_setter(self, "organization", "org", value)


class ReceivingTaskMixin(Base):
    """Mixin for models that belong to a receiving task."""

    __abstract__ = True

    _receiving_task_id: Mapped[UUID] = mapped_column(
        SQLUUID(), ForeignKey("receiving_task._id")
    )

    @property
    def receiving_task_id(self) -> str:
        return _relation_getter(self, "receiving_task", "rt")

    @receiving_task_id.setter
    def receiving_task_id(self, value: str) -> None:
        return _relation_setter(self, "receiving_task", "rt", value)


class ReceivingTaskItemMixin(Base):
    """1:1 mixin for intentory and pick items"""

    __abstract__ = True

    _receiving_task_item_id: Mapped[UUID] = mapped_column(
        SQLUUID(), ForeignKey("receiving_task_item._id")
    )

    @property
    def receiving_task_item_id(self) -> str:
        return _relation_getter(self, "receiving_task_item", "rti")

    @receiving_task_item_id.setter
    def receiving_task_item_id(self, value: str) -> None:
        return _relation_setter(self, "receiving_task_item", "rti", value)


class VendorMixin(Base):
    """1:1 mixin for Vendors"""

    __abstract__ = True

    _vendor_id: Mapped[UUID] = mapped_column(SQLUUID(), ForeignKey("vendor._id"))

    @property
    def vendor_id(self) -> str:
        return _relation_getter(self, "vendor", "vnd")

    @vendor_id.setter
    def vendor_id(self, value: str) -> None:
        return _relation_setter(self, "vendor", "vnd", value)


class PurchaseOrderMixin(Base):
    """1:1 mixin for PurchaseOrders"""

    __abstract__ = True

    _purchase_order_id: Mapped[UUID] = mapped_column(
        SQLUUID(), ForeignKey("purchase_order._id")
    )

    @property
    def purchase_order_id(self) -> str:
        return _relation_getter(self, "purchase_order", "po")

    @purchase_order_id.setter
    def purchase_order_id(self, value: str) -> None:
        return _relation_setter(self, "purchase_order", "po", value)


class ProjectMixin(Base):
    """1:1 mixin for Projects"""

    __abstract__ = True

    _project_id: Mapped[UUID] = mapped_column(SQLUUID(), ForeignKey("project._id"))

    @property
    def project_id(self) -> str:
        return _relation_getter(self, "project", "proj")

    @project_id.setter
    def project_id(self, value: str) -> None:
        return _relation_setter(self, "project", "proj", value)
