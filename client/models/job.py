from dataclasses import dataclass
from typing import Any, Dict

JOB_STATUS_QUEUED = "queued"
JOB_STATUS_WAITING = "waiting"
JOB_STATUS_CANCELING = "canceling"
JOB_STATUS_RUNNING = "running"
JOB_STATUS_CANCELED = "canceled"
JOB_STATUS_SUCCESS = "success"
JOB_STATUS_ERROR = "error"

JOB_STATUS_PENDING = [
    JOB_STATUS_QUEUED,
    JOB_STATUS_WAITING,
    JOB_STATUS_CANCELING,
]

JOB_STATUS_FINALIZED = [
    JOB_STATUS_CANCELED,
    JOB_STATUS_SUCCESS,
    JOB_STATUS_ERROR,
]


@dataclass
class Job:
    id: int
    status: str
    ops: list[Dict[str, Any]]
    opstatus: list[Any]
    opresult: list[Any]

    def is_pending(self) -> bool:
        return self.status in JOB_STATUS_PENDING

    def is_finalized(self) -> bool:
        return self.status in JOB_STATUS_FINALIZED
