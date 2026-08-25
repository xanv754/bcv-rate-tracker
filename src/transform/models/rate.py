from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from transform.constants import Currency


class ExchangeRateDTO(BaseModel):
    currency: Currency
    rate: Decimal
    official_date: date
    scraped_at: datetime
