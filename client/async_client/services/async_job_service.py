from typing import List

from client.async_client.async_api_client import AsyncRAPIClient
from client.models.job import Job


class AsyncJobService:
    _ENDPOINT = "jobs"

    def __init__(self, api_client: AsyncRAPIClient) -> None:
        self.api_client = api_client

    async def get_job_ids(self) -> List[int]:
        jobs_raw = await self.api_client.get(self._ENDPOINT)
        return [job["id"] for job in jobs_raw]

    async def get_jobs(self) -> List[Job]:
        jobs_raw = await self.api_client.get(self._ENDPOINT, bulk=1)
        return [Job.from_job_dict(job) for job in jobs_raw]

    async def get_job_info(self, job_id: int) -> Job:
        job_raw = await self.api_client.get(f"{self._ENDPOINT}/{job_id}")
        return Job.from_job_dict(job_raw)

    async def cancel_job(self, job_id: int) -> None:
        await self.api_client.delete(f"{self._ENDPOINT}/{job_id}")
