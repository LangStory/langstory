from typing import TYPE_CHECKING, Optional, Generator
from uuid import UUID
from datetime import datetime, timezone, timedelta
import jwt
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.logger import get_logger
from app.settings import settings
from app.models.user import User
from app.schemas.user_schemas import ScopedUser
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
        assert decoded["exp"] > datetime.now(timezone.utc).timestamp(), "token is expired"
        try:
            user = User.read(self.db_session, id_=decoded["sub"])
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
            org_data = {
                "id": sql_org.id,
                "name": sql_org.name,
            }
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
        user_data = {
            "id": user.id,
            "email_address": user.email_address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar_url": user.avatar_url,
            "organizations": [o.id for o in user.organizations],
        }
        data = {
            "sub": user.id,
            "org": org_data,
            "exp": expire,
            "user": user_data,
        }
        token = jwt.encode(data.copy(), settings.jwt_secret_key, algorithm=self.algorithm)
        return JWTResponse(token=token, data=data)

    def get_scoped_user(cls, token: str) -> ScopedUser:
        """get a user object from a token"""
        decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[cls.algorithm])
        user_uid = UUID(decoded["sub"].split("user-")[1])
        org = None
        if decoded["org"]:
            org_uid = UUID(decoded["org"].split("org-")[1])
            org = Organization(uid=org_uid, name=decoded["org"])
        return ScopedUser(
            user=User(uid=user_uid, email_address=decoded["user"]["email_address"]),
            organization=org,
        )