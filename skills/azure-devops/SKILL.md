---
name: azure-devops
description: Interact with Azure DevOps REST APIs - work items, repos, pull requests, pipelines, builds, releases, test plans, artifacts, wikis, boards, and more
---

# Azure DevOps Skill

Interact with Azure DevOps services via REST API using curl commands.

## Authentication Setup

Three environment variables are required:

- `AZURE_DEVOPS_PAT` — Personal Access Token
- `AZURE_DEVOPS_ORG` — Organization name (e.g., `myorg`)
- `AZURE_DEVOPS_PROJECT` — Default project name

All curl commands use PAT auth via base64-encoded `:$AZURE_DEVOPS_PAT`:

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1"
```

## API Base URLs

| Service | Base URL |
|---------|----------|
| Core (projects, teams, work items, git, builds, pipelines) | `https://dev.azure.com/$AZURE_DEVOPS_ORG` |
| Release Management | `https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG` |
| Artifacts / Feeds | `https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG` |
| Search | `https://almsearch.dev.azure.com/$AZURE_DEVOPS_ORG` |
| Graph & Identity | `https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG` |
| Audit | `https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG` |
| Extension Management | `https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG` |

All endpoints use `api-version=7.1`.

## Routing

Route the user's request to the appropriate reference file:

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

1. Verify `AZURE_DEVOPS_PAT`, `AZURE_DEVOPS_ORG`, and `AZURE_DEVOPS_PROJECT` are set before making any API calls.
2. Read the appropriate reference file for the endpoint patterns.
3. Execute curl commands via the Bash tool, substituting environment variables.
4. Parse JSON responses with `jq` when extracting specific fields.
5. For paginated results, follow `continuationToken` or `x-ms-continuationtoken` headers.
6. Always include `api-version=7.1` in query parameters.
7. For POST/PUT/PATCH, set `-H "Content-Type: application/json"` (or `application/json-patch+json` for work item updates).
