# SharePoint API

Base path: `https://graph.microsoft.com/v1.0`

Permissions: `Sites.ReadWrite.All`

## Search for Sites

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites?search=keyword" | jq '.value[] | {id, displayName, webUrl}'
```

## Get Root Site

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/root" | jq '{displayName, webUrl}'
```

## Get a Site by Path

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{hostname}:/{site-path}" | jq '{id, displayName, webUrl}'
```

Example:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/team-site"
```

## Get a Site by ID

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}"
```

## List Subsites

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/sites" | jq '.value[] | {displayName, webUrl}'
```

## List Followed Sites

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/followedSites" | jq '.value[] | {displayName, webUrl}'
```

## List Lists on a Site

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists" | jq '.value[] | {id, displayName, list: .list.template}'
```

## Get a List

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}"
```

## Create a List

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists" \
  -d '{
    "displayName": "Project Tasks",
    "list": {"template": "genericList"},
    "columns": [
      {"name": "Status", "choice": {"choices": ["Not Started", "In Progress", "Done"]}},
      {"name": "Priority", "choice": {"choices": ["High", "Medium", "Low"]}}
    ]
  }'
```

## List Items in a List

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items?\$expand=fields&\$top=20" | jq '.value[] | {id, fields: .fields}'
```

With select on fields:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items?\$expand=fields(\$select=Title,Status,Priority)"
```

## Get a List Item

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items/{item-id}?\$expand=fields"
```

## Create a List Item

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items" \
  -d '{
    "fields": {
      "Title": "New Task",
      "Status": "Not Started",
      "Priority": "High"
    }
  }'
```

## Update a List Item

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items/{item-id}/fields" \
  -d '{
    "Status": "In Progress"
  }'
```

## Delete a List Item

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items/{item-id}"
```

## Get Site Drive (Document Library)

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/drive" | jq '{id, name, driveType, webUrl}'
```

## List Files in Site Drive

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/drive/root/children" | jq '.value[] | {name, size, webUrl}'
```

## List Columns in a List

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/columns" | jq '.value[] | {name, displayName, description}'
```

## Delete a List

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}"
```
