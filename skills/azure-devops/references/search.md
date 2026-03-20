# Code / Work Item / Wiki Search API

Base: `https://almsearch.dev.azure.com/$AZURE_DEVOPS_ORG`

**Note**: Search APIs use the `almsearch.dev.azure.com` host.

## Code Search

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://almsearch.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/search/codesearchresults?api-version=7.1" \
  -d '{
    "searchText": "public class MyService",
    "$skip": 0,
    "$top": 25,
    "filters": {
      "Project": ["'"$AZURE_DEVOPS_PROJECT"'"],
      "Repository": [],
      "Path": [],
      "Branch": [],
      "CodeElement": ["class"]
    },
    "$orderBy": [{"field": "filename", "sortOrder": "ASC"}],
    "includeFacets": true
  }'
```

### Code Search Filters

| Filter | Values |
|--------|--------|
| `Project` | Project names |
| `Repository` | Repository names |
| `Path` | Path prefixes (e.g., `/src`) |
| `Branch` | Branch names |
| `CodeElement` | `class`, `comment`, `def`, `interface`, `method`, `namespace`, `property`, `type` |

### Code Search Operators

- `repo:MyRepo` — Search in specific repo
- `path:/src/` — Search in path
- `ext:cs` — Search by file extension
- `file:Program.cs` — Search by filename
- `lang:csharp` — Search by language

Example: `"searchText": "repo:MyRepo path:/src ext:cs class MyService"`

## Work Item Search

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://almsearch.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/search/workitemsearchresults?api-version=7.1" \
  -d '{
    "searchText": "login bug",
    "$skip": 0,
    "$top": 25,
    "filters": {
      "System.TeamProject": ["'"$AZURE_DEVOPS_PROJECT"'"],
      "System.WorkItemType": ["Bug"],
      "System.State": ["Active", "New"],
      "System.AssignedTo": []
    },
    "$orderBy": [{"field": "system.changeddate", "sortOrder": "DESC"}],
    "includeFacets": true
  }'
```

### Work Item Search Operators

- `a:user@example.com` — Assigned to
- `s:Active` — State
- `t:Bug` — Work item type
- `c:user@example.com` — Created by

Example: `"searchText": "t:Bug s:Active login error"`

## Wiki Search

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://almsearch.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/search/wikisearchresults?api-version=7.1" \
  -d '{
    "searchText": "deployment guide",
    "$skip": 0,
    "$top": 25,
    "filters": {
      "Project": ["'"$AZURE_DEVOPS_PROJECT"'"]
    },
    "includeFacets": true
  }'
```

## Search Response Format

All search responses follow this structure:

```json
{
  "count": 42,
  "results": [
    {
      "fileName": "MyService.cs",
      "path": "/src/MyService.cs",
      "repository": {"name": "MyRepo"},
      "project": {"name": "MyProject"},
      "versions": [{"branchName": "main"}],
      "matches": {"content": [{"charOffset": 10, "length": 9}]},
      "contentId": "..."
    }
  ],
  "infoCode": 0,
  "facets": {
    "Repository": [{"name": "MyRepo", "count": 30}]
  }
}
```
