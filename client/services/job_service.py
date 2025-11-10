import time

from client.api_client import BaseApiClient
from client.models.job import Job
from client.utils import dict_to_dataclass


class JobService:
    ENDPOINT = "jobs"

    def __init__(self, api_client: BaseApiClient):
        self.api_client = api_client

    def get_jobs(self) -> list[int]:
        jobs_raw = self.api_client.get(self.ENDPOINT)
        return [job["id"] for job in jobs_raw]

    def get_job_info(self, job_id: int) -> Job:
        job_raw = self.api_client.get(f"{self.ENDPOINT}/{job_id}")
        return dict_to_dataclass(Job, job_raw)

    def cancel_job(self, job_id: int) -> None:
        self.api_client.delete(f"{self.ENDPOINT}/{job_id}")

    def wait_for_job(self, job_id: int, timeout: int = 300, poll_interval: int = 5) -> Job:
        job_info = self.get_job_info(job_id)
        start_time = time.time()
        while not job_info.is_finalized():
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Job {job_id} timed out after {timeout} seconds")
            time.sleep(poll_interval)
            job_info = self.get_job_info(job_id)

        return job_info
