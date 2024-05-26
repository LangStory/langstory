import pytest
from datetime import datetime, timezone
from httpx import AsyncClient
from app.settings import settings


class TestUsers:

    @pytest.fixture
    def setup_client(self, override_app):
        client = AsyncClient(
            app=override_app,
            follow_redirects=True,
            base_url="http://test/auth/username-password/sign-up",
        )
        args = {
            "firstName": "John",
            "lastName": "tavares",
            "emailAddress": "emalie@mail.em",
            "password": "passwordof8",
        }
        yield client, args

    async def test_new_user(self, setup_client):
        client, args = setup_client
        old_allow_new_users = settings.allow_new_users
        try:
            settings.allow_new_users = True
            response = await client.post("", json=args)
            assert response.status_code == 200
            data = response.json()
            assert "token" in data
            assert "sub" in data["data"]
            assert datetime.fromisoformat(data["data"]["exp"]) > datetime.now(
                timezone.utc
            )
        finally:
            settings.allow_new_users = old_allow_new_users

    async def test_new_user_not_allowed(self, setup_client):
        client, args = setup_client
        old_allow_new_users = settings.allow_new_users
        try:
            settings.allow_new_users = False
            response = await client.post("", json=args)
            assert response.status_code == 400
            assert response.json() == {
                "detail": {
                    "message": "Adding new users has been disabled, contact your administrator"
                }
            }
        finally:
            settings.allow_new_users = old_allow_new_users
