# Boards, Backlogs & Sprints API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work`

**Note**: Most board/backlog APIs are team-scoped. Replace `{team}` with the team name or ID.

## Boards

### List Boards

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/boards?api-version=7.1"
```

### Get a Board

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/boards/{boardId}?api-version=7.1"
```

### Get Board Columns

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/boards/{boardId}/columns?api-version=7.1"
```

### Update Board Columns

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/boards/{boardId}/columns?api-version=7.1" \
  -d '[
    {"name": "New", "itemLimit": 0, "stateMappings": {"Bug": "New", "User Story": "New"}},
    {"name": "Active", "itemLimit": 5, "stateMappings": {"Bug": "Active", "User Story": "Active"}},
    {"name": "Closed", "itemLimit": 0, "stateMappings": {"Bug": "Closed", "User Story": "Closed"}}
  ]'
```

### Get Board Rows (Swimlanes)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/boards/{boardId}/rows?api-version=7.1"
```

## Backlogs

### List Backlogs

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/backlogs?api-version=7.1"
```

### Get Backlog Work Items

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/backlogs/{backlogId}/workItems?api-version=7.1"
```

## Iterations (Sprints)

### List Iterations

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings/iterations?api-version=7.1"
```

### Get Current Iteration

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings/iterations?\$timeframe=current&api-version=7.1"
```

### Get Iteration Work Items

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings/iterations/{iterationId}/workitems?api-version=7.1"
```

### Get Iteration Capacity

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings/iterations/{iterationId}/capacities?api-version=7.1"
```

### Add Iteration to Team

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings/iterations?api-version=7.1" \
  -d '{"id": "{iterationId}"}'
```

## Team Settings

```bash
# Get team settings
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings?api-version=7.1"

# Update team settings
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings?api-version=7.1" \
  -d '{
    "backlogIteration": {"id": "{iterationId}"},
    "bugsBehavior": "asTasks",
    "workingDays": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  }'
```

## Team Field Values (Area Paths)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/work/teamsettings/teamfieldvalues?api-version=7.1"
```
