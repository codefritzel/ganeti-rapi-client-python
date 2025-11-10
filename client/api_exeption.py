class GanetiRAPIError(Exception):
    """Base exception for Ganeti API errors."""

    def __init__(self, message: str, status_code: int, url: str):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.url = url


class AuthenticationError(GanetiRAPIError):
    """Raised when authentication fails (401)."""


class AuthorizationError(GanetiRAPIError):
    """Raised when authorization fails (403)."""


class ResourceNotFoundError(GanetiRAPIError):
    """Raised when a resource is not found (404)."""


class BadRequestError(GanetiRAPIError):
    """Raised when the request is invalid (400)."""


class ServerError(GanetiRAPIError):
    """Raised when the server encounters an error (500+)."""
