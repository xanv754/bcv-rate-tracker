import httpx
import pytest

from scraper.client import BCV_RATE_URL, BCVClient, ResponseModel
from utils.errors import BCVConnectionError, BCVResponseError


def _response(status_code: int, content: bytes) -> httpx.Response:
    request = httpx.Request("GET", BCV_RATE_URL)
    return httpx.Response(status_code, content=content, request=request)


class TestBCVClientGetHtml:
    def test_returns_response_model_on_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        fake_response = _response(200, b"<html>ok</html>")
        monkeypatch.setattr("scraper.client.httpx.get", lambda url, verify: fake_response)

        result = BCVClient.get_html()

        assert isinstance(result, ResponseModel)
        assert result.status_code == 200
        assert result.content == "<html>ok</html>"
        assert result.url == BCV_RATE_URL

    def test_raises_bcv_response_error_on_http_status_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        fake_response = _response(500, b"internal error")
        monkeypatch.setattr("scraper.client.httpx.get", lambda url, verify: fake_response)

        with pytest.raises(BCVResponseError) as exc_info:
            BCVClient.get_html()

        assert exc_info.value.status_code == 500

    def test_raises_bcv_connection_error_on_network_failure(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def _raise_connect_error(url: str, verify: bool) -> httpx.Response:
            raise httpx.ConnectError("connection failed")

        monkeypatch.setattr("scraper.client.httpx.get", _raise_connect_error)

        with pytest.raises(BCVConnectionError):
            BCVClient.get_html()
