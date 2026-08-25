from collections.abc import Callable
from datetime import date
from decimal import Decimal

import pytest

from scraper.constants import ScraperCurrencyId
from scraper.parser import BCVParser
from utils.errors import OfficialDateNotFoundError, RateSectionNotFoundError


def _wrap_body(body_inner: str) -> str:
    return f"<html><body>{body_inner}</body></html>"


class TestBCVParserGetRateSection:
    def test_raises_when_body_tag_missing(self) -> None:
        parser = BCVParser("<html><head></head></html>")

        with pytest.raises(RateSectionNotFoundError):
            parser.get_rate_section()

    def test_raises_when_main_container_missing(self) -> None:
        parser = BCVParser(_wrap_body("<div>no main container here</div>"))

        with pytest.raises(RateSectionNotFoundError):
            parser.get_rate_section()

    def test_raises_when_info_general_section_missing(self) -> None:
        parser = BCVParser(_wrap_body('<div class="main-container container"></div>'))

        with pytest.raises(RateSectionNotFoundError):
            parser.get_rate_section()

    def test_raises_when_rate_section_missing(self) -> None:
        html = _wrap_body(
            '<div class="main-container container">'
            '<div class="region region-services"></div>'
            "</div>"
        )

        with pytest.raises(RateSectionNotFoundError):
            BCVParser(html).get_rate_section()

    def test_returns_rate_section_tag_when_present(
        self, build_bcv_html: Callable[..., str]
    ) -> None:
        parser = BCVParser(build_bcv_html())

        section = parser.get_rate_section()

        assert section["class"] == ["view-content"]


class TestBCVParserProcess:
    def test_parses_all_present_currencies(self, build_bcv_html: Callable[..., str]) -> None:
        parser = BCVParser(build_bcv_html())

        rates = parser.process()

        assert set(rates.keys()) == set(ScraperCurrencyId)
        name, value, official_date = rates[ScraperCurrencyId.DOLLAR]
        assert name == "USD"
        assert value == Decimal("203.50000000")
        assert official_date == date(2026, 8, 24)

    def test_skips_currencies_missing_from_the_page(
        self, build_bcv_html: Callable[..., str]
    ) -> None:
        html = build_bcv_html(currencies={"dolar": ("USD", "203,50000000")})

        rates = BCVParser(html).process()

        assert set(rates.keys()) == {ScraperCurrencyId.DOLLAR}

    def test_skips_currency_with_unparseable_rate_value(
        self, build_bcv_html: Callable[..., str]
    ) -> None:
        html = build_bcv_html(currencies={"dolar": ("USD", "not-a-number")})

        rates = BCVParser(html).process()

        assert ScraperCurrencyId.DOLLAR not in rates

    def test_raises_when_official_date_tag_missing(self) -> None:
        html = _wrap_body(
            '<div class="main-container container">'
            '<div class="region region-services">'
            '<div class="view-content">'
            '<div id="dolar"><span>USD</span><strong>203,50</strong></div>'
            "</div></div></div>"
        )

        with pytest.raises(OfficialDateNotFoundError):
            BCVParser(html).process()

    def test_raises_when_official_date_is_unparseable(
        self, build_bcv_html: Callable[..., str]
    ) -> None:
        html = build_bcv_html(official_date_content="not-a-date")

        with pytest.raises(OfficialDateNotFoundError):
            BCVParser(html).process()
