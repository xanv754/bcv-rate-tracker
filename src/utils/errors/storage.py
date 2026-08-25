from utils.errors.base import AppError


class StorageError(AppError):
    """Base exception for errors raised while persisting BCV data to PostgreSQL."""


class DatabaseConfigError(StorageError):
    """Raised when a required database environment variable is missing."""


class DatabaseConnectionError(StorageError):
    """Raised when the PostgreSQL database cannot be reached."""


class DatabasePersistError(StorageError):
    """Raised when a scrape run or exchange rate fails to persist."""
