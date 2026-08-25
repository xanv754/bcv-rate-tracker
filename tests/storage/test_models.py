from collections.abc import Iterator
from datetime import date, datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from storage.models import Base, ExchangeRate, ScrapeRun
from transform.constants import Currency, ScrapeRunStatus


@pytest.fixture()
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    db_session = factory()
    yield db_session
    db_session.close()
    engine.dispose()


class TestExchangeRateModel:
    def test_table_name(self) -> None:
        assert ExchangeRate.__tablename__ == "exchange_rates"

    def test_persists_and_reads_back_fields(self, session: Session) -> None:
        scraped_at = datetime.now(timezone.utc)
        session.add(
            ExchangeRate(
                currency=Currency.DOLLAR,
                rate=Decimal("203.50000000"),
                official_date=date(2026, 8, 24),
                scraped_at=scraped_at,
            )
        )
        session.commit()

        stored = session.query(ExchangeRate).one()
        assert stored.currency == Currency.DOLLAR
        assert stored.rate == Decimal("203.50000000")
        assert stored.official_date == date(2026, 8, 24)

    def test_enforces_unique_currency_and_official_date(self, session: Session) -> None:
        kwargs = dict(
            currency=Currency.EURO,
            rate=Decimal("236.00000000"),
            official_date=date(2026, 8, 24),
            scraped_at=datetime.now(timezone.utc),
        )
        session.add(ExchangeRate(**kwargs))
        session.commit()

        session.add(ExchangeRate(**kwargs))
        with pytest.raises(IntegrityError):
            session.commit()


class TestScrapeRunModel:
    def test_table_name(self) -> None:
        assert ScrapeRun.__tablename__ == "scrape_runs"

    def test_persists_with_optional_fields_omitted(self, session: Session) -> None:
        now = datetime.now(timezone.utc)
        session.add(ScrapeRun(started_at=now, finished_at=now, status=ScrapeRunStatus.FAILED))
        session.commit()

        stored = session.query(ScrapeRun).one()
        assert stored.status == ScrapeRunStatus.FAILED
        assert stored.source_url is None
        assert stored.raw_html_snapshot is None
        assert stored.error_message is None

    def test_persists_with_all_fields_set(self, session: Session) -> None:
        now = datetime.now(timezone.utc)
        session.add(
            ScrapeRun(
                started_at=now,
                finished_at=now,
                status=ScrapeRunStatus.SUCCESS,
                source_url="https://www.bcv.org.ve",
                raw_html_snapshot="<div>snap</div>",
                error_message=None,
            )
        )
        session.commit()

        stored = session.query(ScrapeRun).one()
        assert stored.source_url == "https://www.bcv.org.ve"
        assert stored.raw_html_snapshot == "<div>snap</div>"
