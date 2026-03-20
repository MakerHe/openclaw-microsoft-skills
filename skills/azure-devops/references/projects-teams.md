# Projects, Teams & Process API

## Projects

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects`

### List Projects

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1"
```

### Get a Project

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/{projectId}?api-version=7.1"
```

### Create a Project

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1" \
  -d '{
    "name": "NewProject",
    "description": "A new project",
    "capabilities": {
      "versioncontrol": {"sourceControlType": "Git"},
      "processTemplate": {"templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"}
    }
  }'
```

Common process template IDs:
- Basic: `b8a3a935-7e91-48b8-a94c-606d37c3e9f2`
- Agile: `adcc42ab-9882-485e-a3ed-7678f01f66bc`
- Scrum: `6b724908-ef14-45cf-84f8-768b5384da45`
- CMMI: `27450541-8e31-4150-9947-dc59f998fc01`

### Update a Project

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/{projectId}?api-version=7.1" \
  -d '{"description": "Updated description"}'
```

### Delete a Project

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/{projectId}?api-version=7.1"
```

## Teams

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/{projectId}/teams`

### List Teams

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/$AZURE_DEVOPS_PROJECT/teams?api-version=7.1"
```

### Get a Team

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/$AZURE_DEVOPS_PROJECT/teams/{teamId}?api-version=7.1"
```

### Create a Team

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/$AZURE_DEVOPS_PROJECT/teams?api-version=7.1" \
  -d '{"name": "New Team", "description": "A new team"}'
```

### List Team Members

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/$AZURE_DEVOPS_PROJECT/teams/{teamId}/members?api-version=7.1"
```

## Process

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/process`

### List Processes

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/process/processes?api-version=7.1"
```

### Get a Process

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/process/processes/{processId}?api-version=7.1"
```

## Project Properties

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects/$AZURE_DEVOPS_PROJECT/properties?api-version=7.1-preview.1"
```

## Areas and Iterations

```bash
# List area paths
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/classificationnodes/areas?\$depth=10&api-version=7.1"

# List iteration paths
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/classificationnodes/iterations?\$depth=10&api-version=7.1"

# Create an area
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/classificationnodes/areas?api-version=7.1" \
  -d '{"name": "NewArea"}'

# Create an iteration
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/classificationnodes/iterations?api-version=7.1" \
  -d '{
    "name": "Sprint 1",
    "attributes": {
      "startDate": "2024-01-01T00:00:00Z",
      "finishDate": "2024-01-14T00:00:00Z"
    }
  }'
```
