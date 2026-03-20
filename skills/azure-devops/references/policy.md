# Branch Policy API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy`

## List Policy Configurations

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations?api-version=7.1"
```

## Get a Policy Configuration

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations/{configurationId}?api-version=7.1"
```

## List Policy Types

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/types?api-version=7.1"
```

Common policy type IDs:
- Minimum reviewers: `fa4e907d-c16b-4a4c-9dfa-4906e5d171dd`
- Required reviewers: `fd2167ab-b0be-447a-8571-44ee9a20b4da`
- Work item linking: `40e92b44-2fe1-4dd6-b3d8-74a9c21d0c6e`
- Comment requirements: `c6a1889d-b943-4856-b76f-9e46bb6b0df2`
- Build validation: `0609b952-1397-4640-95ec-e00a01b2c241`
- Merge strategy: `fa4e907d-c16b-4a4c-9dfa-4916e5d171cb`
- Path filter: `0517f88d-4ec5-4343-9d26-9930ebd53069`

## Create a Policy

### Minimum Reviewers

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations?api-version=7.1" \
  -d '{
    "isEnabled": true,
    "isBlocking": true,
    "type": {"id": "fa4e907d-c16b-4a4c-9dfa-4906e5d171dd"},
    "settings": {
      "minimumApproverCount": 2,
      "creatorVoteCounts": false,
      "allowDownvotes": false,
      "resetOnSourcePush": false,
      "scope": [{
        "repositoryId": "{repoId}",
        "refName": "refs/heads/main",
        "matchKind": "Exact"
      }]
    }
  }'
```

### Build Validation

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations?api-version=7.1" \
  -d '{
    "isEnabled": true,
    "isBlocking": true,
    "type": {"id": "0609b952-1397-4640-95ec-e00a01b2c241"},
    "settings": {
      "buildDefinitionId": {definitionId},
      "displayName": "PR Build Validation",
      "manualQueueOnly": false,
      "queueOnSourceUpdateOnly": true,
      "validDuration": 720,
      "scope": [{
        "repositoryId": "{repoId}",
        "refName": "refs/heads/main",
        "matchKind": "Exact"
      }]
    }
  }'
```

### Required Reviewers

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations?api-version=7.1" \
  -d '{
    "isEnabled": true,
    "isBlocking": true,
    "type": {"id": "fd2167ab-b0be-447a-8571-44ee9a20b4da"},
    "settings": {
      "requiredReviewerIds": ["{userId1}", "{userId2}"],
      "filenamePatterns": ["/src/*"],
      "addedFilesOnly": false,
      "message": "Security team review required",
      "scope": [{
        "repositoryId": "{repoId}",
        "refName": "refs/heads/main",
        "matchKind": "Exact"
      }]
    }
  }'
```

### Work Item Linking

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations?api-version=7.1" \
  -d '{
    "isEnabled": true,
    "isBlocking": true,
    "type": {"id": "40e92b44-2fe1-4dd6-b3d8-74a9c21d0c6e"},
    "settings": {
      "scope": [{
        "repositoryId": "{repoId}",
        "refName": "refs/heads/main",
        "matchKind": "Exact"
      }]
    }
  }'
```

## Update a Policy

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations/{configurationId}?api-version=7.1" \
  -d '{
    "isEnabled": true,
    "isBlocking": false,
    "type": {"id": "fa4e907d-c16b-4a4c-9dfa-4906e5d171dd"},
    "settings": {
      "minimumApproverCount": 1,
      "scope": [{
        "repositoryId": "{repoId}",
        "refName": "refs/heads/main",
        "matchKind": "Exact"
      }]
    }
  }'
```

## Delete a Policy

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/configurations/{configurationId}?api-version=7.1"
```

## Policy Evaluations (PR Status)

```bash
# List policy evaluations for a PR
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/policy/evaluations?artifactId=vstfs:///CodeReview/CodeReviewId/{projectId}/{prId}&api-version=7.1"
```

## Scope Match Kinds

- `Exact` — Matches only the specified branch (e.g., `refs/heads/main`)
- `Prefix` — Matches branches starting with the prefix (e.g., `refs/heads/release/`)
- `DefaultBranch` — Matches the default branch (set `refName` to null)
