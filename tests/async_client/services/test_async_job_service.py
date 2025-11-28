from typing import Callable
from unittest.mock import AsyncMock, MagicMock

import pytest

from client.async_client.services.async_job_service import AsyncJobService


class TestAsyncJobService:
    @pytest.mark.asyncio
    async def test_get_jobs(
        self,
        async_job_service: AsyncJobService,
        mock_client: AsyncMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_client.request.return_value = mock_response_from_jsonfile("v2_get_jobs.json")

        jobs = await async_job_service.get_jobs()

        assert mock_client.request.call_args[0][0] == "GET"
        assert "jobs" in mock_client.request.call_args[0][1]
        assert jobs == [1, 2, 3]

    @pytest.mark.asyncio
    async def test_get_job(
        self,
        async_job_service: AsyncJobService,
        mock_client: AsyncMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_client.request.return_value = mock_response_from_jsonfile("v2_get_jobs_job.json")
        job_info = await async_job_service.get_job_info(1)

        assert mock_client.request.call_args[0][0] == "GET"
        assert "jobs/1" in mock_client.request.call_args[0][1]

        assert job_info.id == 1
        assert job_info.status == "success"

    @pytest.mark.asyncio
    async def test_cancel_job(
        self, async_job_service: AsyncJobService, mock_client: AsyncMock, mock_response: Callable[[str], MagicMock]
    ) -> None:
        mock_client.request.return_value = mock_response(data={})  # type: ignore[call-arg]

        await async_job_service.cancel_job(1)

        assert mock_client.request.call_args[0][0] == "DELETE"
        assert "jobs/1" in mock_client.request.call_args[0][1]
