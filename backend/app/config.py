from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field("sqlite+aiosqlite:///./fittrack.db", env="DATABASE_URL")
    secret_key: str = Field("change-this-secret", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    google_client_id: str = Field("", env="GOOGLE_CLIENT_ID")

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
