from utils.errors.base import AppError


class ScraperError(AppError):
    """Base exception for errors raised while scraping BCV exchange rates."""


class BCVConnectionError(ScraperError):
    """Raised when the BCV site cannot be reached (network or timeout failure)."""


class BCVResponseError(ScraperError):
    """Raised when the BCV site responds with an HTTP error status."""

    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


class BCVParsingError(ScraperError):
    """Base exception for errors while parsing the BCV rates HTML page."""


class RateSectionNotFoundError(BCVParsingError):
    """Raised when an expected HTML section is missing, signaling the BCV page structure changed."""


class OfficialDateNotFoundError(BCVParsingError):
    """Raised when the official date cannot be found or parsed in the HTML."""


class RateValueNotFoundError(BCVParsingError):
    """Raised when a specific currency's rate value cannot be found or parsed."""

    def __init__(self, message: str, currency: str) -> None:
        super().__init__(message)
        self.currency = currency
