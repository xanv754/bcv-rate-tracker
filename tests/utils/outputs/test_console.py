from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest

from utils.outputs.constants import (
    CONSOLE_ERROR_STYLE,
    CONSOLE_SPINNER_STYLE,
    CONSOLE_SUCCESS_STYLE,
    CONSOLE_WARNING_STYLE,
)
from utils.outputs.console import ConsoleOutput


@pytest.fixture(autouse=True)
def _reset_singleton() -> Iterator[None]:
    ConsoleOutput._instance = None
    yield
    ConsoleOutput._instance = None


@pytest.fixture()
def console_output() -> ConsoleOutput:
    output = ConsoleOutput()
    output._console = MagicMock()
    return output


class TestConsoleOutputSingleton:
    def test_returns_the_same_instance_every_time(self) -> None:
        assert ConsoleOutput() is ConsoleOutput()


class TestConsoleOutputPrinting:
    def test_message_prints_without_style(self, console_output: ConsoleOutput) -> None:
        console_output.message("hello")

        console_output._console.print.assert_called_once_with("hello")

    def test_success_prints_with_success_style(self, console_output: ConsoleOutput) -> None:
        console_output.success("done")

        console_output._console.print.assert_called_once_with("done", style=CONSOLE_SUCCESS_STYLE)

    def test_warning_prints_with_warning_style(self, console_output: ConsoleOutput) -> None:
        console_output.warning("careful")

        console_output._console.print.assert_called_once_with(
            "careful", style=CONSOLE_WARNING_STYLE
        )

    def test_error_prints_with_error_style(self, console_output: ConsoleOutput) -> None:
        console_output.error("failed")

        console_output._console.print.assert_called_once_with("failed", style=CONSOLE_ERROR_STYLE)

    def test_loading_returns_status_with_spinner(self, console_output: ConsoleOutput) -> None:
        console_output.loading("working...")

        console_output._console.status.assert_called_once_with(
            "working...", spinner=CONSOLE_SPINNER_STYLE
        )
