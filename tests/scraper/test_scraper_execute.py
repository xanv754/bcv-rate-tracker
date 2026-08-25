from collections.abc import Callable

import pytest

from scraper.__main__ import BCVScraper, ScraperFailure, ScraperResponse
from scraper.client import ResponseModel
from scraper.constants import ScraperCurrencyId
from utils.errors import BCVConnectionError


class TestBCVScraperExecuteSuccess:
    def test_returns_scraper_response_with_parsed_rates(
        self, monkeypatch: pytest.MonkeyPatch, build_bcv_html: Callable[..., str]
    ) -> None:
        html = build_bcv_html()
        monkeypatch.setattr(
            "scraper.__main__.BCVClient.get_html",
            staticmethod(
                lambda: ResponseModel(status_code=200, content=html, url="https://example.test")
            ),
        )

        result = BCVScraper.execute()

        assert isinstance(result, ScraperResponse)
        assert set(result.rates.keys()) == set(ScraperCurrencyId)
        assert result.info.url == "https://example.test"


class TestBCVScraperExecuteFailure:
    def test_returns_scraper_failure_when_client_raises_scraper_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _raise_connection_error() -> ResponseModel:
            raise BCVConnectionError("network down")

        monkeypatch.setattr(
            "scraper.__main__.BCVClient.get_html", staticmethod(_raise_connection_error)
        )

        result = BCVScraper.execute()

        assert isinstance(result, ScraperFailure)
        assert result.error_message == "network down"

    def test_returns_scraper_failure_when_parsing_fails(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "scraper.__main__.BCVClient.get_html",
            staticmethod(
                lambda: ResponseModel(
                    status_code=200, content="<html><head></head></html>", url="https://example.test"
                )
            ),
        )

        result = BCVScraper.execute()

        assert isinstance(result, ScraperFailure)
        assert result.error_message
