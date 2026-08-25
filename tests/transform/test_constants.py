from scraper.constants import ScraperCurrencyId
from transform.constants import SCRAPER_ID_TO_CURRENCY, Currency


class TestScraperIdToCurrencyMapping:
    def test_maps_every_scraper_currency_id(self) -> None:
        assert set(SCRAPER_ID_TO_CURRENCY.keys()) == set(ScraperCurrencyId)

    def test_maps_to_the_expected_iso_currency_codes(self) -> None:
        assert SCRAPER_ID_TO_CURRENCY[ScraperCurrencyId.DOLLAR] == Currency.DOLLAR
        assert SCRAPER_ID_TO_CURRENCY[ScraperCurrencyId.EURO] == Currency.EURO
        assert SCRAPER_ID_TO_CURRENCY[ScraperCurrencyId.YUAN] == Currency.YUAN
        assert SCRAPER_ID_TO_CURRENCY[ScraperCurrencyId.LIRA] == Currency.LIRA
        assert SCRAPER_ID_TO_CURRENCY[ScraperCurrencyId.RUBLO] == Currency.RUBLO
