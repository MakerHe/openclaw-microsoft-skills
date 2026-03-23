# Work Items

Service: `client.work_items`

## Get Work Items

```python
result = client.work_items.get(42)
result = client.work_items.get(42, fields=["System.Title", "System.State"])
result = client.work_items.get(42, expand="all")
result = client.work_items.get_batch([1, 2, 3], fields=["System.Title", "System.State"])
```

## Create a Work Item

```python
result = client.work_items.create(
    "Task",
    title="My new task",
    description="Description here",
    assigned_to="user@example.com",
    priority=2,
    extra_fields={"Custom.Field": "value"},
)
```

Work item types: `Task`, `Bug`, `User Story`, `Epic`, `Feature`, `Issue`.

## Update a Work Item

```python
result = client.work_items.update(42, fields={
    "System.State": "Active",
    "System.Title": "Updated title",
})
```

## Delete a Work Item

```python
client.work_items.delete(42)              # move to recycle bin
client.work_items.delete(42, destroy=True) # permanent delete
```

## WIQL Query

```python
result = client.work_items.query(
    "SELECT [System.Id], [System.Title] FROM WorkItems "
    "WHERE [System.TeamProject] = @project AND [System.State] = 'Active'"
)
# result["workItems"] contains IDs; fetch details with get_batch
ids = [wi["id"] for wi in result["workItems"]]
details = client.work_items.get_batch(ids, fields=["System.Title", "System.State"])
```

## Comments

```python
result = client.work_items.add_comment(42, "This is a comment")
result = client.work_items.list_comments(42)
```

## Relations / Links

```python
result = client.work_items.add_relation(42, target_id=99, relation_type="System.LinkTypes.Hierarchy-Forward")
```

Relation types:
- `System.LinkTypes.Hierarchy-Forward` — Parent → Child
- `System.LinkTypes.Hierarchy-Reverse` — Child → Parent
- `System.LinkTypes.Related` — Related
- `System.LinkTypes.Dependency-Forward` — Predecessor
- `System.LinkTypes.Dependency-Reverse` — Successor

## Work Item Types / Revisions / Recycle Bin

```python
result = client.work_items.list_types()
result = client.work_items.list_revisions(42)
result = client.work_items.list_recycle_bin()
result = client.work_items.restore(42)
```
