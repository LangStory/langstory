from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from app.controllers.auth import JWTTokenFlow

class TestAuth:

    def test_refresh_jwt(self):


        response = client.get("/v1/auth/username-password/login")
        assert response.status_code == 501
        assert response.json() == {"detail": "Not Implemented"}