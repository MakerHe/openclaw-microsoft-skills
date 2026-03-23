# OpenClaw Skills

Python SDK and Agent Skill definitions for Microsoft 365 and Azure DevOps integration.

## Packages

| Package | PyPI | Import |
|---------|------|--------|
| `openclaw-microsoft-m365` | `pip install openclaw-microsoft-m365` | `from openclaw_microsoft_m365 import Microsoft365Client` |
| `openclaw-microsoft-azdo` | `pip install openclaw-microsoft-azdo` | `from openclaw_microsoft_azdo import AzureDevOpsClient` |

## Skills

| Skill | Description |
|-------|-------------|
| `skills/microsoft-365/` | Mail, calendar, OneDrive, Teams, OneNote, To Do, contacts, users, groups, SharePoint |
| `skills/azure-devops/` | Work items, repos, pull requests, pipelines, builds, releases, test plans, artifacts, wikis, boards |

## Setup

### 1. Install

```bash
# Microsoft 365 only
pip install openclaw-microsoft-m365

# Azure DevOps only
pip install openclaw-microsoft-azdo

# Both
pip install openclaw-microsoft-m365 openclaw-microsoft-azdo
```

### 2. Configure environment

Create `~/.openclaw/.env`:

```ini
# Microsoft 365 / Azure DevOps OAuth2
MICROSOFT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MICROSOFT_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# MICROSOFT_CLIENT_SECRET=your-secret-here  # optional, confidential client only

# Azure DevOps
AZURE_DEVOPS_ORG=your-org-name
AZURE_DEVOPS_PROJECT=your-project-name
# AZURE_DEVOPS_PAT=your-pat  # optional, alternative to OAuth2
```

```bash
mkdir -p ~/.openclaw/.credentials
chmod 600 ~/.openclaw/.env
```

### 3. App registration (Microsoft Entra ID)

1. **Azure Portal → Entra ID → App registrations → New registration**
2. Under **Authentication → Advanced settings**, set **Allow public client flows** to **Yes**
3. Add delegated **API permissions**:
   - **Microsoft Graph** — `Mail.Read`, `Mail.Send`, `Mail.ReadWrite`, `Calendars.ReadWrite`, `Files.ReadWrite.All`, `Notes.ReadWrite.All`, `Tasks.ReadWrite`, `Contacts.ReadWrite`, `User.Read`, `User.ReadBasic.All`, `Group.Read.All`, `Sites.ReadWrite.All`, `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `ChannelMessage.Send`, `ChatMessage.Send`
   - **Azure DevOps** — `user_impersonation` (resource: `499b84ac-1321-427f-aa17-267ca6975798`)
4. Copy **Application (client) ID** and **Directory (tenant) ID** into `~/.openclaw/.env`

### 4. First login

```python
# Microsoft 365
from openclaw_microsoft_m365 import Microsoft365Client

with Microsoft365Client.from_env() as client:
    client.authenticate()  # prints device-code URL on first run
    me = client.users_groups.get_me()
    print(me["displayName"])
```

```python
# Azure DevOps
from openclaw_microsoft_azdo import AzureDevOpsClient

with AzureDevOpsClient.from_env() as client:
    client.authenticate()  # skip if using PAT
    projects = client.projects_teams.list_projects()
    print(projects["value"])
```

Tokens are saved to `~/.openclaw/.credentials/`. Subsequent calls refresh silently.

## Credentials Layout

```
~/.openclaw/
├── .env
└── .credentials/
    ├── microsoft365.json
    ├── azuredevops.json
    └── refresh_token.json
```

## Development

### Prerequisites

- Python ≥ 3.10

### 1. Clone and create virtual environment

```bash
git clone <repo-url> && cd openclaw-skills

python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

### 2. Install dependencies (offline, from local sources)

All runtime dependencies (`httpx`, etc.) and dev dependencies (`pytest`, `respx`, etc.) are pre-downloaded into the `vendor/` directory. No PyPI access is needed during installation:

```bash
# Install third-party dependencies (offline, from vendor/)
pip install --no-index --find-links vendor -r requirements-dev.txt

# Install both local packages in editable mode (no remote fetching)
pip install --no-deps -e packages/openclaw-microsoft-m365
pip install --no-deps -e packages/openclaw-microsoft-azdo
```

> **Bootstrapping `vendor/` (requires internet, run once by maintainer):**
>
> ```bash
> pip download -r requirements-dev.txt -d vendor/
> git add vendor/
> ```
>
> After that, all other developers can install fully offline by cloning the repo.

### 3. Run tests

```bash
pytest packages/openclaw-microsoft-m365
pytest packages/openclaw-microsoft-azdo
```

## Project Structure

```
packages/
├── openclaw-microsoft-m365/    # Microsoft 365 SDK
├── openclaw-microsoft-azdo/    # Azure DevOps SDK
└── smoke-test.py               # End-to-end auth verification
skills/
├── microsoft-365/              # Agent skill definition + reference docs
└── azure-devops/               # Agent skill definition + reference docs
```

## License

MIT
