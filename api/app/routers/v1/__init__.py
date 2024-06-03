from app.routers.v1.auth.username_password import router as username_password_router
from app.routers.v1.auth.token import router as token_router
from app.routers.v1.auth.magic_link import router as magic_link_router
from app.routers.v1.me import router as me_router
from app.routers.v1.chats import router as chat_router
from app.routers.v1.projects import router as project_router
from app.routers.v1.users import router as user_router
from app.routers.v1.tools import router as tool_router
from app.routers.v1.threads import router as thread_router

ROUTERS = [
    magic_link_router,
    username_password_router,
    me_router,
    chat_router,
    project_router,
    token_router,
    user_router,
    tool_router,
    thread_router,
]
