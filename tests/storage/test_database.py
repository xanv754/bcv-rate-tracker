from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import inspect

from storage.database import Database
from storage.models import ScrapeRun
from transform.constants import ScrapeRunStatus
from utils.env import DatabaseConfig


@pytest.fixture(autouse=True)
def _isolated_database_singleton(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Reset the Database singleton and point it at an isolated in-memory SQLite DB.

    Database() is a process-wide singleton bound to whatever DatabaseConfig.url()
    returns, so tests must not share state with each other or depend on a real
    Postgres instance being reachable.
    """
    Database._instance = None
    monkeypatch.setattr(DatabaseConfig, "url", staticmethod(lambda: "sqlite:///:memory:"))
    yield
    Database._instance = None


class TestDatabaseSingleton:
    def test_returns_the_same_instance_every_time(self) -> None:
        assert Database() is Database()

    def test_reuses_the_same_engine_and_session_factory(self) -> None:
        first = Database()
        second = Database()

        assert first._engine is second._engine
        assert first._session_factory is second._session_factory


class TestDatabaseCreateTables:
    def test_creates_the_expected_tables(self) -> None:
        db = Database()

        db.create_tables()

        inspector = inspect(db._engine)
        assert {"exchange_rates", "scrape_runs"}.issubset(set(inspector.get_table_names()))


class TestDatabaseGetSession:
    def test_returns_a_usable_session(self) -> None:
        db = Database()
        db.create_tables()
        session = db.get_session()

        try:
            now = datetime.now(timezone.utc)
            session.add(ScrapeRun(started_at=now, finished_at=now, status=ScrapeRunStatus.SUCCESS))
            session.commit()

            assert session.query(ScrapeRun).count() == 1
        finally:
            session.close()

    def test_returns_a_new_session_object_on_each_call(self) -> None:
        db = Database()

        assert db.get_session() is not db.get_session()
