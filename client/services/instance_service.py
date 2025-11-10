import typing
from typing import Any

from client.api_client import BaseApiClient
from client.models.instance import InstanceInfo, NewInstance
from client.utils import dataclass_to_dict, dict_to_dataclass


class InstanceService:
    ENDPOINT = "instances"

    def __init__(self, api_client: BaseApiClient):
        self.api_client = api_client

    def get_instance_names(self) -> list[str]:
        instances = self.api_client.get(self.ENDPOINT)
        return [instance["id"] for instance in instances]

    def create_instance(
        self,
        new_instance: NewInstance,
        ip_check: bool = False,
        name_check: bool = False,
        start: bool = True,
        ignore_ipolicy: bool = False,
    ) -> int:
        params_raw = dataclass_to_dict(new_instance)
        # Ensure params is a dict for mypy
        if not isinstance(params_raw, dict):
            raise TypeError("Expected dataclass_to_dict to return a dict")
        params = params_raw
        params["__version__"] = 1
        params["mode"] = "create"
        return typing.cast(
            int,
            self.api_client.post(
                f"{self.ENDPOINT}",
                ip_check=ip_check,
                name_check=name_check,
                start=start,
                ignore_ipolicy=ignore_ipolicy,
                **params,
            ),
        )

    def modify_instance(self, instance_name: str, **kwargs: Any) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{instance_name}/modify", **kwargs))

    def delete_instance(self, instance_name: str) -> int:
        return typing.cast(int, self.api_client.delete(f"{self.ENDPOINT}/{instance_name}"))

    def start_instance(self, instance_name: str) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{instance_name}/startup"))

    def stop_instance(self, instance_name: str) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{instance_name}/shutdown"))

    def restart_instance(self, instance_name: str) -> int:
        return typing.cast(int, self.api_client.post(f"{self.ENDPOINT}/{instance_name}/reboot"))

    def migrate_instance(self, instance_name: str) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{instance_name}/migrate"))

    def failover_instance(self, instance_name: str) -> int:
        return typing.cast(int, self.api_client.put(f"{self.ENDPOINT}/{instance_name}/failover"))

    def grow_instance_disk(self, instance_name: str, disk_index: int, amount: int) -> int:
        return typing.cast(
            int, self.api_client.post(f"{self.ENDPOINT}/{instance_name}/disk/{disk_index}/grow", amount=amount)
        )

    def get_instance(self, instance_name: str) -> InstanceInfo:
        instance_info_raw = self.api_client.get(f"{self.ENDPOINT}/{instance_name}")
        # replace . with _ in keynames e.g. nic.ips -> nic_ips
        instance_info_raw = {key.replace(".", "_"): value for key, value in instance_info_raw.items()}
        return dict_to_dataclass(InstanceInfo, instance_info_raw)

    def get_instance_info(self, instance_name: str, static: bool = False) -> int:
        static_value = int(static)  # RAPI bool is 0 or 1 not 'true' or 'false'
        return typing.cast(int, self.api_client.get(f"{self.ENDPOINT}/{instance_name}/info", static=static_value))
