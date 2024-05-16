from fastapi import Request, APIRouter
from fastapi_sso.sso.google import GoogleSSO

from app.settings import settings

router = APIRouter(prefix="/google", tags=["auth"])

google_sso = GoogleSSO(
    settings.google_oauth_client_id,
    settings.google_oauth_client_secret,
    settings.canonical_url + "/google/callback")

@router.get("/login")
async def google_login():
    with google_sso:
        return await google_sso.get_login_redirect()

@router.get("/callback")
async def google_callback(request: Request):
    with google_sso:
        google_user = await google_sso.verify_and_process(request)
    # find langstory user from google user
    # jwt auth