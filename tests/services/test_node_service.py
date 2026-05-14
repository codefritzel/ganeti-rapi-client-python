from typing import Any, Callable, Dict
from unittest.mock import MagicMock

import pytest

from client.models.node import Node
from client.sync_client.api_client import RAPIClient
from client.sync_client.services.node_service import NodeService


@pytest.fixture
def node_service(api_client: RAPIClient) -> NodeService:
    return NodeService(api_client)


class TestNodeService:
    def test_get_node_names(
        self,
        node_service: NodeService,
        mock_http_client: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response_from_jsonfile("v2_get_nodes.json")

        names = node_service.get_node_names()

        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "GET"  # Check right Request
        assert len(names) == 3
        assert "node1.example.com" in names
        assert "node2.example.com" in names
        assert "node3.example.com" in names

    def test_get_node(
        self,
        node_service: NodeService,
        mock_http_client: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response_from_jsonfile("v2_get_nodes_node.json")

        node: Node = node_service.get_node("node1.example.com")
        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "GET"
        assert "node1.example.com" in call_args[0][1]

        assert isinstance(node, Node)
        assert node.name == "node1.example.com"
        assert node.pip == "192.168.1.200"
        assert node.group_uuid == "4d3bf3ba-972e-49b0-8680-f783fb07a048"

    def test_evacuate_node(
        self,
        node_service: NodeService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)

        job_id = node_service.evacuate_node("node1.example.com")
        call_args = mock_http_client.request.call_args
        assert job_id == 123
        assert call_args[0][0] == "POST"
        assert "node1.example.com/evacuate" in call_args[0][1]

    def test_migrate_node(
        self,
        node_service: NodeService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)

        job_id = node_service.migrate_node("node1.example.com")
        call_args = mock_http_client.request.call_args
        assert job_id == 123
        assert call_args[0][0] == "POST"
        assert "node1.example.com/migrate" in call_args[0][1]

    def test_modify_node(
        self,
        node_service: NodeService,
        mock_http_client: MagicMock,
        mock_response: Callable[[Any, int], MagicMock],
    ) -> None:
        mock_http_client.request.return_value = mock_response(123, 200)

        job_id = node_service.modify_node("node1.example.com", offline=True)
        call_args = mock_http_client.request.call_args
        json: Dict[str, Any] = call_args.kwargs["json"]
        assert job_id == 123
        assert call_args[0][0] == "POST"
        assert "node1.example.com/modify" in call_args[0][1]
        assert "offline" in json and json["offline"]
