from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "developemnt"
    COOKIE_SECURE: bool = False

    POSTGRES_URL: str | None = None

    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None

    QDRANT_API_KEY: str | None = None
    QDRANT_CLUSTER_ENDPOINT: str | None = None

    # somehow mailjet does not want None
    MAILJET_API_KEY: str
    MAILJET_SECRET_KEY: str
    MAILJET_SENDER_EMAIL: str

    SECRET_KEY: str

    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int

    EMAIL_VERIFICATION_TOKEN_TTL_MINUTES: int

    CLIENT_URL: str

    model_config = {"env_file": ".env"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
