from fastapi import APIRouter

router = APIRouter(prefix="/jwt", tags=["auth"])

@router.get("/refresh")
async def refresh_jwt_token():
    """Creates a short-lived identity token from a valid refresh token."""
    raise NotImplementedError
