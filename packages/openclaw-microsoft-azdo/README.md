# openclaw-microsoft-azdo

Python SDK for Azure DevOps REST APIs.

## Installation

```bash
pip install openclaw-microsoft-azdo
```

## Quick Start

```python
from openclaw_microsoft_azdo import AzureDevOpsClient

client = AzureDevOpsClient.from_env()
client.authenticate()

# Work items, repos, pipelines, boards, etc.
items = client.work_items.list(query="SELECT [System.Id] FROM WorkItems")
```
