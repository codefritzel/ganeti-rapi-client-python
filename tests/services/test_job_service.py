from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest

from client.models.job import JOB_STATUS_RUNNING, JOB_STATUS_SUCCESS, Job
from client.services.job_service import JobService


def _time_seq(values: list[float]) -> Iterator[float]:
    it = iter(values)

    def _next() -> float:
        return next(it)

    return _next  # type: ignore[return-value]


class TestJobService:
    def test_wait_for_job(self, monkeypatch: pytest.MonkeyPatch) -> None:
        service = JobService(api_client=MagicMock())

        # --- Scenario 1: job transitions from running to success ---
        pending = Job(id=1, status=JOB_STATUS_RUNNING, ops=[], opstatus=[], opresult=[])
        success = Job(id=1, status=JOB_STATUS_SUCCESS, ops=[], opstatus=[], opresult=[])

        get_job_info_mock_success = MagicMock(side_effect=[pending, success])
        monkeypatch.setattr(service, "get_job_info", get_job_info_mock_success)

        # time: start at 1000.0, then advance slightly (no timeout)
        monkeypatch.setattr("client.services.job_service.time.time", _time_seq([1000.0, 1001.0]))
        sleep_mock_success = MagicMock()
        monkeypatch.setattr("client.services.job_service.time.sleep", sleep_mock_success)

        result = service.wait_for_job(job_id=1, timeout=300, poll_interval=5)

        assert isinstance(result, Job)
        assert result.status == JOB_STATUS_SUCCESS
        # First call before loop + one poll inside loop
        assert get_job_info_mock_success.call_count == 2
        # One sleep between the two get calls
        sleep_mock_success.assert_called_once()

        # --- Scenario 2: immediate timeout on first loop check ---
        pending2 = Job(id=2, status=JOB_STATUS_RUNNING, ops=[], opstatus=[], opresult=[])
        get_job_info_mock_timeout = MagicMock(return_value=pending2)
        monkeypatch.setattr(service, "get_job_info", get_job_info_mock_timeout)

        timeout = 300
        # start_time, then immediately past the timeout on first loop iteration
        monkeypatch.setattr(
            "client.services.job_service.time.time",
            _time_seq([2000.0, 2000.0 + timeout + 1.0]),
        )
        sleep_mock_timeout = MagicMock()
        monkeypatch.setattr("client.services.job_service.time.sleep", sleep_mock_timeout)

        with pytest.raises(TimeoutError) as exc:
            service.wait_for_job(job_id=2, timeout=timeout, poll_interval=5)

        assert f"Job 2 timed out after {timeout} seconds" in str(exc.value)
        # Only the initial get_job_info call should occur before timeout is detected
        assert get_job_info_mock_timeout.call_count == 1
        # sleep should not be called because timeout is detected before sleeping
        sleep_mock_timeout.assert_not_called()
