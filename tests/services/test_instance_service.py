from typing import Any, Callable
from unittest.mock import MagicMock

import pytest

from client.api_client import BaseApiClient
from client.models.instance import InstanceInfo
from client.services.instance_service import InstanceService


@pytest.fixture
def instance_service(api_client: BaseApiClient) -> InstanceService:
    return InstanceService(api_client)


class TestInstanceService:
    def test_get_instance_names(
        self,
        instance_service: InstanceService,
        mock_session: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        # Load response from JSON file
        mock_session.request.return_value = mock_response_from_jsonfile("v2_get_instances.json")

        names = instance_service.get_instance_names()

        call_args = mock_session.request.call_args
        assert call_args[0][0] == "GET"  # Check right Request
        assert len(names) == 3
        assert "instance1.example.com" in names
        assert "instance2.example.com" in names
        assert "instance3.example.com" in names

    def test_start_instance(
        self, instance_service: InstanceService, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        """Test starting an instance."""
        mock_session.request.return_value = mock_response(123, 200)

        job_id = instance_service.start_instance("test-vm")

        assert job_id == 123
        call_args = mock_session.request.call_args
        assert call_args[0][0] == "PUT"
        url = call_args[0][1]
        assert "test-vm" in url

    def test_stop_instance(
        self, instance_service: InstanceService, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        """Test stopping an instance."""
        mock_session.request.return_value = mock_response(123, 200)

        job_id = instance_service.stop_instance("test-vm")

        assert job_id == 123
        call_args = mock_session.request.call_args
        url = call_args[0][1]
        assert "test-vm" in url

    def test_restart_instance(
        self, instance_service: InstanceService, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        """Test restarting an instance."""
        mock_session.request.return_value = mock_response(123, 300)

        job_id = instance_service.restart_instance("test-vm")

        assert job_id == 123
        call_args = mock_session.request.call_args
        assert call_args[0][0] == "POST"
        url = call_args[0][1]
        assert "test-vm" in url

    def test_migrate_instance(
        self, instance_service: InstanceService, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        """Test migrating an instance."""
        mock_session.request.return_value = mock_response(123, 300)

        job_id = instance_service.migrate_instance("test-vm")

        assert job_id == 123
        call_args = mock_session.request.call_args
        assert "migrate" in call_args[0][1]
        url = call_args[0][1]
        assert "test-vm" in url

    def test_failover_instance(
        self, instance_service: InstanceService, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        """Test failover of an instance."""
        mock_session.request.return_value = mock_response(123, 100)

        job_id = instance_service.failover_instance("test-vm")

        assert job_id == 123
        call_args = mock_session.request.call_args
        url = call_args[0][1]
        assert "test-vm" in url

    def test_grow_instance_disk(
        self, instance_service: InstanceService, mock_session: MagicMock, mock_response: Callable[[Any, int], MagicMock]
    ) -> None:
        """Test growing an instance disk."""
        mock_session.request.return_value = mock_response(123, 100)

        job_id = instance_service.grow_instance_disk("test-vm", disk_index=0, amount=10240)

        assert job_id == 123
        call_args = mock_session.request.call_args
        assert call_args[0][0] == "POST"
        assert "test-vm/disk/0/grow" in call_args[0][1]
        assert call_args[1]["json"]["amount"] == 10240

    def test_get_instance(
        self,
        instance_service: InstanceService,
        mock_session: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        """Test getting instance info."""
        mock_session.request.return_value = mock_response_from_jsonfile("v2_get_instances_instance.json")

        instance: InstanceInfo = instance_service.get_instance("test.example.com")
        call_args = mock_session.request.call_args
        assert call_args[0][0] == "GET"
        assert "test.example.com" in call_args[0][1]

        assert isinstance(instance, InstanceInfo)
        assert instance.name == "test.example.com"
        assert "192.168.1.100" in instance.nic_ips
