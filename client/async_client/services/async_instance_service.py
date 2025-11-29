import typing
from typing import Any, Dict, List

from client.async_client.async_api_client import AsyncApiClient
from client.async_client.job_runner import AsyncJobRunner
from client.models.instance import InstanceInfo, NewInstance
from client.utils import dataclass_to_dict


class AsyncInstanceService:
    _ENDPOINT = "instances"

    def __init__(self, api_client: AsyncApiClient, job_runner: AsyncJobRunner) -> None:
        self._api_client = api_client
        self._job_runner = job_runner

    async def get_instance_names(self) -> List[str]:
        instances = await self._api_client.get(self._ENDPOINT)
        return [instance["id"] for instance in instances]

    async def get_instances(self) -> List[InstanceInfo]:
        instances_raw = await self._api_client.get(self._ENDPOINT, bulk=1)
        return [InstanceInfo.from_instance_dict(instance) for instance in instances_raw]

    async def create_instance(
        self,
        new_instance: NewInstance,
        ip_check: bool = False,
        name_check: bool = False,
        start: bool = True,
        ignore_ipolicy: bool = False,
    ) -> None:
        params_raw = dataclass_to_dict(new_instance)
        # Ensure params is a dict for mypy
        if not isinstance(params_raw, dict):
            raise TypeError("Expected dataclass_to_dict to return a dict")
        params = params_raw
        params["__version__"] = 1
        params["mode"] = "create"
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.post(
                f"{self._ENDPOINT}",
                ip_check=ip_check,
                name_check=name_check,
                start=start,
                ignore_ipolicy=ignore_ipolicy,
                **params,
            )
        )

    async def modify_instance(self, instance_name: str, **kwargs: Any) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.put(f"{self._ENDPOINT}/{instance_name}/modify", **kwargs)
        )

    async def delete_instance(self, instance_name: str) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.delete(f"{self._ENDPOINT}/{instance_name}")
        )

    async def start_instance(self, instance_name: str) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.put(f"{self._ENDPOINT}/{instance_name}/startup")
        )

    async def stop_instance(self, instance_name: str) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.put(f"{self._ENDPOINT}/{instance_name}/shutdown")
        )

    async def restart_instance(self, instance_name: str) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.post(f"{self._ENDPOINT}/{instance_name}/reboot")
        )

    async def migrate_instance(self, instance_name: str) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.put(f"{self._ENDPOINT}/{instance_name}/migrate")
        )

    async def failover_instance(self, instance_name: str) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.put(f"{self._ENDPOINT}/{instance_name}/failover")
        )

    async def grow_instance_disk(self, instance_name: str, disk_index: int, amount: int) -> None:
        await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.post(f"{self._ENDPOINT}/{instance_name}/disk/{disk_index}/grow", amount=amount)
        )

    async def get_instance(self, instance_name: str) -> InstanceInfo:
        instance_info_raw = await self._api_client.get(f"{self._ENDPOINT}/{instance_name}")
        return InstanceInfo.from_instance_dict(instance_info_raw)

    async def get_instance_info(self, instance_name: str, static: bool = False) -> Dict[str, Any]:
        static_value = int(static)
        job_result_raw = await self._job_runner.run_and_wait_for_success(
            lambda: self._api_client.get(f"{self._ENDPOINT}/{instance_name}/info", static_value=static_value),
            retry_interval=2,
        )

        return typing.cast(Dict[str, Any], job_result_raw.opresult[0][instance_name])
