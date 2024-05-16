from app.routers.v1.organizations import router as organizations_router
from app.routers.v1.auth.google import router as google_auth_router
from app.routers.v1.auth.username_password import router as username_password_router
from app.routers.v1.auth.jwt import router as jwt_router

ROUTERS = [
    organizations_router,
    google_auth_router,
    username_password_router,
    jwt_router,
]