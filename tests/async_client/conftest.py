from typing import Callable, List
from unittest.mock import AsyncMock

import pytest

from client.async_client.async_api_client import AsyncRAPIClient
from client.async_client.job_runner import AsyncJobRunner
from client.async_client.services.async_job_service import AsyncJobService
from client.models.job import Job


@pytest.fixture
def mock_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def async_api_client(monkeypatch: pytest.MonkeyPatch, mock_client: AsyncMock) -> AsyncRAPIClient:
    client = AsyncRAPIClient("localhost", "username", "password", ssl_verify=False)
    monkeypatch.setattr(client, "_client", mock_client)
    return client


@pytest.fixture
def async_job_service(async_api_client: AsyncRAPIClient) -> AsyncJobService:
    return AsyncJobService(async_api_client)


@pytest.fixture
def async_job_runner(async_job_service: AsyncJobService) -> AsyncJobRunner:
    return AsyncJobRunner(async_job_service)


@pytest.fixture
def fake_get_job(monkeypatch: pytest.MonkeyPatch, async_job_service: AsyncJobService) -> Callable[[List[Job]], None]:
    _jobs: List[Job] = []

    async def _fake_get_job(job_id: int) -> Job:
        return _jobs.pop(0)

    monkeypatch.setattr(async_job_service, "get_job_info", _fake_get_job)

    def set_jobs(jobs: List[Job]) -> None:
        _jobs.clear()
        _jobs.extend(jobs)

    return set_jobs
