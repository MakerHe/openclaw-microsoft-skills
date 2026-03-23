# Authentication & Setup

## Installation

```bash
pip install openclaw-microsoft-azdo
```

## Environment Variables

Store in `~/.openclaw/.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_DEVOPS_ORG` | Organization name | `myorg` |
| `AZURE_DEVOPS_PROJECT` | Default project name | `MyProject` |
| `AZURE_DEVOPS_PAT` | Personal Access Token | `xxxxxxxx...` |
| `MICROSOFT_CLIENT_ID` | App ID for OAuth2 | `xxxxxxxx-xxxx-...` |
| `MICROSOFT_TENANT_ID` | Tenant ID (default: `common`) | `common` |

## Quick Start

```python
from openclaw_microsoft_azdo import AzureDevOpsClient

client = AzureDevOpsClient.from_env()
client.authenticate()   # OAuth2 only; skip for PAT

# Use services
projects = client.projects_teams.list_projects()
print(projects["value"])

client.close()
```

Or as a context manager:

```python
with AzureDevOpsClient.from_env() as client:
    client.authenticate()
    projects = client.projects_teams.list_projects()
```

## API Versioning

All endpoints use `api-version=7.1`. Preview APIs use `7.1-preview.x`.

## Pagination

Many list endpoints return `continuationToken` in the body or `x-ms-continuationtoken` in the response header. Pass it as a query parameter in the next request.
