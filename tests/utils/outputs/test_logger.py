import logging
from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest

from utils.outputs.constants import LOGGER_NAME
from utils.outputs.logger import SystemLogger


@pytest.fixture(autouse=True)
def _isolated_logger_state() -> Iterator[None]:
    """Reset both the singleton and the underlying stdlib logger's handlers.

    logging.getLogger(LOGGER_NAME) is itself a process-wide singleton that keeps its
    handlers once attached, independently of SystemLogger._instance, so both must be
    cleared for LOG_DIR overrides to take effect test-to-test.
    """
    SystemLogger._instance = None
    logging.getLogger(LOGGER_NAME).handlers.clear()
    yield
    SystemLogger._instance = None
    logging.getLogger(LOGGER_NAME).handlers.clear()


@pytest.fixture()
def system_logger(tmp_path, monkeypatch: pytest.MonkeyPatch) -> SystemLogger:
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    logger = SystemLogger()
    logger._logger = MagicMock()
    return logger


class TestSystemLoggerSingleton:
    def test_returns_the_same_instance_every_time(self, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LOG_DIR", str(tmp_path))

        assert SystemLogger() is SystemLogger()

    def test_creates_the_configured_log_directory(
        self, tmp_path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exercises _resolve_log_dir directly.

        Going through SystemLogger() here would be flaky under pytest: pytest's own
        log-capturing machinery auto-attaches handlers to any non-propagating logger
        it finds registered (ours sets propagate=False), which satisfies
        _build_logger's `if not logger.handlers` guard and skips directory creation
        as a side effect unrelated to the code under test.
        """
        log_dir = tmp_path / "custom-logs"
        monkeypatch.setenv("LOG_DIR", str(log_dir))

        resolved = SystemLogger._resolve_log_dir()

        assert resolved == log_dir
        assert log_dir.is_dir()


class TestSystemLoggerLogging:
    def test_info_delegates_to_underlying_logger(self, system_logger: SystemLogger) -> None:
        system_logger.info("informational")

        system_logger._logger.info.assert_called_once_with("informational")

    def test_warning_delegates_to_underlying_logger(self, system_logger: SystemLogger) -> None:
        system_logger.warning("careful")

        system_logger._logger.warning.assert_called_once_with("careful")

    def test_error_delegates_to_underlying_logger(self, system_logger: SystemLogger) -> None:
        system_logger.error("failed")

        system_logger._logger.error.assert_called_once_with("failed")
