from typing import Any, Callable, List

import pytest

from client.async_client.job_runner import AsyncJobRunner, JobFailedError, MaxRetriesExceededError
from client.models.job import Job


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_sleep(delay: int, *args: Any, **kwargs: Any) -> None:
        # do nothing
        return None

    monkeypatch.setattr("asyncio.sleep", fake_sleep)


async def fake_job_run() -> int:
    return 1


class TestAsyncJobRunnerWaitForJob:
    @pytest.mark.asyncio
    async def test_job_finished_after_first_query(
        self, async_job_runner: AsyncJobRunner, fake_get_job: Callable[[List[Job]], None]
    ) -> None:
        fake_get_job([Job(1, "success", [], [], [])])

        job = await async_job_runner.wait_for_job(1)

        assert job.status == "success"

    @pytest.mark.asyncio
    async def test_job_not_finished_in_retries(
        self, async_job_runner: AsyncJobRunner, fake_get_job: Callable[[List[Job]], None]
    ) -> None:
        fake_get_job([Job(1, "running", [], [], []), Job(1, "running", [], [], []), Job(1, "running", [], [], [])])

        with pytest.raises(MaxRetriesExceededError) as excinfo:
            await async_job_runner.wait_for_job(1, max_retries=2)

        assert excinfo.value.max_retries == 2


class TestAsyncJobRunnerRunAndWaitForSuccess:
    @pytest.mark.asyncio
    async def test_job_successful(
        self, async_job_runner: AsyncJobRunner, fake_get_job: Callable[[List[Job]], None]
    ) -> None:
        fake_get_job(
            [
                Job(1, "running", [], [], []),
                Job(1, "success", [], [], []),
            ]
        )

        job = await async_job_runner.run_and_wait_for_success(fake_job_run, 1)

        assert job.status == "success"
        assert job.id == 1

    @pytest.mark.asyncio
    async def test_job_error(self, async_job_runner: AsyncJobRunner, fake_get_job: Callable[[List[Job]], None]) -> None:
        fake_get_job(
            [
                Job(1, "running", [], [], []),
                Job(1, "error", [], [], []),
            ]
        )

        with pytest.raises(JobFailedError):
            await async_job_runner.run_and_wait_for_success(fake_job_run, 1)
