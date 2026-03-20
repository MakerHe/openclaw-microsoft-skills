# Audit Log API

Base: `https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/audit`

**Note**: Audit APIs use the `auditservice.dev.azure.com` host.

## Query Audit Logs

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/audit/auditlog?api-version=7.1" | jq '.decoratedAuditLogEntries[:5]'
```

### With Filters

```bash
# Filter by date range
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/audit/auditlog?startTime=2024-01-01T00:00:00Z&endTime=2024-01-31T23:59:59Z&api-version=7.1"

# Filter by area (e.g., Git, Pipelines)
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/audit/auditlog?api-version=7.1" | jq '[.decoratedAuditLogEntries[] | select(.areaName == "Git")]'
```

### Pagination

```bash
# Use continuationToken from response
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/audit/auditlog?continuationToken={token}&api-version=7.1"
```

## Download Audit Log

```bash
# Download as JSON
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/audit/downloadlog?format=json&startTime=2024-01-01&endTime=2024-01-31&api-version=7.1" \
  -o audit-log.json
```

## Audit Actions

```bash
# List all available audit actions
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://auditservice.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/audit/actions?api-version=7.1"
```

## Common Audit Areas

| Area | Description |
|------|-------------|
| `Git` | Repository and branch operations |
| `Pipelines` | Pipeline runs and changes |
| `Release` | Release management |
| `Security` | Permission changes |
| `Policy` | Branch policy changes |
| `Group` | Group membership changes |
| `Project` | Project-level changes |
| `Organization` | Organization settings |
| `Licensing` | License changes |
| `Extensions` | Extension install/uninstall |

## Audit Log Entry Fields

| Field | Description |
|-------|-------------|
| `id` | Unique audit event ID |
| `correlationId` | Groups related events |
| `activityId` | Activity identifier |
| `actorUserId` | User who performed action |
| `actorDisplayName` | Display name of actor |
| `timestamp` | When the event occurred |
| `areaName` | Service area (Git, Pipelines, etc.) |
| `category` | Category (Modify, Remove, Create, Access) |
| `details` | Human-readable description |
| `actionId` | Machine-readable action ID |
| `projectName` | Project (if applicable) |
| `scopeType` | Scope (Organization, Project) |
