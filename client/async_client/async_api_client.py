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


class AsyncRAPIClient:
    _ERROR_MAP = {400: BadRequestError, 401: AuthenticationError, 403: AuthorizationError, 404: ResourceNotFoundError}

    def __init__(self, rapi_address: str, username: str, password: str, ssl_verify: bool = True, timeout: int = 10):
        self.base_url = f"https://{rapi_address}/2"
        self._client = httpx.AsyncClient(base_url=self.base_url, verify=ssl_verify, timeout=timeout)
        self._client.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

        self._client.auth = httpx.BasicAuth(username, password)

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

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        response: httpx.Response
        try:
            response = await self._client.request(method, f"{self.base_url}/{endpoint}", **kwargs)
        except httpx.HTTPError as e:
            raise GanetiRAPIClientError(f"Client Error: {e}") from e
        if not response.is_success:
            self._handle_error_response(response, endpoint)

        return response.json()

    async def get(self, endpoint: str, **kwargs: Any) -> Any:
        return await self._request("GET", endpoint, params=kwargs)

    async def post(self, endpoint: str, **kwargs: Any) -> Any:
        return await self._request("POST", endpoint, json=dict(kwargs))

    async def put(self, endpoint: str, **kwargs: Any) -> Any:
        return await self._request("PUT", endpoint, json=dict(kwargs))

    async def delete(self, endpoint: str, **kwargs: Any) -> Any:
        return await self._request("DELETE", endpoint, json=dict(kwargs))
