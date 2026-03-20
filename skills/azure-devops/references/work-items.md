# Work Item Tracking API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit`

## Get a Work Item

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}?api-version=7.1"
```

With specific fields:

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}?\$fields=System.Title,System.State,System.AssignedTo&api-version=7.1"
```

With expand (relations, fields, links, all):

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}?\$expand=all&api-version=7.1"
```

## Get Multiple Work Items

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems?ids=1,2,3&api-version=7.1"
```

## Create a Work Item

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/\$Task?api-version=7.1" \
  -d '[
    {"op": "add", "path": "/fields/System.Title", "value": "My new task"},
    {"op": "add", "path": "/fields/System.Description", "value": "Description here"},
    {"op": "add", "path": "/fields/System.AssignedTo", "value": "user@example.com"},
    {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": 2}
  ]'
```

Common work item types: `$Task`, `$Bug`, `$User%20Story`, `$Epic`, `$Feature`, `$Issue`.

## Update a Work Item

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}?api-version=7.1" \
  -d '[
    {"op": "replace", "path": "/fields/System.State", "value": "Active"},
    {"op": "replace", "path": "/fields/System.Title", "value": "Updated title"}
  ]'
```

## Delete a Work Item

```bash
# Move to recycle bin
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}?api-version=7.1"

# Permanently delete
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}?destroy=true&api-version=7.1"
```

## WIQL Query

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/wiql?api-version=7.1" \
  -d '{
    "query": "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.TeamProject] = @project AND [System.WorkItemType] = '\''Task'\'' AND [System.State] = '\''Active'\'' ORDER BY [System.CreatedDate] DESC"
  }'
```

The WIQL response returns work item IDs. Fetch full details with the batch endpoint:

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitemsbatch?api-version=7.1" \
  -d '{
    "ids": [1, 2, 3],
    "fields": ["System.Id", "System.Title", "System.State", "System.AssignedTo"]
  }'
```

## Add a Comment

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}/comments?api-version=7.1-preview.4" \
  -d '{"text": "This is a comment"}'
```

## List Comments

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}/comments?api-version=7.1-preview.4"
```

## Add a Link/Relation

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}?api-version=7.1" \
  -d '[
    {
      "op": "add",
      "path": "/relations/-",
      "value": {
        "rel": "System.LinkTypes.Hierarchy-Forward",
        "url": "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{targetId}"
      }
    }
  ]'
```

Common relation types:
- `System.LinkTypes.Hierarchy-Forward` — Parent → Child
- `System.LinkTypes.Hierarchy-Reverse` — Child → Parent
- `System.LinkTypes.Related` — Related
- `System.LinkTypes.Dependency-Forward` — Predecessor
- `System.LinkTypes.Dependency-Reverse` — Successor

## List Work Item Types

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitemtypes?api-version=7.1" | jq '.value[].name'
```

## Get Work Item Revisions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/workitems/{id}/revisions?api-version=7.1"
```

## Recycle Bin

```bash
# List deleted work items
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/recyclebin?api-version=7.1"

# Restore a work item
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wit/recyclebin/{id}?api-version=7.1" \
  -d '{"IsDeleted": false}'
```
