from datetime import date
from decimal import Decimal

import pytest

from scraper.__main__ import RateInfoModel, ScraperFailure, ScraperResponse
from scraper.constants import ScraperCurrencyId
from transform.__main__ import BCVTransformer
from transform.constants import Currency, ScrapeRunStatus

_DATE = date(2026, 8, 24)


class TestBCVTransformerExecuteSuccess:
    def test_builds_rate_dtos_and_a_successful_scrape_run(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        scraper_response = ScraperResponse(
            rates={
                ScraperCurrencyId.DOLLAR: ("USD", Decimal("203.50000000"), _DATE),
                ScraperCurrencyId.EURO: ("EUR", Decimal("236.00000000"), _DATE),
            },
            info=RateInfoModel(snapshot="<div>snap</div>", url="https://bcv.example/rates"),
        )
        monkeypatch.setattr(
            "transform.__main__.BCVScraper.execute", staticmethod(lambda: scraper_response)
        )

        result = BCVTransformer.execute()

        assert result.scrape_run.status == ScrapeRunStatus.SUCCESS
        assert result.scrape_run.source_url == "https://bcv.example/rates"
        assert result.scrape_run.raw_html_snapshot == "<div>snap</div>"
        assert result.scrape_run.error_message is None
        assert {rate.currency for rate in result.rates} == {Currency.DOLLAR, Currency.EURO}

        dollar_rate = next(rate for rate in result.rates if rate.currency == Currency.DOLLAR)
        assert dollar_rate.rate == Decimal("203.50000000")
        assert dollar_rate.official_date == _DATE
        assert dollar_rate.scraped_at == result.scrape_run.finished_at


class TestBCVTransformerExecuteFailure:
    def test_returns_empty_rates_and_a_failed_scrape_run(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "transform.__main__.BCVScraper.execute",
            staticmethod(lambda: ScraperFailure(error_message="site unreachable")),
        )

        result = BCVTransformer.execute()

        assert result.rates == []
        assert result.scrape_run.status == ScrapeRunStatus.FAILED
        assert result.scrape_run.error_message == "site unreachable"
        assert result.scrape_run.source_url is None
        assert result.scrape_run.raw_html_snapshot is None
