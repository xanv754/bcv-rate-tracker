import pytest

from scraper.__main__ import BCVScraper, ScraperResponse
from scraper.client import ResponseModel

_SAMPLE_HTML = """
<html><body>
<div class="main-container container">
  <div class="region region-services">
    <div class="view-content">
      <span class="date-display-single" content="2026-08-24T00:00:00-04:00">24/08/2026</span>
      <div id="dolar">
        <span>USD</span>
        <strong>203,50000000</strong>
      </div>
    </div>
  </div>
</div>
</body></html>
"""


class TestBCVScraperSnapshot:
    def test_snapshot_keeps_raw_html_tags(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "scraper.__main__.BCVClient.get_html",
            staticmethod(
                lambda: ResponseModel(
                    status_code=200, content=_SAMPLE_HTML, url="https://example.test"
                )
            ),
        )

        result = BCVScraper.execute()

        assert isinstance(result, ScraperResponse)
        assert "<div" in result.info.snapshot
        assert "<strong>203,50000000</strong>" in result.info.snapshot
