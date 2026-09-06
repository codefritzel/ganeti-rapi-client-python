from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Node:
    name: str
    offline: bool
    master_candidate: bool
    drained: bool
    dtotal: Optional[int]
    dfree: Optional[int]
    sptotal: Optional[int]
    spfree: Optional[int]
    mtotal: Optional[int]
    mnode: Optional[int]
    mfree: Optional[int]
    pinst_cnt: int
    sinst_cnt: int
    ctotal: Optional[int]
    cnos: Optional[int]
    cnodes: Optional[int]
    csockets: Optional[int]
    pip: str
    sip: str
    role: str
    pinst_list: list[str]
    sinst_list: list[str]
    master_capable: bool
    vm_capable: bool
    ndparams: Dict[str, Any]
    ctime: float
    group_uuid: str
    mtime: float
    uuid: str
    serial_no: int
    tags: list[str]

    def is_master(self) -> bool:
        return self.role == "M"
