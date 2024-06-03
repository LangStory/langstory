from datetime import datetime, timezone, timedelta
from typing import Optional

import jwt
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.controllers.mixins.auth_mixin import AuthMixin
from app.controllers.mixins.password_mixin import PasswordMixin
from app.http_errors import forbidden, unauthorized
from app.logger import get_logger
from app.models.organization import Organization
from app.models.user import User
from app.schemas.jtw_schema import JWTBase, JWTResponse
from app.schemas.user_schemas import ScopedUser
from app.settings import settings

logger = get_logger(__name__)


class AuthenticateUsernamePasswordFlow(AuthMixin, PasswordMixin):
    """authenticate the user with username and password"""

    def authenticate(self, email_address: str, password: str) -> User:
        """authenticate the user or raise an exception"""
        try:
            user = User.read(self.db_session, email_address)
            if self.password_context.verify(password, user.password):
                return user
            raise ValueError("password is incorrect")
        except (MultipleResultsFound, NoResultFound, ValueError) as e:
            unauthorized(e=e, message="User not found or password is incorrect")


class JWTTokenFlow(AuthMixin):
    algorithm: str = "HS256"

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[cls.algorithm])

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
        self, refresh_token: "JWTBase", org: Optional["str"] = None, expire_min: Optional[int] = 5
    ) -> "JWTResponse":
        """generate a detailed token and readable data for a given user and org"""
        decoded = jwt.decode(
            refresh_token.token, settings.jwt_secret_key, algorithms=[self.algorithm]
        )
        assert (
            decoded["exp"] > datetime.now(timezone.utc).timestamp()
        ), "token is expired"
        try:
            user = User.read(self.db_session, decoded["sub"])
        except (MultipleResultsFound, NoResultFound, ValueError) as e:
            unauthorized(e=e, message="User not found")
        org_data = {}
        if org:
            org_uid = self.get_org_uid(org)
            sql_org = Organization.read(self.db_session, org_uid)
            try:
                assert (
                    sql_org in user.organizations
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
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_min)
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
        token = jwt.encode(
            data.copy(), settings.jwt_secret_key, algorithm=self.algorithm
        )
        return JWTResponse(token=token, data=data)

    def get_scoped_user(cls, token: str) -> ScopedUser:
        """get a user object from a token"""
        decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[cls.algorithm])
        return ScopedUser.from_jwt(decoded)
