from datetime import datetime

from sqlalchemy import DateTime, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column

from storage.constants import SCRAPE_RUN_STATUS_ENUM_NAME
from storage.models.base import Base
from transform.constants import ScrapeRunStatus


class ScrapeRun(Base):
    """ORM model for the scrape_runs table: the outcome of one scraping attempt."""

    __tablename__ = "scrape_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[ScrapeRunStatus] = mapped_column(
        Enum(
            ScrapeRunStatus,
            name=SCRAPE_RUN_STATUS_ENUM_NAME,
            values_callable=lambda enum: [member.value for member in enum],
        )
    )
    source_url: Mapped[str | None] = mapped_column(Text)
    raw_html_snapshot: Mapped[str | None] = mapped_column(Text)
    error_message: Mapped[str | None] = mapped_column(Text)
