from pydantic_settings import BaseSettings, Field

class Settings(BaseSettings):
    google_oauth_client_id: str
    google_oauth_client_secret: str
    canonical_url: str
    validate_user_email: bool = Field(default=False, description="If True user must validate their email address before they can login. This requires an email provider credentials")
    single_tenant: bool = Field(default=False, description="If True, only one organization will exist and all users will be granted access to that organization.")
    allow_new_users: bool = Field(default=True, description="If False, new users will not be able to sign up.")

settings = Settings()