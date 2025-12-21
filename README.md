# Ganeti RAPI Client for Python

A modern, modular, and type-annotated client for the Ganeti Remote API (RAPI).
This library focuses on a clean architecture with typing for excellent editor support.

## Features

- Modern design with a focus on clarity and maintainability
- fully type-annotated API for first-class IDE autocompletion and static analysis (mypy)
- Modular architecture to keep concerns separated and extensible
- Minimal runtime dependencies (only `httpx`)
- Contains a synchronous and asynchronous client

## Requirements

- Python 3.9+
- `httpx`

## Installation

- From source:
  ```bash
  pip install .
  ```

## Usage

### synchronous client
```python
from client import GanetiRAPIClient

client = GanetiRAPIClient(
    "master.example.com:5080",
    "myuser",
    "mypassword",
    ssl_verify=False,
)

# get all instance names
instance_names = client.instance_service.get_instance_names()

# reboot an instance
reboot_job_id = client.instance_service.reboot_instance("my-instance")

# wait for the job to finish
job_result = client.job_service.wait_for_job(reboot_job_id)
if job_result.status == 'success':
    print("Instance rebooted successfully")
else:
    print("Instance reboot failed")
```

### asynchronous client
```python
import asyncio

from client import AsyncGanetiRAPIClient

async def main() -> None:
    client = AsyncGanetiRAPIClient(
        rapi_address="master.example.com:5080",
        username="myuser",
        password="mypassword",
        ssl_verify=False
    )

    instance_info = await client.instance_service.get_instance_info("my_instance.example.com")

    print(instance_info)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```