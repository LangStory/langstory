from typing import Optional, Type
from uuid import UUID
from sqlalchemy import UUID as SQLUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MalformedIdError(Exception):
    pass


def _relation_getter(instance: "Base", prop: str) -> Optional[str]:
    if not getattr(instance, prop):
        return None
    prefix = prop.replace("_", "")
    formatted_prop = f"_{prop}_uid"
    uuid_ = getattr(instance, formatted_prop)
    return f"{prefix}-{uuid_}"


def _relation_setter(instance: Type["Base"], prop: str, value: str) -> None:
    formatted_prop = f"_{prop}_uid"
    prefix = prop.replace("_", "")
    if not value:
        setattr(instance, formatted_prop, None)
        return
    try:
        found_prefix, id_ = value.split("-", 1)
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

    _organization_uid: Mapped[UUID] = mapped_column(
        SQLUUID(), ForeignKey("organization.uid")
    )

    @property
    def organization_id(self) -> str:
        return _relation_getter(self, "organization")

    @organization_id.setter
    def organization_id(self, value: str) -> None:
        _relation_setter(self, "organization", value)


class ProjectMixin(Base):
    """1:1 mixin for Projects"""

    __abstract__ = True

    _project_uid: Mapped[UUID] = mapped_column(SQLUUID(), ForeignKey("project.uid"))

    @property
    def project_id(self) -> str:
        return _relation_getter(self, "project")

    @project_id.setter
    def project_id(self, value: str) -> None:
        _relation_setter(self, "project", value)


class ToolMixin(Base):
    """1:1 mixin for Tools"""

    __abstract__ = True

    _tool_uid: Mapped[UUID] = mapped_column(SQLUUID(), ForeignKey("tool.uid"))

    @property
    def tool_id(self) -> str:
        return _relation_getter(self, "tool")

    @tool_id.setter
    def tool_id(self, value: str) -> None:
        return _relation_setter(self, "tool", value)


class UserMixin(Base):
    """1:1 mixin for Users"""

    __abstract__ = True

    _user_uid: Mapped[UUID] = mapped_column(SQLUUID(), ForeignKey("user.uid"))

    @property
    def user_id(self) -> str:
        return _relation_getter(self, "user")

    @user_id.setter
    def user_id(self, value: str) -> None:
        _relation_setter(self, "user", value)


class ChatMixin(Base):
    """1:1 mixin for Chats"""

    __abstract__ = True

    _chat_uid: Mapped[UUID] = mapped_column(SQLUUID(), ForeignKey("chat.uid"))

    @property
    def chat_id(self) -> str:
        return _relation_getter(self, "chat")

    @chat_id.setter
    def chat_id(self, value: str) -> None:
        _relation_setter(self, "chat", value)


class ThreadMixin(Base):
    """1:1 mixin for threads"""

    __abstract__ = True

    _thread_uid: Mapped[UUID] = mapped_column(SQLUUID(), ForeignKey("thread.uid"))

    @property
    def thread_id(self) -> str:
        return _relation_getter(self, "thread")

    @thread_id.setter
    def thread_id(self, value: str) -> None:
        _relation_setter(self, "thread", value)
