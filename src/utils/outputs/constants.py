from typing import Final

LOGGER_NAME: Final[str] = "bcv_scraper"

LOG_DIR_ENV_VAR: Final[str] = "LOG_DIR"
DEFAULT_LOG_DIR: Final[str] = "logs"
LOG_FILE_NAME: Final[str] = "system.log"
LOG_FILE_ENCODING: Final[str] = "utf-8"

LOG_ROTATION_WHEN: Final[str] = "W0"
LOG_ROTATION_INTERVAL: Final[int] = 1
LOG_BACKUP_COUNT: Final[int] = 0
LOG_DATE_SUFFIX_FORMAT: Final[str] = "%Y-%m-%d"
LOG_ROTATED_FILE_SEPARATOR: Final[str] = "-"

LOG_MESSAGE_FORMAT: Final[str] = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
