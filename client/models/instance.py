from dataclasses import dataclass
from typing import Any, Dict, Optional

from client.utils import dict_to_dataclass


@dataclass
class BackendParams:
    vcpus: int
    memory: int
    minmem: Optional[int] = None
    maxmem: Optional[int] = None
    always_failover: Optional[bool] = None
    auto_balance: Optional[bool] = None
    spindle_use: Optional[bool] = None


@dataclass
class InstanceInfo:
    name: str
    admin_state: str
    os: str
    pnode: str
    snodes: list[str]
    disk_template: str
    nic_ips: list[str]
    nic_macs: list[str]
    nic_modes: list[str]
    nic_uuids: list[str]
    nic_names: list[Optional[str]]
    nic_links: list[str]
    nic_networks: list[str]
    nic_networks_names: list[str]
    nic_bridges: list[str]
    network_port: int
    disk_sizes: list[int]
    disk_spindles: list[Any]
    disk_uuids: list[str]
    disk_names: list[Optional[str]]
    disk_usage: int
    beparams: BackendParams
    hvparams: dict[str, Any]
    oper_state: bool
    oper_ram: int
    oper_vcpus: int
    #    custom_hvparams: Dict[str, Any]
    #    custom_beparams: Dict[str, Any]
    #    custom_nicparams: Dict[str, Any]
    status: str
    ctime: float
    mtime: float
    uuid: str
    serial_no: int
    tags: list[str]

    @staticmethod
    def from_instance_dict(instance_dict_raw: Dict[str, Any]) -> "InstanceInfo":
        # replace . with _ in keynames e.g. nic.ips -> nic_ips
        instance_dict_raw = {key.replace(".", "_"): value for key, value in instance_dict_raw.items()}

        return dict_to_dataclass(InstanceInfo, instance_dict_raw)


@dataclass
class NewInstance:
    name: str
    disk_template: str
    disks: list[dict[str, str]]
    nics: list[dict[str, Any]]
    os: str
    osparams: Optional[dict[str, Any]] = None
    pnode: Optional[str] = None
    snode: Optional[str] = None
    hvparams: Optional[dict[str, Any]] = None
    beparams: Optional[BackendParams] = None
