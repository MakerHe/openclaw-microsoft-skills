# Classic Build API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build`

## List Build Definitions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/definitions?api-version=7.1"
```

## Get a Build Definition

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/definitions/{definitionId}?api-version=7.1"
```

## Queue a Build

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds?api-version=7.1" \
  -d '{
    "definition": {"id": {definitionId}},
    "sourceBranch": "refs/heads/main",
    "parameters": "{\"param1\": \"value1\"}"
  }'
```

## List Builds

```bash
# Recent builds
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds?api-version=7.1&\$top=20"

# Builds for a definition
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds?definitions={definitionId}&api-version=7.1"

# Filter by status
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds?statusFilter=completed&resultFilter=failed&api-version=7.1"
```

Status: `all`, `cancelling`, `completed`, `inProgress`, `none`, `notStarted`, `postponed`.
Result: `canceled`, `failed`, `none`, `partiallySucceeded`, `succeeded`.

## Get a Build

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}?api-version=7.1"
```

## Cancel a Build

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}?api-version=7.1" \
  -d '{"status": "cancelling"}'
```

## Build Logs

```bash
# List logs
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}/logs?api-version=7.1"

# Get specific log
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}/logs/{logId}?api-version=7.1"
```

## Build Timeline (Stages/Jobs/Tasks)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}/timeline?api-version=7.1"
```

## Build Artifacts

```bash
# List artifacts
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}/artifacts?api-version=7.1"

# Get specific artifact
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}/artifacts?artifactName={name}&api-version=7.1"
```

## Build Tags

```bash
# List tags
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}/tags?api-version=7.1"

# Add tag
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}/tags/{tag}?api-version=7.1"
```

## Retention

```bash
# Delete a build
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}?api-version=7.1"

# Retain a build indefinitely
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/build/builds/{buildId}?api-version=7.1" \
  -d '{"keepForever": true}'
```
