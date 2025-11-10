from typing import Callable
from unittest.mock import MagicMock

import pytest

from client.api_client import BaseApiClient
from client.models.node import Node
from client.services.node_service import NodeService


@pytest.fixture
def node_service(api_client: BaseApiClient) -> NodeService:
    return NodeService(api_client)


class TestNodeService:
    def test_get_node_names(
        self,
        node_service: NodeService,
        mock_session: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_session.request.return_value = mock_response_from_jsonfile("v2_get_nodes.json")

        names = node_service.get_node_names()

        call_args = mock_session.request.call_args
        assert call_args[0][0] == "GET"  # Check right Request
        assert len(names) == 3
        assert "node1.example.com" in names
        assert "node2.example.com" in names
        assert "node3.example.com" in names

    def test_get_node(
        self,
        node_service: NodeService,
        mock_session: MagicMock,
        mock_response_from_jsonfile: Callable[[str], MagicMock],
    ) -> None:
        mock_session.request.return_value = mock_response_from_jsonfile("v2_get_nodes_node.json")

        node: Node = node_service.get_node("node1.example.com")
        call_args = mock_session.request.call_args
        assert call_args[0][0] == "GET"
        assert "node1.example.com" in call_args[0][1]

        assert isinstance(node, Node)
        assert node.name == "node1.example.com"
        assert node.pip == "192.168.1.200"
        assert node.group_uuid == "4d3bf3ba-972e-49b0-8680-f783fb07a048"
