# Audit

Service: `client.audit`

## Query Audit Log

```python
result = client.audit.query(
    start_time="2025-01-01T00:00:00Z",
    end_time="2025-01-31T23:59:59Z",
    skip=0,
)
```

## Download Audit Log

```python
data = client.audit.download(
    format="json",
    start_time="2025-01-01T00:00:00Z",
    end_time="2025-01-31T23:59:59Z",
)
```

Format values: `json`, `csv`.

## List Actions

```python
result = client.audit.list_actions()
```
