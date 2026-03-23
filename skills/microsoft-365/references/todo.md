# Microsoft To Do

Service: `client.todo` — Permissions: `Tasks.ReadWrite`

## Task Lists

```python
result = client.todo.list_task_lists()
result = client.todo.get_task_list(list_id)
result = client.todo.create_task_list("My Task List")
result = client.todo.update_task_list(list_id, "Renamed List")
result = client.todo.delete_task_list(list_id)
```

## Tasks

```python
result = client.todo.list_tasks(list_id, filter="status ne 'completed'")
result = client.todo.get_task(list_id, task_id)
result = client.todo.create_task(
    list_id, title="Buy groceries",
    body="Milk, eggs, bread",
    due="2025-06-20T00:00:00",
    importance="high",
)
result = client.todo.update_task(list_id, task_id, updates={"status": "completed"})
result = client.todo.delete_task(list_id, task_id)
```

Status values: `notStarted`, `inProgress`, `completed`, `waitingOnOthers`, `deferred`.
Importance values: `low`, `normal`, `high`.

## Checklist Items

```python
result = client.todo.list_checklist_items(list_id, task_id)
result = client.todo.add_checklist_item(list_id, task_id, "Subtask item")
result = client.todo.update_checklist_item(list_id, task_id, item_id, updates={"isChecked": True})
```

## Linked Resources

```python
result = client.todo.add_linked_resource(
    list_id, task_id,
    web_url="https://example.com/resource",
    application_name="My App",
    display_name="Related Resource",
)
```
