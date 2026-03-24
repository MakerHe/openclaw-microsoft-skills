---
name: azure-devops
description: Interact with Azure DevOps REST APIs using the openclaw-microsoft-azdo Python SDK — work items, repos, pull requests, pipelines, builds, releases, test plans, artifacts, wikis, boards, and more
---

# Azure DevOps Skill

Interact with Azure DevOps services using the `openclaw-microsoft-azdo` Python SDK.

## Package

```bash
pip install openclaw-microsoft-azdo
```

## Authentication

Environment variables are stored in `~/.openclaw/.env` (read automatically by `from_env()`). Login tokens are persisted in `~/.openclaw/credentials/`.

| Variable | Required | Description |
|----------|----------|-------------|
| `AZURE_DEVOPS_ORG` | Yes | Organization name |
| `AZURE_DEVOPS_PROJECT` | Yes | Default project name |
| `AZURE_DEVOPS_PAT` | No* | Personal Access Token |
| `MICROSOFT_CLIENT_ID` | No* | Application (client) ID for OAuth2 |
| `MICROSOFT_TENANT_ID` | No | Tenant ID (default: `common`) |
| `MICROSOFT_CLIENT_SECRET` | No | Client secret (optional) |

\* Provide either `AZURE_DEVOPS_PAT` or `MICROSOFT_CLIENT_ID`.

### Construct and authenticate

```python
from openclaw_microsoft_azdo import AzureDevOpsClient

client = AzureDevOpsClient.from_env()
client.authenticate()   # only needed for OAuth2; skip for PAT
```

`from_env()` raises `ValueError` if `AZURE_DEVOPS_ORG`, `AZURE_DEVOPS_PROJECT`, or an auth credential is missing.

### Auth method selection

| Condition | Auth used |
|-----------|-----------|
| `AZURE_DEVOPS_PAT` is set | PAT (Basic auth) — `authenticate()` not needed |
| `MICROSOFT_CLIENT_ID` is set | Device Code Flow (Bearer) — call `authenticate()` |

### `authenticate()` behaviour (OAuth2 only)

- **Token valid** — prints `"Authentication successful (existing token is still valid)."`.
- **Silent refresh** — acquires a new token silently from the saved refresh token.
- **First run** — prints a device-code URL + code; blocks until login completes.
- **Expired** — clears stale credentials and falls back to device-code flow.

After `authenticate()` the client attaches the correct auth header to every request automatically.

## Routing

| Topic | Reference |
|-------|-----------|
| Auth, base URLs, API versioning | `references/auth-and-setup.md` |
| Work items (create, query, update, WIQL) | `references/work-items.md` |
| Git repos, pull requests, branches, commits | `references/git-repos.md` |
| YAML pipelines (runs, definitions) | `references/pipelines.md` |
| Classic builds | `references/builds.md` |
| Release management (classic releases) | `references/releases.md` |
| Test plans, suites, cases, runs, results | `references/test-plans.md` |
| Azure Artifacts, feeds, packages | `references/artifacts.md` |
| Wiki pages | `references/wiki.md` |
| Projects, teams, processes | `references/projects-teams.md` |
| Boards, backlogs, sprints, iterations | `references/boards-backlogs.md` |
| Service hooks (subscriptions, events) | `references/service-hooks.md` |
| Security namespaces, ACLs, permissions | `references/security-permissions.md` |
| Graph users, groups, memberships | `references/graph-identity.md` |
| Dashboards, widgets | `references/dashboards.md` |
| Code/work item/wiki search | `references/search.md` |
| Notifications, subscriptions | `references/notifications.md` |
| Audit logs | `references/audit.md` |
| Extensions | `references/extensions.md` |
| Service connections / endpoints | `references/service-endpoints.md` |
| Branch policies | `references/policy.md` |

## Instructions

1. **Authenticate** — `AzureDevOpsClient.from_env()` then `client.authenticate()` (OAuth2 only). If `from_env()` raises `ValueError`, tell the user which variable is missing and stop.
2. **Route** — read the appropriate reference file for the user's request.
3. **Execute** — call methods on the client's service attributes (`client.work_items`, `client.git_repos`, etc.).
4. **Parse** — extract and present relevant fields from the returned data.
5. **Paginate** — follow `continuationToken` for paginated results.
6. **Cleanup** — call `client.close()` or use `with AzureDevOpsClient.from_env() as client:`.
