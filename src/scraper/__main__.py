from datetime import date

from scraper.client import BCVClient
from scraper.parser import BCVParser
from scraper.constants import ScraperCurrencyId
from utils.errors import ScraperError
from utils.outputs import ConsoleOutput


class BCVScraper:
    @staticmethod
    def execute() -> dict[ScraperCurrencyId, tuple[str, float, date]] | None:
        """Fetch and parse today's BCV exchange rates, or None if the operation failed."""
        try:
            bcv_response = BCVClient.get_html()
            return BCVParser(bcv_response.content).process()
        except ScraperError:
            ConsoleOutput().error(
                "Could not retrieve today's exchange rate information from BCV."
            )
            return None


if __name__ == "__main__":
    rates = BCVScraper.execute()
    print(rates)
