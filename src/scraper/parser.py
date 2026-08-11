from datetime import date, datetime

from bs4 import BeautifulSoup, Tag

from scraper.constants import (
    MAIN_CONTAINER_CLASS,
    INFO_RATE_GENERAL_CLASS,
    RATE_SECTION_CLASS,
    OFFICIAL_DATE_CLASS,
    DATE_CONTENT_ATTR,
    ScraperCurrencyId,
)
from utils.errors import (
    OfficialDateNotFoundError,
    RateSectionNotFoundError,
    RateValueNotFoundError,
)


class BCVParser:
    _html: str

    def __init__(self, html_doc: str) -> None:
        self._html = html_doc

    def _get_rate_section(self) -> Tag:
        soup = BeautifulSoup(self._html, "html.parser")
        soup = soup.find("body")
        if not soup:
            raise RateSectionNotFoundError(
                "Could not find the <body> tag in the BCV page"
            )

        main_section = soup.find("div", class_=MAIN_CONTAINER_CLASS)
        if not main_section:
            raise RateSectionNotFoundError(
                f"Could not find the main container section ('{MAIN_CONTAINER_CLASS}')"
            )

        info_general_section = main_section.find("div", class_=INFO_RATE_GENERAL_CLASS)
        if not info_general_section:
            raise RateSectionNotFoundError(
                f"Could not find the info rate general section ('{INFO_RATE_GENERAL_CLASS}')"
            )

        rate_section = info_general_section.find("div", class_=RATE_SECTION_CLASS)
        if not rate_section:
            raise RateSectionNotFoundError(
                f"Could not find the rate section ('{RATE_SECTION_CLASS}')"
            )

        return rate_section

    def _get_official_date(self, rate_section: Tag) -> date:
        date_tag = rate_section.find("span", class_=OFFICIAL_DATE_CLASS)
        if not date_tag:
            raise OfficialDateNotFoundError(
                f"Could not find the official date tag ('{OFFICIAL_DATE_CLASS}')"
            )

        date_content = str(date_tag[DATE_CONTENT_ATTR])
        if not date_content:
            raise OfficialDateNotFoundError(
                f"The official date tag has no '{DATE_CONTENT_ATTR}' attribute"
            )

        try:
            return datetime.fromisoformat(date_content).date()
        except ValueError as exc:
            raise OfficialDateNotFoundError(
                f"Could not parse official date from '{date_content}'"
            ) from exc

    def _get_rate_values(
        self, rate_section: Tag, id_name: str, date: date
    ) -> tuple[str, float, date]:
        rate_tag = rate_section.find("div", id=id_name)
        if not rate_tag:
            raise RateValueNotFoundError(
                f"Could not find the rate block for '{id_name}'", currency=id_name
            )

        name_tag = rate_tag.find("span")
        rate_value_tag = rate_tag.find("strong")
        if not name_tag or not rate_value_tag:
            raise RateValueNotFoundError(
                f"Could not find the name or value tag for '{id_name}'",
                currency=id_name,
            )

        rate_name = name_tag.text.strip().upper()
        try:
            rate_value = float(rate_value_tag.text.strip().replace(",", "."))
        except ValueError as exc:
            raise RateValueNotFoundError(
                f"Could not parse rate value for '{id_name}'", currency=id_name
            ) from exc

        return rate_name, rate_value, date

    def process(self) -> dict[ScraperCurrencyId, tuple[str, float, date]]:
        """Parse the BCV HTML page and return each currency's rate, name and official date."""
        rate_section = self._get_rate_section()
        official_date = self._get_official_date(rate_section)

        rates = {}
        for currency_id in ScraperCurrencyId:
            try:
                rates[currency_id] = self._get_rate_values(
                    rate_section, currency_id.value, official_date
                )
            except RateValueNotFoundError:
                continue

        return rates
