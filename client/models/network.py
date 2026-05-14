from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Network:
    name: str
    uuid: str
    network: str  # network_address
    gateway: str
    mac_prefix: str
    free_count: int
    reserved_count: int
    map: str
    group_list: List[str]
    external_reservations: str
    network6: Optional[str] = None
    gateway6: Optional[str] = None


@dataclass
class NewNetwork:
    network_name: str
    network: str  # network_address
    gateway: Optional[str] = None
    network6: Optional[str] = None
    gateway6: Optional[str] = None
    mac_prefix: Optional[str] = None
    tags: List[str] = field(default_factory=list)
