from datetime import datetime, timezone

from transform.constants import ScrapeRunStatus
from transform.models import ScrapeRunDTO


class TestScrapeRunDTOSnapshotNormalization:
    _NOW = datetime.now(timezone.utc)

    def _build(self, raw_html_snapshot: str | None) -> ScrapeRunDTO:
        return ScrapeRunDTO(
            started_at=self._NOW,
            finished_at=self._NOW,
            status=ScrapeRunStatus.SUCCESS,
            raw_html_snapshot=raw_html_snapshot,
        )

    def test_collapses_indentation_and_line_breaks(self) -> None:
        raw = "\n    <div>\n      USD\n    </div>\n    \n      36,50\n    "
        dto = self._build(raw)

        assert dto.raw_html_snapshot == "<div> USD </div> 36,50"

    def test_strips_leading_and_trailing_whitespace(self) -> None:
        dto = self._build("   USD 36,50   ")

        assert dto.raw_html_snapshot == "USD 36,50"

    def test_whitespace_only_snapshot_becomes_none(self) -> None:
        dto = self._build("   \n\t  ")

        assert dto.raw_html_snapshot is None

    def test_none_snapshot_stays_none(self) -> None:
        dto = self._build(None)

        assert dto.raw_html_snapshot is None
