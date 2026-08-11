from utils.outputs import SystemLogger


class AppError(Exception):
    """Base exception for every custom error in the system.

    Any subclass instance is logged to the system log as an error the
    moment it is created, so raising it is enough to guarantee it gets
    recorded — no logging call is needed at the raise site.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        SystemLogger().error(f"{self.__class__.__name__}: {message}")
