# Branch Policies

Service: `client.policy`

## Configurations

```python
result = client.policy.list_configurations()
result = client.policy.get_configuration(config_id)
result = client.policy.create(configuration={
    "isEnabled": True, "isBlocking": True,
    "type": {"id": "fa4e907d-c16b-4a4c-9dfa-4916e5d171ab"},
    "settings": {"minimumApproverCount": 2, "scope": [{"repositoryId": repo_id, "refName": "refs/heads/main", "matchKind": "exact"}]},
})
result = client.policy.update(config_id, configuration={...})
client.policy.delete(config_id)
```

## Policy Types

```python
result = client.policy.list_types()
```

Common policy type IDs:
- `fa4e907d-...` — Minimum number of reviewers
- `7ed39669-...` — Work item linking
- `cbdc66da-...` — Comment requirements
- `0609b952-...` — Build validation

## Evaluations

```python
result = client.policy.list_evaluations(project_id, pr_id)
```
