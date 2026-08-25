import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

from utils.outputs.constants import (
    DEFAULT_LOG_DIR,
    LOG_BACKUP_COUNT,
    LOG_DATE_FORMAT,
    LOG_DATE_SUFFIX_FORMAT,
    LOG_DIR_ENV_VAR,
    LOG_FILE_ENCODING,
    LOG_FILE_NAME,
    LOG_MESSAGE_FORMAT,
    LOG_ROTATED_FILE_SEPARATOR,
    LOG_ROTATION_INTERVAL,
    LOG_ROTATION_WHEN,
    LOGGER_NAME,
)

load_dotenv()


class SystemLogger:
    """Writes system events to a weekly-rotating log file, at INFO, WARNING or ERROR level."""

    _instance: "SystemLogger | None" = None
    _logger: logging.Logger

    def __new__(cls) -> "SystemLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._logger = cls._build_logger()
        return cls._instance

    @staticmethod
    def _resolve_log_dir() -> Path:
        log_dir = Path(os.getenv(LOG_DIR_ENV_VAR, DEFAULT_LOG_DIR))
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    @staticmethod
    def _rotated_file_namer(default_name: str) -> str:
        base, separator, suffix = default_name.rpartition(".")
        if not separator:
            return default_name
        return f"{base}{LOG_ROTATED_FILE_SEPARATOR}{suffix}"

    @classmethod
    def _build_logger(cls) -> logging.Logger:
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if not logger.handlers:
            log_path = cls._resolve_log_dir() / LOG_FILE_NAME
            handler = TimedRotatingFileHandler(
                filename=str(log_path),
                when=LOG_ROTATION_WHEN,
                interval=LOG_ROTATION_INTERVAL,
                backupCount=LOG_BACKUP_COUNT,
                encoding=LOG_FILE_ENCODING,
            )
            handler.suffix = LOG_DATE_SUFFIX_FORMAT
            handler.namer = cls._rotated_file_namer
            handler.setFormatter(
                logging.Formatter(fmt=LOG_MESSAGE_FORMAT, datefmt=LOG_DATE_FORMAT)
            )
            logger.addHandler(handler)

        return logger

    def info(self, message: str) -> None:
        """Log an informational message."""
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self._logger.error(message)


if __name__ == "__main__":
    logger = SystemLogger()
    logger.info("This is a test log message")
