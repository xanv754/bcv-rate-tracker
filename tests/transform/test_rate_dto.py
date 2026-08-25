from datetime import date, datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from transform.constants import Currency
from transform.models import ExchangeRateDTO

_NOW = datetime.now(timezone.utc)
_DATE = date(2026, 8, 24)


class TestExchangeRateDTO:
    def test_accepts_valid_fields(self) -> None:
        dto = ExchangeRateDTO(
            currency=Currency.DOLLAR,
            rate=Decimal("203.50000000"),
            official_date=_DATE,
            scraped_at=_NOW,
        )

        assert dto.currency == Currency.DOLLAR
        assert dto.rate == Decimal("203.50000000")
        assert dto.official_date == _DATE
        assert dto.scraped_at == _NOW

    def test_accepts_currency_as_iso_code_string(self) -> None:
        dto = ExchangeRateDTO(
            currency="EUR", rate=Decimal("236.00"), official_date=_DATE, scraped_at=_NOW
        )

        assert dto.currency == Currency.EURO

    def test_rejects_unknown_currency_code(self) -> None:
        with pytest.raises(ValidationError):
            ExchangeRateDTO(currency="XXX", rate=Decimal("1"), official_date=_DATE, scraped_at=_NOW)

    def test_rejects_non_numeric_rate(self) -> None:
        with pytest.raises(ValidationError):
            ExchangeRateDTO(
                currency=Currency.DOLLAR,
                rate="not-a-number",
                official_date=_DATE,
                scraped_at=_NOW,
            )

    def test_rejects_missing_official_date(self) -> None:
        with pytest.raises(ValidationError):
            ExchangeRateDTO(currency=Currency.DOLLAR, rate=Decimal("1"), scraped_at=_NOW)
