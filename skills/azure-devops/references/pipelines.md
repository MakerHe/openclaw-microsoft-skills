# Pipelines (YAML) API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines`

## List Pipelines

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines?api-version=7.1"
```

## Get a Pipeline

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/{pipelineId}?api-version=7.1"
```

## Create a Pipeline

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines?api-version=7.1" \
  -d '{
    "name": "my-pipeline",
    "folder": "/",
    "configuration": {
      "type": "yaml",
      "path": "/azure-pipelines.yml",
      "repository": {
        "id": "{repoId}",
        "type": "azureReposGit"
      }
    }
  }'
```

## Run a Pipeline

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/{pipelineId}/runs?api-version=7.1" \
  -d '{
    "resources": {
      "repositories": {
        "self": {
          "refName": "refs/heads/main"
        }
      }
    },
    "templateParameters": {
      "param1": "value1"
    }
  }'
```

## List Pipeline Runs

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/{pipelineId}/runs?api-version=7.1"
```

## Get a Pipeline Run

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/{pipelineId}/runs/{runId}?api-version=7.1"
```

## Get Pipeline Run Log

```bash
# List logs
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/{pipelineId}/runs/{runId}/logs?api-version=7.1"

# Get a specific log
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/{pipelineId}/runs/{runId}/logs/{logId}?api-version=7.1"
```

## Pipeline Approvals

```bash
# List pending approvals
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/approvals?api-version=7.1-preview.1"

# Approve
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/approvals?api-version=7.1-preview.1" \
  -d '[{"approvalId": "{approvalId}", "status": "approved", "comment": "Looks good"}]'
```

## Environments

```bash
# List environments
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/environments?api-version=7.1-preview.1"

# Get environment
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/environments/{environmentId}?api-version=7.1-preview.1"

# Create environment
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/environments?api-version=7.1-preview.1" \
  -d '{"name": "production", "description": "Production environment"}'
```

## Pipeline Preview (Dry Run)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/pipelines/{pipelineId}/preview?api-version=7.1-preview.1" \
  -d '{
    "previewRun": true,
    "resources": {
      "repositories": {
        "self": {"refName": "refs/heads/main"}
      }
    }
  }'
```
