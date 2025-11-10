import types
from typing import Any

import requests

from client.api_exeption import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    GanetiRAPIError,
    ResourceNotFoundError,
    ServerError,
)


class BaseApiClient:
    _ERROR_MAP = {400: BadRequestError, 401: AuthenticationError, 403: AuthorizationError, 404: ResourceNotFoundError}

    def __init__(self, rapi_address: str, username: str, password: str, ssl_verify: bool = True):
        self.base_url = f"https://{rapi_address}/2"
        self.username = username
        self.password = password
        self._session = requests.Session()

        self._session.auth = (self.username, self.password)
        self._session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

        self._session.verify = ssl_verify

    def _handle_error_response(self, response: requests.Response, url: str) -> None:
        """Handle an error response from the API."""
        status_code = response.status_code
        try:
            error_data = response.json()
            error_message = error_data.get("message", response.text)
            error_explain = error_data.get("explain", "")
            if error_explain:
                error_message = f"{error_message}: {error_explain}"
        except Exception:
            error_message = response.text or f"HTTP {status_code} Error"

        if status_code in self._ERROR_MAP:
            raise self._ERROR_MAP[status_code](
                message=error_message,
                status_code=status_code,
                url=url,
            )
        if 500 <= status_code < 600:
            raise ServerError(
                message=error_message,
                status_code=status_code,
                url=url,
            )
        raise GanetiRAPIError(
            message=f"Unexpected error: {error_message}",
            status_code=status_code,
            url=url,
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        response = self._session.request(method, f"{self.base_url}/{endpoint}", **kwargs)

        if not response.ok:
            self._handle_error_response(response, f"{self.base_url}/{endpoint}")

        return response

    def get(self, endpoint: str, **kwargs: Any) -> Any:
        return self._request("GET", endpoint, params=kwargs).json()

    def post(self, endpoint: str, **kwargs: Any) -> Any:
        return self._request("POST", endpoint, json=dict(kwargs)).json()

    def put(self, endpoint: str, **kwargs: Any) -> Any:
        return self._request("PUT", endpoint, json=dict(kwargs)).json()

    def delete(self, endpoint: str) -> Any:
        return self._request("DELETE", endpoint).json()

    def close(self) -> None:
        """Close the session and cleanup."""
        self._session.close()

    def __enter__(self) -> "BaseApiClient":
        return self

    def __exit__(self, exc_type: BaseException, exc_val: BaseException, exc_tb: types.TracebackType) -> None:
        self.close()
