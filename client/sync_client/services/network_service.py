import typing
from typing import Any, List, Optional

from client.models.network import Network, NewNetwork
from client.sync_client.api_client import RAPIClient
from client.utils import dataclass_to_dict, dict_to_dataclass


class NetworkService:
    ENDPOINT = "networks"

    def __init__(self, api_client: RAPIClient):
        self.api_client = api_client

    def get_network_names(self) -> list[str]:
        networks = self.api_client.get(self.ENDPOINT)
        return [network["name"] for network in networks]

    def get_network(self, network_name: str) -> Network:
        network_raw = self.api_client.get(f"{self.ENDPOINT}/{network_name}")
        return dict_to_dataclass(Network, network_raw)

    def create_network(
        self,
        new_network: NewNetwork,
        conflicts_check: bool = False,
        add_reserved_ips: Optional[List[str]] = None,
    ) -> int:
        network_params = typing.cast(dict[str, Any], dataclass_to_dict(new_network))

        return typing.cast(
            int,
            self.api_client.post(
                f"{self.ENDPOINT}", conflicts_check=conflicts_check, add_reserved_ips=add_reserved_ips, **network_params
            ),
        )

    def delete_network(self, network_name: str) -> int:
        return typing.cast(int, self.api_client.delete(f"{self.ENDPOINT}/{network_name}"))

    def modify_network(self, network_name: str, **kwargs: Any) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{network_name}/modify", **kwargs))

    def connect_network(self, network_name: str, group_name: Optional[str] = None) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{network_name}/connect", group_name=group_name))

    def disconnect_network(self, network_name: str, group_name: Optional[str] = None) -> int:
        return typing.cast(
            int, self.api_client.put(f"{self.ENDPOINT}/{network_name}/disconnect", group_name=group_name)
        )

    def rename_network(self, network_name: str, new_name: str) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{network_name}/rename", new_name=new_name))
