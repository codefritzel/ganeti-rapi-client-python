from client.async_client.async_api_client import AsyncRAPIClient
from client.async_client.job_runner import AsyncJobRunner
from client.async_client.services.async_instance_service import AsyncInstanceService
from client.async_client.services.async_job_service import AsyncJobService


class AsyncGanetiRAPIClient:
    def __init__(
        self, rapi_address: str, username: str, password: str, ssl_verify: bool = True, timeout: int = 10
    ) -> None:
        self._client = AsyncRAPIClient(rapi_address, username, password, ssl_verify=ssl_verify)
        self.job_service = AsyncJobService(self._client)
        self._job_runner = AsyncJobRunner(self.job_service)

        self.instance_service = AsyncInstanceService(self._client, self._job_runner)
