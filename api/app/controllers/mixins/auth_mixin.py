from typing import Generator, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from sqlalchemy.orm import Session



class AuthMixin:

    """common utilites for auth"""

    db_session: "Generator[Session, None, None]"

    def __init__(self, db_session: "Generator[Session, None, None]"):
        self.db_session = db_session

    @classmethod
    def standardized_email(cls, email: str) -> str:
        return email.strip().lower()

    @classmethod
    def get_org_uid(cls, org: str) -> str:
        return UUID(org.split("organization-")[1])