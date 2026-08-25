from collections.abc import Iterator
from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from storage.__main__ import BCVStorage
from storage.models import Base, ExchangeRate, ScrapeRun
from transform import ExchangeRateDTO, ScrapeRunDTO, TransformResult
from transform.constants import Currency, ScrapeRunStatus
from utils.errors import DatabaseConnectionError, DatabasePersistError

_DATE = date(2026, 8, 24)


class _FakeDatabase:
    """Stands in for storage.database.Database, backed by an in-memory SQLite DB."""

    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def get_session(self):
        return self._session_factory()


@pytest.fixture()
def sqlite_session_factory() -> Iterator[sessionmaker]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine)
    engine.dispose()


def _rate_dto(
    currency: Currency = Currency.DOLLAR,
    rate: str = "203.50000000",
    official_date: date = _DATE,
) -> ExchangeRateDTO:
    return ExchangeRateDTO(
        currency=currency,
        rate=Decimal(rate),
        official_date=official_date,
        scraped_at=datetime.now(timezone.utc),
    )


def _scrape_run_dto(status: ScrapeRunStatus = ScrapeRunStatus.SUCCESS) -> ScrapeRunDTO:
    now = datetime.now(timezone.utc)
    return ScrapeRunDTO(started_at=now, finished_at=now, status=status)


class TestBCVStorageExecutePersistence:
    def test_persists_scrape_run_and_rates(
        self, monkeypatch: pytest.MonkeyPatch, sqlite_session_factory: sessionmaker
    ) -> None:
        monkeypatch.setattr(
            "storage.__main__.Database", lambda: _FakeDatabase(sqlite_session_factory)
        )
        result = TransformResult(rates=[_rate_dto()], scrape_run=_scrape_run_dto())

        BCVStorage.execute(result)

        session = sqlite_session_factory()
        try:
            assert session.query(ScrapeRun).count() == 1
            assert session.query(ExchangeRate).count() == 1
        finally:
            session.close()

    def test_skips_already_stored_rate_for_same_currency_and_date(
        self, monkeypatch: pytest.MonkeyPatch, sqlite_session_factory: sessionmaker
    ) -> None:
        monkeypatch.setattr(
            "storage.__main__.Database", lambda: _FakeDatabase(sqlite_session_factory)
        )
        rate = _rate_dto()

        BCVStorage.execute(TransformResult(rates=[rate], scrape_run=_scrape_run_dto()))
        BCVStorage.execute(TransformResult(rates=[rate], scrape_run=_scrape_run_dto()))

        session = sqlite_session_factory()
        try:
            assert session.query(ExchangeRate).count() == 1
            assert session.query(ScrapeRun).count() == 2
        finally:
            session.close()

    def test_persists_a_failed_scrape_run_with_no_rates(
        self, monkeypatch: pytest.MonkeyPatch, sqlite_session_factory: sessionmaker
    ) -> None:
        monkeypatch.setattr(
            "storage.__main__.Database", lambda: _FakeDatabase(sqlite_session_factory)
        )
        result = TransformResult(
            rates=[], scrape_run=_scrape_run_dto(status=ScrapeRunStatus.FAILED)
        )

        BCVStorage.execute(result)

        session = sqlite_session_factory()
        try:
            stored_run = session.query(ScrapeRun).one()
            assert stored_run.status == ScrapeRunStatus.FAILED
        finally:
            session.close()


class TestBCVStorageExecuteErrorHandling:
    def test_raises_database_connection_error_and_rolls_back_on_operational_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        session = MagicMock()
        session.commit.side_effect = OperationalError("stmt", {}, Exception("down"))
        monkeypatch.setattr(
            "storage.__main__.Database", lambda: MagicMock(get_session=lambda: session)
        )
        result = TransformResult(rates=[], scrape_run=_scrape_run_dto())

        with pytest.raises(DatabaseConnectionError):
            BCVStorage.execute(result)

        session.rollback.assert_called_once()
        session.close.assert_called_once()

    def test_raises_database_persist_error_and_rolls_back_on_sqlalchemy_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        session = MagicMock()
        session.commit.side_effect = SQLAlchemyError("boom")
        monkeypatch.setattr(
            "storage.__main__.Database", lambda: MagicMock(get_session=lambda: session)
        )
        result = TransformResult(rates=[], scrape_run=_scrape_run_dto())

        with pytest.raises(DatabasePersistError):
            BCVStorage.execute(result)

        session.rollback.assert_called_once()
        session.close.assert_called_once()

    def test_closes_the_session_even_on_success(
        self, monkeypatch: pytest.MonkeyPatch, sqlite_session_factory: sessionmaker
    ) -> None:
        real_session = sqlite_session_factory()
        session = MagicMock(wraps=real_session)
        monkeypatch.setattr(
            "storage.__main__.Database", lambda: MagicMock(get_session=lambda: session)
        )
        result = TransformResult(rates=[], scrape_run=_scrape_run_dto())

        BCVStorage.execute(result)

        session.close.assert_called_once()
        real_session.close()
