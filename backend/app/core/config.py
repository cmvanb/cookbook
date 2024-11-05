import secrets
from typing import Annotated, Any

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith('['):
        return [i.strip() for i in v.split(',')]
    elif isinstance(v, list | str):
        return v

    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    API_PREFIX: str = '/api'

    SECRET_KEY: str = secrets.token_urlsafe(32)

    # NOTE: 7 days in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    FRONTEND_HOST: str = 'http://localhost:3000'

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip('/') for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str = 'cookbook'

    DATABASE_PATH: str = ''

    FIRST_SUPERUSER_EMAIL: str = ''

    FIRST_SUPERUSER_PASSWORD: str = ''

settings = Settings()
