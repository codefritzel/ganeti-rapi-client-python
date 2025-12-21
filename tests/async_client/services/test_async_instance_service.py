from typing import Callable
from unittest.mock import AsyncMock, MagicMock

import pytest

from client.async_client.async_api_client import AsyncRAPIClient
from client.async_client.job_runner import AsyncJobRunner
from client.async_client.services.async_instance_service import AsyncInstanceService


@pytest.fixture
def instance_service(async_api_client: AsyncRAPIClient, async_job_runner: AsyncJobRunner) -> AsyncInstanceService:
    return AsyncInstanceService(async_api_client, async_job_runner)


class TestAsyncJobService:
    @pytest.mark.asyncio
    async def test_get_instance_names(
        self,
        instance_service: AsyncInstanceService,
        mock_client: AsyncMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_client.request.return_value = mock_response_from_jsonfile("v2_get_instances.json")

        instance_names = await instance_service.get_instance_names()

        assert mock_client.request.call_args[0][0] == "GET"
        assert "instances" in mock_client.request.call_args[0][1]

        assert instance_names == ["instance1.example.com", "instance2.example.com", "instance3.example.com"]

    @pytest.mark.asyncio
    async def test_get_instances(
        self,
        instance_service: AsyncInstanceService,
        mock_client: AsyncMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_client.request.return_value = mock_response_from_jsonfile("v2_get_instances_bulk.json")

        instances = await instance_service.get_instances()
        assert mock_client.request.call_args[0][0] == "GET"
        assert "instances" in mock_client.request.call_args[0][1]

        # check bulk param is set
        assert mock_client.request.call_args[1]["params"].get("bulk", None) == 1

        assert instances[0].name == "test.example.com"
        assert instances[1].name == "test2.example.com"
