from enum import Enum

from scraper import ScraperCurrencyId


class Currency(str, Enum):
    """ISO 4217 currency codes expected by the exchange_rates schema."""

    EURO = "EUR"
    DOLLAR = "USD"
    YUAN = "CNY"
    LIRA = "TRY"
    RUBLO = "RUB"


class ScrapeRunStatus(str, Enum):
    """Outcome of a scrape run, as stored in the scrape_runs schema."""

    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"


SCRAPER_ID_TO_CURRENCY: dict[ScraperCurrencyId, Currency] = {
    ScraperCurrencyId.EURO: Currency.EURO,
    ScraperCurrencyId.DOLLAR: Currency.DOLLAR,
    ScraperCurrencyId.YUAN: Currency.YUAN,
    ScraperCurrencyId.LIRA: Currency.LIRA,
    ScraperCurrencyId.RUBLO: Currency.RUBLO,
}
