from client.api_client import BaseApiClient
from client.models.node import Node
from client.utils import dict_to_dataclass


class NodeService:
    ENDPOINT = "nodes"

    def __init__(self, api_client: BaseApiClient):
        self.api_client = api_client

    def get_node_names(self) -> list[str]:
        nodes = self.api_client.get(self.ENDPOINT)
        return [node["id"] for node in nodes]

    def get_node(self, node_name: str) -> Node:
        node_info_raw = self.api_client.get(f"{self.ENDPOINT}/{node_name}")
        node_info_raw = {key.replace(".", "_"): value for key, value in node_info_raw.items()}
        return dict_to_dataclass(Node, node_info_raw)
