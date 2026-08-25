from datetime import datetime, timezone

from pydantic import BaseModel

from scraper import BCVScraper, ScraperFailure
from transform.constants import SCRAPER_ID_TO_CURRENCY, ScrapeRunStatus
from transform.models import ExchangeRateDTO, ScrapeRunDTO


class TransformResult(BaseModel):
    rates: list[ExchangeRateDTO]
    scrape_run: ScrapeRunDTO


class BCVTransformer:
    @staticmethod
    def execute() -> TransformResult:
        """Fetch, validate, and package today's BCV exchange rate data for storage."""
        started_at = datetime.now(timezone.utc)
        scraper_result = BCVScraper.execute()
        finished_at = datetime.now(timezone.utc)

        if isinstance(scraper_result, ScraperFailure):
            return TransformResult(
                rates=[],
                scrape_run=ScrapeRunDTO(
                    started_at=started_at,
                    finished_at=finished_at,
                    status=ScrapeRunStatus.FAILED,
                    error_message=scraper_result.error_message,
                ),
            )

        rates = [
            ExchangeRateDTO(
                currency=SCRAPER_ID_TO_CURRENCY[scraper_id],
                rate=rate_value,
                official_date=official_date,
                scraped_at=finished_at,
            )
            for scraper_id, (_, rate_value, official_date) in scraper_result.rates.items()
        ]

        return TransformResult(
            rates=rates,
            scrape_run=ScrapeRunDTO(
                started_at=started_at,
                finished_at=finished_at,
                status=ScrapeRunStatus.SUCCESS,
                source_url=scraper_result.info.url,
                raw_html_snapshot=scraper_result.info.snapshot,
            ),
        )


if __name__ == "__main__":
    result = BCVTransformer.execute()
    print(result)
