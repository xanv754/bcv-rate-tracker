from datetime import date

from scraper.client import BCVClient
from scraper.parser import BCVParser
from scraper.constants import Currency


class BCVScraper:
    @staticmethod
    def execute() -> dict[Currency, tuple[str, float, date]] | None:
        bcv_response = BCVClient.get_html()

        if bcv_response.status_code == 200 and bcv_response.content:
            parser = BCVParser(bcv_response.content)
            return parser.process()

        return None


if __name__ == "__main__":
    rates = BCVScraper.execute()
    print(rates)
