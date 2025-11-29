import types
from typing import Any

import httpx

from client.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    GanetiRAPIClientError,
    GanetiRAPIError,
    ResourceNotFoundError,
    ServerError,
)


class RAPIClient:
    _ERROR_MAP = {400: BadRequestError, 401: AuthenticationError, 403: AuthorizationError, 404: ResourceNotFoundError}

    def __init__(self, rapi_address: str, username: str, password: str, ssl_verify: bool = True, timeout: int = 10):
        self.base_url = f"https://{rapi_address}/2"
        self.timeout = timeout
        self._http_client = httpx.Client(base_url=self.base_url, verify=ssl_verify, timeout=timeout)

        self._http_client.auth = httpx.BasicAuth(username, password)
        self._http_client.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def _handle_error_response(self, response: httpx.Response, url: str) -> None:
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

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        try:
            response = self._http_client.request(method, f"{self.base_url}/{endpoint}", **kwargs)
        except httpx.RequestError as e:
            raise GanetiRAPIClientError(f"Client Error: {e}") from e

        if not response.is_success:
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
        self._http_client.close()

    def __enter__(self) -> "RAPIClient":
        return self

    def __exit__(self, exc_type: BaseException, exc_val: BaseException, exc_tb: types.TracebackType) -> None:
        self.close()
