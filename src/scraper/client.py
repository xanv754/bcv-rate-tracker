import httpx
from pydantic import BaseModel

from scraper.constants import SSL_VERIFICATION_DISABLED_MESSAGE
from utils.errors import BCVConnectionError, BCVResponseError
from utils.outputs import SystemLogger

BCV_URL_BASE = "https://www.bcv.org.ve"
BCV_RATE_URL = f"{BCV_URL_BASE}/tasas-informativas-sistema-bancario"


class ResponseModel(BaseModel):
    status_code: int
    content: str | None = None
    url: str


class BCVClient:
    @staticmethod
    def get_html() -> ResponseModel:
        """Fetch the BCV exchange rates page HTML, raising on connection or HTTP errors."""
        try:
            SystemLogger().warning(SSL_VERIFICATION_DISABLED_MESSAGE)
            response = httpx.get(BCV_RATE_URL, verify=False)
            response.raise_for_status()
            return ResponseModel(
                status_code=response.status_code,
                content=response.text,
                url=BCV_RATE_URL,
            )
        except httpx.HTTPStatusError as exc:
            raise BCVResponseError(
                f"Failed to fetch data from {BCV_RATE_URL}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.HTTPError as exc:
            raise BCVConnectionError(
                f"Unexpected error occurred while fetching data from {BCV_RATE_URL}: {str(exc)}"
            ) from exc
