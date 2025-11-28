import asyncio
import typing
from typing import Any, Callable, Coroutine

from client.async_client.services.async_job_service import AsyncJobService
from client.models.job import JOB_STATUS_SUCCESS, Job


class MaxRetriesExceededError(Exception):
    def __init__(self, max_retries: int) -> None:
        self.max_retries = max_retries


class JobFailedError(Exception):
    def __init__(self, job: Job) -> None:
        self.job = job


class AsyncJobRunner:
    def __init__(self, job_service: AsyncJobService):
        self._job_service = job_service

    async def wait_for_job(
        self, job_id: int, max_retries: int = -1, retry_interval: int = 5, init_interval: int = 1
    ) -> Job:
        await asyncio.sleep(init_interval)
        job = await self._job_service.get_job_info(job_id)
        retries = 0

        while (retries < max_retries or max_retries == -1) and not job.is_finalized():
            await asyncio.sleep(retry_interval)
            job = await self._job_service.get_job_info(job_id)
            retries += 1

        if not job.is_finalized():
            raise MaxRetriesExceededError(max_retries)

        return job

    async def run_and_wait_for_success(
        self,
        start_job_func: Callable[[], Coroutine[Any, Any, Any]],
        max_retries: int = -1,
        retry_interval: int = 5,
        init_interval: int = 1,
    ) -> Job:
        job_id = typing.cast(int, await start_job_func())

        job = await self.wait_for_job(job_id, max_retries, retry_interval, init_interval)

        if job.status != JOB_STATUS_SUCCESS:
            raise JobFailedError(job)

        return job
