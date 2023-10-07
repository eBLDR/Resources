"""
Config file.
"""
import datetime
import os

from pydantic import BaseSettings

ALL_ENVS = [
    "local",
    "development",
    "staging",
    "production",
]


def get_environment():
    """Gets current environment name.
    :return: environment name
    :rtype: str
    """
    environment = os.getenv("ENVIRONMENT", "local").lower()
    if environment not in ALL_ENVS:
        raise EnvironmentError(f"Unknown environment: {environment}")
    return environment


ENVIRONMENT = get_environment()


class Settings(BaseSettings):
    """Environment variables."""
    ENVIRONMENT: str = ENVIRONMENT
    TESTING: bool = os.getenv("TESTING", False)
    SECRET_KEY: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int

    LOGS_PATH: str

    @property
    def LOGS_FILENAME(self):
        filename = f"{str(datetime.datetime.utcnow().date()).replace('-', '')}.log"
        return os.path.join(self.LOGS_PATH, filename)

    APP_NAME: str
    APP_PROTOCOL: str
    APP_HOST: str
    APP_PORT: str

    @property
    def APP_URL(self):
        return f"{self.APP_PROTOCOL}{self.APP_HOST}:{self.APP_PORT}"

    API_V1_STR: str

    @property
    def API_V1_URL(self):
        return f"{self.APP_URL}{self.API_V1_STR}"

    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int
    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DB_NAME: str

    @property
    def POSTGRESQL_URI(self):
        return f"postgresql+asyncpg://{self.POSTGRESQL_USERNAME}:{self.POSTGRESQL_PASSWORD}@{self.POSTGRESQL_HOST}/{self.POSTGRESQL_DB_NAME}"

    class Config:
        env_file = f"{ENVIRONMENT}.env"


def load_settings():
    """Load app setting (environment variables).
    :return: app setting
    :rtype: Settings
    """
    settings_ = Settings()
    if settings_.TESTING:
        settings_.POSTGRESQL_DB_NAME = f"test_{settings_.POSTGRESQL_DB_NAME}"
    return settings_


settings = load_settings()
