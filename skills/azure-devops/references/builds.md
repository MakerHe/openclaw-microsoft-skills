# Builds

Service: `client.builds`

## Definitions

```python
result = client.builds.list_definitions()
result = client.builds.get_definition(definition_id)
```

## Queue / List / Get

```python
result = client.builds.queue(definition_id, source_branch="refs/heads/main", parameters={"key": "value"})
result = client.builds.list(definitions=definition_id, status_filter="completed", top=10)
result = client.builds.get(build_id)
```

## Cancel / Delete / Retain

```python
result = client.builds.cancel(build_id)
client.builds.delete(build_id)
result = client.builds.retain(build_id, keep_forever=True)
```

## Logs / Timeline

```python
result = client.builds.list_logs(build_id)
result = client.builds.get_log(build_id, log_id)
result = client.builds.get_timeline(build_id)
```

## Artifacts / Tags

```python
result = client.builds.list_artifacts(build_id)
result = client.builds.get_artifact(build_id, "drop")
result = client.builds.list_tags(build_id)
result = client.builds.add_tag(build_id, "release-candidate")
```
