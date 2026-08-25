import os

from dotenv import load_dotenv
from sqlalchemy import URL

from utils.env.constants import (
    DATABASE_DRIVERNAME,
    DB_HOST_ENV_VAR,
    DB_NAME_ENV_VAR,
    DB_PASSWORD_ENV_VAR,
    DB_PORT_ENV_VAR,
    DB_SSLMODE_ENV_VAR,
    DB_USER_ENV_VAR,
    DEFAULT_DB_HOST,
    DEFAULT_DB_PORT,
)
from utils.errors import DatabaseConfigError

load_dotenv()


class DatabaseConfig:
    """Reads PostgreSQL connection settings from environment variables."""

    @staticmethod
    def _require(env_var: str) -> str:
        value = os.getenv(env_var)
        if not value:
            raise DatabaseConfigError(f"Missing required environment variable: {env_var}")
        return value

    @staticmethod
    def host() -> str:
        return os.getenv(DB_HOST_ENV_VAR, DEFAULT_DB_HOST)

    @staticmethod
    def port() -> int:
        return int(os.getenv(DB_PORT_ENV_VAR, DEFAULT_DB_PORT))

    @staticmethod
    def name() -> str:
        return DatabaseConfig._require(DB_NAME_ENV_VAR)

    @staticmethod
    def user() -> str:
        return DatabaseConfig._require(DB_USER_ENV_VAR)

    @staticmethod
    def password() -> str:
        return DatabaseConfig._require(DB_PASSWORD_ENV_VAR)

    @staticmethod
    def sslmode() -> str | None:
        return os.getenv(DB_SSLMODE_ENV_VAR)

    @staticmethod
    def url() -> URL:
        """Build the SQLAlchemy connection URL from the configured environment variables."""
        sslmode = DatabaseConfig.sslmode()
        return URL.create(
            drivername=DATABASE_DRIVERNAME,
            username=DatabaseConfig.user(),
            password=DatabaseConfig.password(),
            host=DatabaseConfig.host(),
            port=DatabaseConfig.port(),
            database=DatabaseConfig.name(),
            query={"sslmode": sslmode} if sslmode else {},
        )
