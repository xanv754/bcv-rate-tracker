from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from storage.constants import CURRENCY_ENUM_NAME, CURRENCY_MAX_LENGTH
from storage.models.base import Base
from transform.constants import Currency


class ExchangeRate(Base):
    """ORM model for the exchange_rates table: one BCV rate for a currency on a given date."""

    __tablename__ = "exchange_rates"
    __table_args__ = (UniqueConstraint("currency", "official_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[Currency] = mapped_column(
        Enum(
            Currency,
            name=CURRENCY_ENUM_NAME,
            native_enum=False,
            length=CURRENCY_MAX_LENGTH,
            values_callable=lambda enum: [member.value for member in enum],
        )
    )
    rate: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    official_date: Mapped[date] = mapped_column(Date)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
