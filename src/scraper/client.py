import httpx
from pydantic import BaseModel

BCV_URL_BASE = "https://www.bcv.org.ve"
BCV_RATE_URL = f"{BCV_URL_BASE}/tasas-informativas-sistema-bancario"


class ResponseModel(BaseModel):
    status_code: int
    content: str | None = None
    error: str | None = None


class BCVClient:

    @staticmethod
    def get_html() -> ResponseModel:
        try:
            response = httpx.get(BCV_RATE_URL, verify=False)
            response.raise_for_status()
            return ResponseModel(
                status_code=response.status_code, content=response.text
            )
        except httpx.HTTPStatusError as exc:
            return ResponseModel(
                status_code=exc.response.status_code,
                error=f"Failed to fetch data from {BCV_RATE_URL}",
            )
        except httpx.HTTPError as exc:
            return ResponseModel(
                status_code=500,
                error=f"Unexpected error occurred while fetching data from {BCV_RATE_URL}: {str(exc)}",
            )
