from uuid import UUID
from app.controllers.mixins.database_mixin import DatabaseMixin


class AuthMixin(DatabaseMixin):
    """common utilites for auth"""

    @classmethod
    def standardized_email(cls, email: str) -> str:
        return email.strip().lower()

    @classmethod
    def get_org_uid(cls, org: str) -> str:
        return UUID(org.split("organization-")[1])
