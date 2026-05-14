import typing
from typing import Any, Optional

from client.models.node import Node
from client.sync_client.api_client import RAPIClient
from client.utils import dict_to_dataclass


class NodeService:
    ENDPOINT = "nodes"

    def __init__(self, api_client: RAPIClient):
        self.api_client = api_client

    def get_node_names(self) -> list[str]:
        nodes = self.api_client.get(self.ENDPOINT)
        return [node["id"] for node in nodes]

    def get_node(self, node_name: str) -> Node:
        node_info_raw = self.api_client.get(f"{self.ENDPOINT}/{node_name}")
        node_info_raw = {key.replace(".", "_"): value for key, value in node_info_raw.items()}
        return dict_to_dataclass(Node, node_info_raw)

    def evacuate_node(
        self,
        node_name: str,
        early_release: bool = False,
        iallocator: Optional[str] = None,
        ignore_soft_errors: bool = False,
        mode: Optional[str] = None,
        remote_node: Optional[str] = None,
    ) -> int:
        return typing.cast(
            int,
            self.api_client.post(
                f"{self.ENDPOINT}/{node_name}/evacuate",
                early_release=early_release,
                iallocator=iallocator,
                ignore_soft_errors=ignore_soft_errors,
                mode=mode,
                remote_node=remote_node,
            ),
        )

    def migrate_node(
        self,
        node_name: str,
        allow_runtime_changes: bool = True,
        iallocator: Optional[str] = None,
        mode: Optional[str] = None,
        target_node: Optional[str] = None,
    ) -> int:
        return typing.cast(
            int,
            self.api_client.post(
                f"{self.ENDPOINT}/{node_name}/migrate",
                allow_runtime_changes=allow_runtime_changes,
                iallocator=iallocator,
                mode=mode,
                target_node=target_node,
            ),
        )

    def modify_node(self, node_name: str, **kwargs: Any) -> int:
        return typing.cast(int, self.api_client.post(f"{self.ENDPOINT}/{node_name}/modify", **kwargs))
