# Pipelines

Service: `client.pipelines`

## List / Get

```python
result = client.pipelines.list()
result = client.pipelines.get(pipeline_id)
```

## Create a Pipeline

```python
result = client.pipelines.create(
    name="Build Pipeline",
    folder="/",
    repo_id="repo-guid",
    repo_name="my-repo",
    yaml_path="/azure-pipelines.yml",
)
```

## Run a Pipeline

```python
result = client.pipelines.run(pipeline_id, branch="main", variables={"env": {"value": "prod"}})
```

## Runs / Logs

```python
result = client.pipelines.list_runs(pipeline_id)
result = client.pipelines.get_run(pipeline_id, run_id)
result = client.pipelines.list_run_logs(pipeline_id, run_id)
result = client.pipelines.get_run_log(pipeline_id, run_id, log_id)
```

## Preview YAML

```python
result = client.pipelines.preview(pipeline_id, branch="main")
```

## Approvals

```python
result = client.pipelines.list_approvals()
result = client.pipelines.approve(approval_id, comment="LGTM")
```

## Environments

```python
result = client.pipelines.list_environments()
result = client.pipelines.get_environment(environment_id)
result = client.pipelines.create_environment("production", description="Prod env")
```
