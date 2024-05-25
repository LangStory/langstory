# from app.routers.v1.auth.google import router as google_auth_router
from app.routers.v1.auth.username_password import router as username_password_router
from app.routers.v1.auth.token import router as token_router
from app.routers.v1.chats import router as chat_router
from app.routers.v1.projects import router as project_router

ROUTERS = [
    #    google_auth_router,
    username_password_router,
    chat_router,
    project_router,
    token_router,
]
