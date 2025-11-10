from client.api_client import BaseApiClient
from client.services.instance_service import InstanceService
from client.services.job_service import JobService
from client.services.node_service import NodeService


class GanetiRapiClient:
    def __init__(self, rapi_address: str, username: str, password: str, ssl_verify: bool = True):
        self._client = BaseApiClient(rapi_address, username, password, ssl_verify=ssl_verify)
        self.instance_service = InstanceService(self._client)
        self.job_service = JobService(self._client)
        self.node_service = NodeService(self._client)
