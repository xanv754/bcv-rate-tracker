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

__all__ = [
    "AppError",
    "ScraperError",
    "BCVConnectionError",
    "BCVResponseError",
    "BCVParsingError",
    "RateSectionNotFoundError",
    "OfficialDateNotFoundError",
    "RateValueNotFoundError",
]
