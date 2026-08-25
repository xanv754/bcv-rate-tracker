import re
from datetime import datetime

from pydantic import BaseModel, field_validator

from transform.constants import ScrapeRunStatus

_WHITESPACE_RUN = re.compile(r"\s+")


class ScrapeRunDTO(BaseModel):
    started_at: datetime
    finished_at: datetime
    status: ScrapeRunStatus
    source_url: str | None = None
    raw_html_snapshot: str | None = None
    error_message: str | None = None

    @field_validator("raw_html_snapshot")
    @classmethod
    def normalize_snapshot(cls, value: str | None) -> str | None:
        """Collapse the source HTML's indentation and line breaks into single spaces."""
        if value is None:
            return value

        normalized = _WHITESPACE_RUN.sub(" ", value).strip()
        return normalized or None
