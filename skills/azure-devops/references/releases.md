# Releases

Service: `client.releases`

## Definitions

```python
result = client.releases.list_definitions()
result = client.releases.get_definition(definition_id)
```

## Create / List / Get

```python
result = client.releases.create(definition_id, description="Release v1.0", artifacts=[{"alias": "drop", "instanceReference": {"id": "123"}}])
result = client.releases.list(definition_id=definition_id, top=10)
result = client.releases.get(release_id)
```

## Deploy / Approvals

```python
result = client.releases.deploy(release_id, environment_id, comment="Deploying to prod")
result = client.releases.list_approvals(status_filter="pending")
result = client.releases.approve(approval_id, comments="Approved")
```

## Tasks / Gates / Delete

```python
result = client.releases.get_tasks(release_id, environment_id, attempt=1)
result = client.releases.list_gates(release_id, environment_id)
client.releases.delete(release_id)
```
