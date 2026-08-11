from typing import Final
from enum import Enum


class ScraperCurrencyId(str, Enum):
    """Currency identifiers as they appear in the BCV HTML (div id attributes)."""

    EURO = "euro"
    DOLLAR = "dolar"
    YUAN = "yuan"
    LIRA = "lira"
    RUBLO = "rublo"


MAIN_CONTAINER_CLASS: Final[str] = "main-container container"

INFO_RATE_GENERAL_CLASS: Final[str] = "region region-services"

RATE_SECTION_CLASS: Final[str] = "view-content"

OFFICIAL_DATE_CLASS: Final[str] = "date-display-single"
DATE_CONTENT_ATTR: Final[str] = "content"
