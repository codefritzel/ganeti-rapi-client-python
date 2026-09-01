from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from client.utils import dict_to_dataclass

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
    ops: List[Dict[str, Any]]
    summary: List[str]
    opstatus: List[Any]
    opresult: List[Any] = field(default_factory=list)

    # as unixtimestamp like time.time()
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def is_pending(self) -> bool:
        return self.status in JOB_STATUS_PENDING

    def is_finalized(self) -> bool:
        return self.status in JOB_STATUS_FINALIZED

    @staticmethod
    def from_job_dict(data: Dict[str, Any]) -> "Job":
        start_timestamp = None
        end_timestamp = None
        if data["start_ts"] is not None:
            start_timestamp = merge_time(data["start_ts"])
        if data["end_ts"] is not None:
            end_timestamp = merge_time(data["end_ts"])

        data["start_time"] = start_timestamp
        data["end_time"] = end_timestamp
        return dict_to_dataclass(Job, data)


def merge_time(timetuple: Tuple[int, int]) -> float:
    """Merges a tuple into time as a floating point number.
    @return: Time as a floating point number expressed in seconds
    """

    (seconds, microseconds) = timetuple
    return float(seconds) + (float(microseconds) * 0.000001)
