from typing import Any, Callable
from unittest.mock import MagicMock

import pytest

from client.api_client import BaseApiClient
from client.api_exeption import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    ResourceNotFoundError,
    ServerError,
)


class TestErrorHandling:
    def test_bad_request_error_400(
        self, api_client: BaseApiClient, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        error_response = mock_response({"message": "Bad request", "explain": "Invalid body contents"}, 400)
        error_response.ok = False
        mock_session.request.return_value = error_response
        with pytest.raises(BadRequestError) as exc_info:
            api_client.get("/dummy")
        assert exc_info.value.status_code == 400
        assert exc_info.value.message == "Bad request: Invalid body contents"

    # b'{"code": 404, "message": "Not Found", "explain": "Nothing matches the given URI"}\n'
    def test_authentication_error_401(
        self, api_client: BaseApiClient, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        error_response = mock_response({"message": "Authentication required"}, 401)
        error_response.ok = False
        mock_session.request.return_value = error_response

        with pytest.raises(AuthenticationError) as exc_info:
            api_client.get("/dummy")

        assert exc_info.value.status_code == 401
        assert exc_info.value.message == "Authentication required"

    def test_authorisation_error_403(
        self, api_client: BaseApiClient, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        error_response = mock_response({"message": "Permission denied"}, 403)
        error_response.ok = False
        mock_session.request.return_value = error_response

        with pytest.raises(AuthorizationError) as exc_info:
            api_client.get("/dummy")

        assert exc_info.value.status_code == 403
        assert exc_info.value.message == "Permission denied"

    def test_resource_not_found_error_404(
        self, api_client: BaseApiClient, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        error_response = mock_response({"message": "Not Found", "explain": "Nothing matches the given URI"}, 404)
        error_response.ok = False
        mock_session.request.return_value = error_response
        with pytest.raises(ResourceNotFoundError) as exc_info:
            api_client.get("/dummy")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not Found: Nothing matches the given URI"

    def test_generic_error_500(
        self, api_client: BaseApiClient, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        error_response = mock_response({"message": "Internal Server Error"}, 502)
        error_response.ok = False
        mock_session.request.return_value = error_response
        with pytest.raises(ServerError) as exc_info:
            api_client.get("/dummy")

        assert exc_info.value.status_code == 502
        assert exc_info.value.message == "Internal Server Error"
