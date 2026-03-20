# Security & Permissions API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/security`

## Security Namespaces

### List Namespaces

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/security/securitynamespaces?api-version=7.1"
```

### Get a Namespace

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/security/securitynamespaces/{namespaceId}?api-version=7.1"
```

Common namespace IDs:
- Git Repositories: `2e9eb7ed-3c0a-47d4-87c1-0ffdd275fd87`
- Build: `33344d9c-fc72-4d6f-aba5-fa317101a7e9`
- Project: `52d39943-cb85-4d7f-8fa8-c6baac873819`
- Identity: `5a27515b-ccd7-42c9-84f1-54c998f03866`
- Work Item Tracking: `73e71c45-d483-40d5-bdba-62fd076f7f87`

## Access Control Lists (ACLs)

### Query ACLs

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/accesscontrollists/{namespaceId}?token={securityToken}&api-version=7.1"
```

### Set ACL

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/accesscontrollists/{namespaceId}?api-version=7.1" \
  -d '{
    "value": [{
      "inheritPermissions": true,
      "token": "{securityToken}",
      "acesDictionary": {
        "{identityDescriptor}": {
          "descriptor": "{identityDescriptor}",
          "allow": 4,
          "deny": 0
        }
      }
    }]
  }'
```

## Access Control Entries (ACEs)

### Set ACE

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/accesscontrolentries/{namespaceId}?api-version=7.1" \
  -d '{
    "token": "{securityToken}",
    "merge": true,
    "accessControlEntries": [{
      "descriptor": "{identityDescriptor}",
      "allow": 4,
      "deny": 0,
      "extendedInfo": {}
    }]
  }'
```

### Remove ACE

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/accesscontrolentries/{namespaceId}?token={securityToken}&descriptors={identityDescriptor}&api-version=7.1"
```

## Permissions Evaluation

### Has Permissions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/security/permissionevaluationbatch?api-version=7.1" \
  -X POST -H "Content-Type: application/json" \
  -d '{
    "alwaysAllowAdministrators": false,
    "evaluations": [{
      "securityNamespaceId": "{namespaceId}",
      "token": "{securityToken}",
      "permissions": 4
    }]
  }'
```

## Security Tokens

Common token formats:
- **Project**: `$PROJECT:vstfs:///Classification/TeamProject/{projectId}`
- **Git repo**: `repoV2/{projectId}/{repoId}`
- **Git branch**: `repoV2/{projectId}/{repoId}/refs/heads/{branchName}`
- **Build definition**: `{projectId}/{definitionId}`
- **Area path**: `vstfs:///Classification/Node/{areaId}`

## Identity Descriptors

Get the identity descriptor for a user/group:

```bash
# Search for a user
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/identities?searchFilter=General&filterValue=user@example.com&api-version=7.1" | jq '.[0].descriptor'
```
