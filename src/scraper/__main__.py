from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from scraper.client import BCVClient
from scraper.parser import BCVParser
from scraper.constants import ScraperCurrencyId
from utils.errors import ScraperError
from utils.outputs import ConsoleOutput


class RateInfoModel(BaseModel):
    snapshot: str
    url: str


class ScraperResponse(BaseModel):
    rates: dict[ScraperCurrencyId, tuple[str, Decimal, date]]
    info: RateInfoModel


class ScraperFailure(BaseModel):
    error_message: str


class BCVScraper:
    @staticmethod
    def execute() -> ScraperResponse | ScraperFailure:
        """Fetch and parse today's BCV exchange rates, or a failure with the error detail."""
        try:
            bcv_response = BCVClient.get_html()
            parser = BCVParser(bcv_response.content)
            rates = parser.process()
            return ScraperResponse(
                rates=rates,
                info=RateInfoModel(
                    snapshot=str(parser.get_rate_section()), url=bcv_response.url
                ),
            )
        except ScraperError as error:
            ConsoleOutput().error(
                "Could not retrieve today's exchange rate information from BCV."
            )
            return ScraperFailure(error_message=error.message)


if __name__ == "__main__":
    rates = BCVScraper.execute()
    print(rates)
