from typing import Any

from client.async_client.async_api_client import AsyncRAPIClient
from client.models.node import Node
from client.utils import dict_to_dataclass


class AsyncNodeService:
    _ENDPOINT = "nodes"

    def __init__(self, api_client: AsyncRAPIClient) -> None:
        self._api_client = api_client

    async def get_node_names(self) -> list[str]:
        nodes = await self._api_client.get(self._ENDPOINT)
        return [node["id"] for node in nodes]

    async def get_nodes(self) -> list[Node]:
        nodes_raw = await self._api_client.get(self._ENDPOINT, bulk=1)

        def replace_point(data_dict: dict[str, Any]) -> dict[str, Any]:
            return {key.replace(".", "_"): value for key, value in data_dict.items()}

        return [dict_to_dataclass(Node, replace_point(node_raw)) for node_raw in nodes_raw]

    async def get_node(self, node_name: str) -> Node:
        node_info_raw = await self._api_client.get(f"{self._ENDPOINT}/{node_name}")
        node_info_raw = {key.replace(".", "_"): value for key, value in node_info_raw.items()}
        return dict_to_dataclass(Node, node_info_raw)
