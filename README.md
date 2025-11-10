# Ganeti RAPI Client for Python

A modern, modular, and type-annotated client for the Ganeti Remote API (RAPI).
This library focuses on a clean architecture with typing for excellent editor support.

## Features

- Modern design with a focus on clarity and maintainability
- fully type-annotated API for first-class IDE autocompletion and static analysis (mypy)
- Modular architecture to keep concerns separated and extensible
- Minimal runtime dependencies (only `requests`)

## Requirements

- Python 3.9+
- `requests`

## Installation

- From source:
  ```bash
  pip install .
  ```

## Usage
```python
from client import GanetiRapiClient

client = GanetiRapiClient(
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