from collections.abc import Callable
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

from cli import BCVCli, cli
from transform import ScrapeRunStatus
from utils.errors import DatabaseConnectionError


def _raiser(exception: Exception) -> Callable[[], None]:
    def _raise() -> None:
        raise exception

    return _raise


class TestBCVCliInitDb:
    def test_creates_tables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        fake_db = MagicMock()
        monkeypatch.setattr("cli.Database", lambda: fake_db)

        BCVCli.init_db()

        fake_db.create_tables.assert_called_once()


class TestBCVCliRun:
    def test_stores_rates_when_transformer_succeeds(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transform_result = MagicMock()
        transform_result.scrape_run.status = ScrapeRunStatus.SUCCESS
        transform_result.rates = [MagicMock(), MagicMock()]
        monkeypatch.setattr(
            "cli.BCVTransformer.execute", staticmethod(lambda: transform_result)
        )
        store_execute = MagicMock()
        monkeypatch.setattr("cli.BCVStorage.execute", store_execute)

        BCVCli.run()

        store_execute.assert_called_once_with(transform_result)

    def test_raises_system_exit_when_run_status_is_failed(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        transform_result = MagicMock()
        transform_result.scrape_run.status = ScrapeRunStatus.FAILED
        transform_result.scrape_run.error_message = "network down"
        monkeypatch.setattr(
            "cli.BCVTransformer.execute", staticmethod(lambda: transform_result)
        )
        monkeypatch.setattr("cli.BCVStorage.execute", MagicMock())

        with pytest.raises(SystemExit) as exc_info:
            BCVCli.run()

        assert exc_info.value.code == 1


class TestCliInitDbCommand:
    def test_exits_with_error_code_when_app_error_is_raised(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "cli.BCVCli.init_db",
            staticmethod(_raiser(DatabaseConnectionError("db down"))),
        )

        result = CliRunner().invoke(cli, ["init-db"])

        assert result.exit_code == 1

    def test_succeeds_when_init_db_completes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("cli.BCVCli.init_db", staticmethod(lambda: None))

        result = CliRunner().invoke(cli, ["init-db"])

        assert result.exit_code == 0


class TestCliRunCommand:
    def test_exits_with_error_code_when_app_error_is_raised(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "cli.BCVCli.run", staticmethod(_raiser(DatabaseConnectionError("db down")))
        )

        result = CliRunner().invoke(cli, ["run"])

        assert result.exit_code == 1

    def test_succeeds_when_run_completes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("cli.BCVCli.run", staticmethod(lambda: None))

        result = CliRunner().invoke(cli, ["run"])

        assert result.exit_code == 0
