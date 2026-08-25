from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest

from utils.errors import (
    AppError,
    BCVConnectionError,
    BCVParsingError,
    BCVResponseError,
    DatabaseConfigError,
    DatabaseConnectionError,
    DatabasePersistError,
    OfficialDateNotFoundError,
    RateSectionNotFoundError,
    RateValueNotFoundError,
    ScraperError,
    StorageError,
)


@pytest.fixture(autouse=True)
def _stub_system_logger(monkeypatch: pytest.MonkeyPatch) -> Iterator[MagicMock]:
    """AppError logs itself on construction; stub the logger so tests stay side-effect free."""
    fake_logger = MagicMock()
    monkeypatch.setattr("utils.errors.base.SystemLogger", lambda: fake_logger)
    yield fake_logger


class TestAppError:
    def test_stores_message(self) -> None:
        error = AppError("something failed")

        assert error.message == "something failed"
        assert str(error) == "something failed"

    def test_logs_itself_on_creation(self, _stub_system_logger: MagicMock) -> None:
        AppError("boom")

        _stub_system_logger.error.assert_called_once_with("AppError: boom")

    def test_subclass_logs_with_its_own_class_name(self, _stub_system_logger: MagicMock) -> None:
        BCVConnectionError("network down")

        _stub_system_logger.error.assert_called_once_with("BCVConnectionError: network down")


class TestErrorHierarchy:
    @pytest.mark.parametrize(
        "error_cls",
        [BCVConnectionError, BCVParsingError, RateSectionNotFoundError, OfficialDateNotFoundError],
    )
    def test_scraper_error_subclasses_are_scraper_and_app_errors(self, error_cls) -> None:
        assert issubclass(error_cls, ScraperError)
        assert issubclass(error_cls, AppError)

    @pytest.mark.parametrize(
        "error_cls", [DatabaseConfigError, DatabaseConnectionError, DatabasePersistError]
    )
    def test_storage_error_subclasses_are_storage_and_app_errors(self, error_cls) -> None:
        assert issubclass(error_cls, StorageError)
        assert issubclass(error_cls, AppError)

    def test_bcv_response_error_carries_status_code(self) -> None:
        error = BCVResponseError("bad response", status_code=503)

        assert error.status_code == 503

    def test_rate_value_not_found_error_carries_currency(self) -> None:
        error = RateValueNotFoundError("missing rate", currency="dolar")

        assert error.currency == "dolar"
