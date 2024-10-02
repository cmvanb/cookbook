import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = 'cookbook'
    DATABASE_PATH: str = ''
    API_PREFIX: str = '/api'

settings = Settings()
