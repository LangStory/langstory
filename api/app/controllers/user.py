"""Business logic for user related operations."""
from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from app.settings import settings
from app.controllers.mixins.auth_mixin import AuthMixin
from app.controllers.mixins.password_mixin import PasswordMixin
from app.http_errors import bad_request
from app.models.organization import Organization
from app.models.user import User

if TYPE_CHECKING:
    from app.schemas.user_schemas import NewUser


class CreateNewUserFlow(AuthMixin, PasswordMixin):
    """create a new user"""

    def add_user_to_default_org(self, user: User) -> User:
        org = Organization.default(self.db_session)
        self.db_session.add(user)
        user.organizations.append(org)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def create_user_with_username_password(self, user: "NewUser") -> User:
        """create a new user"""
        if not settings.allow_new_users:
            bad_request(message="Adding new users has been disabled, contact your administrator")
        if not user.password or len(user.password) < 8:
            bad_request(message="Password must be at least 8 characters long")

        user.email_address = self.standardized_email(user.email_address)
        user.password = self.password_context.hash(user.password)
        try:
            user = User(**user.model_dump(exclude_none=True)).create(self.db_session)
            user = self.add_user_to_default_org(user)
            return user
        except IntegrityError as e:
            self.db_session.rollback()
            bad_request(e=e, message="User already exists")
