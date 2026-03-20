# Dashboards & Widgets API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard`

**Note**: Dashboard APIs are team-scoped. Replace `{team}` with the team name or ID.

## Dashboards

### List Dashboards

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards?api-version=7.1-preview.3"
```

### Get a Dashboard

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}?api-version=7.1-preview.3"
```

### Create a Dashboard

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards?api-version=7.1-preview.3" \
  -d '{
    "name": "Sprint Dashboard",
    "description": "Dashboard for current sprint"
  }'
```

### Update a Dashboard

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}?api-version=7.1-preview.3" \
  -d '{
    "name": "Updated Dashboard",
    "description": "Updated description"
  }'
```

### Delete a Dashboard

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}?api-version=7.1-preview.3"
```

## Widgets

### List Widgets on a Dashboard

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}/widgets?api-version=7.1-preview.2"
```

### Get a Widget

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}/widgets/{widgetId}?api-version=7.1-preview.2"
```

### Create a Widget

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}/widgets?api-version=7.1-preview.2" \
  -d '{
    "name": "Query Results",
    "contributionId": "ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.QueryScalarWidget",
    "size": {"rowSpan": 1, "columnSpan": 2},
    "position": {"row": 1, "column": 1},
    "settings": "{\"queryId\": \"{queryId}\", \"queryName\": \"My Query\"}"
  }'
```

### Update a Widget

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}/widgets/{widgetId}?api-version=7.1-preview.2" \
  -d '{
    "name": "Updated Widget",
    "size": {"rowSpan": 2, "columnSpan": 2}
  }'
```

### Delete a Widget

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/{team}/_apis/dashboard/dashboards/{dashboardId}/widgets/{widgetId}?api-version=7.1-preview.2"
```

## Common Widget Contribution IDs

- `ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.QueryScalarWidget` — Query Scalar
- `ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.QueryTileWidget` — Query Tile
- `ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.MarkdownWidget` — Markdown
- `ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.BurndownWidget` — Burndown
- `ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.VelocityWidget` — Velocity
- `ms.vss-dashboards-web.Microsoft.VisualStudioOnline.Dashboards.CumulativeFlowDiagramWidget` — CFD
