from typing import TYPE_CHECKING, Optional, Generator
from datetime import datetime, timezone, timedelta
import jwt
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.logger import get_logger
from app.settings import settings
from app.models.user import User
from app.models.organization import Organization
from app.schemas.jtw_schema import JWTBase, JWTResponse
from app.http_errors import forbidden, unauthorized

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = get_logger(__name__)


class AuthBase:
    """common utilites for auth"""

    db_session: "Generator[Session, None, None]"

    def __init__(self, db_session: "Generator[Session, None, None]"):
        self.db_session = db_session

    @classmethod
    def standardized_email(cls, email: str) -> str:
        return email.strip().lower()


class CreateUserFlow(AuthBase):
    """create a new user"""

    def create_with_email_password(self, email_address: str, password: str) -> User:
        """standard old-school u/p"""

    def create_with_email_sso(self, email_address: str) -> User:
        """create using 3rd party auth"""

    def _create_user(self, email_address: str, password: Optional[str] = None) -> User:
        """underlying mechanics to create a user"""


class JWTTokenFlow(AuthBase):
    algorithm: str = "HS256"

    def get_refresh_token(self, user: User) -> "JWTResponse":
        """generates a bare refresh token for a given user"""
        logger.debug("generating refresh token for %s", user.email_address)
        expire = datetime.now(timezone.utc) + timedelta(days=365)
        data = {"sub": user.id, "exp": expire}
        token = jwt.encode(
            data.copy(), settings.jwt_secret_key, algorithm=self.algorithm
        )
        logger.debug(
            "refresh token for %s created, expires %s", user.email_address, expire
        )
        return JWTResponse(token=token, data=data)

    def get_auth_token(
            self, refresh_token: "JWTBase", org: Optional["str"] = None
    ) -> "JWTResponse":
        """generate a detailed token and readable data for a given user and org"""
        decoded = jwt.decode(
            refresh_token.token, settings.jwt_secret_key, algorithms=[self.algorithm]
        )
        try:
            user = User.read(id_=decoded.sub)
        except (MultipleResultsFound, NoResultFound, ValueError) as e:
            unauthorized(e=e, message="User not found")
        org_data = {}
        if org:
            sql_org = Organization.read(self.db_session, uid=org)
            try:
                assert (
                        org in user.organizations
                ), f"User {user.uid} is not a member of org {org}"
            except AssertionError as e:
                forbidden(
                    e=e,
                    message="User does not belong to this organization or it does not exist",
                )
            org_data = sql_org.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
        user_data = user.model_dump()
        breakpoint()
