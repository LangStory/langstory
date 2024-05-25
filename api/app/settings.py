from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    google_oauth_client_id: Optional[str] = None
    google_oauth_client_secret: Optional[str] = None
    organization_name: Optional[str] = "LangStory"
    canonical_url: str
    validate_user_email: bool = Field(
        default=False,
        description="If True user must validate their email address before they can login. This requires an email provider credentials",
    )
    allow_new_users: bool = Field(
        default=True, description="If False, new users will not be able to sign up."
    )

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    jwt_secret_key: str
    smtp_email_host: Optional[str] = None
    smtp_email_port: Optional[int] = None
    smtp_email_user: Optional[str] = None
    smtp_email_password: Optional[str] = None



settings = Settings()
