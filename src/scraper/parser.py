from datetime import date, datetime

from bs4 import BeautifulSoup, Tag

from scraper.constants import (
    MAIN_CONTAINER_CLASS,
    INFO_RATE_GENERAL_CLASS,
    RATE_SECTION_CLASS,
    OFFICIAL_DATE_CLASS,
    DATE_CONTENT_ATTR,
    CURRENCY_RATE_IDS,
    Currency,
)


class BCVParser:
    _html: str

    def __init__(self, html_doc: str) -> None:
        self._html = html_doc

    def _get_rate_section(self) -> Tag | None:
        soup = BeautifulSoup(self._html, "html.parser")
        soup = soup.find("body")
        if not soup:
            return None

        main_section = soup.find("div", class_=MAIN_CONTAINER_CLASS)
        if not main_section:
            return None

        info_general_section = main_section.find("div", class_=INFO_RATE_GENERAL_CLASS)
        if not info_general_section:
            return None

        rate_section = info_general_section.find("div", class_=RATE_SECTION_CLASS)
        return rate_section

    def _get_official_date(self, rate_section: Tag) -> date | None:
        date_tag = rate_section.find("span", class_=OFFICIAL_DATE_CLASS)
        if not date_tag:
            return None

        date_content = str(date_tag[DATE_CONTENT_ATTR])
        if not date_content:
            return None

        try:
            official_date = datetime.fromisoformat(date_content).date()
            return official_date
        except ValueError:
            return None

    def _get_rate_values(
        self, rate_section: Tag, id_name: str, date: date
    ) -> tuple[str, float, date] | None:
        rate_tag = rate_section.find("div", id=id_name)
        if not rate_tag:
            return None

        name_tag = rate_tag.find("span")
        rate_value_tag = rate_tag.find("strong")
        if not name_tag or not rate_value_tag:
            return None

        rate_name = name_tag.text.strip().upper()
        rate_value = float(rate_value_tag.text.strip().replace(",", "."))

        return rate_name, rate_value, date

    def process(self) -> dict[Currency, tuple[str, float, date]] | None:
        rate_section = self._get_rate_section()
        if not rate_section:
            return None

        official_date = self._get_official_date(rate_section)
        if not official_date:
            return None

        rates = {}
        for currency, id_name in CURRENCY_RATE_IDS.items():
            rate_values = self._get_rate_values(rate_section, id_name, official_date)
            if rate_values:
                rates[currency] = rate_values

        return rates
