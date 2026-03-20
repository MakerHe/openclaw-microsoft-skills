# Release Management API

Base: `https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release`

**Note**: Release Management uses the `vsrm.dev.azure.com` host.

## List Release Definitions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/definitions?api-version=7.1"
```

## Get a Release Definition

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/definitions/{definitionId}?api-version=7.1"
```

## Create a Release

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases?api-version=7.1" \
  -d '{
    "definitionId": {definitionId},
    "description": "Release via API",
    "artifacts": [
      {
        "alias": "{artifactAlias}",
        "instanceReference": {
          "id": "{buildId}",
          "name": null
        }
      }
    ]
  }'
```

## List Releases

```bash
# Recent releases
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases?api-version=7.1&\$top=20"

# By definition
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases?definitionId={definitionId}&api-version=7.1"
```

## Get a Release

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases/{releaseId}?api-version=7.1"
```

## Update Release Environment (Deploy)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases/{releaseId}/environments/{environmentId}?api-version=7.1" \
  -d '{
    "status": "inProgress",
    "comment": "Deploying via API"
  }'
```

Environment status: `undefined`, `notStarted`, `inProgress`, `succeeded`, `canceled`, `rejected`, `queued`, `scheduled`, `partiallySucceeded`.

## Approvals

```bash
# List pending approvals
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/approvals?statusFilter=pending&api-version=7.1"

# Approve
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/approvals/{approvalId}?api-version=7.1" \
  -d '{"status": "approved", "comments": "Approved via API"}'
```

## Release Logs

```bash
# Get logs for an environment
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases/{releaseId}/environments/{environmentId}/attempts/{attemptId}/tasks?api-version=7.1"
```

## Delete a Release

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases/{releaseId}?api-version=7.1"
```

## Gates

```bash
# List gates for an environment
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vsrm.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/release/releases/{releaseId}/environments/{environmentId}/gates?api-version=7.1-preview.1"
```
