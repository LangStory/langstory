import pytest
from uuid import UUID
from datetime import datetime, timezone, timedelta
from jwt.exceptions import ExpiredSignatureError

from app.controllers.auth import JWTTokenFlow
from app.schemas.jtw_schema import JWTBase
from app.models.user import User

class TestAuth:

    @pytest.fixture
    def setup_state(self, db_session):
        user = User(
            username="test_user",
            email="email@email.com",)
        return user.create(db_session), db_session

    def test_refresh_jwt(self, setup_state):
        user, db_session  = setup_state
        flow = JWTTokenFlow(db_session)
        token = flow.get_refresh_token(user)
        assert token.data["exp"] > datetime.now(timezone.utc)
        assert token.data["sub"] == user.id

    def test_auth_jwt(self, setup_state):
        _, db_session  = setup_state
        flow = JWTTokenFlow(db_session)

        fixed_user = User(uid=UUID('11d52aeb-0dc3-4a90-a8b8-27b061c49920'), email="stubbed_email@email.test").create(db_session)
        fixed_refresh_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                               "eyJzdWIiOiJ1c2VyLTExZDUyYWViLTBkYzMtNG"
                               "E5MC1hOGI4LTI3YjA2MWM0OTkyMCIsImV4cCI6M"
                               "Tc0ODAzOTUyNn0.Sdo9nueYQYb-CPfqz8GAwrf0y9ngM0"
                               "_qbcCGw-_IHfo")
        token = flow.get_auth_token(JWTBase(token=fixed_refresh_token))
        assert token.data["exp"] < datetime.now(timezone.utc) + timedelta(minutes=15)
        assert token.data["sub"] == fixed_user.id
        assert token.data["user"]["email_address"] == fixed_user.email_address
        assert token.data["user"]["id"] == token.data["sub"]
        assert not token.data["org"]

    def test_auth_jwt_fails_expired(self, setup_state):
        _, db_session  = setup_state
        flow = JWTTokenFlow(db_session)
        fixed_user = User(uid=UUID('11d52aeb-0dc3-4a90-a8b8-27b061c49920'), email="stubbed_email@email.test").create(db_session)
        expired_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                         "eyJzdWIiOiJ1c2VyLTExZDUyYWViLTBkYzMtNG"
                         "E5MC1hOGI4LTI3YjA2MWM0OTkyMCIsImV4cCI6"
                         "MTcxNjQxODI3OH0.XadUn9x4rbYCuv7gVNGrSE"
                         "fPZSnUH1gMZz6caCILdXw")
        with pytest.raises(ExpiredSignatureError):
            flow.get_auth_token(JWTBase(token=expired_token))