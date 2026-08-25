"""Shared fixtures for the BCV Scraper test suite."""
from collections.abc import Callable

import pytest

_PAGE_TEMPLATE = "<html><body>{body}</body></html>"
_CURRENCY_BLOCK_TEMPLATE = '<div id="{id}"><span>{name}</span><strong>{value}</strong></div>'

_DEFAULT_CURRENCIES: dict[str, tuple[str, str]] = {
    "dolar": ("USD", "203,50000000"),
    "euro": ("EUR", "236,12345678"),
    "yuan": ("CNY", "28,30000000"),
    "lira": ("TRY", "5,90000000"),
    "rublo": ("RUB", "2,45000000"),
}


@pytest.fixture()
def build_bcv_html() -> Callable[..., str]:
    """Factory that assembles a minimal BCV rates page, matching the real site markup.

    Kept as a builder (rather than a fixed constant) so scraper/parser tests can each
    ask for only the currencies or date they need without duplicating the page markup.
    """

    def _build(
        official_date_content: str = "2026-08-24T00:00:00-04:00",
        currencies: dict[str, tuple[str, str]] | None = None,
    ) -> str:
        selected = _DEFAULT_CURRENCIES if currencies is None else currencies
        blocks = "".join(
            _CURRENCY_BLOCK_TEMPLATE.format(id=currency_id, name=name, value=value)
            for currency_id, (name, value) in selected.items()
        )
        body = (
            '<div class="main-container container">'
            '<div class="region region-services">'
            '<div class="view-content">'
            f'<span class="date-display-single" content="{official_date_content}">24/08/2026</span>'
            f"{blocks}"
            "</div></div></div>"
        )
        return _PAGE_TEMPLATE.format(body=body)

    return _build
