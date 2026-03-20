# Graph & Identity API

Base: `https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph`

**Note**: Graph APIs use the `vssps.dev.azure.com` host.

## Users

### List Users

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/users?api-version=7.1-preview.1"
```

### Get a User

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/users/{userDescriptor}?api-version=7.1-preview.1"
```

### Create a User (from AAD)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/users?api-version=7.1-preview.1" \
  -d '{
    "principalName": "user@example.com",
    "storageKey": "",
    "originId": "{aadObjectId}"
  }'
```

### Delete a User

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/users/{userDescriptor}?api-version=7.1-preview.1"
```

## Groups

### List Groups

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/groups?api-version=7.1-preview.1"
```

### Get a Group

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/groups/{groupDescriptor}?api-version=7.1-preview.1"
```

### Create a Group

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/groups?scopeDescriptor={scopeDescriptor}&api-version=7.1-preview.1" \
  -d '{"displayName": "My Custom Group", "description": "A custom group"}'
```

### Delete a Group

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/groups/{groupDescriptor}?api-version=7.1-preview.1"
```

## Memberships

### List Memberships (Group Members)

```bash
# Members of a group
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/memberships/{subjectDescriptor}?direction=Down&api-version=7.1-preview.1"

# Groups a user belongs to
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/memberships/{subjectDescriptor}?direction=Up&api-version=7.1-preview.1"
```

### Add Membership

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/memberships/{subjectDescriptor}/{containerDescriptor}?api-version=7.1-preview.1"
```

### Remove Membership

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/memberships/{subjectDescriptor}/{containerDescriptor}?api-version=7.1-preview.1"
```

## Descriptors

### Get Descriptor from Storage Key

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/descriptors/{storageKey}?api-version=7.1-preview.1"
```

## Scope Descriptors

### Get Scope Descriptor for a Project

```bash
# Get the scope descriptor to create project-scoped groups
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/descriptors/{projectId}?api-version=7.1-preview.1"
```

## Subject Lookup

### Lookup Subjects by Descriptor

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/graph/subjectlookup?api-version=7.1-preview.1" \
  -d '{
    "lookupKeys": [
      {"descriptor": "{descriptor1}"},
      {"descriptor": "{descriptor2}"}
    ]
  }'
```

## Identities (Legacy)

```bash
# Search by email
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/identities?searchFilter=General&filterValue=user@example.com&api-version=7.1"

# Search by display name
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://vssps.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/identities?searchFilter=DisplayName&filterValue=John%20Doe&api-version=7.1"
```
