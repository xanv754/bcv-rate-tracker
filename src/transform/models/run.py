from datetime import datetime

from pydantic import BaseModel

from transform.constants import ScrapeRunStatus


class ScrapeRunDTO(BaseModel):
    started_at: datetime
    finished_at: datetime
    status: ScrapeRunStatus
    source_url: str | None = None
    raw_html_snapshot: str | None = None
    error_message: str | None = None
