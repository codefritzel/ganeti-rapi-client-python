from dataclasses import dataclass
from typing import Any, Dict, Optional

from client.utils import dict_to_dataclass

# Instance status
INSTANCE_STATE_RUNNING = "running"

INSTANCE_STATE_ADMIN_DOWN = "ADMIN_down"
INSTANCE_STATE_ERROR_DOWN = "ERROR_down"

INSTANCE_STATE_DOWN = [
    INSTANCE_STATE_ADMIN_DOWN,
    INSTANCE_STATE_ERROR_DOWN,
]


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
class NetworkInfo:
    name: str
    uuid: str


@dataclass
class InstanceNic:
    name: str
    uuid: str
    ip: str
    mac: str
    mode: str
    link: str
    bridge: str
    #    vlan: str
    network: NetworkInfo


@dataclass
class InstanceDisk:
    name: str
    uuid: str
    size: int
    spindle: bool


@dataclass
class InstanceInfo:
    name: str
    admin_state: str
    os: str
    pnode: str
    snodes: list[str]
    disk_template: str
    nics: list[InstanceNic]
    network_port: int
    disks: list[InstanceDisk]
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

    def is_running(self) -> bool:
        return self.status == INSTANCE_STATE_RUNNING

    def is_stopped(self) -> bool:
        return self.status in INSTANCE_STATE_DOWN

    @staticmethod
    def from_instance_dict(instance_dict_raw: Dict[str, Any]) -> "InstanceInfo":
        nics: list[Dict[str, Any]] = []
        disks: list[Dict[str, Any]] = []
        for key, value in instance_dict_raw.items():
            if key.startswith("nic.") and key.endswith("s"):
                new_key = key.replace("nic.", "")[:-1]  # nic.ips -> ip
                for idx, item in enumerate(value):
                    if len(nics) <= idx:
                        nics.append({})
                    nics[idx][new_key] = item

            if key.startswith("disk."):
                new_key = key.replace("disk.", "")[:-1]  # disk.sizes -> size
                for idx, item in enumerate(value):
                    if len(disks) <= idx:
                        disks.append({})
                    disks[idx][new_key] = item

        # remove the old nic. and disk. keys
        for key in list(instance_dict_raw.keys()):
            if key.startswith(("disk.", "nic.")):
                del instance_dict_raw[key]

        instance_dict_raw["disks"] = disks
        instance_dict_raw["nics"] = nics

        return dict_to_dataclass(InstanceInfo, instance_dict_raw)


@dataclass
class NewInstance:
    instance_name: str
    disk_template: str
    disks: list[dict[str, str]]
    nics: list[dict[str, Any]]
    os: str
    osparams: Optional[dict[str, Any]] = None
    pnode: Optional[str] = None
    snode: Optional[str] = None
    hvparams: Optional[dict[str, Any]] = None
    beparams: Optional[BackendParams] = None
