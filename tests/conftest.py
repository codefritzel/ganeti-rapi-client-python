import json
from pathlib import Path
from typing import Any, Callable
from unittest.mock import MagicMock

import pytest

from client import GanetiRAPIClient
from client.sync_client.api_client import RAPIClient


@pytest.fixture
def mock_http_client() -> MagicMock:
    """Create a mock session."""
    http_client = MagicMock()
    http_client.auth = None
    http_client.headers = {}
    http_client.verify = True

    return http_client


@pytest.fixture
def api_client(mock_http_client: MagicMock, monkeypatch: pytest.MonkeyPatch) -> RAPIClient:
    """Create a base api client with mocked session."""
    client = RAPIClient("localhost", "username", "password", ssl_verify=False)
    # Replace the session with our mock
    monkeypatch.setattr(client, "_http_client", mock_http_client)
    return client


@pytest.fixture
def ganeti_rapi_client(api_client: RAPIClient, monkeypatch: pytest.MonkeyPatch) -> GanetiRAPIClient:
    """Create a ganeti rapi client with mocked session."""
    client = GanetiRAPIClient("localhost", "username", "password", ssl_verify=False)
    # Replace the internal client's session
    monkeypatch.setattr(client, "_client", api_client)
    return client


@pytest.fixture
def _testdata_dir() -> Path:
    """Return the path to the testdata directory."""
    return Path(__file__).parent / "testdata"


@pytest.fixture
def mock_response() -> Callable[[Any, int], MagicMock]:
    """Create a mock response factory."""

    def _create_mock_response(data: Any, status_code: int = 200) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = data or {}
        response.ok = status_code < 400
        response.is_success = status_code < 400
        return response

    return _create_mock_response


@pytest.fixture
def mock_response_from_jsonfile(
    _testdata_dir: Path, mock_response: Callable[[Any, int], MagicMock]
) -> Callable[[str], MagicMock]:
    """Create a mock response from a JSON file.
    Usage:
        def test_example(self, mock_response_from_file):
            response = mock_response_from_file("test_data.json")
    """

    def _create_from_file(filename: str, status_code: int = 200) -> MagicMock:
        path = _testdata_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"File {path} not found")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return mock_response(data, status_code)

    return _create_from_file
