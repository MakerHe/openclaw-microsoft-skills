# OpenClaw Customize Skills

Custom AgentSkills for OpenClaw, providing Microsoft 365 and Azure DevOps integration via REST APIs.

## Skills

| Skill | Description |
|-------|-------------|
| **microsoft-365** | Microsoft Graph API — mail, calendar, OneDrive, Teams, OneNote, To Do, contacts, users, groups, SharePoint |
| **azure-devops** | Azure DevOps REST API — work items, repos, pull requests, pipelines, builds, releases, test plans, artifacts, wikis, boards |
| **shared/auth** | Shared Device Code Flow (OAuth2) authentication module used by both skills |

## Authentication

Both skills authenticate via **Microsoft Entra ID Device Code Flow**. A single user login can provide tokens for both Microsoft Graph and Azure DevOps.

### Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MICROSOFT_CLIENT_ID` | Yes | Application (client) ID from Entra ID app registration |
| `MICROSOFT_TENANT_ID` | No | Tenant ID (default: `common`) |
| `MICROSOFT_CLIENT_SECRET` | No | Client secret (only for confidential client apps) |
| `AZURE_DEVOPS_ORG` | For AZDO | Azure DevOps organization name |
| `AZURE_DEVOPS_PROJECT` | For AZDO | Default Azure DevOps project |

### How It Works

1. Authenticate once with Device Code Flow (scope: `https://graph.microsoft.com/.default offline_access`)
2. Receive an access token (Graph) + refresh token
3. Use the refresh token to silently acquire an Azure DevOps token — **no second login required**

See `skills/shared/auth/device-code-flow.md` for the full flow.

## Installation

Copy the `skills/` directory into your OpenClaw workspace:

```
~/.openclaw/workspace/skills/
├── azure-devops/
│   ├── SKILL.md
│   └── references/
├── microsoft-365/
│   ├── SKILL.md
│   └── references/
└── shared/
    └── auth/
        └── device-code-flow.md
```

## License

Internal use only.
