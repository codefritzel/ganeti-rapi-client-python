from collections.abc import Callable
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

from client.models.network import Network, NewNetwork
from client.sync_client.api_client import RAPIClient
from client.sync_client.services.network_service import NetworkService


@pytest.fixture
def network_service(api_client: RAPIClient) -> NetworkService:
    return NetworkService(api_client)


class TestNetworkService:
    def test_get_network_names(
        self,
        network_service: NetworkService,
        mock_http_client: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response_from_jsonfile("v2_get_networks.json")
        names = network_service.get_network_names()

        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "GET"  # Check right Request
        assert len(names) == 2
        assert "net-1" in names
        assert "net-2" in names

    def test_get_network(
        self,
        network_service: NetworkService,
        mock_http_client: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response_from_jsonfile("v2_get_networks_bulk.json")

        network = network_service.get_network("net-1")

        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "GET"  # Check right Request
        assert "net-1" in call_args[0][1]

        assert isinstance(network, Network)
        assert network.uuid == "02fcc24c-128f-416f-b6ef-f8993ed5ba91"
        assert network.network == "10.0.0.0/23"
        assert network.gateway == "10.0.0.1"
        assert network.network6 is None
        assert network.gateway6 is None

    def test_create_network(
        self,
        network_service: NetworkService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)

        new_network = NewNetwork(
            network_name="net-3",
            network="10.0.0.0/23",
            gateway="10.0.0.1",
        )

        job_id = network_service.create_network(new_network)
        assert job_id == 123
        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "POST"

    def test_delete_network(
        self,
        network_service: NetworkService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)
        job_id = network_service.delete_network("test-net")

        assert job_id == 123
        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "DELETE"
        assert "test-net" in call_args[0][1]

    def test_connect_network(
        self,
        network_service: NetworkService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)
        job_id = network_service.connect_network("test-net")

        assert job_id == 123
        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "PUT"
        assert "test-net/connect" in call_args[0][1]

    def test_disconnect_network(
        self,
        network_service: NetworkService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)
        job_id = network_service.disconnect_network("test-net")

        assert job_id == 123
        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "PUT"
        assert "test-net/disconnect" in call_args[0][1]

    def test_rename_network(
        self,
        network_service: NetworkService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)
        job_id = network_service.rename_network("test-net", "new-test-net")

        assert job_id == 123
        call_args = mock_http_client.request.call_args
        json: Dict[str, Any] = call_args.kwargs["json"]
        assert call_args[0][0] == "PUT"
        assert "test-net/rename" in call_args[0][1]
        assert "new_name" in json
        assert json["new_name"] == "new-test-net"
