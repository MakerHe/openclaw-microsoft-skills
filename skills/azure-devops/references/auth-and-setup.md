# Authentication & Setup

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_DEVOPS_PAT` | Personal Access Token | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `AZURE_DEVOPS_ORG` | Organization name | `myorg` |
| `AZURE_DEVOPS_PROJECT` | Default project name | `MyProject` |

## PAT Authentication

Azure DevOps REST API uses Basic auth with an empty username and PAT as password:

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1"
```

Alternatively, manually encode the header:

```bash
B64_PAT=$(printf ":%s" "$AZURE_DEVOPS_PAT" | base64)
curl -s -H "Authorization: Basic $B64_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1"
```

## Base URLs

| Service | Base URL |
|---------|----------|
| Core APIs | `https://dev.azure.com/{org}` |
| Release Management | `https://vsrm.dev.azure.com/{org}` |
| Artifacts / Feeds | `https://feeds.dev.azure.com/{org}` |
| Search | `https://almsearch.dev.azure.com/{org}` |
| Graph & Identity | `https://vssps.dev.azure.com/{org}` |
| Audit | `https://auditservice.dev.azure.com/{org}` |
| Extension Management | `https://extmgmt.dev.azure.com/{org}` |

## API Versioning

All requests must include `api-version=7.1` as a query parameter. Preview APIs append a preview suffix: `api-version=7.1-preview.1`.

## Pagination

Many list endpoints return paginated results:

- Response includes `continuationToken` in the body or `x-ms-continuationtoken` in the response header.
- Pass it as `continuationToken={token}` query parameter in the next request.
- Continue until no token is returned.

```bash
# First page
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/wiql?api-version=7.1" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project"}'

# Subsequent page (if continuationToken returned)
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/wiql?api-version=7.1&continuationToken={token}" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project"}'
```

## Common Headers

| Header | Value | When |
|--------|-------|------|
| `Content-Type` | `application/json` | POST/PUT/PATCH (most endpoints) |
| `Content-Type` | `application/json-patch+json` | Work item create/update |
| `Accept` | `application/json` | Default for all requests |

## Checking Connection

```bash
# Verify PAT and org by listing projects
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1" | jq '.value[].name'
```
