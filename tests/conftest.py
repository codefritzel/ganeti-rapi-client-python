import json
from pathlib import Path
from typing import Any, Callable
from unittest.mock import MagicMock

import pytest

from client import GanetiRapiClient
from client.api_client import BaseApiClient


@pytest.fixture
def mock_session() -> MagicMock:
    """Create a mock session."""
    session = MagicMock()
    session.auth = None
    session.headers = {}
    session.verify = True

    return session


@pytest.fixture
def api_client(mock_session: MagicMock, monkeypatch: pytest.MonkeyPatch) -> BaseApiClient:
    """Create a base api client with mocked session."""
    client = BaseApiClient("localhost", "username", "password", ssl_verify=False)
    # Replace the session with our mock
    monkeypatch.setattr(client, "_session", mock_session)
    return client


@pytest.fixture
def ganeti_rapi_client(api_client: BaseApiClient, monkeypatch: pytest.MonkeyPatch) -> GanetiRapiClient:
    """Create a ganeti rapi client with mocked session."""
    client = GanetiRapiClient("localhost", "username", "password", ssl_verify=False)
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
