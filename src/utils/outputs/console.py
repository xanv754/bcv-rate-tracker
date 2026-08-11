from rich.console import Console
from rich.status import Status

from utils.outputs.constants import (
    CONSOLE_ERROR_STYLE,
    CONSOLE_SPINNER_STYLE,
    CONSOLE_SUCCESS_STYLE,
    CONSOLE_WARNING_STYLE,
)


class ConsoleOutput:
    """Prints user-facing progress, warnings and errors to the terminal via rich."""

    _instance: "ConsoleOutput | None" = None
    _console: Console

    def __new__(cls) -> "ConsoleOutput":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._console = Console()
        return cls._instance

    def message(self, text: str) -> None:
        """Print a plain informational message."""
        self._console.print(text)

    def success(self, text: str) -> None:
        """Print a message marking a successful operation."""
        self._console.print(text, style=CONSOLE_SUCCESS_STYLE)

    def warning(self, text: str) -> None:
        """Print a controlled warning message."""
        self._console.print(text, style=CONSOLE_WARNING_STYLE)

    def error(self, text: str) -> None:
        """Print a controlled error message."""
        self._console.print(text, style=CONSOLE_ERROR_STYLE)

    def loading(self, text: str) -> Status:
        """Return a context manager that shows a spinner with `text` while a process runs."""
        return self._console.status(text, spinner=CONSOLE_SPINNER_STYLE)


if __name__ == "__main__":
    console = ConsoleOutput()
    console.message("This is a plain message")
    console.success("This is a success message")
    console.warning("This is a warning message")
    console.error("This is an error message")
