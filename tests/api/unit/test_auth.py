import pytest

from app.controllers.auth import JWTTokenFlow
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
        breakpoint()
        assert token.data["expires"]

