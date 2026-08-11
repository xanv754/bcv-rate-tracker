from typing import Final
from enum import Enum


class Currency(str, Enum):
    EURO = "euro"
    DOLLAR = "dollar"
    YUAN = "yuan"
    LIRA = "lira"
    RUBLO = "rublo"


MAIN_CONTAINER_CLASS: Final[str] = "main-container container"

INFO_RATE_GENERAL_CLASS: Final[str] = "region region-services"

RATE_SECTION_CLASS: Final[str] = "view-content"

OFFICIAL_DATE_CLASS: Final[str] = "date-display-single"
DATE_CONTENT_ATTR: Final[str] = "content"

CURRENCY_RATE_IDS: Final[dict[Currency, str]] = {
    Currency.EURO: "euro",
    Currency.DOLLAR: "dolar",
    Currency.YUAN: "yuan",
    Currency.LIRA: "lira",
    Currency.RUBLO: "rublo",
}
