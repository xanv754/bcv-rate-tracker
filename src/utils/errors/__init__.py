from utils.errors.base import AppError
from utils.errors.scraper import (
    ScraperError,
    BCVConnectionError,
    BCVResponseError,
    BCVParsingError,
    RateSectionNotFoundError,
    OfficialDateNotFoundError,
    RateValueNotFoundError,
)
from utils.errors.storage import (
    StorageError,
    DatabaseConfigError,
    DatabaseConnectionError,
    DatabasePersistError,
)

__all__ = [
    "AppError",
    "ScraperError",
    "BCVConnectionError",
    "BCVResponseError",
    "BCVParsingError",
    "RateSectionNotFoundError",
    "OfficialDateNotFoundError",
    "RateValueNotFoundError",
    "StorageError",
    "DatabaseConfigError",
    "DatabaseConnectionError",
    "DatabasePersistError",
]
