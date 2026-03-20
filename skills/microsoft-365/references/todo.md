# Microsoft To Do API

Base path: `https://graph.microsoft.com/v1.0/me/todo`

Permissions: `Tasks.ReadWrite`

## List Task Lists

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists" | jq '.value[] | {id, displayName, isOwner}'
```

## Get a Task List

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}"
```

## Create a Task List

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/todo/lists" \
  -d '{"displayName": "My Task List"}'
```

## Update a Task List

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}" \
  -d '{"displayName": "Renamed Task List"}'
```

## Delete a Task List

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}"
```

## List Tasks

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks" | jq '.value[] | {id, title, status, importance, dueDateTime: .dueDateTime.dateTime}'
```

Filter incomplete tasks:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks?\$filter=status%20ne%20'completed'"
```

## Get a Task

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks/{task-id}"
```

## Create a Task

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks" \
  -d '{
    "title": "Buy groceries",
    "importance": "high",
    "body": {"content": "Milk, eggs, bread", "contentType": "text"},
    "dueDateTime": {"dateTime": "2025-06-20T00:00:00", "timeZone": "UTC"}
  }'
```

## Update a Task

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks/{task-id}" \
  -d '{
    "title": "Updated task title",
    "status": "completed"
  }'
```

Status values: `notStarted`, `inProgress`, `completed`, `waitingOnOthers`, `deferred`.

Importance values: `low`, `normal`, `high`.

## Delete a Task

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks/{task-id}"
```

## Add a Checklist Item

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks/{task-id}/checklistItems" \
  -d '{"displayName": "Subtask item"}'
```

## List Checklist Items

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks/{task-id}/checklistItems" | jq '.value[] | {id, displayName, isChecked}'
```

## Update a Checklist Item

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks/{task-id}/checklistItems/{item-id}" \
  -d '{"isChecked": true}'
```

## Add a Linked Resource

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/todo/lists/{list-id}/tasks/{task-id}/linkedResources" \
  -d '{
    "webUrl": "https://example.com/resource",
    "applicationName": "My App",
    "displayName": "Related Resource"
  }'
```
